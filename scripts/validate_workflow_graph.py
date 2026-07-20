#!/usr/bin/env python3
"""校验 workflows/*.md 的文件交接表与 SKILL 契约对齐（docs/ARCHITECTURE.md §2）。

检查项：
1. 交接表「调用能力」列的每个非本层条目必须存在对应 skills/<name>/ 目录
   （含 SKILL.md）；`design-pattern-<pattern>` 这类模板条目按通配匹配。
2. 每个形如 `NN-*.md` 的输入文件（含 `01..05-*.md` 范围、`<slice>/`、
   `contexts/<ctx>/` 前缀）必须能对应同一 workflow 中更早行的输出文件；
   非文件输入必须命中白名单。
3. 契约字段检查：workflow 正文中反引号包裹的字段 token（`decision`、
   `structured_summary.X` 等）必须出现在该 workflow 引用的某个 skill 的
   SKILL.md「返回什么」部分中——workflow 门禁/分支只准依赖上游已声明的字段。
4. 输出文件编号在同一目录层级（前缀作用域）内不得重复。

用法：python scripts/validate_workflow_graph.py
退出码：有 ERROR 时为 1，否则 0。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
WORKFLOWS_DIR = REPO_ROOT / "skills"

# ---------------------------------------------------------------------------
# 契约字段扫描的忽略清单（可维护：新增误报 token 时加到这里）
# ---------------------------------------------------------------------------
IGNORE_TOKENS = {
    # decision / overall 等字段的枚举值，不是字段名
    "use", "avoid", "partial", "simplify",
    "pass", "fail", "needs_changes",
    "critical", "high", "medium", "low",
    # 文件格式 / 扩展名等非字段词
    "md", "yaml", "yml", "json",
    # 运行清单等约定文件名
    "run.json",
}
# token 末段是这些扩展名时视为文件名而非字段
FILE_EXTENSIONS = {"md", "json", "yaml", "yml", "txt"}

# 工件信封层字段（docs/ARCHITECTURE.md §2 对所有工件统一要求），
# 不属于任何单个 skill 的「返回什么」声明
ENVELOPE_TOKENS = {"artifact_schema_version", "structured_summary"}

# `design-pattern-<pattern>` 之类的模板只应匹配"具体模式"能力；
# 支撑能力（适配判断/实现蓝图/审查/机会扫描）不属于模板取值范围，
# 混入会污染契约字段校验的候选集，掩盖具体模式 SKILL 的漏声明。
TEMPLATE_EXCLUDE = {
    "design-pattern-fit-check",
    "design-pattern-implementation",
    "design-pattern-review",
    "design-pattern-opportunity-scan",
}

# 非文件输入白名单：输入格里若无任何文件 token，必须能命中其中之一
NON_FILE_INPUT_WHITELIST = (
    "用户诉求", "代码路径", "代码库", "原输入", "现状描述",
    "语言剖面", "剖面", "设计文档", "行为黑盒", "该片词汇",
    "关注点", "改造目标", "测试范围", "需求描述", "现有代码",
)

# ---------------------------------------------------------------------------
# 解析工具
# ---------------------------------------------------------------------------
# 交接表数据行的「序」列：00、01…… 或 s0、c01、p01……；— 表示本层步骤
DATA_SEQ_RE = re.compile(r"^(?:\d{1,3}|[a-z]\d{1,2}|[—–-])$")

# 工件文件 token：可选多级前缀（shared/、<slice>/、contexts/<ctx>/patterns/ 等）
# + 编号部分（NN、NN..MM 范围、NN,MM,PP? 列表；? 表示条件工件）
# + 可选 -name + 可选 .md
FILE_TOKEN_RE = re.compile(
    r"^(?P<prefix>(?:[\w<>*-]+/)+)?"
    r"(?P<nums>\d{2}(?:\.\.\d{2}|\??(?:,\d{2}\??)*))"
    r"(?:-(?P<name>[^/\s]+?))?"
    r"(?P<ext>\.md)?$"
)


def parse_nums(nums_str: str) -> list[int]:
    """把编号部分解析成编号列表：'03..07' → [3..7]；'02,04,06?' → [2,4,6]。"""
    if ".." in nums_str:
        a, b = nums_str.split("..", 1)
        return list(range(int(a), int(b) + 1))
    return [int(x.rstrip("?")) for x in nums_str.split(",")]


def prefix_compatible(token_prefix: str, output_prefix: str) -> bool:
    """输入 token 前缀与输出前缀是否兼容——允许省略外层目录
    （如 `patterns/03-*` 引用 `contexts/<ctx>/patterns/03-…`，
    或切片行内省略 `<slice>/`）。"""
    return output_prefix == token_prefix or output_prefix.endswith(token_prefix)

# 契约字段 token：`decision`、`structured_summary.primary_pattern`、`decision=use` 等
FIELD_TOKEN_RE = re.compile(r"^([a-z][a-z_]*(?:\.[a-z][a-z_]*)*)(?:=.*)?$")

BACKTICK_RE = re.compile(r"`([^`]+)`")


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_handoff_rows(lines: list[str]) -> list[dict]:
    """解析文件交接表数据行。

    表格可能被说明段落打断（非 | 行不退出交接模式）；遇到其他表格的
    表头（首格不是序号的 | 行）则退出交接模式。
    """
    rows: list[dict] = []
    cols: dict[str, int] | None = None
    for lineno, line in enumerate(lines, 1):
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if any("调用能力" in c for c in cells):
            cols = {}
            for i, c in enumerate(cells):
                if "调用能力" in c:
                    cols["cap"] = i
                elif "输入" in c:
                    cols["in"] = i
                elif "输出" in c:
                    cols["out"] = i
            continue
        if all(re.fullmatch(r"[:\-\s]*", c) for c in cells):
            continue  # 分隔行 |:--|:--|
        if cols is not None and cells and DATA_SEQ_RE.fullmatch(cells[0]):
            rows.append({"line": lineno, "cells": cells, "cols": cols})
        else:
            cols = None  # 进入了别的表格
    return rows


def resolve_capability(raw: str) -> tuple[str, str | None]:
    """返回 (kind, name)。kind: internal（本层）/ skill / template。"""
    if "本层" in raw:
        return "internal", None
    text = raw.replace("`", "").strip()
    text = re.sub(r"（[^）]*）", "", text).strip()  # 去掉（局部）等注记
    if not text:
        return "internal", None
    if text.startswith("selected"):
        text = text[len("selected"):].strip()
    if "<" in text:
        return "template", text
    return "skill", text


def template_to_regex(template: str) -> re.Pattern:
    parts = re.split(r"<[^>]+>", template)
    return re.compile("^" + "[a-z0-9-]+".join(re.escape(p) for p in parts) + "$")


def extract_file_tokens(cell: str) -> list[tuple[str, re.Match]]:
    """从表格单元格提取工件文件 token（优先反引号内，兼容裸写）。"""
    candidates = BACKTICK_RE.findall(cell)
    rest = BACKTICK_RE.sub(" ", cell)
    candidates += re.findall(r"[\w<>./*-]*\d{2}[\w<>./*-]*", rest)
    tokens: list[tuple[str, re.Match]] = []
    seen: set[str] = set()
    for cand in candidates:
        cand = cand.strip()
        if not cand or cand in seen:
            continue
        seen.add(cand)
        m = FILE_TOKEN_RE.fullmatch(cand)
        if m:
            tokens.append((cand, m))
    return tokens


def extract_returns_section(skill_name: str, cache: dict[str, str]) -> str:
    """取 skills/<name>/SKILL.md 中「## 返回什么」段的文本（含 YAML 声明）。"""
    if skill_name in cache:
        return cache[skill_name]
    text = ""
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if skill_md.is_file():
        collecting = False
        in_fence = False
        collected: list[str] = []
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                if collecting:
                    collected.append(line)
                continue
            if not in_fence and re.match(r"^##\s+", line):
                if collecting:
                    break
                if re.match(r"^##\s+返回什么", line):
                    collecting = True
                continue
            if collecting and not in_fence and stripped == "---":
                break
            if collecting:
                collected.append(line)
        text = "\n".join(collected)
    cache[skill_name] = text
    return text


