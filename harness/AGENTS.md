# Task workflow

Apply this workflow alongside existing instructions. Platform rules and the actual assignment take priority. This kit supplies a workflow, not an application or a task solution.

## Boundaries

- Use the platform-provided coding agent and its permitted model. Do not connect personal keys, subscriptions, external AI services, or change platform/security/approval settings.
- Do not use Computer Use, browser automation, automatic screenshots, or remote control. Verify UI behavior manually in the platform's preview. CLI unit tests, builds, and local HTTP checks may be used within the task's rules.
- Keep task content, files, logs, and results inside the provided environment. No Git Push, external publishing, telemetry, or tools that send task content to another service. Do not include task text in public web queries.
- Download only necessary public sources through the provided environment's permitted tools. Record the URL, pinned version, license, used portions, and public-status check. Do not upload private local files or replace the whole solution with an external result.
- If a task forbids AI in a later phase, stop AI assistance for that phase. Do not bypass upload, network, recording, or supervision restrictions.

## Work loop

1. Read the assignment and relevant existing code. Use `task-brief` to identify acceptance checks and required output paths. Do not assume a language, framework, port, or deliverable filename.
2. Make the smallest complete change. Reuse project patterns and dependencies. Check every caller affected by a changed interface. Avoid unrelated cleanup and speculative options.
   For UI work only, use `ui-ux-pro-max` to search its bundled local data. Respect existing visual direction and the detected stack; do not turn recommended external font or image URLs into automatic external loads.
3. When debugging, reproduce the failure, inspect the relevant path, test one cause, fix the cause, and rerun the reproducer. Preserve input validation and data-loss protections.
4. Run the project's relevant checks. For a new behavior, cover an ordinary case and a failure or boundary case where that could affect correctness. Do not add test infrastructure for a trivial document edit.
5. Use `verification-before-completion` before claiming success. Record the actual command, result, and limits. For a web preview, bind the server as the platform requires, use the actual port, keep its process running, and ask the user to check interactions manually.
6. Check required files and save state before handoff. Explain the implemented behavior and choices so the user can understand their own result. Do not claim a successful platform submission from a local file check.

## Evidence

Use the assignment's specified planning/collaboration files. If none are specified and a record is useful, use a single WORKLOG.md with goal/acceptance checks, decisions, verification, public sources, and remaining limits. Include only actual work and results.

Do not fabricate stakeholder conversations, test output, measurements, source licenses, or completed work. Preserve local work history as permitted; do not transmit it externally.
