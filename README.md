# Backend Best Practices

后端最佳实践插件用于把后端代码优化从“靠经验判断”变成可重复执行的工程流程。

它覆盖两类场景：

- **全量优化**：从一个既有后端系统出发，先读懂现状，再规划架构重构、读模型拆分、设计模式落地和验收。
- **增量优化**：围绕一个模块、接口、PR、性能问题或设计坏味道，做小范围诊断、修正和审查。

核心原则：先解释现状，再决定是否重构；先补安全网，再改实现；一次只推进一个可验收切片。

---

## 能力总览

| 目标 | 使用能力 |
| :-- | :-- |
| 读懂当前系统 | `system-model-view-read` |
| 既有项目渐进重构 | `ddd-refactor` |
| 新功能从 0 到 1 建模 | `ddd-new` |
| 判断读侧是否需要 CQRS | `cqrs-read-model-review` / `cqrs-read-model-refactor` |
| 设计业务聚合视图和读模型 | `cqrs-read-model-new` / `cqrs-read-model-refactor` |
| 判断是否适合设计模式 | `design-pattern` |
| 固定某个 GoF 模式落地 | `design-pattern-<pattern>` |
| 审查领域模型 | `ddd-review` |
| 生成接口优先的契约和骨架 | `ddd-spec` / `ddd-scaffold` |

常用命令：

```text
/backend-best-practices:system-model-view-read <代码路径>
/backend-best-practices:ddd-refactor <代码路径>
/backend-best-practices:ddd-new <需求描述>
/backend-best-practices:cqrs-read-model-refactor <代码路径或现状>
/backend-best-practices:cqrs-read-model-review <工件>
/backend-best-practices:design-pattern <设计问题或代码路径> --lang=<语言>
/backend-best-practices:design-pattern-<pattern> <设计问题或代码路径> --lang=<语言>
```

---

## 全量代码优化流程

全量优化适合这些情况：

- 系统已经能跑，但领域边界、模块职责或调用链混乱。
- 想做架构梳理、拆模块、拆服务、读写分离或长期维护性治理。
- 不确定当前架构适合怎么重构。
- 需要先形成“现状地图 + 重构路线图”，再逐步落地。

推荐顺序：

```text
1. system-model-view-read
2. ddd-refactor
3. cqrs-read-model-refactor
4. design-pattern
5. ddd-review / cqrs-read-model-review / design-pattern-review
6. ddd-spec / ddd-scaffold
```

### 1. 先读懂系统

先不要改代码，先运行：

```text
/backend-best-practices:system-model-view-read <代码路径>
```

目标产物：

- 系统一句话业务定位。
- API / Controller / Job / Consumer 到业务用例的入口地图。
- 子域、限界上下文、聚合、不变量和领域交互。
- 页面、API、报表对应的业务视图和字段来源。
- 写侧 Domain 与读侧 Read Model / View Model 的边界。
- 风险和坏味道清单。
- 最小修正路径。

判断标准：

- 能从业务概念反查代码位置。
- 能从代码入口反查业务含义。
- 能说明哪些逻辑属于领域真源，哪些只是查询展示。

### 2. 决定全量重构边界

读码报告完成后，再运行：

```text
/backend-best-practices:ddd-refactor <代码路径>
```

它会走 brownfield workflow：

```text
ddd-code-survey
→ ddd-seam-finder
→ ddd-strangler-plan
→ 逐切片建模、实现、验收
```

目标产物：

- 现状领域模型。
- 隐含上下文和坏味道。
- 可切割接缝。
- 防腐层 ACL 落点。
- 绞杀式迁移批次。
- 每个切片的回滚策略和特征化测试范围。

放行条件：

- 旧系统全程可运行。
- 每个切片能独立交付、独立回滚。
- 没有特征化测试覆盖前，不直接替换旧行为。

### 3. 梳理读侧和查询模型

如果系统存在复杂列表页、报表、搜索、聚合统计、跨表查询或 API DTO 污染领域模型，运行：

```text
/backend-best-practices:cqrs-read-model-refactor <代码路径或现状>
```

它会判断是否真的需要 CQRS 式读模型，而不是默认引入复杂度。

重点检查：

- 查询是否把聚合 Entity 直接暴露给 API。
- UI 字段是否缺少真源。
- 读侧排序、筛选、聚合是否污染写侧模型。
- 新鲜度要求是否明确。
- 同步、重建、失败补偿策略是否可接受。

可能结论：

- `avoid`：普通 DTO / Query Service 足够。
- `partial`：只为部分高复杂视图建立读模型。
- `use`：读写模型确实需要分离。

### 4. 只在有变化轴时使用设计模式

如果某个切片里出现稳定接口 + 多种变化、复杂对象创建、状态生命周期、处理链或外部系统适配，再运行：

```text
/backend-best-practices:design-pattern <设计问题或代码路径> --lang=<语言>
```

它会先做 fit check：

- 是否真的需要模式。
- 是否可以用简单函数、组合、依赖注入或语言原生机制解决。
- 创建型、结构型、行为型中哪些模式匹配变化轴。
- 哪些模式不推荐。

