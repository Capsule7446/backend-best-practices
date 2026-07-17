---
name: ddd-application-orchestration
description: "为每个应用用例设计执行编排：步骤顺序、Unit of Work 与事务边界、幂等方案、领域事件→集成事件与 Outbox、重试边界与可观测性——只编排，不做业务判断。"
risk: safe
category: application
inputs: "应用用例目录（含 Input Port、领域调用、错误语义）+ 事务与一致性策略 + 可靠性/审计要求"
outputs: "用例编排表 / 事务边界声明 / 幂等方案 / 事件投递策略 / 重试边界 / 可观测性要求 / 长流程候选清单"
tags: "[application, orchestration, unit-of-work, idempotency, outbox]"
---

# Application Orchestration（应用编排设计）

## 做什么

回答"用例如何执行、事务在哪里、幂等和事件投递如何保证"。编排只决定"先做什么后做什么"，**不决定"业务上是否允许"**——业务判断全部委派给聚合与领域服务。

## 需要什么参数

- **必需**：应用用例目录（每个用例含 Input Port、领域调用、错误语义）；事务与一致性策略。
- **可选**：可靠投递要求、审计要求、基础设施约束（有无消息中间件等）。

## 怎么做

1. **写用例标准步骤序**：用例授权 → 幂等查取/占用 → 开启 UoW → 加载聚合 → 调用聚合/领域服务 → 保存（带期望版本）→ 领域事件映射集成事件并 append Outbox → 提交 → 存幂等结果 → 映射 Result。每步标 owner（application / domain），偏离标准序须写明理由。
2. **声明事务边界**：单聚合实例单事务；一个事务修改多聚合实例必须显式解释；列回滚触发（领域拒绝 / 持久化错误 / Outbox 追加失败）。
3. **设计幂等方案**：作用域至少 `tenant + actor + use_case + idempotency_key`；同 key 不同载荷 → reject；已完成请求 → 返回原结果。**必须覆盖崩溃窗口**：幂等完成记录与业务提交同一 UoW，或 reservation 用带过期的 lease/状态机。命令幂等与消费者 Inbox 去重是两个机制，不得混用。
4. **定事件投递策略**：领域事件→集成事件的映射归 Application；要求可靠投递时用 transactional outbox 或等价机制——不允许存在"数据库已提交、事件永久丢失"窗口。
5. **隔离外部 I/O**：外部网络调用不进无界事务；跨边界动作走提交后处理 / Outbox 投递器 / 长流程（登记为候选，交长流程决策能力处理）。
6. **划重试边界**：可重试（瞬时持久化错误、业务安全的乐观冲突）；禁止重试（领域拒绝、授权失败、幂等冲突）。
7. **登记可观测性**：correlation_id 必须；事件带 causation_id；受审计用例声明审计点。

## 返回什么

每个写用例一条编排条目：

~~~yaml
orchestration:
  use_case_id:
  steps:
    - { order:, action:, owner: application | domain, port: }
  transaction:
    aggregate_instances_modified:
    optimistic_lock:
    rollback_on: []
  idempotency:
    required:
    scope: []
    same_key_different_payload: reject
    completed_request: return_previous_result
    crash_window_strategy: same_uow | lease
  events:
    reliable_delivery_required:
    strategy: transactional_outbox | after_commit | none
  retry: { allowed_for: [], forbidden_for: [] }
  observability: { correlation_id:, causation_id:, audit: }
~~~

另附：长流程候选清单（跨事务/跨时间/需补偿的用例）。

> **返回格式自检**：每个写用例有完整步骤序且每步有 owner；事务边界与回滚触发齐全；可重试入口的幂等方案覆盖崩溃窗口；要求可靠投递的用例无"已提交但事件丢失"窗口；步骤中不含任何业务规则判断；长流程候选已单列。

---

附加文件（按需读取）：`examples.md` — 取消订单编排走查。
