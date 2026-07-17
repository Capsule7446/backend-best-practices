# 架构：三层职责分离

本插件把开发工序拆成三层，各层职责严格互斥。核心原则：**SKILL 是纯能力，WORKFLOW 是唯一统筹者，COMMAND 是薄入口。**

---

## 1. SKILL = 纯能力

铁律：**单个 SKILL 实现单个能力，绝不与外部耦合。** 它就是一个纯函数——给定输入，产出输出，**不知道谁调用它、上一步是谁、下一步是谁、门禁是什么、要不要回溯。**

### 正文四段（必需最小集，可按能力扩充）

以下四段**每个 skill 必须实现**；某些能力若确有需要，可在此基础上**增加段落**（如"约束""术语"），但不得引入任何外部耦合。四段是下限，不是上限。

1. **做什么（Purpose）**——这个能力本身，一句话讲清。
2. **需要什么参数（Parameters）**——按**数据形状**描述输入（"需要一份含 {…} 的工件"），标必需/可选。**禁止**写"来自 X skill"。
3. **怎么做（Procedure）**——执行该能力的方法步骤。
4. **返回什么（Returns）**——产出工件及其结构，并附**自己的返回格式自检**（见 §5 两级自检的第①级）。

### SKILL.md 只放技能描述；其余信息拆成按需加载的附加文件

SKILL.md 是**默认会被加载进 context 的核心**，所以只保留"技能本身的描述"（上面四段）。示例、深度参考、语言剖面、长走查等**一律拆到同目录附加文件**（如 `examples.md`、`reference.md`），SKILL.md 只用一行**指路**，由 AI 在**需要时**才去读——渐进披露，避免一次性把所有东西塞进 context。

```
skills/<capability>/
├── SKILL.md        默认加载：四段纯能力描述 + 附加文件指路
├── examples.md     按需加载：输入→输出走查示例
└── reference.md    按需加载：深度方法/边界情况（可选）
```

frontmatter（砍掉 stage/driver/回溯，只留发现所需）：

```yaml
---
name: <capability>
description: "<做什么，一句话；不写触发时机>"
risk: safe|caution
category: <discovery|strategic|tactical|application|validation|specification|implementation|reverse>
inputs: "<输入工件/参数，简述>"
outputs: "<产出工件，简述>"
tags: "[...]"
---
```

**移除清单**：`使用时机`（相对流程的）、`回溯触发`、`stage`、`driver`、`source`、一切指向他 skill 的引用与"被回溯触发"字样；示例等重内容移出到附加文件。

---

## 2. WORKFLOW = 统筹（文件交接）

WORKFLOW 是**唯一**知道顺序、门禁、回溯的地方。skill 之间通过**文件**传递工件，由 workflow 主流程把控。

### 文件交接协议

- workflow 建一个运行工作区 `<workdir>/`（默认 `./run/<flow>/`，按流程名分目录，或用户指定）。
- 每个 skill 产出**一个主工件文件**，由 workflow 统一编号命名：`01-<cap>.md`、`02-<cap>.md`……多上下文/多切片时用子目录（`contexts/<ctx>/01-<cap>.md`、`<slice>/01-<cap>.md`）。
- **条件工件记法**：条件执行步骤的工件在下游输入中必须带 `?` 标记（如 `04,05,06?-*.md`），表示"可缺席，缺席时跳过读取"。禁止用 `NN..MM` 范围囊括条件工件——条件不触发时会造成读取不存在文件的断裂。
- **调用契约**：workflow 调用某 skill 时，传入「输入文件路径（一个或多个）+ 输出文件路径」。skill 读入 → 纯计算 → 写出。skill 不自己决定文件名、不感知编号。
- workflow 维护一个运行清单 `_manifest.md`（或 `run.json`）：记录各阶段状态、门禁结果、回溯记录。

### 工件信封（所有主工件统一格式）

每个主工件文件统一采用三段式信封：

