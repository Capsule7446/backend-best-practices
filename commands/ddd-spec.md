---
description: 把战术工件导出为语言中立接口契约规范。薄入口：仅调用 ddd-spec-bridge 能力。
argument-hint: <战术工件路径/描述> [--openspec]
---

# /backend-best-practices:ddd-spec

薄入口。把战术工件交给 **`ddd-spec-bridge`** 能力执行，产出端口契约规范/事件 schema/不变量命题/验收准则。

- `$ARGUMENTS`：战术建模工件（必需）。
- `--openspec`：可选，额外按 OpenSpec 格式导出。

动作：调用 `ddd-spec-bridge`，输入工件路径、输出规范文件。
