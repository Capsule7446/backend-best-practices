# Workflow：Design Pattern

> 统筹者。用于从设计问题选择 GoF 设计模式，并生成语言惯用实现。由 `/backend-best-practices:design-pattern` 触发。

## 0. 入口

1. 采集设计目标、现有代码/目标结构、变化轴、约束和目标语言。
2. 建运行工作区 `<workdir>/`（默认 `./run/`），写入 `_manifest.md`。
3. 先判断是否需要模式；若 `decision=avoid/simplify`，停止完整流程，只输出替代方案。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | design-pattern-fit-check | 用户诉求/代码路径 | `01-design-pattern-fit.md` | G0 |
| 02 | design-pattern-implementation | 用户诉求,`01-design-pattern-fit.md` | `02-design-pattern-implementation.md` | |
| 03 | design-pattern-review | `01..02-*.md` + 代码/方案 | `03-design-pattern-review.md` | G1 |

## 2. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `01-design-pattern-fit.md` 后 | `use` 必须有真实变化轴；`simplify/avoid` 必须有更简单方案 |
| G1 审查 | `03-design-pattern-review.md` 后 | 无 critical/high；实现符合目标语言习惯；新增抽象有明确职责 |

## 3. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 模式只匹配类图，不匹配问题 | design-pattern-fit-check |
| 目标语言实现不惯用 | design-pattern-implementation |
| 角色职责混乱 | design-pattern-implementation |
| 过度设计或隐藏全局状态 | design-pattern-fit-check / design-pattern-review |
| 测试点不足 | design-pattern-implementation |

## 4. 编排纪律

- 模式服务变化轴，不服务“看起来专业”。
- 三类模式都必须可选，但一次设计只保留最小必要组合。
- 输出实现时先给语言无关蓝图，再给目标语言代码。
- 不把 Java 类继承结构强加给 TypeScript、Python、Go、Rust 等语言。
