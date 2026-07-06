---
name: design-pattern-implementation
description: "把选定设计模式转成语言无关蓝图，并按 Java、TypeScript、Python、Go、C#、Kotlin、Rust 等主流语言生成惯用实现。"
---

# Design Pattern Implementation（模式实现）

## 做什么

将已选设计模式落成可维护实现：先输出语言无关结构，再按目标语言生成符合当地习惯的代码或伪代码。

## 需要什么参数

- **必需**：模式名称、具体模式 SKILL 产出的指南、使用场景、业务角色、目标语言。
- **可选**：现有接口、命名规范、并发/性能要求、框架边界、测试框架。

## 怎么做

1. 读取具体 `design-pattern-<pattern>` SKILL 的意图、适用条件、角色、协作关系、语言差异附件和案例附件。
2. 先写语言无关蓝图：角色、接口、对象生命周期、错误边界、扩展点。
3. 依据目标语言选择惯用表达，不机械翻译 Java 类图。
4. 保留模式的最小结构，避免加入无需求支撑的抽象层。
5. 给出关键测试点：替换性、扩展性、边界条件、并发或生命周期。
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
  pattern: Design Pattern Implementation（模式实现）
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
