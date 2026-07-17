---
description: 对应用层设计或实现做客观审查。薄入口：仅调用 ddd-application-review 能力。
argument-hint: <应用层工件或代码路径> [--mode=design|impl]
---

# /backend-best-practices:ddd-application-review

薄入口。把工件交给 **`ddd-application-review`** 能力执行，产出检查项证据表/分级发现/硬约束触发清单/结论。

- `$ARGUMENTS`：应用用例目录、编排设计，或应用层代码路径（必需）。
- `--mode`：可选，`design`（设计态）或 `impl`（实现态，需测试证据）。

动作：调用 `ddd-application-review`，输入工件/代码路径、输出审查报告文件。评分与放行判定由调用方/workflow 依据 `references/application-review-rubric.md` 决定，本命令不编排。
