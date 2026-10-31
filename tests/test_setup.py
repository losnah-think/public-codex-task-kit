from contextlib import redirect_stdout
import io
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "setup.py"
LAUNCHER = runpy.run_path(str(SCRIPT))
REVISION = LAUNCHER["REVISION"]


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def run_main(self):
        with mock.patch.object(Path, "cwd", return_value=self.project), redirect_stdout(io.StringIO()) as output:
            result = LAUNCHER["main"]()
        return result, output.getvalue()

    @mock.patch("subprocess.check_output", return_value=REVISION + "\n")
    @mock.patch("subprocess.run")
    def test_fresh_install_preserves_cwd_and_checks_before_install(self, run, _):
        original_cwd = Path.cwd()
        result, output = self.run_main()
        self.assertEqual(result, 0)
        self.assertEqual(Path.cwd(), original_cwd)
        self.assertEqual(list(self.project.iterdir()), [])
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(commands[0][-3:-1], ["v1.1.0", LAUNCHER["REPOSITORY"]])
        self.assertEqual(commands[1], commands[2] + ["--check"])
        self.assertIn(str(self.project), commands[2])
        self.assertIn(REVISION, commands[2])
        self.assertNotIn("--upgrade", commands[2])
        self.assertIn("(7 skills)", output)
        self.assertIn("in this session to apply them", output)

    @mock.patch("subprocess.check_output", return_value=REVISION)
    @mock.patch("subprocess.run")
    def test_existing_or_symlinked_receipt_selects_upgrade(self, run, _):
        receipt = self.project / ".agents/public-task-kit/source.json"
        receipt.parent.mkdir(parents=True)
        for symlink in (False, True):
            with self.subTest(symlink=symlink):
                if receipt.exists():
                    receipt.unlink()
                if symlink:
                    receipt.symlink_to(self.project / "missing.json")
                else:
                    receipt.write_text("fixture")
                run.reset_mock()
                self.run_main()
                commands = [call.args[0] for call in run.call_args_list]
                self.assertEqual(commands[1], commands[2] + ["--check"])
                self.assertIn("--upgrade", commands[2])

    @mock.patch("subprocess.check_output", return_value="0" * 40)
    @mock.patch("subprocess.run")
    def test_revision_mismatch_never_executes_installer(self, run, _):
        with self.assertRaisesRegex(RuntimeError, "pinned revision"):
            self.run_main()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(list(self.project.iterdir()), [])

    @mock.patch("subprocess.check_output", return_value=REVISION)
    @mock.patch("subprocess.run", side_effect=[None, subprocess.CalledProcessError(1, "preflight")])
    def test_failed_preflight_prevents_install(self, run, _):
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_main()
        self.assertEqual(run.call_count, 2)
        self.assertIn("--check", run.call_args.args[0])
        self.assertEqual(list(self.project.iterdir()), [])

    @mock.patch("subprocess.check_output", return_value=REVISION)
    @mock.patch("subprocess.run")
    def test_downloaded_exec_context_needs_no_file_binding(self, run, _):
        namespace = {"__name__": "__main__"}
        with mock.patch.object(Path, "cwd", return_value=self.project), redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                exec(compile(SCRIPT.read_bytes(), "<downloaded-setup>", "exec"), namespace)
        self.assertEqual(result.exception.code, 0)
        self.assertNotIn("__file__", namespace)
        self.assertEqual(run.call_count, 3)


if __name__ == "__main__":
    unittest.main()
