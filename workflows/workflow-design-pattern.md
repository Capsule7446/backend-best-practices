# Workflow：Design Pattern

> 统筹者。用于从设计问题选择 GoF 设计模式，路由到对应的独立模式 SKILL，并生成语言惯用实现。由 `/backend-best-practices:design-pattern` 或 `/backend-best-practices:design-pattern-<pattern>` 触发。

## 0. 入口

1. 采集设计目标、现有代码/目标结构、变化轴、约束和目标语言。
2. 建运行工作区 `<workdir>/`（默认 `./run/design-pattern/`），写入 `_manifest.md`。
3. 若命令已固定模式（如 `design-pattern-state`），把它作为强候选，但仍需校验适配性。
4. 先判断是否需要模式；若 `decision=simplify/avoid`，不进入 02-04，以 `01-design-pattern-fit.md`（必须含 `simpler_alternative`）为最终产物，在 `_manifest.md` 记录结案。`simplify/avoid` 是正当结论，不算流程失败。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | design-pattern-fit-check | 用户诉求/代码路径 | `01-design-pattern-fit.md` | G0 |
| 02 | selected `design-pattern-<pattern>` | 用户诉求,`01-design-pattern-fit.md` | `02-pattern-guide.md` | G1 |

02 的 selected pattern 取 `01-design-pattern-fit.md` 中 `structured_summary.primary_pattern`；若命令入口已固定模式，则校验两者一致，不一致时停下让用户裁决。
| 03 | design-pattern-implementation | 用户诉求,`01-design-pattern-fit.md`,`02-pattern-guide.md` | `03-design-pattern-implementation.md` | |
| 04 | design-pattern-review | `01..03-*.md` + 代码/方案 | `04-design-pattern-review.md` | G2 |

## 2. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `01-design-pattern-fit.md` 后 | `structured_summary` 存在且含 `decision`（缺失视为格式不合格，重跑 01）；`decision=use` 必须有真实 `change_axis` 与 `primary_pattern`；`decision=simplify/avoid` 必须有 `simpler_alternative` |
| G1 模式指南 | `02-pattern-guide.md` 后 | 主体必须是 Markdown 设计说明，包含思想、适用场景、最佳实践范式、多语言附件和案例附件；可附 `structured_summary` 供串接 |
| G2 审查 | `04-design-pattern-review.md` 后 | Markdown 审查报告无 critical/high；实现符合目标语言习惯；新增抽象有明确职责 |

## 3. 模式路由表

| 类别 | 模式 SKILL |
| :-- | :-- |
| 创建型 | `design-pattern-abstract-factory` / `design-pattern-builder` / `design-pattern-factory-method` / `design-pattern-prototype` / `design-pattern-singleton` |
| 结构型 | `design-pattern-adapter` / `design-pattern-bridge` / `design-pattern-composite` / `design-pattern-decorator` / `design-pattern-facade` / `design-pattern-flyweight` / `design-pattern-proxy` |
| 行为型 | `design-pattern-chain-of-responsibility` / `design-pattern-command` / `design-pattern-interpreter` / `design-pattern-iterator` / `design-pattern-mediator` / `design-pattern-memento` / `design-pattern-observer` / `design-pattern-state` / `design-pattern-strategy` / `design-pattern-template-method` / `design-pattern-visitor` |

## 4. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 模式只匹配类图，不匹配问题 | design-pattern-fit-check |
| 选错具体模式 | design-pattern-fit-check + selected `design-pattern-<pattern>` |
| 模式指南缺少附件或案例 | selected `design-pattern-<pattern>` |
| 目标语言实现不惯用 | design-pattern-implementation |
| 角色职责混乱 | design-pattern-implementation |
| 过度设计或隐藏全局状态 | design-pattern-fit-check / design-pattern-review |
| 测试点不足 | design-pattern-implementation |

## 5. 编排纪律

- 本 workflow 是**独立入口**（局部设计问题直达）；在 greenfield/brownfield 主流程内，模式支线由主 workflow 直接调用同批纯 SKILL（scan → fit → 蓝图 → 层内实现 → review），不嵌套本 workflow。
- 蓝图（`03-design-pattern-implementation.md`）按 `owner_layer` 标注归属；落在分层代码库时，真实代码由该层实现能力按蓝图落地。
- 模式服务变化轴，不服务“看起来专业”。
- 三类模式都必须可选，但一次设计只保留最小必要组合；每个 GoF 模式都有独立 SKILL 承载细节。
- 具体模式 SKILL 以 Markdown 设计说明为主，不强制固定 YAML；需要串接时才追加 `structured_summary`。
- 输出实现时先给语言无关蓝图，再给目标语言代码。
- 不把 Java 类继承结构强加给 TypeScript、Python、Go、Rust 等语言。
