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

## Antislop and copywriting

- Repository: https://github.com/miqdadbadjuber/anti-slop
- Public visibility checked on 2026-10-31 KST using GitHub repository metadata (`visibility: public`).
- Pinned commit: `3005235d030b4793146ad9afe8d01045efd90e1d`, upstream version 3.2.24.
- Source mapping: substantive rules from `skills/antislop/SKILL.md` → `skills/antislop/references/core-rules.md`; `skills/antislop/VERSION` → same relative path; `skills/antislop-copywriting/SKILL.md` → same path. Root LICENSE is preserved beside both Skills.
- License: MIT, copyright (c) 2026 Miqdad Badjuber (antislop).
- Changes: a new project adapter replaces upstream install/update/global-mode procedures; core rules retain their identifiers, with the excluded browser/MCP performance-guide pointer replaced by an evidence requirement. Copywriting uses the installed core path and project restrictions. Manual UI checks stay pending; prose-only UI checks are N/A, never fabricated PASS.
- Scope: core filter and copywriting only. Optional UI/human/mobile/code modules, MCP tools, installers, global settings, and external/browser tooling are not included.

## Humanize Korean

- Repository: https://github.com/epoko77-ai/im-not-ai
- Public visibility checked on 2026-10-31 KST using GitHub repository metadata (`visibility: public`).
- Pinned commit: `b37e0206d31fffd9149bf57168d4d62eb2086bee`.
- Source mapping: `copilot/skills/humanize-korean/SKILL.md` → `skills/humanize-korean/SKILL.md`; five files (`quick-rules.md`, `ai-tell-taxonomy.md`, `rewriting-playbook.md`, `metrics.py`, `metrics_v2.py`) from `skills/humanize-korean/references/` → same path; root `scripts/verify_change_rate.py` and `scripts/console.py` → this Skill's `scripts/`; root LICENSE → this Skill's LICENSE.
- License: MIT, copyright (c) 2026 epoko77-ai.
- Changes: the single-call Skill is adapted to provided Codex and local references, required output paths take priority, metadata must use actual evidence, and the executable thresholds (>=30% warning, >=50% reject, exit 3 error) override inconsistent `over` wording in prose. Runtime scripts and reference rules are unchanged.
- Scope: local style polishing with protected facts, conditions, names, numbers, quotations, and register. No external model or multi-agent orchestration is included. A change-rate check does not establish semantic preservation.

## Korean proofreading

- Repository: https://github.com/amondnet/yoonmoon
- Public visibility checked on 2026-10-31 KST using GitHub repository metadata (`visibility: public`).
- Pinned commit: `c88853106c8fa8448447136f5aa3fc8bb9650303`.
- Source mapping: `skills/proofread/SKILL.md` and `skills/proofread/references/proofreading-rules.md` → same paths; root LICENSE → this Skill's LICENSE.
- License: MIT, copyright (c) 2026 Minsu Lee.
- Changes: routing to unavailable style tools is replaced with the bundled humanize-korean Skill, and input/data preservation and platform restrictions are stated. No executable code or service is added.
- Scope: spelling, spacing, standard forms, punctuation, and clear grammatical errors, with meaning and register preserved.

## Format references

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/agents-md

These documentation pages were consulted for Skill and AGENTS.md placement. Their page content is not redistributed.

## Using this kit in a restricted environment

Record this repository's URL, exact checked-out commit, license, files used, changes, and public-visibility check in the provided environment. The installer writes `.agents/public-task-kit/source.json` with the caller-supplied kit ref and file SHA256 hashes.

Public visibility at one time does not guarantee future availability. Keep this kit public for the required retention period and recheck any upstream repository as required. Do not send task content, files, or records to GitHub to record usage.
