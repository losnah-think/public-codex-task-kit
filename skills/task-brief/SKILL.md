---
name: task-brief
description: Convert a provided coding task and its existing README into a short implementation plan with acceptance checks and required deliverables. Use when beginning a task or when its requirements change.
license: MIT
---

# Task Brief

Read the task instructions, existing AGENTS.md, README, and relevant files before editing. Existing platform and task rules take priority over this workflow.

When installed with this kit, also read `.agents/public-task-kit/AGENTS.md` for its work loop and environment boundaries.

Identify the concrete outcome, required output paths, prohibited actions, input/output contracts, and how each essential requirement can be checked. Separate stated requirements from assumptions. Ask only about missing information that could change correctness; ask the platform's designated stakeholder or helper when available.

Write a short plan in the required planning file if one is specified. Otherwise keep a compact WORKLOG.md in the project. Use the project's actual filenames and verification commands, not invented defaults. For each step, name what will change and how to verify it. Reuse existing code and dependencies before adding anything.

If no testing command exists, choose one small observable check relevant to the behavior. Do not replace evidence with “looks right,” or invent tests that were not run. For a bug, reproduce the failure before editing and check the same behavior after the fix.

Keep the record focused: requirements, important decisions, actual checks, public sources used, and remaining limits. Do not create a second planning system or prewrite answers for an AI-prohibited follow-up stage.
