from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .orchestrator import Orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(prog="olhos-de-deus")
    parser.add_argument("mission", help="Missao a ser planejada e roteada")
    args = parser.parse_args()

    mission = Orchestrator().run(args.mission)
    print(json.dumps(asdict(mission), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