def field_declared(
    skill_name: str, part: str, cache: dict[str, str], anchor: str | None = None
) -> bool:
    """字段必须以 YAML key（行首/列表项/flow 内的 `part:`）或反引号精确标注
    出现在「返回什么」段才算声明；散文里的裸子串提及不算。
    传入 anchor（如 structured_summary）时，字段必须出现在该锚点 key 之后——
    防止 workflow 依赖 `structured_summary.X` 时被顶层同名字段蒙混过关。"""
    text = extract_returns_section(skill_name, cache)
    if not text:
        return False
    if anchor:
        am = re.search(rf"(?m)^\s*{re.escape(anchor)}\s*:", text)
        if not am:
            return False
        text = text[am.start():]
    key_pattern = rf"(?m)(?:^\s*(?:-\s*)?|[{{,]\s*){re.escape(part)}\s*\??\s*:"
    if re.search(key_pattern, text):
        return True
    return f"`{part}`" in text


# ---------------------------------------------------------------------------
# 各项检查
# ---------------------------------------------------------------------------

def check_workflow(
    wf: Path,
    skill_names: set[str],
    returns_cache: dict[str, str],
    errors: list[str],
    warnings: list[str],
) -> None:
    loc = rel(wf)
    lines = wf.read_text(encoding="utf-8").splitlines()
    rows = parse_handoff_rows(lines)

    if not rows:
        warnings.append(f"WARNING: {loc}: 未找到文件交接表（表头需含「调用能力/输入文件/输出文件」列）")

    referenced_skills: list[str] = []
    outputs: list[dict] = []  # {prefix, num, basename, full, line, skills}

    for row in rows:
        cells, cols, lineno = row["cells"], row["cols"], row["line"]

        def cell(key: str) -> str:
            idx = cols.get(key)
            return cells[idx] if idx is not None and idx < len(cells) else ""

        # --- 1. 调用能力必须有对应 skill 目录 ---------------------------------
        cap_raw = cell("cap")
        kind, cap = resolve_capability(cap_raw)
        row_skills: list[str] = []  # 本行产出工件的生产者（用于契约字段血缘收窄）
        if kind == "skill":
            if cap not in skill_names:
                errors.append(
                    f"ERROR: {loc}:{lineno}: 调用能力 `{cap}` 没有对应的 skills/{cap}/ 目录"
                )
            elif not (SKILLS_DIR / cap / "SKILL.md").is_file():
                errors.append(
                    f"ERROR: {loc}:{lineno}: skills/{cap}/ 存在但缺少 SKILL.md"
                )
            else:
                referenced_skills.append(cap)
                row_skills = [cap]
        elif kind == "template":
            regex = template_to_regex(cap)
            matched = sorted(
                n for n in skill_names if regex.match(n) and n not in TEMPLATE_EXCLUDE
            )
            if not matched:
                errors.append(
                    f"ERROR: {loc}:{lineno}: 模板能力 `{cap}` 在 skills/ 下没有任何匹配目录"
                )
            else:
                referenced_skills.extend(matched)
                row_skills = matched

        # --- 2. 输入文件必须来自更早行的输出 ----------------------------------
        in_cell = cell("in")
        in_tokens = extract_file_tokens(in_cell)
        if in_cell and not in_tokens:
            if not any(w in in_cell for w in NON_FILE_INPUT_WHITELIST):
                warnings.append(
                    f"WARNING: {loc}:{lineno}: 输入「{in_cell}」既不是工件文件，"
                    f"也未命中非文件输入白名单"
                )
        for tok, m in in_tokens:
            check_input_lineage(tok, m, outputs, loc, lineno, errors, warnings)

        # --- 3/4. 登记输出并检查编号重复 --------------------------------------
        out_cell = cell("out")
        for tok, m in extract_file_tokens(out_cell):
            nums = parse_nums(m.group("nums"))
            if len(nums) > 1:
                continue  # 输出不应是范围/列表，跳过
            prefix = m.group("prefix") or ""
            num = nums[0]
            basename = tok[len(prefix):] if prefix and tok.startswith(prefix) else tok
            dup = next((o for o in outputs if o["prefix"] == prefix and o["num"] == num), None)
            if dup:
                errors.append(
                    f"ERROR: {loc}:{lineno}: 输出文件编号重复——`{tok}` 与第 {dup['line']} 行的 "
                    f"`{dup['full']}` 在同一目录层级使用相同编号 {num:02d}"
                )
            outputs.append(
                {"prefix": prefix, "num": num, "basename": basename, "full": tok,
                 "line": lineno, "skills": row_skills}
            )

    # --- 契约字段检查 ----------------------------------------------------------
    check_contract_fields(wf, lines, referenced_skills, outputs, returns_cache, errors, warnings)


