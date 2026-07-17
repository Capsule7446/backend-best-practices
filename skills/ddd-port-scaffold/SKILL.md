---
name: ddd-port-scaffold
description: "接口优先脚手架：把语言中立的后端契约规范按目标语言的语言剖面，实例化为分层项目骨架——Domain/Application/Read/Adapter/Composition Root 的接口与结构占位，只含签名与契约注释，不含实现。"
risk: safe
category: implementation
inputs: "后端契约规范（Domain 端口 + 应用用例契约 + 出站端口 + 读侧契约可选）+ 目标语言标识（语言剖面）+ 聚合目录/不变量表"
outputs: "分层项目骨架 / 端口与 Input Port 接口骨架 / 值对象·标识骨架 / 测试骨架占位 / 依赖方向说明 / 待实现清单 / 所用语言剖面记录"
tags: "[implementation, ports, scaffold, language-agnostic]"
---

# Port Scaffold（分层项目骨架）

## 做什么

把后端契约规范翻译成目标语言的**分层项目骨架**——先立约、不填肉（实现由各层实现能力接手）。覆盖 Domain 端口、Application Input/Output Port、读侧 Query Port 与 Composition Root 占位。适配任意面向接口开发的语言。

## 需要什么参数

- **必需**：后端契约规范（至少含 Domain 端口；有应用用例契约与读侧契约时一并消费）；聚合目录与不变量表；`语言剖面`入参——目标语言标识（`java|go|ts|python|csharp|rust|kotlin|...`）。
- **可选**：既有代码风格约定（命名、包结构）、DI 方式偏好、模块化偏好（单体模块目录/多包）。

## 怎么做

1. **载入语言剖面**：从 `references/language-profiles/<lang>.md` 取该语言的分层构造映射（Domain/Application/Read/Adapter/Composition Root/架构测试）；未收录则按索引文件中的"剖面问卷"现场采集。
2. **生成分层目录骨架**：按 bounded context 分模块——`domain/`（model/service/event/port）、`application/`（command/query/port/policy/process_manager）、`read/`（contract/model/projection 占位，按需）、`adapters/`（inbound/outbound 占位）、`bootstrap/`（composition root 占位）、`tests/`（domain/application/contract/architecture 分目录占位）。
3. **映射 Domain 端口**：每个中立端口 → 该语言接口/trait/Protocol，逐方法翻译签名，**保留契约注释**（前置/查询边界/事务/不变量引用）。
4. **映射 Application 契约**：每用例生成 Input Port + Command/Result 类型骨架；出站端口（UoW/Outbox/幂等存储/网关/Read Store）生成接口骨架。
5. **映射值对象与标识**：值对象 → 不可变值类型（按值相等）；标识 → ID 类型。
6. **生成依赖方向骨架**：领域包只声明接口与领域类型；应用包只依赖领域与端口抽象；适配器/基础设施留空占位；架构测试骨架断言依赖方向。
7. **植入契约追踪注释**：每个接口/方法注明对应不变量/用例编号与一致性策略。
8. **输出骨架文件清单**（仅签名 + 注释，无逻辑），按层标"待实现"占位点与归属实现能力。

## 返回什么

| 工件 | 结构 |
| :--- | :--- |
| 分层项目骨架 | 按 context 分模块的目录结构 + 各层占位文件 |
| 端口/Input Port 骨架 | 目标语言接口文件：签名 + 契约注释，无实现 |
| 值对象/标识骨架 | 不可变值类型与 ID 类型，含相等性策略 |
| 测试骨架占位 | domain/application/contract/architecture 测试目录与命名占位 |
| 依赖方向说明 | 包/模块结构 + 依赖指向（内核零外部依赖，应用只依赖抽象）|
| 待实现清单 | 文件、占位点、对应聚合/用例/不变量、归属层 |
| 所用语言剖面 | 采用的剖面与分层构造映射（可复现）|

> **返回格式自检**：每个端口/Input Port 方法保留契约注释；值对象用该语言不可变构造且按值相等；领域内核无基础设施/框架依赖、应用层只引用领域内核与端口抽象；骨架内**无业务实现逻辑**；每个接口/方法关联到具体不变量或用例编号；待实现清单每项标注归属层；未收录语言已补齐剖面。

---

附加文件（按需读取）：`examples.md`（同目录走查示例）、`references/language-profiles/`（**插件根目录**下的分层语言剖面，按目标语言只读一个文件）。
