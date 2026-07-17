---
name: design-pattern-opportunity-scan
description: "扫描分层契约与代码中的真实变化轴，产出有证据的模式候选关注点清单；没有变化轴时输出空清单是正当结果。"
---

# Design Pattern Opportunity Scan（模式机会扫描）

## 做什么

在契约与代码稳定后扫描真实存在的变化轴，产出候选关注点清单，供后续逐个做适配判断。**没有变化轴时输出空清单是正当结果，不是失败。**

## 需要什么参数

- **必需**：分层契约（domain / application / read / adapter 各层接口与职责）；当前代码或接口骨架。
- **可选**：已知变体清单与已承诺的未来变化；复杂条件逻辑、状态生命周期、第三方边界的位置；测试与性能约束。

## 怎么做

1. **逐层扫描变化轴信号**：

   | 信号 | 典型表现 |
   | :--- | :--- |
   | 同一稳定接口下多实现 | 多个实现挂在同一契约后，且数量在真实增长 |
   | 复杂创建 | 构造需要多步骤、多前置校验或多种配置组合 |
   | 状态生命周期 | 实体有明确状态机，跃迁规则散落在条件分支里 |
   | 处理链 | 请求要依次经过多个可增减、可重排的处理环节 |
   | 外部边界 | 第三方接口形状与领域语言不合，或供应商可能更换 |

2. **先评估更简单机制**：每个候选关注点先问函数、组合、依赖注入、枚举、表驱动或语言原生机制是否足够；足够时记入 `simpler_alternatives`，可直接不立案。
3. **只留有证据的**：证据 = 已存在的多实现、已承诺的需求变化、复现过的修改热点；"将来可能会变"不是证据。
4. **标注归属与边界**：每个关注点标 `owner_layer` 与受影响契约，写明哪条接口是稳定边界（模式若引入，应藏在它后面）。
5. **无发现时**：`concerns` 输出空数组，并在正文说明扫描过哪些轴、为什么当前不需要模式。

## 边界

- 本扫描只**立案**，不做模式的最终选型与取舍；每个 concern 的适配决定留给后续判断。
- 不为凑数立案：宁可空清单，也不输出无证据的"教科书式机会"。
- 不建议会增加层级、隐藏控制流或制造全局状态的方案作为 `pattern_candidate`。

## 返回什么

默认返回一份 **Markdown 扫描说明**，包含：扫描范围与输入概况；各层发现（或未发现）的变化轴；每个关注点的证据、稳定边界与更简单替代评估；无发现时的"为什么不需要模式"说明。文末追加 `structured_summary` 供统筹方按字段分支与路由：

~~~yaml
structured_summary:
  concerns:
    - concern_id:
      owner_layer: domain | application | read | adapter
      problem:
      change_axis:
      evidence:
      stable_boundary:
      simpler_alternatives:
        - item
      pattern_candidate:
      affected_contracts:
        - item
~~~

> **返回自检**：每个 concern 必有 change_axis 与 evidence，无证据的关注点不得立案；没有变化轴时 `concerns` 为空数组（`[]`）且正文说明为什么不需要模式；`pattern_candidate` 只是候选待判，本扫描不做最终适配决定；正文必须先是可读的 Markdown 说明，`structured_summary` 不得替代它。
