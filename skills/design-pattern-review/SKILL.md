---
name: design-pattern-review
description: "审查设计模式使用是否必要、角色是否清楚、实现是否符合目标语言习惯，并发现过度设计、模式误用和可测试性问题。"
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

默认返回一份 **Markdown 审查报告**，而不是固定 YAML 文件。报告必须包含：

1. 总体结论：pass / needs_changes / fail
2. 模式适配度
3. 分级发现
4. 证据
5. 修正建议
6. 更简单替代方案
7. 目标语言惯用性说明
8. 必改项

当结果需要交给 workflow 或后续 SKILL 串接时，在文末追加一个可选的 `structured_summary` 小节即可：

~~~yaml
structured_summary:
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
  required_changes:
    - change:
~~~

> **返回自检**：正文必须先是可读的 Markdown 审查报告；`fail` 必须给可执行替代方案；每条 high/critical 必须有证据；不得把“没按某语言经典写法”误判为错误。
