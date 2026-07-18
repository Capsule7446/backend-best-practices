# Backend Best Practices（后端最佳实践）

Backend Best Practices 将后端代码优化从“靠经验判断”变成可重复、可验收的工程流程，覆盖 DDD、应用层、CQRS 读模型、GoF 设计模式和系统建模。

## 适用场景

- 读懂既有系统、梳理领域边界和调用链。
- 新功能从 0 到 1 建模，或对既有系统进行渐进式重构。
- 判断是否需要 CQRS、读模型、聚合视图或设计模式。
- 审查领域模型、应用层、契约、骨架和迁移切片。

## Command

### 系统与 DDD

`system-model-view-read`、`ddd-new`、`ddd-refactor`、`ddd-review`、`ddd-application-review`、`ddd-spec`、`ddd-scaffold`。

### CQRS 读模型

`cqrs-read-model-new`、`cqrs-read-model-refactor`、`cqrs-read-model-review`。

### 设计模式

`design-pattern` 负责模式适配性判断；另有 23 个 `design-pattern-<pattern>` 命令，覆盖创建型、结构型和行为型 GoF 模式。

完整入口见 [`commands/`](commands/)。

## Workflow

| Workflow | 用途 |
| --- | --- |
| `workflow-system-model-view-read` | 系统阅读、入口地图、领域视图和风险报告。 |
| `workflow-greenfield` | 新系统或新上下文的 DDD 建模与落地。 |
| `workflow-brownfield` | 既有系统的调查、接缝识别、绞杀式迁移和分片重构。 |
| `workflow-read-model-greenfield` / `workflow-read-model-brownfield` / `workflow-read-model-review` | 读模型的设计、迁移和审查。 |
| `workflow-design-pattern` | 设计模式 fit check、方案、实现和审查。 |

## Skill

技能按阶段分为：

- `ddd-*`：上下文、子域、聚合、领域交互、应用编排、端口适配器、接缝、迁移和验收。
- `cqrs-*`：读模型适配性、聚合视图、设计、实现、同步和验收。
- `design-pattern-*`：23 个 GoF 模式、适配性检查、机会扫描、实现和审查。

完整清单见 [`skills/`](skills/)。技能是 Workflow 的可复用步骤，不建议绕过路由直接拼接不相关步骤。

## 推荐流程

```text
system-model-view-read
→ ddd-refactor 或 ddd-new
→ cqrs-read-model-refactor（确有读侧复杂度时）
→ design-pattern（确有稳定变化轴时）
→ review → spec → scaffold → acceptance
```

每个切片都应有特征化测试、契约、不变量、灰度切换和回滚路径。目标不是套用架构，而是让代码更容易解释、测试和局部替换。

## 不适用场景

- 只改一个文案、格式或简单函数，不需要架构分析。
- 没有代码、业务约束或验收标准，却要求生成完整架构。
- 为了“显得专业”而强行引入 CQRS 或设计模式。
