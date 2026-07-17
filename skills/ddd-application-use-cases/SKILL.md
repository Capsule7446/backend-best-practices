---
name: ddd-application-use-cases
description: "把参与者、命令与策略映射成应用用例目录：每个写命令一个 Use Case——Input Port、Command/Result 形状、授权分层、领域调用与错误语义，全部语言中立。"
risk: safe
category: application
inputs: "含 {命令·事件目录, 参与者, 策略清单} 与 {聚合目录, 不变量表, 领域服务契约} 的工件（可选：安全/审计/兼容约束）"
outputs: "应用用例目录 / Input Port 清单 / Command·Result 契约 / 授权分层表 / 错误语义表 / 用例追踪表"
tags: "[application, use-case, input-port, command]"
---

# Application Use Cases（应用用例目录）

## 做什么

回答"系统有哪些应用用例、谁调用、输入输出是什么、调用哪个领域行为"。每个**写命令**映射到唯一 Use Case；查询只登记归属（读侧契约由查询侧能力设计）。用例是 Interface 层与 Domain 层之间的稳定契约。

## 需要什么参数

- **必需**：一份含 {命令·事件目录, 参与者, 策略清单} 的发现工件；一份含 {聚合目录, 不变量表, 领域服务契约} 的战术工件。
- **可选**：安全/审计要求、兼容约束、幂等要求来源（重试入口清单）。

## 怎么做

1. **提取写命令**：逐条建 Use Case（`UC-<CTX>-<NAME>`），不建的必须标注排除理由；查询命令只登记为查询用例占位。
2. **定 actor 与触发**：每个用例声明 actor 类型、是否需认证、触发方式（http / message / job / cli）。
3. **定义 Input Port 与 Command 形状**：业务输入字段 + `expected_version?` + `idempotency_key?`，全部中立类型。
4. **授权分层登记**：用例级授权归 Application；资格/所有权等业务不变量归 Domain；Authentication 归入站适配器。此处只登记归属，不重复判定。
5. **映射领域调用**：每个用例 → 聚合根方法或领域服务 + 所守不变量编号 + 预期领域事件。
6. **定 Result 与错误语义**：Result 只含本事务已确认事实（id、提交后状态、聚合版本、consistency_token?）；错误为具名集合（Unauthorized / NotFound / 领域具名拒绝 / ConcurrencyConflict / IdempotencyConflict）。
7. **建追踪链**：`GOAL → CMD → UC → AGG方法 → INV → EVT → AC`，缺环即缺陷。

## 返回什么

每个用例一条结构化条目：

~~~yaml
use_case:
  id: UC-<CTX>-<NAME>
  bounded_context:
  kind: command | query
  actor: { type:, authentication_required: }
  trigger: { type: http | message | job | cli, source: }
  input_port:
  command: { type:, fields: }
  authorization: { application: [], domain: [] }
  domain_invocations:
    - { aggregate:, method:, invariants: [] }
  expected_events: []
  result: { type:, fields: }
  errors: []
  acceptance: []
~~~

另附：Input Port 清单、错误语义表、`GOAL→CMD→UC→AGG→INV→EVT→AC` 追踪表。

> **返回格式自检**：每个写命令有唯一 UC 或显式排除理由；每个 UC 归属一个 bounded context；每个业务行为追踪到聚合方法/领域服务与不变量编号；Command/Result 不暴露领域实体、ORM 实体、HTTP 或消息框架类型；错误集合具名且含并发/幂等冲突。

---

附加文件（按需读取）：`examples.md` — 取消订单用例走查。
