#!/usr/bin/env python3
"""对一次 workflow 运行的工件（run 工作区）做追踪链校验。

用法：
    python scripts/validate_traceability.py <workdir>

检查三件事（对应 docs/ARCHITECTURE.md「统一 ID 与追踪」）：

1. 工件信封——每个主工件头部声明 `artifact_schema_version`。
2. 引用即定义——工件中引用的每个前缀 ID（UC-/INV-/VIEW-…），必须在其
   「归属工件」（按前缀→文件名模式映射）中出现过；只被散文提及、
   却不存在于归属工件中的 ID 视为断链。
3. 链路覆盖——每个 UC 同文件内应携带 INV 与 AC 引用（写侧链）；
   每个 VIEW 必须在 fit 矩阵工件中有结论（读侧链）。

结构/契约字段校验属 validate_workflow_graph.py，此处不重复。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ID_RE = re.compile(
    r"\b(GOAL|CTX|CMD|QRY|UC|INV|AGG|EVT|IEVT|VIEW|RM|PORT|PM|PAT|AC|TEST)"
    r"-[A-Z0-9][A-Z0-9-]*\b"
)

# 前缀 → 归属工件的文件名片段（任一命中即认定为归属工件）
HOME_PATTERNS: dict[str, list[str]] = {
    "GOAL": ["scope"],
    "CTX": ["contexts"],
    "CMD": ["discover", "use-cases"],
    "QRY": ["discover", "views"],
    "UC": ["use-cases"],
    "INV": ["aggregates"],
    "AGG": ["aggregates"],
    "EVT": ["interactions", "aggregates", "discover"],
    "IEVT": ["orchestration", "spec"],
    "VIEW": ["views"],
    "RM": ["read-models", "read-model-design"],
    "PORT": ["interactions", "spec"],
    "PM": ["process-managers"],
    "PAT": ["scan", "fit"],
    "AC": ["use-cases", "spec"],
    "TEST": ["acceptance"],
}

FIT_PATTERNS = ["read-fit", "fit-check"]
SKIP_FILES = {"_manifest.md"}


def artifact_files(workdir: Path) -> list[Path]:
    return sorted(
        p for p in workdir.rglob("*.md")
        if p.name not in SKIP_FILES
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) != 2:
        print("用法: python scripts/validate_traceability.py <workdir>")
        return 2
    workdir = Path(sys.argv[1])
    if not workdir.is_dir():
        print(f"ERROR: 工作区不存在: {workdir}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    files = artifact_files(workdir)
    if not files:
        print(f"ERROR: {workdir} 下没有任何 .md 工件")
        return 1

    texts: dict[Path, str] = {
        p: p.read_text(encoding="utf-8", errors="replace") for p in files
    }

    def rel(p: Path) -> str:
        return p.relative_to(workdir).as_posix()

    # --- 1. 工件信封 -------------------------------------------------------
    for p, text in texts.items():
        head = "\n".join(text.splitlines()[:5])
        if "artifact_schema_version" not in head:
            errors.append(f"ERROR: {rel(p)}: 头部缺少 artifact_schema_version 声明")

    # --- 收集 ID：出现位置（全部） 与 定义位置（归属工件 + 结构化行） ---------
    # 结构化行 = 表格行 / YAML 键值或列表项 / 标题——散文句子里的提及只算引用，不算定义。
    STRUCTURED_LINE_RE = re.compile(r"^\s*(\||#|-\s|\*\s|[\w`\"'（(]{1,40}\s*[:：])")

    def is_home_file(prefix: str, p: Path) -> bool:
        return any(
            re.search(rf"(?:^|\d+-|-){re.escape(pat)}(?:-|\.|$)", p.name)
            for pat in HOME_PATTERNS.get(prefix, [])
        )

    seen_in: dict[str, set[Path]] = {}
    defined: set[str] = set()
    for p, text in texts.items():
        for line in text.splitlines():
            for m in ID_RE.finditer(line):
                id_ = m.group(0)
                seen_in.setdefault(id_, set()).add(p)
                if is_home_file(m.group(1), p) and STRUCTURED_LINE_RE.match(line):
                    defined.add(id_)

    def in_home(id_: str) -> bool:
        return id_ in defined

    # --- 2. 引用即定义 -----------------------------------------------------
    for id_, places in sorted(seen_in.items()):
        if not in_home(id_):
            where = ", ".join(sorted(rel(p) for p in places))
            errors.append(
                f"ERROR: ID `{id_}` 被引用（{where}）但未在其归属工件"
                f"（{'/'.join(HOME_PATTERNS.get(id_.split('-', 1)[0], ['?']))}）的结构化行"
                f"（表格/YAML/标题）中定义——引用未定义"
            )

    # --- 3a. 写侧链：每个 UC 的区块内应携带 INV 与 AC -----------------------
    # 区块 = 该 UC 首次出现处到下一个 UC 首次出现处；逐 UC 分别核对，
    # 防止"同文件另一个用例有 INV/AC"掩盖断链用例。
    for p, text in texts.items():
        if not is_home_file("UC", p):
            continue
        # 查询用例（kind: query 或登记在 query_use_cases 行）不守不变量，
        # 其契约与验收由读侧链承担——跳过写侧 UC→INV/AC 检查。
        query_ucs: set[str] = set()
        for line in text.splitlines():
            if "query_use_cases" in line or re.search(r"kind:\s*query", line):
                query_ucs.update(
                    m.group(0) for m in ID_RE.finditer(line) if m.group(1) == "UC"
                )
        # 区块以结构化定义锚点（`id: UC-…`）切分——文件开头的追踪矩阵/登记表
        # 先列出 UC 不会制造错位区块；重复定义取首个锚点。无任何锚点时退回
        # 首次出现位置切分（兼容非 id: 形态的工件）。无锚点的 UC 只做
        # "引用即定义"检查，不做区块链检查。
        anchor_re = re.compile(r"(?m)^\s*-?\s*id\s*[:：]\s*(UC-[A-Z0-9][A-Z0-9-]*)")
        first_pos: dict[str, int] = {}
        for m in anchor_re.finditer(text):
            if m.group(1) not in first_pos:
                first_pos[m.group(1)] = m.start()
        if not first_pos:
            for m in ID_RE.finditer(text):
                if m.group(1) == "UC" and m.group(0) not in first_pos:
                    first_pos[m.group(0)] = m.start()
        if not first_pos:
            continue
        ordered = sorted(first_pos.items(), key=lambda kv: kv[1])
        for i, (uc, start) in enumerate(ordered):
            end = ordered[i + 1][1] if i + 1 < len(ordered) else len(text)
            chunk = text[start:end]
            if uc in query_ucs or re.search(r"kind:\s*query", chunk):
                continue
            kinds = {m.group(1) for m in ID_RE.finditer(chunk)}
            # 追踪链是硬约束：缺环即 ERROR；合法缺席须逐环节显式声明
            # `invariants: n/a(理由)` / `acceptance: n/a(理由)`（一处 n/a 不通杀两环）。
            na_inv = re.search(r"(?:invariants|不变量)\s*[:：][^\n]{0,60}n/a", chunk, re.I)
            na_ac = re.search(r"(?:acceptance|验收)\s*[:：][^\n]{0,60}n/a", chunk, re.I)
            if "INV" not in kinds and not na_inv:
                errors.append(
                    f"ERROR: {rel(p)}: `{uc}` 区块内未引用任何 INV 且无显式 n/a(理由)——写侧追踪链（UC→INV）缺环"
                )
            if "AC" not in kinds and not na_ac:
                errors.append(
                    f"ERROR: {rel(p)}: `{uc}` 区块内未引用任何 AC 且无显式 n/a(理由)——验收追踪（UC→AC）缺环"
                )

    # --- 3b. 读侧链：每个 VIEW 必须在 fit 矩阵中拥有有效 decision ------------
    # "拥有结论" = VIEW 出现在结构化行，且该行或其后 3 行内有 decision: use|partial|avoid
    #（兼容 YAML 条目 id 与 decision 分行的形态）；散文/待办里的提及不算。
    DECISION_RE = re.compile(r"decision\s*[:：]\s*(use|partial|avoid)")
    fit_ids_with_decision: set[str] = set()
    has_fit_file = False
    for p, t in texts.items():
        if not any(pat in p.name for pat in FIT_PATTERNS):
            continue
        has_fit_file = True
        lines = t.splitlines()
        for i, line in enumerate(lines):
            hits = [m.group(0) for m in ID_RE.finditer(line) if m.group(1) == "VIEW"]
            if not hits or not STRUCTURED_LINE_RE.match(line):
                continue
            window = "\n".join(lines[i : i + 4])
            if DECISION_RE.search(window):
                fit_ids_with_decision.update(hits)
    view_ids = sorted(
        id_ for id_ in seen_in if id_.startswith("VIEW-") and in_home(id_)
    )
    if view_ids and not has_fit_file:
        errors.append("ERROR: 存在 VIEW 定义但工作区没有任何 fit 矩阵工件（read-fit/fit-check）")
    else:
        for v in view_ids:
            if v not in fit_ids_with_decision:
                errors.append(
                    f"ERROR: 视图 `{v}` 在 fit 矩阵工件中没有有效 decision（use|partial|avoid）——读侧链断裂"
                )

    # --- 汇总 ---------------------------------------------------------------
    for line in errors:
        print(line)
    for line in warnings:
        print(line)
    print(
        f"\nvalidate_traceability: 检查 {len(files)} 个工件、{len(seen_in)} 个 ID —— "
        f"{len(errors)} 个 ERROR，{len(warnings)} 个 WARNING"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
