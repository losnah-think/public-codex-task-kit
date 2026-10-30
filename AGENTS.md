# Maintaining this public kit

Keep this repository generic: portable instructions, local-only installation, and tests. Do not add task solutions, private guides, credentials, personal machine details, external-model integrations, browser automation, or telemetry.

The installed workflow is harness/AGENTS.md. Installation affects only the chosen project and preserves its existing instructions. Do not overwrite global Codex or platform configuration.

Run `python3 -m unittest discover -s tests -v` after changing the installer. Preserve vendored license text and update SOURCES.md when vendored content changes.
