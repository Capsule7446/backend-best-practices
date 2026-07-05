---
name: design-pattern-review
description: "审查设计模式使用是否必要、角色是否清楚、实现是否符合目标语言习惯，并发现过度设计、模式误用和可测试性问题。"
risk: safe
category: validation
inputs: "设计模式方案 / 代码片段 / 目标语言 / 设计约束 / 测试"
outputs: "审查结论 / 分级发现 / 修正建议 / 更简单替代方案"
tags: "[design-patterns, review, over-engineering, maintainability, language-agnostic]"
---

# Design Pattern Review（模式审查）

## 做什么

审查一份设计模式方案或代码实现，判断它是否真正提升可维护性，并指出模式误用、语言不惯用和过度设计。

## 需要什么参数

- **必需**：方案或代码、声称使用的模式、目标语言、设计目标。
- **可选**：测试、性能约束、并发约束、未来变化假设。

## 怎么做

1. 验证模式是否匹配真实变化轴，而不是只匹配类图形状。
2. 检查角色职责是否单一，协作是否清楚，依赖方向是否稳定。
3. 检查目标语言实现是否惯用，是否能用更简单机制表达。
4. 标记全局状态、隐式控制流、继承滥用、抽象泄漏和测试困难。
5. 给出最小修正路径；必要时建议退回普通函数、组合或依赖注入。

## 返回什么

```yaml
verdict: pass | needs_changes | fail
pattern:
fit_score: 0-100
findings:
  - severity: critical | high | medium | low
    issue:
    evidence:
    fix:
simpler_alternatives:
  - alternative:
    when_to_prefer:
language_idiom_notes:
  - note:
required_changes:
  - change:
```

> **返回格式自检**：`fail` 必须给可执行替代方案；每条 high/critical 必须有证据；不得把“没按某语言经典写法”误判为错误。
