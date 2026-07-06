# Template Method 多语言实现差异

核心意图：在父结构中固定流程骨架，把可变步骤留给子类或钩子。

## 语言中立蓝图

| 角色 | 职责 |
| :--- | :--- |
| Client | 发起用例，只依赖稳定接口或角色。 |
| Stable Abstraction | 表达不会随变体频繁变化的能力。 |
| Variation | 承载会变化的算法、产品、状态、结构或访问方式。 |
| Composition Boundary | 决定具体变体如何被创建、组合或替换。 |

## 主流语言差异

| 语言 | 推荐表达 | 差异注意 |
| :--- | :--- | :--- |
| Java | interface / record / sealed class / DI | 适合显式角色和类型边界，但不要为简单变化制造过深类层级。 |
| TypeScript | interface/type / union / factory function / 函数组合 | 利用结构类型和 discriminated union，避免机械复制 Java 抽象类。 |
| Python | Protocol/ABC / dataclass / callable / context manager | 许多行为型模式可用函数对象表达，保持显式边界即可。 |
| Go | 小接口 / struct 组合 / 函数选项 / 显式错误 | 用组合和接口包装表达模式，不追求继承式类图。 |
| C# | interface / record / delegate / DI / async stream | delegate 可简化 Strategy/Command；生命周期交给容器更清楚。 |
| Kotlin | interface / data class / sealed class / object / DSL builder | sealed hierarchy 适合 State/Interpreter；object 单例需避免业务可变状态。 |
| Rust | trait / enum / builder / newtype / Arc | 用 trait object 或 enum 表达变化；所有权会影响对象图设计。 |

## 针对 模板方法 的落地建议

- Java/C#：适合用显式接口表达角色；通过 DI 或组合根选择具体实现。
- TypeScript/Python：优先考虑函数、对象字面量、协议或 union，只有需要状态和生命周期时才引入 class。
- Go/Rust：用小接口/trait、组合和显式错误表达协作，避免继承式术语污染实现。
- Kotlin：优先用 sealed class、data class、object、函数类型或 DSL 简化样板。

## 反模式提醒

- 不要为 模板方法 强制创建 Abstract*、Concrete* 命名；用业务语言命名角色。
- 不要让模式隐藏错误处理、事务边界、权限边界或生命周期。
- 不要把 Template Method 与框架机制绑定；框架只是实现细节。
