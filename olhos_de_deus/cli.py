from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .bootstrap import bootstrap_sources
from .integrations import IntegrationHub
from .orchestrator import Orchestrator
from .ruflo import RufloAdapter
from .sources import load_sources


def _json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _add_external_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--external-root", default="external", help="Diretorio dos repositorios externos")


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

    doctor = sub.add_parser("doctor", help="Verifica o estado operacional das sete integracoes")
    doctor.add_argument("--external-root", default="external", help="Diretorio dos repositorios externos")
    doctor.add_argument("--comfyui-url", default=None, help="URL da API externa do ComfyUI")
    doctor.add_argument("--probe-services", action="store_true", help="Testa servicos de rede configurados")
    doctor.add_argument("--json", action="store_true", dest="as_json")
    doctor.add_argument("--strict", action="store_true", help="Retorna erro se alguma integracao nao estiver operacional")
    doctor.add_argument("--with-ruflo", action="store_true", help="Inclui o meta-harness Ruflo como fase 0")
    doctor.add_argument("--ruflo-workspace", default=".", help="Workspace usado pelo Ruflo")

    ruflo = sub.add_parser("ruflo", help="Fase 0 opcional: meta-orquestrador Ruflo")
    ruflo_sub = ruflo.add_subparsers(dest="ruflo_command", required=True)

    ruflo_status = ruflo_sub.add_parser("status", help="Mostra o estado local do Ruflo")
    ruflo_status.add_argument("--workspace", default=".")

    ruflo_init = ruflo_sub.add_parser("init", help="Inicializa Ruflo em um workspace")
    ruflo_init.add_argument("--workspace", default=".")
    ruflo_init.add_argument("--wizard", action="store_true", help="Usa o assistente interativo oficial")
    ruflo_init.add_argument("--execute", action="store_true", help="Executa de verdade; sem isso apenas mostra o comando")

    ruflo_mcp = ruflo_sub.add_parser("mcp", help="Mostra o comando oficial do servidor MCP Ruflo")
    ruflo_mcp.add_argument("--workspace", default=".")

    ruflo_probe = ruflo_sub.add_parser("probe", help="Consulta a versao do Ruflo via npx")
    ruflo_probe.add_argument("--workspace", default=".")
    ruflo_probe.add_argument("--execute", action="store_true", help="Permite acesso ao pacote via npx; sem isso e dry-run")

    phase = sub.add_parser("phase", help="Executa ou consulta uma das sete fases")
    phases = phase.add_subparsers(dest="phase_name", required=True)

    graphify = phases.add_parser("graphify", help="Fase 1: inteligencia estrutural")
    graphify.add_argument("target", nargs="?", default=".")
    graphify.add_argument("--execute", action="store_true")
    _add_external_root(graphify)

    comfyui = phases.add_parser("comfyui", help="Fase 2: workflow visual por API")
    comfyui.add_argument("--url", default=None, help="URL da API do ComfyUI")
    comfyui.add_argument("--workflow", help="Arquivo JSON em formato de API do ComfyUI")
    comfyui.add_argument("--probe", action="store_true", help="Testa se a API esta acessivel")
    comfyui.add_argument("--execute", action="store_true", help="Envia o workflow para a API")
    _add_external_root(comfyui)

    speckit = phases.add_parser("spec-kit", help="Fase 3: especificacao orientada a plano")
    speckit.add_argument("target", nargs="?", default=".")
    speckit.add_argument("--integration", default="copilot")
    speckit.add_argument("--execute", action="store_true")
    _add_external_root(speckit)

    qa = phases.add_parser("qa-skills", help="Fase 4: skills de QA")
    qa.add_argument("skill", nargs="?", help="Nome da skill; vazio lista as disponiveis")
    _add_external_root(qa)

    output = phases.add_parser("i-have-adhd", help="Fase 5: perfil operacional de saida")
    _add_external_root(output)

    agency = phases.add_parser("agency-agents", help="Fase 6: catalogo de agentes")
    agency.add_argument("query", nargs="?", help="Busca um agente; vazio lista o catalogo")
    _add_external_root(agency)

    artemis = phases.add_parser("artemis", help="Fase 7: operacao Android")
    artemis.add_argument("task", help="Tarefa a ser executada no dispositivo")
    artemis.add_argument("--profile", choices=("flash", "pro"), default="flash")
    artemis.add_argument("--execute", action="store_true")
    _add_external_root(artemis)
    return parser