1. 头部声明 `artifact_schema_version: 2`（工件格式版本，独立于插件版本，格式演进时递增）。
2. 可读的 **Markdown 正文**——给人审的真源，不得只有 YAML。
3. 文末 `structured_summary` YAML 小节——当 workflow 需要按字段做门禁或分支时**必须存在**，字段形状以该 SKILL「返回什么」的声明为准。

**契约铁律**：workflow 门禁与分支只准依赖 `structured_summary` 中**已在 SKILL 返回声明里出现**的字段。依赖未声明字段即契约断裂——先修 SKILL 的返回声明，再改 workflow。

### workflow 互斥规则

- workflow **不嵌套调用** workflow；需要复用能力时直接调用对应纯 SKILL。
- 一次运行只有一个 workflow，独占一个 `<workdir>/` 与其中的 `_manifest.md`。
- 各 workflow 的默认工作区互不相同（`./run/<flow>/`），防止工件编号与 `_manifest.md` 互相覆盖。

### 统一 ID 与追踪

工件中的可追踪对象统一使用前缀 ID，跨工件引用时只用 ID，不复述内容：

```text
GOAL- 业务目标   CTX- 限界上下文   CMD- 命令        QRY- 查询
UC-  应用用例    INV- 不变量       AGG- 聚合        EVT- 领域事件
IEVT- 集成事件   VIEW- 业务视图    RM-  读模型      PORT- 端口
PM-  流程管理器  PAT- 模式决策     AC-  验收准则    TEST- 可执行测试
```

三条必须闭合的追踪链（由 workflow 门禁核对、校验脚本抽查）：

```text
写侧   GOAL → CMD → UC → AGG → INV → EVT → PORT → IMPL → TEST
读侧   GOAL → QRY → VIEW → 字段来源 → RM/查询方案 → 同步策略 → TEST
模式   变化轴 → PAT → 角色映射 → 代码位置 → 扩展性 TEST
```

### 门禁与回溯（只在 workflow）

- **门禁**：workflow 读某阶段的产物文件，按门禁标准核对；不过则不放行进入下一步。
- **回溯**：不过时，workflow 按自己的回溯规则**重跑某个上游 skill**（可携带修正说明作为额外输入）。skill 只是被再次调用，**它自己不知道这是一次回溯**。
- 需要停下与用户确认的强门禁，也由 workflow 决定在哪停。

---

## 3. 两级自检（各管各的）

产物要过**两道独立的检查**，分属两层，不要混为一谈：

| 级别 | 谁做 | 检查什么 |
| :--- | :--- | :--- |
| ① 返回格式自检 | **SKILL** | 我的产出**是否符合我自己声明的返回格式/结构**（字段齐不齐、形状对不对）。只对自己负责。 |
| ② 需求满足门禁 | **WORKFLOW** | 这份产出**是否满足 workflow 自己的需求**（量化阈值、完整性、是否放行/回溯）。SKILL 不掺和。 |

一句话：SKILL 保证"我交出的东西格式合格"，WORKFLOW 判断"这东西够不够格进下一步"。

---

## 4. COMMAND = 薄入口

只解析参数、调用目标，不含编排逻辑：

- **单能力入口**：`/<plugin>:<cap> <args>` → 调用某个 skill，产出工件。
- **流程入口**：`/<plugin>:<name> <args>` → 启动一条 workflow。

---

## 5. 一图看清数据流

```
COMMAND ──启动──> WORKFLOW
                    │  建 <workdir>/、维护 _manifest
                    ├─ 调 SKILL_A (in: 用户输入, out: 01-a.md)
                    ├─ 门禁? 读 01-a.md 核对 ── 不过 ─> 重跑 SKILL_A(带修正)
                    ├─ 调 SKILL_B (in: 01-a.md, out: 02-b.md)
                    └─ …
SKILL 只看到：给我的输入文件 → 我的输出文件。对流程一无所知。
```
