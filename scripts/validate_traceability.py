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

    # --- 收集 ID：出现位置（全部） 与 归属工件内出现（定义） -----------------
    seen_in: dict[str, set[Path]] = {}
    for p, text in texts.items():
        for m in ID_RE.finditer(text):
            seen_in.setdefault(m.group(0), set()).add(p)

    def in_home(id_: str) -> bool:
        prefix = id_.split("-", 1)[0]
        patterns = HOME_PATTERNS.get(prefix, [])
        return any(
            any(pat in p.name for pat in patterns) for p in seen_in.get(id_, ())
        )

    # --- 2. 引用即定义 -----------------------------------------------------
    for id_, places in sorted(seen_in.items()):
        if not in_home(id_):
            where = ", ".join(sorted(rel(p) for p in places))
            errors.append(
                f"ERROR: ID `{id_}` 被引用（{where}）但未出现在其归属工件"
                f"（{'/'.join(HOME_PATTERNS.get(id_.split('-', 1)[0], ['?']))}）中——引用未定义"
            )

    # --- 3a. 写侧链：UC 同文件内应携带 INV 与 AC ---------------------------
    for p, text in texts.items():
        if not any(pat in p.name for pat in HOME_PATTERNS["UC"]):
            continue
        ucs = sorted({m.group(0) for m in ID_RE.finditer(text) if m.group(1) == "UC"})
        if not ucs:
            continue
        has_inv = any(m.group(1) == "INV" for m in ID_RE.finditer(text))
        has_ac = any(m.group(1) == "AC" for m in ID_RE.finditer(text))
        if not has_inv:
            warnings.append(
                f"WARNING: {rel(p)}: 定义了 {len(ucs)} 个 UC 但未引用任何 INV——写侧追踪链（UC→INV）缺环"
            )
        if not has_ac:
            warnings.append(
                f"WARNING: {rel(p)}: 定义了 {len(ucs)} 个 UC 但未引用任何 AC——验收追踪（UC→AC）缺环"
            )

    # --- 3b. 读侧链：每个 VIEW 必须进 fit 矩阵 ------------------------------
    fit_text = "\n".join(
        t for p, t in texts.items() if any(pat in p.name for pat in FIT_PATTERNS)
    )
    view_ids = sorted(
        id_ for id_ in seen_in if id_.startswith("VIEW-") and in_home(id_)
    )
    if view_ids and not fit_text:
        errors.append("ERROR: 存在 VIEW 定义但工作区没有任何 fit 矩阵工件（read-fit/fit-check）")
    else:
        for v in view_ids:
            if v not in fit_text:
                errors.append(f"ERROR: 视图 `{v}` 没有出现在 fit 矩阵工件中——读侧链（VIEW→fit 结论）断裂")

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
