---
name: bbp-data-integrity
description: "Protect data correctness: transaction boundaries, consistency choices, concurrency control, and safe schema migrations. Trigger when writing persistence code, multi-step writes, or database migrations."
risk: safe
category: data
tags: "[backend, data, transactions, migrations]"
---

# Backend Best Practices — Data Integrity

Most "impossible" production bugs are integrity bugs: a partial write, a lost update, a migration that locked the table. This skill keeps writes correct under concurrency and failure, and keeps schema changes safe under live traffic.

## When to Use

- Writing code that persists state, especially multi-step or multi-row writes.
- Introducing concurrency on shared data (counters, balances, inventory, bookings).
- Authoring or reviewing a database migration that runs against a live system.

## Principles

1. **A business operation is one transaction.** Everything that must be true together commits together, or not at all. *Why:* partial writes leave the system in a state no code expects.
2. **Keep transactions short; never wait on the outside world inside one.** No HTTP calls, no queue publishes, no user input while a transaction (and its locks) is open. *Why:* an open transaction holds locks; external latency turns into contention and deadlocks.
3. **Choose consistency explicitly.** Decide per operation: strong consistency (same transaction) or eventual (via an event), and write down why. *Why:* accidental eventual consistency is just a race condition with a nicer name.
4. **Guard concurrent writes with a version or a lock.** Use optimistic concurrency (version column, compare-and-set) by default; reserve pessimistic locks for genuine hotspots. *Why:* read-modify-write without a guard silently loses updates.
5. **Make retriable writes idempotent.** A retry of the same logical operation must not double-apply (dedupe key, unique constraint, or upsert). *Why:* every layer above will retry on timeout.
6. **Cross-service or cross-aggregate consistency is eventual, with compensation.** Coordinate via events/outbox and define the compensating action for failure. *Why:* two-phase commit across services is a distributed liability; sagas are the sane default.
7. **Migrations are expand → migrate → contract, and always reversible.** Add the new shape, backfill and dual-write, then remove the old shape in a later release — each step deployable and rollback-safe. *Why:* an in-place `ALTER`/rename breaks the running old code the instant it deploys.

## Anti-Patterns

- Two related writes with no shared transaction ("insert order, then decrement stock") — a crash between them corrupts state.
- An external API call in the middle of an open transaction.
- Read-modify-write on a balance/counter with no version check → lost updates under load.
- Treating a DB row as the aggregate and letting any code mutate any column directly.
- A migration that renames/drops a column in one step while old code still reads it.
- Using `double`/`float` for money.

## Checklist

- [ ] Each business operation commits atomically — all-or-nothing, one transaction.
- [ ] No network/queue/user wait happens inside an open transaction.
- [ ] Strong vs eventual consistency is a **documented choice** per write path, not an accident.
- [ ] Concurrent writes to shared data use **optimistic version or explicit lock**; no unguarded read-modify-write.
- [ ] Retriable writes are **idempotent** (dedupe key / unique constraint / upsert).
- [ ] Cross-service/aggregate flows use events + a defined **compensation**, not distributed transactions.
- [ ] Migrations follow **expand → migrate → contract**, each step reversible and safe for the currently-deployed code.
- [ ] Money uses integer minor units or decimal — never binary floating point.

## Example

```text
Scenario: place an order and reserve stock, safely, under concurrency.

# Principle 1 + 4: atomic reserve with optimistic concurrency
UPDATE stock
   SET quantity = quantity - 1, version = version + 1
 WHERE sku = 'ABC' AND quantity >= 1 AND version = :expectedVersion;
# 0 rows affected => someone else won the race => reject, don't retry blindly.

# Principle 6: order + stock live in one aggregate/tx; fulfillment is another service.
# So publish an event instead of reaching across:
BEGIN;
  INSERT INTO orders(id, status) VALUES ('ord_123', 'confirmed');
  INSERT INTO outbox(topic, payload) VALUES ('OrderConfirmed', '{"orderId":"ord_123"}');
COMMIT;                     # event is delivered by the outbox relay, after commit

# Principle 7: rename column `status` -> `fulfillment_status` without downtime
#   v1: ADD fulfillment_status; app dual-writes both columns
#   v2: backfill fulfillment_status; app reads new, still writes both
#   v3: DROP status                      # only after no code references it
```
