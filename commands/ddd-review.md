---
description: 对现有建模工件做质量评估。薄入口：仅调用 ddd-model-review 能力。
argument-hint: <建模工件路径/描述> [--focus=一致性|完整性|不变量|聚合|可实现性]
---

# /backend-best-practices:ddd-review

薄入口。把工件交给 **`ddd-model-review`** 能力执行，产出五维评分/问题清单/发现/结论。

- `$ARGUMENTS`：待评估的建模工件（路径或描述，必需）。
- `--focus`：可选，聚焦某一维。

动作：调用 `ddd-model-review`，输入工件路径、输出评估报告文件。回溯目标由调用方/workflow 依据发现决定，本命令不编排。
