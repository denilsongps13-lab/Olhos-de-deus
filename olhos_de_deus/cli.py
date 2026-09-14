from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .bootstrap import bootstrap_sources
from .orchestrator import Orchestrator
from .sources import load_sources


def _json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="olhos-de-deus")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Planeja, roteia e valida uma missao")
    run.add_argument("mission", help="Missao a ser planejada e roteada")

    sources = sub.add_parser("sources", help="Lista os sete projetos upstream")
    sources.add_argument("--json", action="store_true", dest="as_json")

    bootstrap = sub.add_parser("bootstrap", help="Clona/atualiza os projetos upstream")
    bootstrap.add_argument("names", nargs="*", help="Nomes opcionais; vazio = todos")
    bootstrap.add_argument("--target", default="external", help="Diretorio de destino")
    bootstrap.add_argument("--dry-run", action="store_true", help="Mostra o que seria executado")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "run":
        mission = Orchestrator().run(args.mission)
        _json(asdict(mission))
        return

    if args.command == "sources":
        data = [source.to_dict() for source in load_sources()]
        if args.as_json:
            _json(data)
        else:
            for source in data:
                print(f"{source['name']}: {source['repo']} [{source['ref']}] ({source['license']})")
        return

    if args.command == "bootstrap":
        results = bootstrap_sources(args.target, args.names, dry_run=args.dry_run)
        _json([asdict(result) for result in results])
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
