# Sources and licenses

This repository contains general-purpose instructions and local installation code. It contains no assignment solution, private guide, personal machine information, or credentials.

## Original work

`skills/task-brief/`, `harness/`, `scripts/`, `tests/`, `templates/`, and this repository's documentation are original kit content under the root MIT LICENSE. No existing local private Skill was copied into them.

## Verification Before Completion

- Repository: https://github.com/obra/superpowers
- Public visibility checked on 2026-10-31 KST using GitHub repository metadata (`visibility: public`).
- Pinned commit: `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`.
- Source: `skills/verification-before-completion/SKILL.md`.
- Installed location: `skills/verification-before-completion/SKILL.md` in this kit.
- License: MIT, copyright (c) 2025 Jesse Vincent. Original license is included beside the vendored Skill.
- Changes: none. The full Superpowers plugin and its other workflows are not bundled.
- Scope: fresh verification before claiming completion. References to PRs/pushes in the general-purpose upstream file do not override platform restrictions.

## UI UX Pro Max

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Public visibility checked on 2026-10-31 KST using GitHub repository metadata (`visibility: public`).
- Pinned commit: `9a3f14f7423037ccb8feeb4fee7482291b9c820e`.
- Source mapping: `.claude/skills/ui-ux-pro-max/SKILL.md` → this kit's `skills/ui-ux-pro-max/SKILL.md`; `.claude/skills/ui-ux-pro-max/references/` → its `references/`; the four runtime files from `src/ui-ux-pro-max/scripts/` → its `scripts/`; all 39 files from `src/ui-ux-pro-max/data/` → its `data/`; root `LICENSE` → its `LICENSE`.
- License: MIT, copyright (c) 2024 Next Level Builder. Original license and data provenance/font license metadata are included.
- Changes: the Skill's command examples use project-local Python3 paths; a short restricted-environment note was added. Runtime scripts, references, and data are unmodified.
- Scope: offline search for UI/UX recommendations. The upstream `/stack/` scaffold, browser/Claude tooling, npm CLI, MCP configuration, hooks, refresh scripts, and test fixtures are excluded.

## Format references

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/agents-md

These documentation pages were consulted for Skill and AGENTS.md placement. Their page content is not redistributed.

## Using this kit in a restricted environment

Record this repository's URL, exact checked-out commit, license, files used, changes, and public-visibility check in the provided environment. The installer writes `.agents/public-task-kit/source.json` with the caller-supplied kit ref and file SHA256 hashes.

Public visibility at one time does not guarantee future availability. Keep this kit public for the required retention period and recheck any upstream repository as required. Do not send task content, files, or records to GitHub to record usage.
