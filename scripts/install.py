#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile


BUNDLE = Path(__file__).resolve().parents[1]
START = b"<!-- public-task-kit:start -->"
END = b"<!-- public-task-kit:end -->"
POINTER = (
    START + b"\n"
    b"Read `.agents/public-task-kit/AGENTS.md` as additional workflow guidance; "
    b"platform/task instructions retain priority.\n" + END + b"\n"
)


def no_symlinks(path, root):
    current = path
    while True:
        if current.is_symlink():
            raise ValueError("Symlink refused: " + str(current))
        if current != path and current.exists() and not current.is_dir():
            raise ValueError("Parent is not a directory: " + str(current))
        if current == root:
            return
        if current.parent == current:
            raise ValueError("Path is outside root: " + str(path))
        current = current.parent


def read_prior_receipt(path, project, source_url, payload):
    no_symlinks(path, project)
    if not path.is_file():
        raise ValueError("--upgrade requires an existing source.json receipt")
    original = path.read_bytes()
    receipt = json.loads(original)
    if not isinstance(receipt, dict) or receipt.get("repository") != source_url.rstrip("/"):
        raise ValueError("Prior receipt repository does not match SOURCE_URL")
    revision = receipt.get("supplied_ref")
    files = receipt.get("files")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise ValueError("Prior receipt has an invalid supplied_ref")
    if not isinstance(files, dict) or not files:
        raise ValueError("Prior receipt must contain a nonempty files dictionary")
    managed = {}
    for key, digest in files.items():
        if not isinstance(key, str) or "\\" in key or "\x00" in key:
            raise ValueError("Prior receipt has an unsafe file path")
        parts = PurePosixPath(key).parts
        known = key in {
            ".agents/public-task-kit/AGENTS.md",
            ".agents/public-task-kit/SOURCES.md",
            ".agents/public-task-kit/LICENSE",
        } or (
            len(parts) >= 4 and parts[:2] == (".agents", "skills")
            and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", parts[2])
        )
        if not known or ".." in parts or PurePosixPath(key).as_posix() != key:
            raise ValueError("Prior receipt has an unsafe file path: " + key)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            raise ValueError("Prior receipt has an invalid SHA256: " + key)
        target = project / key
        no_symlinks(target, project)
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest.lower():
            raise ValueError("Managed file was modified or deleted: " + str(target))
        if target not in payload:
            raise ValueError("Bundle omits a managed file; automatic removal is unsupported: " + key)
        managed[target] = digest.lower()
    managed[path] = hashlib.sha256(original).hexdigest()
    return managed


def replace_atomic(path, content, expected_digest):
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_digest:
        raise ValueError("Managed file changed during upgrade: " + str(path))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".task-kit-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def install(project, revision, check=False, bundle=BUNDLE, upgrade=False):
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise ValueError("--ref must be a full 40-character commit SHA")
    project = Path(project).expanduser().absolute()
    if project.is_symlink() or not project.is_dir():
        raise ValueError("--project must be an existing, non-symlink directory")
    project = project.resolve()
    bundle = Path(bundle).absolute()

    def read_source(path):
        no_symlinks(path, bundle)
        if not path.is_file():
            raise ValueError("Source is not a regular file: " + str(path))
        return path.read_bytes()

    source_url = read_source(bundle / "SOURCE_URL").decode("utf-8").strip()
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?", source_url):
        raise ValueError("SOURCE_URL must contain one HTTPS GitHub repository URL")

    payload = {}
    guidance_dir = project / ".agents/public-task-kit"
    payload[guidance_dir / "AGENTS.md"] = read_source(bundle / "harness/AGENTS.md")
    for filename in ("SOURCES.md", "LICENSE"):
        source = bundle / filename
        if source.exists() or source.is_symlink():
            payload[guidance_dir / filename] = read_source(source)

    skills = bundle / "skills"
    no_symlinks(skills, bundle)
    if not skills.is_dir():
        raise ValueError("Bundle has no skills directory")
    for folder in sorted(skills.iterdir()):
        no_symlinks(folder, bundle)
        if not folder.is_dir():
            continue
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", folder.name):
            raise ValueError("Invalid skill directory name: " + folder.name)
        read_source(folder / "SKILL.md")
        for source in sorted(folder.rglob("*")):
            no_symlinks(source, bundle)
            if not source.is_dir():
                target = project / ".agents/skills" / source.relative_to(skills)
                payload[target] = read_source(source)

    receipt_path = guidance_dir / "source.json"
    managed = read_prior_receipt(receipt_path, project, source_url, payload) if upgrade else {}
    receipt = {
        "repository": source_url.rstrip("/"),
        "supplied_ref": revision.lower(),
        "files": {
            path.relative_to(project).as_posix(): hashlib.sha256(data).hexdigest()
            for path, data in sorted(payload.items())
        },
    }
    payload[receipt_path] = (
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    agents = project / "AGENTS.md"
    no_symlinks(agents, project)
    if agents.exists() and not agents.is_file():
        raise ValueError("AGENTS.md is not a regular file")
    original = agents.read_bytes() if agents.exists() else b""
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1 or POINTER not in original:
            raise ValueError("Existing public-task-kit guidance block conflicts")
        suffix = b""
    else:
        separator = b"" if not original else (b"\n" if original.endswith(b"\n") else b"\n\n")
        suffix = separator + POINTER

    changes = []
    for target, content in payload.items():
        no_symlinks(target, project)
        if target.exists():
            if not target.is_file() or target.read_bytes() != content:
                if target not in managed:
                    raise ValueError("Existing file conflicts; nothing overwritten: " + str(target))
                changes.append((target, content, "UPDATE"))
        else:
            changes.append((target, content, "WRITE"))

    messages = [action + " " + str(path) for path, _, action in changes]
    if suffix:
        messages.append("APPEND " + str(agents))
    if not check:
        if (agents.read_bytes() if agents.exists() else b"") != original:
            raise ValueError("AGENTS.md changed during preflight; retry")
        for target, content, action in changes:
            target.parent.mkdir(parents=True, exist_ok=True)
            no_symlinks(target, project)
            if action == "UPDATE":
                replace_atomic(target, content, managed[target])
            else:
                with target.open("xb") as handle:
                    handle.write(content)
        if suffix:
            no_symlinks(agents, project)
            with agents.open("ab") as handle:
                handle.write(suffix)
    return messages


def main():
    parser = argparse.ArgumentParser(description="Install project-local skills without overwriting user files.")
    parser.add_argument("--project", required=True, help="Existing project directory")
    parser.add_argument("--ref", required=True, help="Full kit commit SHA supplied by the caller")
    parser.add_argument("--check", action="store_true", help="Preflight and report planned writes only")
    parser.add_argument("--upgrade", action="store_true", help="Update only unmodified files tracked by a valid prior receipt")
    args = parser.parse_args()
    try:
        messages = install(args.project, args.ref, args.check, upgrade=args.upgrade)
    except (OSError, ValueError, UnicodeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    print("\n".join(messages) if messages else "Already installed; no changes.")
    if args.check:
        print("Check only; no files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
