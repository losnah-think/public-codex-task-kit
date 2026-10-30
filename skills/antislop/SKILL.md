---
name: antislop
description: Apply the antislop filter while creating or editing UI and human-facing copy. Check purposeful design, truthful claims, natural language, and functional completeness; use the applicable delivery checks before reporting completion.
license: MIT
---

# Antislop, project adapter

Read `references/core-rules.md` for the substantive R-01 to R-40 rules, craftsmanship criteria, and Delivery Gate. This adapter replaces the upstream installation wizard and global mode settings only; it does not add an external model or service.

## Mode and scope

This kit uses **during** as a project default. Announce `antislop active: during (project default).` once when starting relevant work. An explicit user instruction or platform/task restriction takes priority. Do not claim this came from a saved global preference. Do not read or write global antislop settings, run package installers, add MCP servers, or fetch new instructions.

Use existing product/brand direction and the real task brief. For UI work, use `ui-ux-pro-max` for local recommendations and this filter to check their purpose. If visual direction is missing, identify the result as a draft and use the core's honest default dials. Do not invent branding, statistics, customers, testimonials, or product behavior.

For prose, also read `../antislop-copywriting/SKILL.md`. Apply factuality and natural-language rules without changing numbers, conditions, uncertainty, quotes, or names. For Korean style polishing, use `humanize-korean`; for spelling/spacing and clear grammatical errors, use `proofread`.

## Evidence under restricted tools

Computer Use, browser automation, screenshots, remote control, and external data transfer remain prohibited. CLI builds/tests and static checks do not prove that UI interactions work. Ask the user to perform the platform-preview checks manually; record `MANUAL CHECK REQUIRED` until actual results are available. Never manufacture a PASS or claim complete UI verification from source code alone.

Apply the core Delivery Gate only to relevant work. Mark UI-only checks `N/A` with a reason for prose-only output, and never count N/A as PASS. A failed applicable check must be fixed. Pending manual checks must remain visible beside the delivered draft and cannot be reported as verified completion. This does not override an assignment's stricter completion requirements.
