---
name: bbp-api-contract
description: "Design and review HTTP/RPC API contracts: resource modeling, status codes, pagination, versioning, idempotency, and a consistent error envelope. Trigger when adding or changing a public/service endpoint."
risk: safe
category: api
tags: "[backend, api, contract]"
---

# Backend Best Practices — API Contract

The API is a contract, not an afterthought. Once a client depends on a shape, that shape is a promise. This skill makes an endpoint's contract explicit and consistent before it ships, so clients never have to guess and never break on a silent change.

## When to Use

- Adding a new HTTP/RPC endpoint, or changing the request/response shape of an existing one.
- Reviewing a diff that touches routes, DTOs, serializers, or status codes.
- Designing a public API surface where backward compatibility matters.

## Principles

1. **Model resources, not actions.** Prefer `POST /orders` + `POST /orders/{id}/cancellation` over `POST /createOrder` / `POST /cancelOrderNow`. *Why:* nouns compose and stay stable; verbs multiply and drift.
2. **Status codes carry meaning; the body carries detail.** `2xx` success, `4xx` caller's fault, `5xx` our fault. Never return `200` with `{"error": ...}`. *Why:* infrastructure (caches, proxies, clients) acts on the code, not your JSON.
3. **One error envelope, everywhere.** Every error returns the same shape: a stable machine `code`, a human `message`, and optional `details`. *Why:* clients write one error handler, not one per endpoint.
4. **Write operations are idempotent or explicitly not.** Support an idempotency key for creates/payments so a retry can't double-charge. *Why:* networks retry; without a key, at-least-once delivery becomes duplicate side effects.
5. **Collections are always paginated and bounded.** No endpoint returns an unbounded list; every list has a default and maximum page size. *Why:* an unbounded query is an outage waiting for the table to grow.
6. **Evolve additively; version on breakage.** Adding an optional field is not a breaking change; removing/renaming/retyping is — that needs a new version. *Why:* additive change keeps every existing client working.
7. **Validate at the boundary, reject fast.** Reject malformed input with `400` and a field-level error list before any business logic runs. *Why:* untrusted input should never reach the domain.

## Anti-Patterns

- `200 OK` wrapping `{"success": false}` — breaks every generic HTTP client and cache.
- A different error JSON shape per endpoint (`error` here, `message` there, `errors[]` elsewhere).
- `GET /users` that returns the entire table with no `limit`.
- Overloading one field with two meanings across contexts (a status that means shipping in one path and payment in another).
- Silent breaking changes: renaming a field in place and "telling clients to update".
- Leaking internals in errors — stack traces, SQL, or `NullPointerException` in the response body.

## Checklist

- [ ] Paths name resources (nouns); actions are sub-resources or verbs only where REST genuinely can't express them.
- [ ] Every response uses a status code that matches outcome class (2xx/4xx/5xx); no `200`-with-error.
- [ ] All errors share one envelope with a **stable `code`**, human `message`, optional `details`.
- [ ] Every create/payment/state-change accepts an **idempotency key** (or is documented as safe to retry).
- [ ] Every collection endpoint has a **default and max page size** and a documented pagination scheme.
- [ ] The change is **additive**, or a new API version was introduced for the breaking part.
- [ ] Input is validated at the boundary; invalid requests get `400` + field-level errors, no business logic runs.
- [ ] No internal detail (stack trace, SQL, framework exception) leaks into any response.

## Example

```text
Endpoint: create an order (idempotent), then list orders (paginated).

POST /orders
  Idempotency-Key: 4d9f...   # retry-safe: same key => same result, no duplicate order
  201 Created
  { "id": "ord_123", "status": "pending", "total": {"amount": 4200, "currency": "TWD"} }

Error (same envelope everywhere):
  422 Unprocessable Entity
  {
    "code": "order.line_items.empty",     # stable, machine-readable
    "message": "An order must contain at least one line item.",
    "details": [{ "field": "lineItems", "issue": "required" }]
  }

GET /orders?limit=20&cursor=eyJpZCI6...   # bounded; default 20, max 100
  200 OK
  { "data": [ ...20 orders... ], "nextCursor": "eyJpZCI6..." }
```