固定模式时：

```text
/backend-best-practices:design-pattern-strategy <问题> --lang=java
/backend-best-practices:design-pattern-state <问题> --lang=typescript
/backend-best-practices:design-pattern-adapter <问题> --lang=go
```

原则：

- 模式服务变化轴，不服务“看起来专业”。
- 每次只引入最小必要模式。
- 先给语言无关角色和协作，再生成目标语言惯用实现。

### 5. 验收和落地

全量优化不是一次性重写。每个切片都要经过：

```text
特征化测试
→ 局部建模
→ 模型审查
→ 契约规范
→ 接口骨架
→ 适配实现
→ 验收
→ 灰度切换
```

相关命令：

```text
/backend-best-practices:ddd-review <工件>
/backend-best-practices:ddd-spec <战术工件>
/backend-best-practices:ddd-scaffold <规范> --lang=<语言>
/backend-best-practices:cqrs-read-model-review <工件>
```

完成标准：

- 旧行为有测试锁住。
- 新实现通过契约、不变量和等价行为验收。
- 切换路径可灰度。
- 回滚路径明确。
- 临时 ACL 有退役计划。

---

## 增量代码优化流程

增量优化适合这些情况：

- 一个模块职责过大。
- 一个接口响应结构混乱。
- 一个 PR 引入设计风险。
- 一个查询越来越慢。
- 一段代码可能适合抽象，但不确定用什么模式。
- 只想优化一个切片，不想启动全量改造。

推荐顺序：

```text
1. 先定位问题类型
2. 选择最小 workflow 或 skill
3. 输出局部方案
4. 修改代码
5. 用对应 review 能力复查
```

### 问题类型选择表

| 现象 | 优先使用 |
| :-- | :-- |
| 看不懂模块承担什么业务 | `system-model-view-read`，限定关注模块 |
| 领域对象越来越像数据库表 | `ddd-review` 或 `ddd-refactor` |
| Service 很厚，规则散落 | `ddd-refactor` |
| API DTO 直接绑 Entity | `cqrs-read-model-refactor` |
| 列表页/报表查询复杂 | `cqrs-read-model-refactor` |
| 同一个行为有多种算法 | `design-pattern`，常见候选 `strategy` |
| 生命周期状态判断很多 | `design-pattern`，常见候选 `state` |
| 外部/遗留接口污染内部模型 | `design-pattern` 或 `ddd-refactor`，常见候选 `adapter` / ACL |
| 复杂子系统需要统一入口 | `design-pattern`，常见候选 `facade` |
| PR 只想做设计审查 | `ddd-review` / `cqrs-read-model-review` / `design-pattern-review` |

### 增量优化模板

给 Agent 的输入建议包含：

```text
目标：
代码路径：
当前问题：
不可破坏的行为：
目标语言/框架：
性能或兼容约束：
希望产出：诊断 / 计划 / 代码修改 / review
```

示例：

```text
/backend-best-practices:system-model-view-read src/order --focus=订单状态流转
```

```text
/backend-best-practices:cqrs-read-model-refactor src/reporting --goal=优化运营报表查询
```

```text
/backend-best-practices:design-pattern src/payment --lang=java --goal=不同支付渠道策略可扩展
```

### 增量优化的放行标准

每次小改都至少满足：

- 改动边界清楚。
- 旧行为没有被意外改变。
- 新抽象有明确变化轴。
- 读侧和写侧职责没有混在一起。
- 测试覆盖了关键分支。
- Review 没有 critical/high 问题。

---

## 全量和增量如何配合

推荐节奏：

```text
全量读码报告
→ 全量重构路线图
→ 选择第一个小切片
→ 增量落地
→ review
→ 合并
→ 下一个切片
```

不要把全量优化理解成一次性大重写。全量流程负责建立方向和地图，增量流程负责一片一片安全落地。

---

## 产物目录建议

建议为每次运行建立独立工作区：

```text
run/
  system-read/
    00-routing.md
    01-code-survey.md
    ...
    15-system-reading-report.md
  refactor/
    01-survey.md
    02-seams.md
    03-plan.md
    slice-order/
      00-characterization.md
      01-aggregates.md
      ...
  read-model/
    01-fit-check.md
    ...
  design-pattern/
    01-design-pattern-fit.md
    ...
```

保留这些工件可以让后续 PR、审查和重构决策有依据。

---

## 最小使用指南

如果你只有一个后端项目，不知道从哪开始：

```text
/backend-best-practices:system-model-view-read <代码路径>
```

如果你已经知道要重构某个模块：

```text
/backend-best-practices:ddd-refactor <模块路径>
```

如果问题集中在查询、列表页、报表或 API 响应：

```text
/backend-best-practices:cqrs-read-model-refactor <模块路径或现状描述>
```

如果你怀疑需要设计模式：

```text
/backend-best-practices:design-pattern <问题或代码路径> --lang=<语言>
```

最终目标不是“套上架构”，而是让后端代码更容易解释、更容易测试、更容易局部替换，并且每一步都能回滚。
