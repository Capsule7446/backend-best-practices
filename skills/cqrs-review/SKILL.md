---
name: cqrs-review
description: "审查 CQRS 读模型、聚合视图、领域解耦、同步策略和过度设计风险，输出分级发现与最小修正建议。"
risk: safe
category: validation
inputs: "CQRS 适配判断 / 聚合视图 / 读模型 / 同步策略 / API 或迁移设计"
outputs: "总体结论 / 严重度摘要 / 发现清单 / 最小可行修正 / 下一步"
tags: "[cqrs, review, read-model, architecture-review]"
---

# CQRS Review（读模型设计审查）

## 做什么

审查 CQRS Read Model 方案是否保护 Domain、是否按查询视图建模、是否有字段来源和刷新策略，并识别过度设计。

## 需要什么参数

- **必需**：读模型或聚合视图设计、字段来源、同步/刷新策略。
- **可选**：适配判断、API 契约、测试策略、迁移计划、代码路径。

## 怎么做

1. 检查 fit：是否真的需要独立读模型，简单 DTO/Query Service 是否已足够。
2. 检查 domain decoupling：Domain 是否被展示字段、统计字段、格式化字段污染。
3. 检查 read model：字段来源、派生规则、索引、查询契约是否清楚。
4. 检查 sync/freshness：刷新策略、延迟容忍、失败处理、重建策略是否明确。
5. 检查安全和测试：权限、字段映射、查询契约、同步失败和回归验证。
6. 标出反模式：Entity 直接响应 API、默认事件溯源、默认微服务、默认双库、隐藏 stale data。

## 返回什么

```yaml
overall: pass | needs_changes | fail
severity_summary:
  critical:
  high:
  medium:
  low:
findings:
  - severity:
    area:
    problem:
    recommendation:
    affected_artifact:
minimal_viable_fix:
next_steps:
```

> **返回格式自检**：每条发现有严重度、领域、问题、建议和影响工件；必须覆盖字段来源、刷新策略、Domain 污染和过度设计四类检查。

---

附加参考（按需读取）：`references/anti-patterns.md`。
