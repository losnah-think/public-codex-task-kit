# Maintaining this public kit

If the user supplies this repository URL and asks to read/run/install/apply it, read START.md and follow its installation and current-session application procedure in the user's actual task project. Preserve that project as the working target. Report real verification results and stop on platform restrictions or file conflicts. The maintenance instructions below apply when editing this kit itself.

Keep this repository generic: portable instructions, local-only installation, and tests. Do not add task solutions, private guides, credentials, personal machine details, external-model integrations, browser automation, or telemetry.

The installed workflow is harness/AGENTS.md. Installation affects only the chosen project and preserves its existing instructions. Do not overwrite global Codex or platform configuration.

Run `python3 -m unittest discover -s tests -v` after changing the installer. Preserve vendored license text and update SOURCES.md when vendored content changes.
