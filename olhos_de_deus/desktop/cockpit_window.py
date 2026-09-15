from __future__ import annotations

import json
from functools import partial
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from olhos_de_deus import __version__

from .widgets import AnimatedCoreWidget
from .window import OlhosDeDeusWindow


class CockpitWindow(OlhosDeDeusWindow):
    """Cockpit-style shell inspired by the selected Modelo 2 mockup.

    The redesign is intentionally presentation-only: real execution still flows
    through DesktopController and the existing pages/adapters. No fake agent or
    integration success is introduced by the dashboard.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.ruflo_dock = None
        self._last_cockpit_result: dict[str, Any] | None = None
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Olho de Deus · Cockpit de Inteligência Artificial")
        self.resize(1540, 920)
        self.setMinimumSize(1180, 720)

    def set_ruflo_dock(self, dock) -> None:
        self.ruflo_dock = dock

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(215)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 18, 15, 15)
        layout.setSpacing(6)

        logo = QLabel("◉")
        logo.setObjectName("CockpitLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand = QLabel("OLHO DE DEUS")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("INTELIGÊNCIA EM AÇÃO")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        def nav(key: str, text: str, callback) -> None:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.clicked.connect(callback)
            self._nav_buttons[key] = button
            layout.addWidget(button)

        nav("dashboard", "⌂  Dashboard", lambda: self._show_page("dashboard"))
        nav("missions", "◎  Missões", lambda: self._show_page("missions"))
        nav("integrations", "△  Integrações", lambda: self._show_page("integrations"))
        nav("ruflo", "◉  Ruflo", self._show_ruflo)
        nav("doctor", "✚  Doctor", lambda: self._show_page("doctor"))
        nav("logs", "▤  Logs", lambda: self._show_page("logs"))
        nav("settings", "⚙  Configurações", lambda: self._show_page("settings"))
        layout.addStretch(1)

        quote = QLabel("“MAIS INTELIGÊNCIA\nPARA UM MUNDO MELHOR”")
        quote.setObjectName("CockpitQuote")
        quote.setWordWrap(True)
        layout.addWidget(quote)
        layout.addSpacing(12)
        version = QLabel(f"OLHO DE DEUS v{__version__}\nWindows Desktop")
        version.setObjectName("Muted")
        layout.addWidget(version)
        return sidebar

    def _status_item(self, title: str, value: str) -> tuple[QFrame, QLabel]:
        frame = QFrame()
        frame.setObjectName("CockpitStatusItem")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        title_label = QLabel(title)
        title_label.setObjectName("CockpitStatusTitle")
        value_label = QLabel(value)
        value_label.setObjectName("CockpitStatusValue")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return frame, value_label

    def _operation_card(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame()
        frame.setObjectName("OperationCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        heading = QLabel(title)
        heading.setObjectName("OperationTitle")
        layout.addWidget(heading)
        return frame, layout

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        outer = QHBoxLayout(page)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.setSpacing(12)

        center = QVBoxLayout()
        center.setSpacing(10)
        outer.addLayout(center, 1)

        top = QFrame()
        top.setObjectName("CockpitTopBar")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(8, 6, 8, 6)
        top_layout.setSpacing(6)
        item, self.cockpit_system = self._status_item("STATUS GERAL", "ONLINE")
        top_layout.addWidget(item)
        item, self.cockpit_version = self._status_item("VERSÃO", f"v{__version__}")
        top_layout.addWidget(item)
        item, self.cockpit_agent = self._status_item("AGENTE ATIVO", "Ruflo")
        top_layout.addWidget(item)
        item, self.cockpit_mission = self._status_item("MISSÃO ATUAL", "Aguardando")
        top_layout.addWidget(item, 2)
        model = QLabel("MODELO 2 · COCKPIT")
        model.setObjectName("CockpitModel")
        top_layout.addWidget(model)
        center.addWidget(top)

        hero = QFrame()
        hero.setObjectName("HeroBanner")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(18, 10, 18, 10)
        hero_text = QVBoxLayout()
        hero_title = QLabel("VER MAIS.  PENSAR MAIS.  REALIZAR MAIS.")
        hero_title.setObjectName("HeroTitle")
        hero_sub = QLabel("Cockpit operacional · coordenação, execução e resultados em uma única tela")
        hero_sub.setObjectName("Muted")
        hero_text.addWidget(hero_title)
        hero_text.addWidget(hero_sub)
        hero_layout.addLayout(hero_text, 1)
        self.core_animation = AnimatedCoreWidget()
        self.core_animation.setMinimumHeight(100)
        self.core_animation.setMaximumHeight(125)
        hero_layout.addWidget(self.core_animation, 1)
        center.addWidget(hero)

        command = QFrame()
        command.setObjectName("CommandCard")
        command_layout = QVBoxLayout(command)
        command_layout.setContentsMargins(14, 12, 14, 12)
        command_head = QHBoxLayout()
        command_title = QLabel("✣  COMANDO CENTRAL")
        command_title.setObjectName("SectionTitle")
        command_head.addWidget(command_title)
        command_head.addStretch(1)
        command_meta = QLabel("LINGUAGEM NATURAL  •  MULTIAGENTES  •  RESULTADOS REAIS")
        command_meta.setObjectName("CockpitMeta")
        command_head.addWidget(command_meta)
        command_layout.addLayout(command_head)

        self.quick_mission = QPlainTextEdit()
        self.quick_mission.setObjectName("CommandInput")
        self.quick_mission.setMaximumHeight(105)
        self.quick_mission.setPlaceholderText("O que você quer que o Olho de Deus faça?")
        command_layout.addWidget(self.quick_mission)

        buttons = QHBoxLayout()
        execute = QPushButton("▶  EXECUTAR")
        execute.setObjectName("PrimaryButton")
        execute.clicked.connect(self._run_quick_mission)
        plan = QPushButton("▣  PLANEJAR")
        plan.setObjectName("SecondaryButton")
        plan.clicked.connect(lambda: self._prepare_mission(""))
        research = QPushButton("⌕  PESQUISAR")
        research.setObjectName("SecondaryButton")
        research.clicked.connect(lambda: self._prepare_mission("Pesquisar e analisar: "))
        create = QPushButton("＋  CRIAR")
        create.setObjectName("SecondaryButton")
        create.clicked.connect(lambda: self._prepare_mission("Criar: "))
        buttons.addWidget(execute)
        buttons.addWidget(plan)
        buttons.addWidget(research)
        buttons.addWidget(create)
        buttons.addStretch(1)
        command_layout.addLayout(buttons)
        center.addWidget(command)

        response = QFrame()
        response.setObjectName("ResponseCard")
        response_layout = QVBoxLayout(response)
        response_layout.setContentsMargins(12, 10, 12, 10)
        response_head = QHBoxLayout()
        response_title = QLabel(">_  RESPOSTA / EXECUÇÃO")
        response_title.setObjectName("SectionTitle")
        self.cockpit_execution_state = QLabel("● PRONTO")
        self.cockpit_execution_state.setObjectName("Ready")
        response_head.addWidget(response_title)
        response_head.addStretch(1)
        response_head.addWidget(self.cockpit_execution_state)
        response_layout.addLayout(response_head)

        self.cockpit_tabs = QTabWidget()
        self.cockpit_tabs.setObjectName("CockpitTabs")
        self.dashboard_output = QPlainTextEdit()
        self.dashboard_output.setReadOnly(True)
        self.dashboard_output.setObjectName("ConsoleOutput")
        self.dashboard_logs = QPlainTextEdit()
        self.dashboard_logs.setReadOnly(True)
        self.dashboard_logs.setObjectName("ConsoleOutput")
        self.dashboard_results = QPlainTextEdit()
        self.dashboard_results.setReadOnly(True)
        self.dashboard_results.setObjectName("ConsoleOutput")
        self.cockpit_tabs.addTab(self.dashboard_output, "HISTÓRICO")
        self.cockpit_tabs.addTab(self.dashboard_logs, "LOGS")
        self.cockpit_tabs.addTab(self.dashboard_results, "RESULTADOS")
        response_layout.addWidget(self.cockpit_tabs, 1)
        center.addWidget(response, 1)

        operations = QFrame()
        operations.setObjectName("OperationsPanel")
        operations.setFixedWidth(305)
        operations_layout = QVBoxLayout(operations)
        operations_layout.setContentsMargins(10, 10, 10, 10)
        operations_layout.setSpacing(9)
        panel_title = QLabel("⌁  PAINEL DE OPERAÇÕES")
        panel_title.setObjectName("SectionTitle")
        operations_layout.addWidget(panel_title)

        card, card_layout = self._operation_card("RUFLO · AGENTE PRINCIPAL")
        self.ops_ruflo = QLabel("Verificando...")
        self.ops_ruflo.setObjectName("Ready")
        self.ops_ruflo_detail = QLabel("")
        self.ops_ruflo_detail.setObjectName("Muted")
        self.ops_ruflo_detail.setWordWrap(True)
        open_ruflo = QPushButton("ABRIR CONTROLES RUFLO")
        open_ruflo.setObjectName("SecondaryButton")
        open_ruflo.clicked.connect(self._show_ruflo)
        card_layout.addWidget(self.ops_ruflo)
        card_layout.addWidget(self.ops_ruflo_detail)
        card_layout.addWidget(open_ruflo)
        operations_layout.addWidget(card)

        card, card_layout = self._operation_card("SWARM · EQUIPE DE AGENTES")
        self.ops_swarm = QLabel("Verificando...")
        self.ops_swarm.setObjectName("Pending")
        self.ops_swarm_detail = QLabel("Estado real do workspace Ruflo")
        self.ops_swarm_detail.setObjectName("Muted")
        self.ops_swarm_detail.setWordWrap(True)
        card_layout.addWidget(self.ops_swarm)
        card_layout.addWidget(self.ops_swarm_detail)
        operations_layout.addWidget(card)

        card, card_layout = self._operation_card("AGENTES ATIVOS")
        self.ops_agents = QLabel("Nenhum runtime externo confirmado")
        self.ops_agents.setObjectName("Muted")
        self.ops_agents.setWordWrap(True)
        card_layout.addWidget(self.ops_agents)
        operations_layout.addWidget(card)

        card, card_layout = self._operation_card("INTEGRAÇÕES")
        self.ops_integrations = QLabel("0 / 7 READY")
        self.ops_integrations.setObjectName("Ready")
        self.ops_integrations_detail = QLabel("")
        self.ops_integrations_detail.setObjectName("Muted")
        self.ops_integrations_detail.setWordWrap(True)
        manage = QPushButton("GERENCIAR INTEGRAÇÕES")
        manage.setObjectName("SecondaryButton")
        manage.clicked.connect(lambda: self._show_page("integrations"))
        card_layout.addWidget(self.ops_integrations)
        card_layout.addWidget(self.ops_integrations_detail)
        card_layout.addWidget(manage)
        operations_layout.addWidget(card)
        operations_layout.addStretch(1)

        outer.addWidget(operations)
        return page

    def _show_ruflo(self) -> None:
        self._select_nav("ruflo")
        if self.ruflo_dock is None:
            self.statusBar().showMessage("Painel Ruflo ainda não foi anexado à janela", 5000)
            return
        self.ruflo_dock.show()
        self.ruflo_dock.raise_()
        widget = self.ruflo_dock.widget()
        if widget is not None and hasattr(widget, "refresh_status"):
            widget.refresh_status()

    def _prepare_mission(self, prefix: str) -> None:
        text = self.quick_mission.toPlainText().strip()
        if prefix and not text:
            text = prefix.rstrip()
        elif prefix and text:
            text = prefix + text
        self.mission_input.setPlainText(text)
        self._show_page("missions")
        self.mission_input.setFocus()

    def _format_mission_result(self, result: dict[str, Any]) -> str:
        mission = result.get("mission", {}) if isinstance(result, dict) else {}
        lines = [
            f"EXECUTION ID: {result.get('execution_id', '-')}",
            f"DURAÇÃO: {result.get('duration_ms', 0)} ms",
            f"STATUS DO ORQUESTRADOR: {mission.get('status', '-')}",
            "",
        ]
        for step in mission.get("steps", []):
            status = str(step.get("status", "")).upper()
            lines.append(f"[{status}] {step.get('name', '')} · {step.get('capability', '')}")
            for evidence in step.get("evidence", []) or []:
                lines.append(f"    ↳ {evidence}")
            if step.get("error"):
                lines.append(f"    ERRO: {step['error']}")
        lines.append("")
        lines.append("Observação: este painel mostra exatamente o retorno do orquestrador; integrações externas só são consideradas executadas quando produzem evidência real.")
        return "\n".join(lines)

    def _run_quick_mission(self) -> None:
        request = self.quick_mission.toPlainText().strip()
        if not request:
            QMessageBox.information(self, "Comando central", "Digite uma missão antes de executar.")
            return
        self.mission_input.setPlainText(request)
        self.cockpit_execution_state.setText("● EXECUTANDO")
        self.cockpit_execution_state.setObjectName("Pending")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state)
        self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.dashboard_output.setPlainText(
            f"> Missão recebida\n> {request}\n\n> Orquestrador em execução..."
        )
        self.cockpit_tabs.setCurrentWidget(self.dashboard_output)
        self.core_animation.set_activity("working")
        self._run_async(
            partial(self.controller.run_mission, request),
            self._cockpit_mission_finished,
            self._cockpit_mission_failed,
        )

    def _cockpit_mission_finished(self, result: object) -> None:
        payload = result if isinstance(result, dict) else {"result": result}
        self._last_cockpit_result = payload
        pretty = self._format_mission_result(payload)
        self.dashboard_output.setPlainText(pretty)
        self.dashboard_results.setPlainText(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        self.mission_result.setPlainText(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        self.mission_status.setText("CONCLUÍDA")
        self.mission_status.setObjectName("Ready")
        self.cockpit_execution_state.setText("● CONCLUÍDO")
        self.cockpit_execution_state.setObjectName("Ready")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state)
        self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.core_animation.set_activity("success")
        self._refresh_dashboard()
        self._refresh_logs()

    def _cockpit_mission_failed(self, message: str) -> None:
        self.dashboard_output.setPlainText(f"FALHA NA EXECUÇÃO\n\n{message}")
        self.dashboard_results.setPlainText(message)
        self.mission_result.setPlainText(message)
        self.mission_status.setText("FALHOU")
        self.mission_status.setObjectName("Error")
        self.cockpit_execution_state.setText("● ERRO")
        self.cockpit_execution_state.setObjectName("Error")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state)
        self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.core_animation.set_activity("error")
        self._refresh_dashboard()

    def _refresh_dashboard(self) -> None:
        data = self.controller.dashboard()
        ruflo = data.get("ruflo", {})
        summary = data.get("summary", {})
        last = data.get("last_mission")

        self.cockpit_system.setText("ONLINE")
        self.cockpit_version.setText(f"v{data.get('version', __version__)}")
        self.cockpit_agent.setText("Ruflo" if ruflo.get("operational") else "Núcleo local")
        if last:
            request = str(last.get("request", "Última missão"))
            self.cockpit_mission.setText(request[:42] + ("…" if len(request) > 42 else ""))
        else:
            self.cockpit_mission.setText("Aguardando")

        ruflo_ready = bool(ruflo.get("operational"))
        self.ops_ruflo.setText("READY" if ruflo_ready else "PENDING")
        self.ops_ruflo.setObjectName("Ready" if ruflo_ready else "Pending")
        self.ops_ruflo.style().unpolish(self.ops_ruflo)
        self.ops_ruflo.style().polish(self.ops_ruflo)
        self.ops_ruflo_detail.setText(str(ruflo.get("detail", "")))

        adapter = self.controller.ruflo_adapter()
        swarm_ready = bool(adapter.swarm_initialized)
        self.ops_swarm.setText("SWARM CRIADO" if swarm_ready else "NÃO CRIADO")
        self.ops_swarm.setObjectName("Ready" if swarm_ready else "Pending")
        self.ops_swarm.style().unpolish(self.ops_swarm)
        self.ops_swarm.style().polish(self.ops_swarm)
        self.ops_swarm_detail.setText(
            "Coordenação disponível; execução autônoma depende do runtime de agente configurado."
            if swarm_ready
            else "Abra Ruflo para preparar o swarm."
        )
        self.ops_agents.setText(
            "Coordenação Ruflo pronta. Agentes ativos não são simulados; o painel só mostrará atividade quando houver runtime externo configurado."
            if swarm_ready
            else "Nenhum runtime externo confirmado."
        )

        reports = data.get("integrations", [])
        operational = sum(bool(item.get("operational")) for item in reports)
        self.ops_integrations.setText(f"{operational} / {len(reports)} READY")
        state_lines = []
        for item in reports:
            state = "READY" if item.get("operational") else ("INSTALLED" if item.get("installed") else "PENDING")
            state_lines.append(f"{item.get('name')}: {state}")
        self.ops_integrations_detail.setText("\n".join(state_lines[:7]))

        logs = self.controller.storage.recent_logs(35)
        if logs:
            log_lines = []
            for item in reversed(logs):
                phase = f" [{item.get('phase')}]" if item.get("phase") else ""
                log_lines.append(
                    f"{item.get('created_at', '')}  {item.get('level', ''):<5}  {item.get('source', '')}{phase}  {item.get('message', '')}"
                )
            self.dashboard_logs.setPlainText("\n".join(log_lines))
        else:
            self.dashboard_logs.setPlainText("Nenhum log registrado.")

        if not self.dashboard_output.toPlainText().strip():
            self.dashboard_output.setPlainText(
                "> Olho de Deus inicializado.\n"
                "> Cockpit operacional.\n"
                f"> Ruflo: {'READY' if ruflo_ready else 'PENDING'} · Swarm: {'CRIADO' if swarm_ready else 'NÃO CRIADO'}\n"
                f"> Integrações: {operational}/{len(reports)} READY\n\n"
                "Digite uma missão no Comando Central."
            )
        if self._last_cockpit_result is None and last and last.get("result"):
            self.dashboard_results.setPlainText(json.dumps(last.get("result"), ensure_ascii=False, indent=2, default=str))
        elif self._last_cockpit_result is None:
            self.dashboard_results.setPlainText(
                f"Missões registradas: {summary.get('missions', 0)}\nAguardando um novo resultado no cockpit."
            )
