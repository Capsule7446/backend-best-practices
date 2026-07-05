---
name: design-pattern-implementation
description: "把选定设计模式转成语言无关蓝图，并按 Java、TypeScript、Python、Go、C#、Kotlin、Rust 等主流语言生成惯用实现。"
risk: safe
category: implementation
inputs: "模式适配决策 / 业务角色 / 目标语言 / 约束 / 现有接口或代码片段"
outputs: "语言无关蓝图 / 角色映射 / 惯用实现 / 测试点 / 演进注意事项"
tags: "[design-patterns, implementation, language-agnostic, java, typescript, python, go, csharp, kotlin, rust]"
---

# Design Pattern Implementation（模式实现）

## 做什么

将已选设计模式落成可维护实现：先输出语言无关结构，再按目标语言生成符合当地习惯的代码或伪代码。

## 需要什么参数

- **必需**：模式名称、使用场景、业务角色、目标语言。
- **可选**：现有接口、命名规范、并发/性能要求、框架边界、测试框架。

## 怎么做

1. 读取模式的意图、适用条件、角色和协作关系。
2. 先写语言无关蓝图：角色、接口、对象生命周期、错误边界、扩展点。
3. 依据目标语言选择惯用表达，不机械翻译 Java 类图。
4. 保留模式的最小结构，避免加入无需求支撑的抽象层。
5. 给出关键测试点：替换性、扩展性、边界条件、并发或生命周期。
6. 按需读取 `references/design-pattern-catalog.md` 与 `references/design-pattern-language-profiles.md`。

## 返回什么

```yaml
pattern:
category:
intent:
language_neutral_blueprint:
  roles:
    - name:
      responsibility:
  collaborations:
    - from:
      to:
      message:
target_language:
implementation:
  files:
    - path:
      purpose:
      code:
tests:
  - case:
    verifies:
tradeoffs:
  - item:
evolution_notes:
  - note:
```

> **返回格式自检**：实现必须能回溯到模式角色；目标语言代码不得强行保留不惯用的 Java 结构；每个新增抽象都要有变化轴支撑。

---

附加参考（按需读取）：`references/design-pattern-catalog.md`、`references/design-pattern-language-profiles.md`。
