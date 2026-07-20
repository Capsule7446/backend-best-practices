#!/usr/bin/env python3
"""校验插件清单与命令入口的完整性。

检查项：
1. .claude-plugin/plugin.json 可解析；version 是 semver；skills 路径存在。
2. commands/*.md 存在时逐个检查非空；允许插件完全使用 skills/ 作为入口。
3. README.md 中出现的 /backend-best-practices:<cmd> 命令若无对应
   commands/<cmd>.md 文件则 WARNING（<pattern> 等模板按通配匹配）。

用法：python scripts/validate_plugin.py
退出码：有 ERROR 时为 1，否则 0。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
COMMANDS_DIR = REPO_ROOT / "commands"
README = REPO_ROOT / "README.md"

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
README_COMMAND_RE = re.compile(r"/backend-best-practices:([A-Za-z0-9_<>-]+)")


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def template_to_regex(template: str) -> re.Pattern:
    parts = re.split(r"<[^>]+>", template)
    return re.compile("^" + "[a-z0-9-]+".join(re.escape(p) for p in parts) + "$")


def check_plugin_json(errors: list[str]) -> None:
    if not PLUGIN_JSON.is_file():
        errors.append(f"ERROR: 缺少 {rel(PLUGIN_JSON)}")
        return
    try:
        data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        errors.append(f"ERROR: {rel(PLUGIN_JSON)}: JSON 解析失败——{exc}")
        return

    version = data.get("version")
    if not version:
        errors.append(f"ERROR: {rel(PLUGIN_JSON)}: 缺少 `version` 字段")
    elif not SEMVER_RE.fullmatch(str(version)):
        errors.append(
            f"ERROR: {rel(PLUGIN_JSON)}: version `{version}` 不是合法 semver（MAJOR.MINOR.PATCH）"
        )

    skills_path = data.get("skills")
    if not skills_path:
        errors.append(f"ERROR: {rel(PLUGIN_JSON)}: 缺少 `skills` 路径字段")
    else:
        resolved = (REPO_ROOT / str(skills_path).lstrip("./")).resolve()
        if not resolved.is_dir():
            errors.append(
                f"ERROR: {rel(PLUGIN_JSON)}: skills 路径 `{skills_path}` 不存在（解析为 {resolved}）"
            )


def check_commands(errors: list[str]) -> list[str]:
    if not COMMANDS_DIR.is_dir():
        return []
    names: list[str] = []
    for cmd in sorted(COMMANDS_DIR.glob("*.md")):
        names.append(cmd.stem)
        if not cmd.read_text(encoding="utf-8").strip():
            errors.append(f"ERROR: {rel(cmd)}: 命令文件为空")
    return names


def check_readme_commands(command_names: list[str], warnings: list[str]) -> None:
    if not README.is_file():
        warnings.append("WARNING: 缺少 README.md，跳过命令引用检查")
        return
    text = README.read_text(encoding="utf-8")
    for cmd in sorted(set(README_COMMAND_RE.findall(text))):
        if "<" in cmd:
            regex = template_to_regex(cmd)
            if not any(regex.match(n) for n in command_names):
                warnings.append(
                    f"WARNING: README.md 引用了 `/backend-best-practices:{cmd}`，"
                    f"但 commands/ 下没有匹配该模板的命令文件"
                )
        elif cmd not in command_names:
            warnings.append(
                f"WARNING: README.md 引用了 `/backend-best-practices:{cmd}`，"
                f"但缺少 commands/{cmd}.md"
            )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    errors: list[str] = []
    warnings: list[str] = []

    check_plugin_json(errors)
    command_names = check_commands(errors)
    check_readme_commands(command_names, warnings)

    for line in errors:
        print(line)
    for line in warnings:
        print(line)

    print(
        f"\nvalidate_plugin: 检查 plugin.json + {len(command_names)} 个命令 —— "
        f"{len(errors)} 个 ERROR，{len(warnings)} 个 WARNING"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
