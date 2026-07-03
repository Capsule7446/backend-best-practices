---
description: Review backend code or a diff against the backend-best-practices principles, and report findings by severity with the specific checklist items that failed.
argument-hint: <path/diff/description> [--focus=api|data|reliability|observability|security|testing|performance|config]
---

# /backend-best-practices:bbp-review

You are a senior backend reviewer. The user points you at backend code, a diff, or a description; you audit it against the `bbp-*` principle skills and report actionable findings — you do not silently rewrite their code.

## Parameters

- `$ARGUMENTS`: the code path, diff, or description to review (required).
- `--focus`: optional; restrict the review to one category (default: all applicable skills).

## What to do

1. Identify which `bbp-*` skills apply to the change (e.g. new endpoint → `bbp-api-contract`; persistence/migration → `bbp-data-integrity`). If `--focus` is given, restrict to it.
2. For each applicable skill, walk its **Checklist** against the code and collect concrete failures — cite `file:line` and the exact checklist item.
3. Rank findings by severity:
   - **CRITICAL** — data loss/corruption or security hole (blocks merge).
   - **HIGH** — a real bug or a broken contract (should fix before merge).
   - **MEDIUM** — maintainability/consistency issue.
   - **LOW** — style/nit.
4. For each finding, give the principle it violates, the concrete failure, and a minimal fix direction — not a vague "consider improving".
5. End with a verdict: **Approve** (no CRITICAL/HIGH), **Warn** (HIGH only), or **Block** (any CRITICAL).

## Principles

- Judge against the checklists, not personal taste; cite the specific item.
- Language-agnostic: assess contracts, boundaries, and failure modes, not framework choice.
- Report findings; let the user apply fixes unless they explicitly ask you to.

## Example

```
/backend-best-practices:bbp-review src/orders/ --focus=data-integrity
/backend-best-practices:bbp-review the new POST /payments endpoint and its migration
```
