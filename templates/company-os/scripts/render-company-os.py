#!/usr/bin/env python3
"""Render a reusable company-agent OS from a client config.

This script intentionally has no template-engine dependency. It supports simple
placeholders such as:

    {{ company.name }}
    {{ agents.sales.scope | yaml_inline }}
    {{ approval_policy.drafts_allowed | bool_lower }}
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"

PLACEHOLDER = re.compile(r"{{\s*([^}]+?)\s*}}")


def deep_get(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        part = part.strip()
        if not part:
            continue
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"Missing config key: {path}")
        value = value[part]
    return value


def apply_filter(value: Any, filter_name: str) -> str:
    if filter_name == "bool_lower":
        return "true" if bool(value) else "false"
    if filter_name == "yaml_inline":
        return json.dumps(value)
    if filter_name == "json":
        return json.dumps(value, indent=2)
    raise ValueError(f"Unsupported filter: {filter_name}")


def render_text(text: str, config: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        expr = match.group(1).strip()
        if "|" in expr:
            key, filter_name = [p.strip() for p in expr.split("|", 1)]
            return apply_filter(deep_get(config, key), filter_name)
        value = deep_get(config, expr)
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return str(value)

    return PLACEHOLDER.sub(replace, text)


def render_tree(config: dict[str, Any], output: Path) -> list[Path]:
    written: list[Path] = []
    output.mkdir(parents=True, exist_ok=True)
    for tpl in sorted(TEMPLATE_DIR.rglob("*.tpl")):
        rel = tpl.relative_to(TEMPLATE_DIR)
        out_rel = Path(str(rel).removesuffix(".tpl"))
        target = output / out_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_text(tpl.read_text(encoding="utf-8"), config), encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a company-agent OS from a config YAML file.")
    parser.add_argument("--config", required=True, help="Client company YAML config")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--force", action="store_true", help="Delete output directory before rendering")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    if output.exists() and args.force:
        shutil.rmtree(output)
    elif output.exists() and any(output.iterdir()):
        raise SystemExit(f"Output directory is not empty. Use --force to replace: {output}")

    written = render_tree(config, output)
    print(f"rendered_company_os={output}")
    print(f"files_written={len(written)}")
    for path in written:
        print(path.relative_to(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
