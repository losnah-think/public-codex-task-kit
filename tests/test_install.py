import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


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

    def run_install(self, revision=REF, **kwargs):
        return installer.install(self.project, revision, bundle=self.bundle, **kwargs)

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

    def test_upgrade_preserves_user_files_and_reinstalls(self):
        (self.project / "AGENTS.md").write_text("Project instructions.\n")
        (self.project / "notes.txt").write_text("User notes.\n")
        self.run_install()
        original_agents = (self.project / "AGENTS.md").read_bytes()
        self.put("harness/AGENTS.md", "Updated workflow.\n")
        self.put("skills/test-skill/SKILL.md", "Updated skill.\n")
        self.put("skills/new-skill/SKILL.md", "New skill.\n")
        messages = self.run_install("b" * 40, upgrade=True)
        self.assertTrue(any(message.startswith("UPDATE ") for message in messages))
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), original_agents)
        self.assertEqual((self.project / "notes.txt").read_text(), "User notes.\n")
        self.assertEqual((self.project / ".agents/skills/test-skill/SKILL.md").read_text(), "Updated skill.\n")
        self.assertTrue((self.project / ".agents/skills/new-skill/SKILL.md").is_file())
        receipt = json.loads((self.project / ".agents/public-task-kit/source.json").read_text())
        self.assertEqual(receipt["supplied_ref"], "b" * 40)
        for path, digest in receipt["files"].items():
            self.assertEqual(hashlib.sha256((self.project / path).read_bytes()).hexdigest(), digest)
        before = self.snapshot()
        self.assertEqual(self.run_install("b" * 40, upgrade=True), [])
        self.assertEqual(self.snapshot(), before)

    def test_upgrade_refuses_modified_deleted_or_symlinked_managed_file(self):
        self.run_install()
        target = self.project / ".agents/skills/test-skill/SKILL.md"
        original = target.read_bytes()
        self.put("harness/AGENTS.md", "Updated workflow.\n")
        for state in ("modified", "deleted", "symlink"):
            with self.subTest(state=state):
                if state == "modified":
                    target.write_text("User edits.\n")
                else:
                    target.unlink()
                    if state == "symlink":
                        target.symlink_to(self.bundle / "skills/test-skill/SKILL.md")
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "modified or deleted|Symlink refused"):
                    self.run_install("b" * 40, upgrade=True)
                self.assertEqual(self.snapshot(), before)
                if target.is_symlink():
                    target.unlink()
                target.write_bytes(original)

    def test_upgrade_requires_valid_receipt(self):
        with self.assertRaisesRegex(ValueError, "requires an existing"):
            self.run_install(upgrade=True)
        self.assertEqual(list(self.project.iterdir()), [])
        self.run_install()
        path = self.project / ".agents/public-task-kit/source.json"
        original = path.read_text()
        receipt = json.loads(original)
        variants = [
            dict(receipt, repository="https://github.com/other/repo"),
            dict(receipt, supplied_ref="main"),
            dict(receipt, files={".agents/skills/test-skill/../../outside": "a" * 64}),
            dict(receipt, files={".agents/skills/test-skill/SKILL.md": "bad"}),
            dict(receipt, files=[]),
            [],
        ]
        for malformed in variants:
            with self.subTest(receipt=malformed):
                path.write_text(json.dumps(malformed))
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    self.run_install("b" * 40, upgrade=True)
                self.assertEqual(self.snapshot(), before)
        path.write_text("not JSON")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_install("b" * 40, upgrade=True)
        self.assertEqual(self.snapshot(), before)

    def test_upgrade_check_writes_nothing(self):
        self.run_install()
        self.put("harness/AGENTS.md", "Updated workflow.\n")
        before = self.snapshot()
        self.assertTrue(self.run_install("b" * 40, upgrade=True, check=True))
        self.assertEqual(self.snapshot(), before)

    def test_upgrade_keeps_unmanaged_conflicts_and_does_not_remove_files(self):
        self.run_install()
        target = self.project / ".agents/skills/new-skill/SKILL.md"
        target.parent.mkdir()
        target.write_text("User skill.\n")
        self.put("skills/new-skill/SKILL.md", "Bundle skill.\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.run_install("b" * 40, upgrade=True)
        self.assertEqual(self.snapshot(), before)
        (self.bundle / "skills/test-skill/LICENSE").unlink()
        with self.assertRaisesRegex(ValueError, "automatic removal is unsupported"):
            self.run_install("b" * 40, upgrade=True)
        self.assertEqual(self.snapshot(), before)

    def test_atomic_replace_failure_does_not_truncate_managed_file(self):
        self.run_install()
        self.put("skills/test-skill/SKILL.md", "Updated skill.\n")
        before = self.snapshot()
        with mock.patch.object(installer.os, "replace", side_effect=OSError("disk error")):
            with self.assertRaisesRegex(OSError, "disk error"):
                self.run_install("b" * 40, upgrade=True)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.project.rglob(".task-kit-*")), [])


if __name__ == "__main__":
    unittest.main()
