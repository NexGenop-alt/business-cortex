"""Command line interface for Business Cortex."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.core.dispatcher import DryRunDispatcher, HermesCliDispatcher
from cortex.core.orchestrator import BusinessCortex, DEFAULT_CONFIG


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Business Cortex workflow router")
    parser.add_argument("--config", default="config/client.example.json", help="Path to client config JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Route a business request")
    run.add_argument("request", nargs="+", help="Business request text")
    run.add_argument("--config", dest="run_config", help="Path to client config JSON")
    run.add_argument("--format", choices=["json", "summary"], default="summary")
    run.add_argument("--dispatch", choices=["none", "dry-run", "hermes"], default="none", help="Optionally dispatch generated handoffs")

    init = sub.add_parser("init-client", help="Write an example client config")
    init.add_argument("path", help="Destination config path")
    init.add_argument("--name", default="Client Organization")
    init.add_argument("--industry", default="general business")
    return parser


def load_cortex(config_path: str) -> BusinessCortex:
    path = Path(config_path).expanduser()
    if path.exists():
        return BusinessCortex.from_json_file(str(path))
    return BusinessCortex(DEFAULT_CONFIG)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init-client":
        config = dict(DEFAULT_CONFIG)
        config["organization"] = {"name": args.name, "industry": args.industry}
        path = Path(args.path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(config, indent=2) + "\n")
        print(f"Wrote client config: {path}")
        return 0

    cortex = load_cortex(getattr(args, "run_config", None) or args.config)
    if args.command == "run":
        result = cortex.run(" ".join(args.request))
        output = result.to_dict()
        if args.dispatch != "none":
            dispatcher = DryRunDispatcher(cortex.store) if args.dispatch == "dry-run" else HermesCliDispatcher(cortex.store)
            dispatches = []
            for task in result.handoffs:
                profile = cortex.agents[task.agent_key].profile if task.agent_key in cortex.agents else task.agent_key
                dispatches.append(dispatcher.dispatch(task, profile=profile).to_dict())
            output["dispatches"] = dispatches
        if args.format == "json":
            print(json.dumps(output, indent=2))
        else:
            print(result.summary)
            print(f"workflow: {result.workflow}")
            print(f"next_action: {result.next_action}")
            for task in result.handoffs:
                print(f"handoff: {task.agent_key} -> {task.agent_name}")
            for item in output.get("dispatches", []):
                print(f"dispatch: {item['agent_key']} status={item['status']} run_id={item.get('run_id')}")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
