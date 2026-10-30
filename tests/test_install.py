import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install.py"
SPEC = importlib.util.spec_from_file_location("kit_install", SCRIPT)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)
REF = "a" * 40


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bundle = self.root / "bundle"
        self.project = self.root / "project"
        self.project.mkdir()
        self.put("SOURCE_URL", "https://github.com/example/public-kit\n")
        self.put("harness/AGENTS.md", "Follow the task instructions.\n")
        self.put("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: Test fixture.\n---\n")
        self.put("skills/test-skill/LICENSE", "Fixture license.\n")
        self.put("skills/test-skill/references/detail.md", "Reference fixture.\n")
        self.put("SOURCES.md", "Fixture source.\n")
        self.put("LICENSE", "Bundle fixture license.\n")

    def put(self, path, content):
        target = self.bundle / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def run_install(self, **kwargs):
        return installer.install(self.project, REF, bundle=self.bundle, **kwargs)

    def snapshot(self):
        return {
            path.relative_to(self.project).as_posix(): path.read_bytes()
            for path in self.project.rglob("*") if path.is_file() and not path.is_symlink()
        }

    def test_preserves_agents_installs_license_and_receipt(self):
        original = b"# Existing instructions\nKeep this exact content."
        (self.project / "AGENTS.md").write_bytes(original)
        self.run_install()
        agents = (self.project / "AGENTS.md").read_bytes()
        self.assertTrue(agents.startswith(original))
        self.assertEqual(agents.count(installer.START), 1)
        self.assertEqual((self.project / ".agents/skills/test-skill/LICENSE").read_text(), "Fixture license.\n")
        self.assertTrue((self.project / ".agents/skills/test-skill/references/detail.md").is_file())
        receipt = json.loads((self.project / ".agents/public-task-kit/source.json").read_text())
        self.assertEqual(receipt["supplied_ref"], REF)
        self.assertEqual(receipt["repository"], "https://github.com/example/public-kit")
        for path, digest in receipt["files"].items():
            self.assertEqual(hashlib.sha256((self.project / path).read_bytes()).hexdigest(), digest)

    def test_reinstall_is_idempotent(self):
        self.run_install()
        before = self.snapshot()
        self.assertEqual(self.run_install(), [])
        self.assertEqual(self.snapshot(), before)

    def test_check_writes_nothing(self):
        (self.project / "AGENTS.md").write_text("Existing.\n")
        before = self.snapshot()
        self.assertTrue(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())

    def test_conflict_fails_before_any_write(self):
        target = self.project / ".agents/skills/test-skill/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("User-owned skill.\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.run_install()
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents/public-task-kit").exists())

    def test_destination_symlinks_are_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink refused"):
            self.run_install()
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_agents_symlink_is_refused(self):
        outside = self.root / "private.md"
        outside.write_text("Private original.")
        (self.project / "AGENTS.md").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlink refused"):
            self.run_install()
        self.assertEqual(outside.read_text(), "Private original.")
        self.assertFalse((self.project / ".agents").exists())

    def test_source_symlink_is_refused(self):
        source = self.bundle / "skills/test-skill/LICENSE"
        source.unlink()
        source.symlink_to(self.bundle / "LICENSE")
        with self.assertRaisesRegex(ValueError, "Symlink refused"):
            self.run_install()
        self.assertEqual(list(self.project.iterdir()), [])

    def test_invalid_ref_and_missing_project_are_refused(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            installer.install(self.project, "main", bundle=self.bundle)
        with self.assertRaisesRegex(ValueError, "existing"):
            installer.install(self.root / "missing", REF, bundle=self.bundle)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_modified_marker_is_not_replaced(self):
        (self.project / "AGENTS.md").write_bytes(installer.START + b"\nUser changes\n" + installer.END)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "block conflicts"):
            self.run_install()
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