def check_input_lineage(
    tok: str,
    m: re.Match,
    outputs: list[dict],
    loc: str,
    lineno: int,
    errors: list[str],
    warnings: list[str],
) -> None:
    prefix = m.group("prefix") or ""
    nums = parse_nums(m.group("nums"))

    if len(nums) > 1:  # 范围 / 列表输入：每个编号都要有前缀兼容的更早产出
        for n in nums:
            matched = [
                o for o in outputs
                if o["num"] == n and prefix_compatible(prefix, o["prefix"])
            ]
            if not matched:
                errors.append(
                    f"ERROR: {loc}:{lineno}: 输入 `{tok}` 中的编号 {n:02d} "
                    f"在更早行没有对应的输出文件（前缀作用域「{prefix or '任意'}」）"
                )
            elif not prefix and len({o["prefix"] for o in matched}) > 1:
                # 空前缀 + 同编号工件散布在多个目录：作用域歧义，可能跨上下文/切片误引用
                scopes = sorted({o["prefix"] or "（根）" for o in matched})
                warnings.append(
                    f"WARNING: {loc}:{lineno}: 输入 `{tok}` 中的编号 {n:02d} 未写前缀，"
                    f"但多个目录都有同编号工件（{', '.join(scopes)}）——请补前缀消除歧义"
                )
        return

    num = nums[0]
    name = m.group("name") or ""
    basename = tok[len(prefix):] if prefix and tok.startswith(prefix) else tok
    # ① 完整路径精确匹配
    if any(o["full"] == tok for o in outputs):
        return
    # ② 任意前缀下的同名文件（行内常省略 <slice>/、contexts/<ctx>/ 等外层前缀）
    if any(o["basename"] == basename for o in outputs):
        return
    # ③ 通配文件名（如 `patterns/03-*`）：编号 + 前缀兼容即可
    if "*" in name and any(
        o["num"] == num and prefix_compatible(prefix, o["prefix"]) for o in outputs
    ):
        return
    # ④ 编号能对上但文件名不一致（疑似工件改名后引用未同步）
    same_num = [
        o for o in outputs if o["num"] == num and prefix_compatible(prefix, o["prefix"])
    ]
    if same_num:
        warnings.append(
            f"WARNING: {loc}:{lineno}: 输入 `{tok}` 编号对应更早输出 `{same_num[0]['full']}`，"
            f"但文件名不一致——疑似工件改名后引用未同步"
        )
        return
    errors.append(
        f"ERROR: {loc}:{lineno}: 输入文件 `{tok}` 无法对应同一 workflow 中更早行的任何输出文件"
    )


