---
description: 把接口契约规范按语言剖面实例化为接口骨架。薄入口：仅调用 ddd-port-scaffold 能力。
argument-hint: <上下文/规范> --lang=<java|go|ts|python|csharp|rust|kotlin|...> [--style=现有项目约定]
---

# /backend-best-practices:ddd-scaffold

薄入口。把端口契约规范交给 **`ddd-port-scaffold`** 能力执行，产出目标语言的接口骨架（仅签名+契约注释，不含实现）。

- `$ARGUMENTS`：上下文或端口契约规范（必需）。
- `--lang`：目标落地语言（必需）；未收录语言触发剖面问卷现场采集 5 项。
- `--style`：可选，沿用现有项目命名/包结构/DI 约定。

动作：调用 `ddd-port-scaffold`，输入规范路径 + 语言剖面、输出骨架文件。
