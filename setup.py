#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile


REPOSITORY = "https://github.com/losnah-think/public-codex-task-kit.git"
VERSION = "v1.1.0"
REVISION = "8e7435af2fe28cc57cfffde178822987b8e3fb46"
SKILLS = (
    "task-brief", "ui-ux-pro-max", "antislop", "antislop-copywriting",
    "humanize-korean", "proofread", "verification-before-completion",
)


def main():
    if sys.version_info < (3, 9):
        raise RuntimeError("Python 3.9 or newer is required")
    project = Path.cwd()
    receipt = project / ".agents/public-task-kit/source.json"
    with tempfile.TemporaryDirectory(prefix="public-task-kit-") as bundle:
        subprocess.run([
            "git", "-c", "advice.detachedHead=false", "clone", "--quiet",
            "--depth", "1", "--branch", VERSION, REPOSITORY, bundle,
        ], check=True)
        actual = subprocess.check_output(
            ["git", "-C", bundle, "rev-parse", "HEAD"], text=True,
        ).strip()
        if actual != REVISION:
            raise RuntimeError("Downloaded commit does not match the pinned revision")
        command = [
            sys.executable, str(Path(bundle) / "scripts/install.py"),
            "--project", str(project), "--ref", REVISION,
        ]
        if receipt.exists() or receipt.is_symlink():
            command.append("--upgrade")
        subprocess.run(command + ["--check"], check=True)
        subprocess.run(command, check=True)
    print("Installed public-codex-task-kit payload " + VERSION + " (7 skills).")
    print("Commit: " + REVISION)
    print("Skills: " + ", ".join(SKILLS))
    print("Codex: read AGENTS.md, .agents/public-task-kit/AGENTS.md, and each installed SKILL.md in this session to apply them.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(1)