def _run_phase(args: argparse.Namespace) -> None:
    comfyui_url = getattr(args, "url", None)
    hub = IntegrationHub(args.external_root, comfyui_url=comfyui_url)

    if args.phase_name == "graphify":
        adapter = hub.adapter("graphify")
        result = adapter.run(args.target, dry_run=not args.execute)
        if isinstance(result, tuple):
            _json({"phase": 1, "execute": False, "command": result})
        else:
            _json({"phase": 1, "execute": True, "returncode": result.returncode, "stdout": result.stdout})
        return

    if args.phase_name == "comfyui":
        adapter = hub.adapter("comfyui")
        if args.workflow:
            workflow_path = Path(args.workflow).expanduser().resolve()
            workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
            if not args.execute:
                _json(
                    {
                        "phase": 2,
                        "execute": False,
                        "endpoint": adapter.endpoint,
                        "workflow": str(workflow_path),
                        "nodes": len(workflow),
                    }
                )
                return
            _json(adapter.queue_prompt(workflow))
            return
        _json(adapter.report(probe_services=args.probe).to_dict())
        return

    if args.phase_name == "spec-kit":
        adapter = hub.adapter("spec-kit")
        result = adapter.init_project(args.target, integration=args.integration, dry_run=not args.execute)
        if isinstance(result, tuple):
            _json({"phase": 3, "execute": False, "command": result, "target": str(Path(args.target).resolve())})
        else:
            _json({"phase": 3, "execute": True, "returncode": result.returncode, "stdout": result.stdout})
        return

    if args.phase_name == "qa-skills":
        adapter = hub.adapter("qa-skills")
        if args.skill:
            print(adapter.load_skill(args.skill))
        else:
            _json({"phase": 4, "skills": adapter.list_skills()})
        return

    if args.phase_name == "i-have-adhd":
        adapter = hub.adapter("i-have-adhd")
        print(adapter.load_rules())
        return

    if args.phase_name == "agency-agents":
        adapter = hub.adapter("agency-agents")
        if args.query:
            path = adapter.find_agent(args.query)
            _json({"phase": 6, "agent": path.stem, "path": str(path)})
        else:
            _json({"phase": 6, "agents": adapter.list_agents()})
        return

    if args.phase_name == "artemis":
        adapter = hub.adapter("artemis")
        result = adapter.run(args.task, profile=args.profile, dry_run=not args.execute)
        if isinstance(result, tuple):
            _json({"phase": 7, "execute": False, "command": result})
        else:
            _json({"phase": 7, "execute": True, "returncode": result.returncode, "stdout": result.stdout})
        return

    raise SystemExit(2)


def _run_ruflo(args: argparse.Namespace) -> None:
    adapter = RufloAdapter(args.workspace)

    if args.ruflo_command == "status":
        _json(adapter.report().to_dict())
        return

    if args.ruflo_command == "init":
        result = adapter.init_workspace(wizard=args.wizard, dry_run=not args.execute)
        if isinstance(result, tuple):
            _json(
                {
                    "phase": 0,
                    "name": "ruflo",
                    "execute": False,
                    "workspace": str(adapter.workspace),
                    "command": result,
                }
            )
        else:
            _json(
                {
                    "phase": 0,
                    "name": "ruflo",
                    "execute": True,
                    "workspace": str(adapter.workspace),
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )
        return

    if args.ruflo_command == "mcp":
        _json(
            {
                "phase": 0,
                "name": "ruflo",
                "workspace": str(adapter.workspace),
                "command": adapter.build_mcp_command(),
                "note": "Preview only: MCP is a long-running process and is not started implicitly.",
            }
        )
        return

    if args.ruflo_command == "probe":
        result = adapter.probe_runtime(dry_run=not args.execute)
        if isinstance(result, tuple):
            _json({"phase": 0, "name": "ruflo", "execute": False, "command": result})
        else:
            _json(
                {
                    "phase": 0,
                    "name": "ruflo",
                    "execute": True,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )
        return

    raise SystemExit(2)


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

    if args.command == "doctor":
        hub = IntegrationHub(args.external_root, comfyui_url=args.comfyui_url)
        reports = list(hub.reports(probe_services=args.probe_services))
        if args.with_ruflo:
            reports.insert(0, RufloAdapter(args.ruflo_workspace).report())
        if args.as_json:
            _json(
                {
                    "operational": sum(item.operational for item in reports),
                    "total": len(reports),
                    "phases": [item.to_dict() for item in reports],
                }
            )
        else:
            for item in reports:
                state = "READY" if item.operational else ("INSTALLED" if item.installed else "PENDING")
                print(f"{item.phase}. {item.name}: {state} - {item.detail}")
        if args.strict and not all(item.operational for item in reports):
            raise SystemExit(1)
        return

    if args.command == "ruflo":
        _run_ruflo(args)
        return

    if args.command == "phase":
        _run_phase(args)
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
