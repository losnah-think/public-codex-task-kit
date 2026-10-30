import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


BUNDLE = Path(__file__).resolve().parents[1]
INSTALL = runpy.run_path(str(BUNDLE / "scripts/install.py"))["install"]
REF = "0" * 40
OFFLINE_RUNNER = """
import runpy, sys
def refuse_network(event, args):
    if event.startswith("socket."):
        raise RuntimeError("Network access is not allowed in this test")
sys.addaudithook(refuse_network)
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def snapshot(self):
        return {
            path.relative_to(self.project).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.project.rglob("*") if path.is_file()
        }

    def test_real_bundle_preserves_agents_licenses_and_reinstalls(self):
        original = b"# Project instructions\nKeep this content."
        (self.project / "AGENTS.md").write_bytes(original)
        INSTALL(self.project, REF)
        self.assertTrue((self.project / "AGENTS.md").read_bytes().startswith(original))
        skills = self.project / ".agents/skills"
        self.assertEqual({path.name for path in skills.iterdir()}, {
            "task-brief", "verification-before-completion", "ui-ux-pro-max",
        })
        for name in ("verification-before-completion", "ui-ux-pro-max"):
            self.assertEqual((skills / name / "LICENSE").read_bytes(),
                             (BUNDLE / "skills" / name / "LICENSE").read_bytes())
        receipt = json.loads((self.project / ".agents/public-task-kit/source.json").read_text())
        for path, digest in receipt["files"].items():
            self.assertEqual(hashlib.sha256((self.project / path).read_bytes()).hexdigest(), digest)
        before = self.snapshot()
        self.assertEqual(INSTALL(self.project, REF), [])
        self.assertEqual(self.snapshot(), before)

    def test_installed_ui_search_works_offline_from_unrelated_cwd(self):
        INSTALL(self.project, REF)
        script = self.project / ".agents/skills/ui-ux-pro-max/scripts/search.py"
        elsewhere = self.root / "unrelated"
        elsewhere.mkdir()
        before = self.snapshot()

        def search(*args):
            result = subprocess.run(
                [sys.executable, "-B", "-c", OFFLINE_RUNNER, str(script), *args],
                cwd=elsewhere, capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

        ux = search("keyboard focus", "--domain", "ux", "--json")
        self.assertEqual(ux["domain"], "ux")
        self.assertGreater(ux["count"], 0)
        self.assertEqual(ux["count"], len(ux["results"]))
        self.assertTrue(all(row.get("Description") and row.get("Do") for row in ux["results"]))
        design = search("dashboard", "--design-system", "--json")
        self.assertIsNone(design["persistence"])
        self.assertTrue(design["design_system"]["style"]["name"])
        self.assertTrue(design["design_system"]["colors"]["primary"])
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
