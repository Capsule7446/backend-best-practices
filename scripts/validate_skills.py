#!/usr/bin/env python3
"""校验 skills/*/SKILL.md 是否符合「纯能力」契约（docs/ARCHITECTURE.md §1）。

检查项：
1. frontmatter 存在且含 name、description；name 与目录名一致。
2. 正文四段齐全：## 做什么 / ## 需要什么参数 / ## 怎么做 / ## 返回什么。
3. 正文不得出现流程耦合内容：使用时机 / 回溯触发 / ## 上游 / ## 下游。
4. SKILL.md 超过 200 行给 WARNING（渐进披露：重内容应拆到同目录附加文件）。

用法：python scripts/validate_skills.py
退出码：有 ERROR 时为 1，否则 0。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_KEYS = ("name", "description")
REQUIRED_SECTIONS = ("做什么", "需要什么参数", "怎么做", "返回什么")
FORBIDDEN_PATTERNS = (
    ("使用时机", "流程耦合：『使用时机』应由 workflow 掌握，skill 不写触发时机"),
    ("回溯触发", "流程耦合：『回溯触发』只存在于 workflow"),
    ("## 上游", "流程耦合：『上游』段落——skill 不感知上一步"),
    ("## 下游", "流程耦合：『下游』段落——skill 不感知下一步"),
)
MAX_LINES = 200

FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str] | None, int]:
    """返回 (frontmatter字典, 正文起始行索引)。无 frontmatter 时返回 (None, 0)。"""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm: dict[str, str] = {}
            for line in lines[1:i]:
                m = FRONTMATTER_KEY_RE.match(line)
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
            return fm, i + 1
    return None, 0


def check_skill(skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    loc = rel(skill_md)

    if not skill_md.is_file():
        errors.append(f"ERROR: {rel(skill_dir)}/: 缺少 SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. frontmatter
    fm, body_start = parse_frontmatter(lines)
    if fm is None:
        errors.append(f"ERROR: {loc}: 缺少 frontmatter（文件必须以 --- 开头的 YAML 块开始）")
        body_start = 0
    else:
        for key in REQUIRED_KEYS:
            if not fm.get(key):
                errors.append(f"ERROR: {loc}: frontmatter 缺少必需键 `{key}`（或其值为空）")
        name = fm.get("name")
        if name and name != skill_dir.name:
            errors.append(
                f"ERROR: {loc}: frontmatter name `{name}` 与目录名 `{skill_dir.name}` 不一致"
            )

    body_lines = lines[body_start:]

    # 2. 正文四段
    headings = [HEADING_RE.match(ln).group(1) for ln in body_lines if HEADING_RE.match(ln)]
    for section in REQUIRED_SECTIONS:
        if not any(h == section or h.startswith(section) for h in headings):
            errors.append(f"ERROR: {loc}: 正文缺少必需段落 `## {section}`")

    # 3. 禁止的流程耦合内容
    for offset, line in enumerate(body_lines):
        lineno = body_start + offset + 1
        for pattern, reason in FORBIDDEN_PATTERNS:
            if pattern in line:
                errors.append(f"ERROR: {loc}:{lineno}: 出现 `{pattern}`——{reason}")

    # 4. 行数（渐进披露）
    if len(lines) > MAX_LINES:
        warnings.append(
            f"WARNING: {loc}: 共 {len(lines)} 行，超过 {MAX_LINES} 行——"
            f"重内容应拆到同目录附加文件（examples.md / reference.md），SKILL.md 只留指路"
        )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    errors: list[str] = []
    warnings: list[str] = []

    if not SKILLS_DIR.is_dir():
        print(f"ERROR: 找不到 skills 目录：{SKILLS_DIR}")
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    for skill_dir in skill_dirs:
        check_skill(skill_dir, errors, warnings)

    for line in errors:
        print(line)
    for line in warnings:
        print(line)

    print(
        f"\nvalidate_skills: 检查 {len(skill_dirs)} 个 skill —— "
        f"{len(errors)} 个 ERROR，{len(warnings)} 个 WARNING"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
