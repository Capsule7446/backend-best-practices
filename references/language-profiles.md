# 语言剖面（Language Profiles）

> 供 `ddd-port-scaffold` 与各分层实现能力（`ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl` / `cqrs-read-model-impl`）使用。把语言中立的构造（Domain / Application / Read / 出入站适配器 / 组合根）映射到各面向接口语言。
> **渐进披露：确定目标语言后，只加载 `language-profiles/<lang>.md` 一个文件，不要全部载入。**

## 如何选剖面

1. 按目标语言标识（`java|kotlin|csharp|go|ts|python|rust`）在下表找到对应剖面文件。
2. 多语言仓库按"当前要落地的模块"所用语言选，一次只取一个剖面。
3. 未收录语言：用下方"剖面问卷"现场采集 5 项，即可直接交给 `ddd-port-scaffold` 生成骨架。

## 剖面目录

| 语言标识 | 剖面文件 |
| :--- | :--- |
| `java` | [language-profiles/java.md](language-profiles/java.md) |
| `kotlin` | [language-profiles/kotlin.md](language-profiles/kotlin.md) |
| `csharp` | [language-profiles/csharp.md](language-profiles/csharp.md) |
| `go` | [language-profiles/go.md](language-profiles/go.md) |
| `ts` | [language-profiles/typescript.md](language-profiles/typescript.md) |
| `python` | [language-profiles/python.md](language-profiles/python.md) |
| `rust` | [language-profiles/rust.md](language-profiles/rust.md) |

每个剖面文件统一覆盖八段：Domain / Application / Read / Inbound Adapter / Outbound Adapter / Composition Root / 架构测试 / 测试框架与包可见性。

## 未收录语言：剖面问卷（现场采集 5 项）

任何支持"面向接口编程"的语言都能纳入。问下面 5 个问题，答完即得一行剖面，交给 `backend-best-practices:ddd-port-scaffold` 直接生成骨架——**建模工件零改动，换语言 = 换这 5 个答案**。

| # | 采集项 | 要回答的问题 | 它决定 |
| :--- | :--- | :--- | :--- |
| 1 | **端口/接口** | 用什么声明"只有签名、无实现"的纯抽象契约？ | 端口与骨架写法 |
| 2 | **值对象（不可变 + 按值相等）** | 如何定义"创建后不可变、按值比较相等"的小类型？ | 值对象/领域事件写法 |
| 3 | **标识类型（防基本类型偏执）** | 如何把 `OrderId` 做成与 `string`/`int` **不可混用**的独立类型？ | ID 类型写法 |
| 4 | **依赖注入** | 领域如何拿到端口的实现？关键：领域**绝不 `new` 具体实现**。 | 依赖方向与组合根落点 |
| 5 | **错误与缺失** | 非法操作怎么拒绝、缺失值怎么表达？异常还是 `Result`？null 还是 `Option`？ | 不变量强制与错误表达 |

补充确认两点：**领域内核能否零外部依赖地组织**（独立 module/包/crate）、**有无编译期或 lint 手段守护依赖方向**。

### 剖面完整性校验（交给 port-scaffold 前逐项对照）

- [ ] 5 项全部有明确答案，且补充确认了"领域可独立组织 + 有守护依赖方向的手段"
- [ ] 端口是**纯抽象**：只签名、零实现、不泄漏框架/基础设施类型
- [ ] 值对象**不可变 + 按值相等**；ID 类型与基本类型**不可混用**
- [ ] 领域**不依赖具体实现**：依赖只向内，DI 在最外层组合根装配
- [ ] 错误/缺失表达统一，且翻译为**领域语义错误**，不外泄底层异常/`null`
- [ ] 契约语义（前置/后置/事务边界/不变量编号）以注释随骨架保留，换语言不丢失
