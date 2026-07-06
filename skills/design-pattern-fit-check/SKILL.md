---
name: design-pattern-fit-check
description: "把设计问题映射到 GoF 设计模式，按创建型、结构型、行为型三类给出最小可行模式选择，避免为套模式而套模式。"
---

# Design Pattern Fit Check（模式适配判断）

## 做什么

判断一个设计问题是否需要设计模式，并从创建型、结构型、行为型模式中选择最小、最贴合变化轴的方案。

## 需要什么参数

- **必需**：设计问题、当前代码结构或目标结构、主要变化轴、不可破坏的约束。
- **可选**：目标语言、框架限制、性能要求、并发要求、测试约束、团队熟悉度。

## 怎么做

1. 先识别问题本质：对象创建、结构组合/适配、行为分派/协作/状态变化。
2. 先评估语言原生机制、简单函数、组合、依赖注入是否足够。
3. 从三类模式中各列候选，并标明每个候选解决的变化轴。
4. 选择一个首选模式；只在职责确实分离时才加入辅助模式。
5. 明确不推荐模式，特别是会增加层级、隐藏控制流或制造全局状态的方案。
6. 按需读取 `references/design-pattern-catalog.md` 与 `references/design-pattern-language-profiles.md`。

## 返回什么

默认返回一份 **Markdown 设计说明**，而不是固定 YAML 文件。说明必须包含：

1. 模式思想
2. 适用场景
3. 不适用场景
4. 角色与职责
5. 最佳实践范式
6. 目标语言实现提示
7. 案例摘要
8. 测试点
9. 权衡与风险

当结果需要交给 workflow 或后续 SKILL 串接时，在文末追加一个可选的 `structured_summary` 小节即可：

~~~yaml
structured_summary:
  pattern: Design Pattern Fit Check（模式适配判断）
  category:
  use_when:
    - item
  avoid_when:
    - item
  roles:
    - name:
      responsibility:
  target_language:
  implementation_idioms:
    - item
  tests:
    - case:
      verifies:
  tradeoffs:
    - item
~~~

> **返回自检**：正文必须先是可读的 Markdown 设计说明；`structured_summary` 只作为串接摘要，不得替代完整说明。

---

附加参考（按需读取）：`references/design-pattern-catalog.md`、`references/design-pattern-language-profiles.md`。
