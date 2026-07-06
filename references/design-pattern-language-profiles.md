# Design Pattern Language Profiles

目标：把模式思想翻译成目标语言习惯，而不是复制 Java 写法。

| 语言 | 优先表达 | 注意 |
| :--- | :--- | :--- |
| Java | interface、record、sealed class、enum、DI container、builder | Singleton 避免业务全局状态；Template Method 可被组合替代时不要强继承 |
| TypeScript | interface/type、union、函数组合、class、decorator、factory function | 利用结构类型和 discriminated union；不要为每个角色都建 class |
| Python | protocol/ABC、dataclass、callable、context manager、descriptor | Strategy/Command 常可用函数对象；Singleton 多用模块或注入 |
| Go | 小接口、struct 组合、函数选项、显式错误、channel | 避免继承式类图；Decorator/Adapter 常是接口包装 |
| C# | interface、record、delegate、LINQ、DI、async stream | 可用 delegate 简化 Strategy/Command；注意生命周期由容器管理 |
| Kotlin | interface、data class、sealed class、object、extension、DSL builder | State/Interpreter 可用 sealed hierarchy；Singleton 用 `object` 但谨慎承载业务状态 |
| Rust | trait、enum、struct、builder、newtype、Arc/Mutex | State/Visitor 可用 enum 或 trait object；显式所有权会影响对象图 |

## 通用落地步骤

1. 定义模式角色与协作，不先写代码。
2. 把接口边界映射到目标语言最小抽象。
3. 处理生命周期：谁创建、谁拥有、谁释放、谁缓存。
4. 处理错误：同步异常、显式错误值、Result、Promise/async。
5. 处理并发：不可变对象优先；共享状态必须可见、可测。
6. 写测试：替换实现、扩展新变体、失败路径、组合顺序。

## 常见翻译

| 模式族 | Java/C# | TypeScript/Python | Go/Rust/Kotlin |
| :--- | :--- | :--- | :--- |
| Strategy | interface + implementations | function/callable 或对象 | 小接口 / trait / function type |
| Factory | static factory / DI factory | factory function | constructor function / associated function |
| Decorator | wrapper implements same interface | higher-order function / wrapper object | interface/trait wrapper |
| State | state interface + concrete states | union + dispatch 或对象 | enum state machine 或 trait object |
| Observer | event bus/listener | callbacks/signals/observable | channel/listener trait/flow |
| Builder | fluent builder | options object / dataclass defaults | functional options / builder struct |

## 反强绑定规则

- 不要求所有语言都有“抽象类 + 具体类”。
- 不要求每个模式都产生文件级类结构。
- 不要求保留 GoF 示例命名。
- 不因目标语言没有类继承就放弃模式；优先保留意图和协作。
