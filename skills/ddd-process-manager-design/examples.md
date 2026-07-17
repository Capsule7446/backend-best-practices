# 走查示例：订单履约

输入（节选）：候选 `UC-ORDERING-FULFILL-ORDER`——付款确认后预留库存、超时未付关单；跨 Ordering/Billing/Inventory 三个上下文。

判定：跨多个本地事务 + 等待外部事件 + 需超时与补偿 → `process_manager`。

~~~yaml
process_decision:
  use_case_id: UC-ORDERING-FULFILL-ORDER
  decision: process_manager
  reason: 跨 3 个上下文的本地事务，需等待支付事件，未付款需 30 分钟超时关单，库存不足需退款补偿。

process_manager:
  id: PM-ORDERING-FULFILLMENT
  owner_context: Ordering
  correlation_key: order_id
  states: [ awaiting_payment, paid, awaiting_inventory, inventory_reserved, completed, compensation_required, failed ]
  transitions:
    - { on: PaymentConfirmed, from: awaiting_payment, to: paid, emits_command: ReserveInventory }
    - { on: InventoryReserved, from: paid, to: inventory_reserved, emits_command: ConfirmFulfillment }
    - { on: InventoryReservationRejected, from: paid, to: compensation_required, emits_command: RefundPayment }
    - { on: PaymentRefunded, from: compensation_required, to: failed }
  timeouts:
    - { state: awaiting_payment, after: PT30M, emits_command: ExpireOrder }
  duplicate_handling: { event_id_deduplication: true }
  ordering: { key: order_id, source_version_required: true }
  compensation:
    - { when: InventoryReservationRejected, command: RefundPayment }
  recovery: { retry: 指数退避x3, dlq: 超限入死信, manual_intervention: 运营后台重放 }
~~~

反例（流程管理器里不允许出现）：

```text
if refund_amount > order.paid_amount ...   # 金额判定 → Billing 聚合的规则
if inventory.stock >= qty ...              # 库存判定 → Inventory 聚合的规则
```

对照候选 `UC-NOTIFY-ORDER-CANCELLED`（取消后发通知）：单事件单动作、无状态、失败可直接重试 → `choreography`，订阅事件即可，不建 PM。
