---
name: design-pattern-builder
description: "GoF Builder（建造者）设计模式能力。用于在 构造参数多、默认值多、校验复杂，或同一构造过程需要生成不同表示。 时，输出语言无关思想、适用场景、最佳实践范式、多语言实现差异和案例。"
entrypoint: fixed-pattern
workflow: workflow-design-pattern
pattern: builder
argument-hint: <设计问题或代码路径> [--lang=<语言>]
---


## 固定入口

该 Skill 同时承担固定模式入口：将输入交给 `workflow-design-pattern` 编排，并将候选模式固定为 `builder`。

参数：`<设计问题或代码路径> [--lang=<语言>]`

# Builder（建造者）

## 做什么

使用 建造者 模式解决这类问题：把复杂对象的构造步骤与最终表示分离。

## 思想

- 把稳定部分和变化部分分离。
- 让调用方依赖稳定抽象，而不是依赖会频繁变化的具体实现。
- 通过 创建型 模式的角色协作，把变化限制在可替换、可测试、可演进的边界内。

## 适用场景

- 构造参数多、默认值多、校验复杂，或同一构造过程需要生成不同表示。
- 变化轴明确，且简单函数、组合或语言原生机制不足以保持清晰。
- 需要让新增变体的成本低于修改既有调用方的成本。

## 不适用场景

- 简单 DTO 或只有两三个参数时不要引入。
- 需求尚未证明会变化，只是为了“看起来有设计模式”。
- 模式引入的抽象比问题本身更难理解、测试或排查。

## 需要什么参数

- **必需**：设计目标、当前结构或目标结构、变化轴、目标语言。
- **可选**：性能约束、并发约束、框架限制、测试框架、现有接口。

## 最佳实践范式

- Builder 负责收集参数和校验组合；目标对象保持不可变；必填字段尽量通过构造器或分阶段 builder 表达。
- 先写语言无关角色：Client、抽象角色、具体变体、创建/协作边界。
- 再按目标语言选择惯用实现，不强制复制 Java 类图。
- 保持模式最小化：每个新增抽象必须对应一个真实变化轴。
- 为替换变体、失败路径和边界条件写测试。

## 怎么做

1. 明确要保护的稳定接口和要隔离的变化点。
2. 定义模式角色、职责和协作消息。
3. 选择目标语言的最小惯用表达。
4. 给出案例代码或伪代码，并标出可替换点。
5. 审查是否存在过度设计、隐藏状态或不清楚的生命周期。

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
  pattern: Builder（建造者）
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

附件（按需读取）：language-differences.md、examples.md。
