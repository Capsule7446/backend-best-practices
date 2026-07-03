# backend-best-practices

> Turn "what senior backend engineers just know" into repeatable, checkable, language-agnostic Claude Code skills.

A set of opinionated backend implementation principles for Claude Code and Cowork. Each principle is packaged as an **executable SOP** — not a passive wiki page — with a clear scope, concrete rules, the anti-patterns they replace, a pass/fail checklist, and worked examples. The goal: make an agent produce backend code that a seasoned reviewer would sign off on, consistently, in any language.

---

## The problem it solves

Backend quality lives in tacit knowledge: transaction boundaries, idempotency, error taxonomies, timeouts, observability, safe migrations. It's hard to standardize, hard to hand off, and easy for an agent to get subtly wrong.

This plugin fixes each principle into a structured skill:

- every skill states **when it applies, the rules, the anti-patterns, a checklist, and examples**;
- the checklist is a **review gate** — code that fails it doesn't ship;
- rules are **language-agnostic** (Go / Java / TypeScript / Python / C# / Rust / …); only the syntax of the examples changes.

> **Core idea**: each skill = a reviewer's mental checklist made explicit and enforceable.

### Design principles

1. **Principle, anti-pattern, and check travel together** — a rule you can't verify is just an opinion, so every skill ends in a checklist.
2. **Language-agnostic by default** — principles are about contracts, boundaries, and failure modes, not frameworks. Examples are illustrative, not prescriptive.
3. **Opinionated, with rationale** — every rule says *why*, so it can be overridden deliberately rather than ignored accidentally.

---

## Quick start

```text
# Review backend code / a diff against the principles
/backend-best-practices:bbp-review src/orders/ --focus=data-integrity

# Or invoke a single principle skill directly while implementing
"Apply backend-best-practices:bbp-api-contract to this new endpoint."
```

---

## Skill catalog

Each skill is `skills/<name>/SKILL.md`. Status marks how fleshed out it is today.

| Skill | Covers | Status |
| :--- | :--- | :--- |
| `bbp-api-contract` | Resource design, status codes, pagination, versioning, idempotency, error envelopes | ✅ Ready |
| `bbp-data-integrity` | Transaction boundaries, consistency, concurrency control, safe migrations | ✅ Ready |
| `bbp-error-handling` | Error taxonomy, failure propagation, retries, timeouts, circuit breakers | 📝 Planned |
| `bbp-observability` | Structured logging, metrics (RED/USE), tracing, correlation IDs | 📝 Planned |
| `bbp-security` | AuthN/AuthZ, input validation, secrets, least privilege, rate limiting | 📝 Planned |
| `bbp-testing` | Test pyramid, contract tests, fixtures vs mocks, coverage that means something | 📝 Planned |
| `bbp-performance` | N+1 queries, pagination limits, caching, connection pools, backpressure | 📝 Planned |
| `bbp-config` | Config vs secrets, 12-factor, startup validation, environment parity | 📝 Planned |

> The two ✅ skills define the contract and tone. The 📝 ones are stubs to be filled in the same shape.

---

## The SKILL.md contract

Every `bbp-*/SKILL.md` shares one structure so skills are consistent and composable. Frontmatter:

```yaml
---
name: bbp-<skill-name>
description: "<one line: what it enforces + when it applies>"
risk: safe
category: <api|data|reliability|observability|security|testing|performance|config>
tags: "[backend, <focus>]"
---
```

Body, fixed sections in order: **When to Use / Principles / Anti-Patterns / Checklist / Example**.

- **When to Use** — the situations that trigger the skill.
- **Principles** — the numbered rules, each with a one-line rationale.
- **Anti-Patterns** — the concrete mistakes each principle replaces.
- **Checklist** — the pass/fail review gate.
- **Example** — a short, language-labelled illustration (syntax is illustrative).

---

## Layout

```
backend-best-practices/
├── .claude-plugin/plugin.json   plugin manifest
├── README.md                    this file
├── skills/                      one directory per principle
├── commands/                    slash-command entry points
└── scripts/pack.ps1             packaging for release
```

---

## License

MIT © 2026 Capsule7446