def producers_on_line(line: str, outputs: list[dict]) -> set[str]:
    """解析一行中引用的工件文件，返回其生产者 skill 集合（血缘收窄用）。"""
    producers: set[str] = set()
    for tok, m in extract_file_tokens(line):
        prefix = m.group("prefix") or ""
        nums = set(parse_nums(m.group("nums")))
        basename = tok[len(prefix):] if prefix and tok.startswith(prefix) else tok
        for o in outputs:
            if not o["skills"]:
                continue
            if (
                o["full"] == tok
                or o["basename"] == basename
                or (o["num"] in nums and prefix_compatible(prefix, o["prefix"]))
            ):
                producers.update(o["skills"])
    return producers


def check_contract_fields(
    wf: Path,
    lines: list[str],
    referenced_skills: list[str],
    outputs: list[dict],
    returns_cache: dict[str, str],
    errors: list[str],
    warnings: list[str],
) -> None:
    loc = rel(wf)
    skills = set(referenced_skills)
    # 正文里以反引号点名的 skill（如条件支线的说明段）也算被引用
    all_skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    for line in lines:
        for span in BACKTICK_RE.findall(line):
            if span.strip() in all_skill_names:
                skills.add(span.strip())
    skills = sorted(skills)
    reported: set[tuple[str, tuple[str, ...]]] = set()

    for lineno, line in enumerate(lines, 1):
        # 血缘收窄：本行引用了具体工件时，候选生产者限定为这些工件的产出 skill
        # （外加本行反引号点名的 skill）；避免无关 skill 的同名字段掩盖真实断裂。
        line_scope = producers_on_line(line, outputs)
        for span in BACKTICK_RE.findall(line):
            if span.strip() in all_skill_names:
                line_scope.add(span.strip())
        candidates = sorted(line_scope) if line_scope else skills
        for span in BACKTICK_RE.findall(line):
            fm = FIELD_TOKEN_RE.fullmatch(span.strip())
            if not fm:
                continue
            token = fm.group(1)
            if token in IGNORE_TOKENS:
                continue
            dedup_key = (token, tuple(candidates))
            if dedup_key in reported:
                continue
            # 去掉信封层组件（artifact_schema_version、structured_summary.X 的信封部分）；
            # 但 structured_summary.X 的 X 必须声明在 structured_summary 块内（anchor 约束）
            raw_parts = token.split(".")
            parts = [p for p in raw_parts if p not in ENVELOPE_TOKENS]
            anchor = "structured_summary" if "structured_summary" in raw_parts and parts else None
            if not parts:
                continue  # 纯信封字段，属架构级契约，不查 skill 声明
            if parts[-1] in FILE_EXTENSIONS:
                continue  # 文件名
            if all(p in IGNORE_TOKENS for p in parts):
                continue
            reported.add(dedup_key)
            if not candidates:
                warnings.append(
                    f"WARNING: {loc}:{lineno}: 字段 `{token}` 无法核对——该 workflow 未引用任何已存在的 skill"
                )
                continue
            declared_by = [
                s for s in candidates
                if all(field_declared(s, p, returns_cache, anchor=anchor) for p in parts)
            ]
            if not declared_by:
                scope_note = "行内工件血缘" if line_scope else "全 workflow 引用"
                errors.append(
                    f"ERROR: {loc}:{lineno}: 契约断裂——workflow 依赖字段 `{token}`，"
                    f"但它未以 YAML key 或反引号标注形式出现在候选 skill 的"
                    f"「返回什么」声明中（收窄范围：{scope_note}；已核对：{', '.join(candidates)}）"
                )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    errors: list[str] = []
    warnings: list[str] = []

    if not WORKFLOWS_DIR.is_dir():
        print(f"ERROR: 找不到 skills 目录：{WORKFLOWS_DIR}")
        return 1
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: 找不到 skills 目录：{SKILLS_DIR}")
        return 1

    skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    returns_cache: dict[str, str] = {}

    workflow_files = sorted(
        path for path in WORKFLOWS_DIR.glob("workflow-*/SKILL.md")
    )
    for wf in workflow_files:
        check_workflow(wf, skill_names, returns_cache, errors, warnings)

    for line in errors:
        print(line)
    for line in warnings:
        print(line)

    print(
        f"\nvalidate_workflow_graph: 检查 {len(workflow_files)} 个 workflow —— "
        f"{len(errors)} 个 ERROR，{len(warnings)} 个 WARNING"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
