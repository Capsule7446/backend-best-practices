---
name: ddd-process-manager-design
description: "条件能力：对跨事务、跨时间、需超时/补偿的长流程做 none/choreography/process-manager 决策；升级时设计流程管理器的状态、迁移、超时、补偿、去重与恢复。"
risk: safe
category: application
inputs: "长流程候选清单 + 相关事件契约 + 一致性与恢复要求"
outputs: "流程决策表 / 流程管理器设计（状态机/超时/补偿/去重/恢复）"
tags: "[application, process-manager, saga, compensation]"
---

# Process Manager Design（长流程决策与设计）

## 做什么

对"一个业务结果需要多个本地事务/多个上下文/一段时间才能达成"的流程，先判定是否值得引入流程管理器，再为确需升级的流程设计可恢复的协调器。**流程管理器只协调事实与命令，不拥有业务规则**——"是否允许退款""库存是否足够"永远由对应聚合判定。

## 需要什么参数

- **必需**：长流程候选清单（用例、涉及事务/上下文、时间跨度）；相关领域/集成事件契约。
- **可选**：超时与补偿的业务口径、人工介入渠道、消息基础设施能力。

## 怎么做

1. **逐候选判定**：仅当以下至少一条成立才考虑升级——跨多个本地事务；需等待外部事件；跨时间/跨上下文；需要超时、重试或补偿；进程重启后必须继续；需要人工介入恢复。都不成立 → `none`；事件链短且无需集中状态 → `choreography`；否则 → `process_manager`。每个结论写理由。
2. **设计流程管理器**（仅对升级者）：owner 上下文、correlation key、状态集（含终态与 `compensation_required`）、事件→迁移→发出命令、每个等待态的超时与超时命令。
3. **消息语义**：event_id 去重；按 correlation key 排序；乱序容忍策略。
4. **补偿映射**：每个失败事件 → 补偿命令；补偿仍失败 → 恢复策略（retry / DLQ / 人工介入）。
5. **恢复设计**：崩溃后从持久化状态继续；不确定态可查询对账。
6. **规则防线自检**：设计中出现"判断金额/资格/库存"即违规——改为向对应聚合发命令并消费其结果事件。

## 返回什么

~~~yaml
process_decision:
  use_case_id:
  decision: none | choreography | process_manager
  reason:

process_manager:            # 仅 decision=process_manager 时
  id: PM-<CTX>-<NAME>
  owner_context:
  correlation_key:
  states: []
  transitions:
    - { on:, from:, to:, emits_command: }
  timeouts:
    - { state:, after:, emits_command: }
  duplicate_handling: { event_id_deduplication: true }
  ordering: { key:, source_version_required: }
  compensation:
    - { when:, command: }
  recovery: { retry:, dlq:, manual_intervention: }
~~~

> **返回格式自检**：每个候选有显式决策与理由；每个状态可达且有出口（终态除外）；每个迁移有触发事件与目标；每个等待态有超时与超时动作；补偿链有终点（不允许无限补偿）；设计中不含任何业务资格/金额/库存判定。

---

附加文件（按需读取）：`examples.md` — 订单履约流程走查。
