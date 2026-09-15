from __future__ import annotations

import json
import math
from functools import partial
from typing import Any

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from olhos_de_deus import __version__
from .window import OlhosDeDeusWindow


class HudEyeWidget(QWidget):
    """Decorative eye/HUD drawn locally so the cockpit has no image dependency."""

    def __init__(self, compact: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.compact = compact
        self.setMinimumSize(90 if compact else 150, 62 if compact else 110)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        scale = min(w, h)

        p.setPen(QPen(QColor(0, 151, 217, 80), 1))
        for factor in (0.72, 0.55, 0.38):
            r = scale * factor / 2
            p.drawEllipse(QPointF(cx, cy), r, r)

        path = QPainterPath()
        path.moveTo(cx - scale * 0.38, cy)
        path.cubicTo(cx - scale * 0.18, cy - scale * 0.24, cx + scale * 0.18, cy - scale * 0.24, cx + scale * 0.38, cy)
        path.cubicTo(cx + scale * 0.18, cy + scale * 0.24, cx - scale * 0.18, cy + scale * 0.24, cx - scale * 0.38, cy)
        p.setPen(QPen(QColor(43, 220, 255, 225), 2.0 if not self.compact else 1.5))
        p.drawPath(path)

        glow = QRadialGradient(QPointF(cx, cy), scale * 0.18)
        glow.setColorAt(0.0, QColor(230, 255, 255, 255))
        glow.setColorAt(0.18, QColor(71, 230, 255, 240))
        glow.setColorAt(0.55, QColor(0, 132, 220, 150))
        glow.setColorAt(1.0, QColor(0, 50, 100, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glow)
        p.drawEllipse(QPointF(cx, cy), scale * 0.17, scale * 0.17)

        p.setBrush(QColor(2, 15, 30, 245))
        p.drawEllipse(QPointF(cx, cy), scale * 0.075, scale * 0.075)
        p.setBrush(QColor(150, 250, 255, 240))
        p.drawEllipse(QPointF(cx - scale * 0.025, cy - scale * 0.025), scale * 0.018, scale * 0.018)

        p.setPen(QPen(QColor(55, 214, 255, 130), 1))
        for i in range(12):
            angle = i * math.pi / 6
            r1, r2 = scale * 0.25, scale * 0.34
            p.drawLine(QPointF(cx + math.cos(angle) * r1, cy + math.sin(angle) * r1),
                       QPointF(cx + math.cos(angle) * r2, cy + math.sin(angle) * r2))
        p.end()


class NetworkGlobeWidget(QWidget):
    """Cinematic network-globe banner drawn with QPainter."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(118)
        self.setMaximumHeight(135)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        grad = QLinearGradient(0, 0, rect.width(), rect.height())
        grad.setColorAt(0, QColor(3, 13, 24))
        grad.setColorAt(0.48, QColor(4, 31, 55))
        grad.setColorAt(1, QColor(2, 13, 28))
        p.fillRect(rect, grad)

        cx = rect.width() * 0.62
        cy = rect.height() * 1.08
        radius = rect.height() * 0.92
        rg = QRadialGradient(QPointF(cx, cy), radius)
        rg.setColorAt(0, QColor(5, 82, 145, 210))
        rg.setColorAt(0.5, QColor(0, 55, 110, 180))
        rg.setColorAt(1, QColor(0, 10, 30, 0))
        p.setBrush(rg)
        p.setPen(QPen(QColor(35, 170, 255, 150), 1.2))
        p.drawEllipse(QPointF(cx, cy), radius, radius)

        p.setPen(QPen(QColor(57, 177, 240, 75), 0.8))
        for yoff in (-0.42, -0.20, 0.02, 0.24):
            rr = QRectF(cx - radius, cy - radius * (0.36 + yoff), radius * 2, radius * 0.34)
            p.drawArc(rr, 0, 180 * 16)
        for xoff in (-0.45, -0.22, 0, 0.22, 0.45):
            p.drawArc(QRectF(cx - radius * (0.32 + abs(xoff) * 0.25), cy - radius,
                             radius * (0.64 + abs(xoff) * 0.5), radius * 2), 90 * 16, 180 * 16)

        nodes = [
            (0.47, 0.45), (0.55, 0.31), (0.63, 0.42), (0.71, 0.28), (0.77, 0.46),
            (0.59, 0.57), (0.68, 0.59), (0.83, 0.34), (0.88, 0.52), (0.74, 0.67),
        ]
        p.setPen(QPen(QColor(54, 199, 255, 110), 0.9))
        pts = [QPointF(rect.width() * x, rect.height() * y) for x, y in nodes]
        links = [(0,1),(1,2),(2,3),(3,4),(2,5),(5,6),(3,7),(7,8),(6,9),(4,8),(6,8)]
        for a, b in links:
            p.drawLine(pts[a], pts[b])
        for pt in pts:
            p.setBrush(QColor(83, 230, 255, 230))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(pt, 2.2, 2.2)
        p.end()


class CockpitWindow(OlhosDeDeusWindow):
    """High-fidelity cockpit shell while preserving the real controller/adapters."""

    def __init__(self, *args, **kwargs) -> None:
        self.ruflo_dock = None
        self._last_cockpit_result: dict[str, Any] | None = None
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Olho de Deus · Cockpit de Inteligência Artificial")
        self.resize(1600, 960)
        self.setMinimumSize(1240, 760)

    def set_ruflo_dock(self, dock) -> None:
        self.ruflo_dock = dock

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(4)

        eye = HudEyeWidget(compact=True)
        eye.setFixedHeight(90)
        layout.addWidget(eye)
        brand = QLabel("OLHO DE DEUS")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("INTELIGÊNCIA EM AÇÃO")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        def nav(key: str, text: str, callback) -> None:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.clicked.connect(callback)
            self._nav_buttons[key] = button
            layout.addWidget(button)

        nav("dashboard", "⌂   Dashboard", lambda: self._show_page("dashboard"))
        nav("missions", "◎   Missões", lambda: self._show_page("missions"))
        nav("integrations", "△   Integrações", lambda: self._show_page("integrations"))
        nav("ruflo", "◉   Ruflo", self._show_ruflo)
        nav("doctor", "✚   Doctor", lambda: self._show_page("doctor"))
        nav("logs", "▤   Logs", lambda: self._show_page("logs"))
        nav("settings", "⚙   Configurações", lambda: self._show_page("settings"))
        layout.addStretch(1)

        quote = QLabel("“ MAIS INTELIGÊNCIA\n   PARA UM\n   MUNDO MELHOR ”")
        quote.setObjectName("CockpitQuote")
        layout.addWidget(quote)
        layout.addSpacing(8)
        version = QLabel(f"◉  OLHO DE DEUS v{__version__}\n    SISTEMA OPERACIONAL DE INTELIGÊNCIA")
        version.setObjectName("SidebarFooter")
        version.setWordWrap(True)
        layout.addWidget(version)
        return sidebar

    def _status_item(self, icon: str, title: str, value: str) -> tuple[QFrame, QLabel]:
        frame = QFrame()
        frame.setObjectName("CockpitStatusItem")
        row = QHBoxLayout(frame)
        row.setContentsMargins(11, 7, 11, 7)
        row.setSpacing(9)
        icon_label = QLabel(icon)
        icon_label.setObjectName("StatusIcon")
        row.addWidget(icon_label)
        text = QVBoxLayout()
        text.setSpacing(1)
        title_label = QLabel(title)
        title_label.setObjectName("CockpitStatusTitle")
        value_label = QLabel(value)
        value_label.setObjectName("CockpitStatusValue")
        text.addWidget(title_label)
        text.addWidget(value_label)
        row.addLayout(text, 1)
        return frame, value_label

    def _operation_card(self, title: str, subtitle: str = "") -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame()
        frame.setObjectName("OperationCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(5)
        heading = QLabel(title)
        heading.setObjectName("OperationTitle")
        layout.addWidget(heading)
        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("OperationSubtitle")
            layout.addWidget(sub)
        return frame, layout

    def _status_row(self, name: str, state: str, ready: bool) -> QWidget:
        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 1, 0, 1)
        dot = QLabel("●")
        dot.setObjectName("DotReady" if ready else "DotPending")
        name_label = QLabel(name)
        name_label.setObjectName("OperationRowName")
        status = QLabel(state)
        status.setObjectName("ReadyBadge" if ready else "PendingBadge")
        lay.addWidget(dot)
        lay.addWidget(name_label, 1)
        lay.addWidget(status)
        return row

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        outer = QHBoxLayout(page)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(10)

        center = QVBoxLayout()
        center.setSpacing(8)
        outer.addLayout(center, 1)

        top = QFrame()
        top.setObjectName("CockpitTopBar")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(7, 5, 7, 5)
        top_layout.setSpacing(5)
        item, self.cockpit_system = self._status_item("●", "STATUS GERAL", "ONLINE")
        top_layout.addWidget(item)
        item, self.cockpit_version = self._status_item("◉", "VERSÃO", f"v{__version__}")
        top_layout.addWidget(item)
        item, self.cockpit_agent = self._status_item("✺", "AGENTE ATIVO", "Ruflo")
        top_layout.addWidget(item)
        item, self.cockpit_mission = self._status_item("◎", "MISSÃO ATUAL", "Aguardando")
        top_layout.addWidget(item, 2)
        model = QLabel("MODELO 2 — COCKPIT")
        model.setObjectName("CockpitModel")
        top_layout.addWidget(model)
        center.addWidget(top)

        hero = QFrame()
        hero.setObjectName("HeroBanner")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(18, 8, 18, 8)
        hero_text = QVBoxLayout()
        hero_text.setSpacing(2)
        for line in ("VER MAIS.", "PENSAR MAIS.", "REALIZAR MAIS."):
            lab = QLabel(line)
            lab.setObjectName("HeroTitle")
            hero_text.addWidget(lab)
        hero_layout.addLayout(hero_text)
        globe = NetworkGlobeWidget()
        hero_layout.addWidget(globe, 1)
        hero_quote = QLabel("“ DADOS HOJE.\n  UM AMANHÃ MELHOR. ”")
        hero_quote.setObjectName("HeroQuote")
        hero_quote.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        hero_layout.addWidget(hero_quote)
        center.addWidget(hero)

        command = QFrame()
        command.setObjectName("CommandCard")
        command_layout = QVBoxLayout(command)
        command_layout.setContentsMargins(14, 10, 14, 10)
        command_layout.setSpacing(7)
        command_head = QHBoxLayout()
        command_title = QLabel("✣  COMANDO CENTRAL")
        command_title.setObjectName("SectionTitle")
        command_head.addWidget(command_title)
        command_head.addStretch(1)
        meta = QLabel("LINGUAGEM NATURAL   •   MULTIAGENTES   •   RESULTADOS REAIS")
        meta.setObjectName("CockpitMeta")
        command_head.addWidget(meta)
        command_layout.addLayout(command_head)

        self.quick_mission = QPlainTextEdit()
        self.quick_mission.setObjectName("CommandInput")
        self.quick_mission.setMaximumHeight(120)
        self.quick_mission.setPlaceholderText("O que você quer que o Olho de Deus faça?")
        command_layout.addWidget(self.quick_mission)

        buttons = QHBoxLayout()
        execute = QPushButton("▶   EXECUTAR     Enter")
        execute.setObjectName("PrimaryButton")
        execute.clicked.connect(self._run_quick_mission)
        plan = QPushButton("▣   PLANEJAR")
        plan.setObjectName("SecondaryButton")
        plan.clicked.connect(lambda: self._prepare_mission(""))
        research = QPushButton("⌕   PESQUISAR")
        research.setObjectName("SecondaryButton")
        research.clicked.connect(lambda: self._prepare_mission("Pesquisar e analisar: "))
        create = QPushButton("＋   CRIAR")
        create.setObjectName("SecondaryButton")
        create.clicked.connect(lambda: self._prepare_mission("Criar: "))
        more = QPushButton("•••")
        more.setObjectName("SecondaryButton")
        buttons.addWidget(execute)
        buttons.addWidget(plan)
        buttons.addWidget(research)
        buttons.addWidget(create)
        buttons.addWidget(more)
        buttons.addStretch(1)
        command_layout.addLayout(buttons)
        center.addWidget(command)

        response = QFrame()
        response.setObjectName("ResponseCard")
        response_layout = QVBoxLayout(response)
        response_layout.setContentsMargins(12, 9, 12, 9)
        response_layout.setSpacing(5)
        response_head = QHBoxLayout()
        response_title = QLabel(">_  RESPOSTA / EXECUÇÃO")
        response_title.setObjectName("SectionTitle")
        self.cockpit_execution_state = QLabel("● EXECUÇÃO EM TEMPO REAL")
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
        files_placeholder = QPlainTextEdit()
        files_placeholder.setReadOnly(True)
        files_placeholder.setObjectName("ConsoleOutput")
        files_placeholder.setPlainText("Arquivos produzidos por executores reais aparecerão aqui.")
        agents_placeholder = QPlainTextEdit()
        agents_placeholder.setReadOnly(True)
        agents_placeholder.setObjectName("ConsoleOutput")
        agents_placeholder.setPlainText("Atividade de agentes aparecerá aqui quando houver runtime externo configurado.\nNenhuma atividade é simulada.")
        self.cockpit_tabs.addTab(self.dashboard_output, "HISTÓRICO")
        self.cockpit_tabs.addTab(self.dashboard_logs, "LOGS")
        self.cockpit_tabs.addTab(self.dashboard_results, "RESULTADOS")
        self.cockpit_tabs.addTab(files_placeholder, "ARQUIVOS")
        self.cockpit_tabs.addTab(agents_placeholder, "PENSAMENTO DOS AGENTES")
        response_layout.addWidget(self.cockpit_tabs, 1)

        bottom = QHBoxLayout()
        command_line = QLabel("Digite uma mensagem ou comando...")
        command_line.setObjectName("CommandBar")
        bottom.addWidget(command_line, 1)
        send = QPushButton("➤")
        send.setObjectName("SendButton")
        send.clicked.connect(self._run_quick_mission)
        bottom.addWidget(send)
        response_layout.addLayout(bottom)
        center.addWidget(response, 1)

        operations = QFrame()
        operations.setObjectName("OperationsPanel")
        operations.setFixedWidth(320)
        operations_layout = QVBoxLayout(operations)
        operations_layout.setContentsMargins(10, 10, 10, 10)
        operations_layout.setSpacing(8)
        panel_title = QLabel("⌁  PAINEL DE OPERAÇÕES")
        panel_title.setObjectName("SectionTitle")
        operations_layout.addWidget(panel_title)

        card, card_layout = self._operation_card("✺  Ruflo", "Agente principal")
        self.ops_ruflo = QLabel("Verificando...")
        self.ops_ruflo.setObjectName("ReadyBadge")
        self.ops_ruflo_detail = QLabel("")
        self.ops_ruflo_detail.setObjectName("Muted")
        self.ops_ruflo_detail.setWordWrap(True)
        metrics = QLabel("INTELIGÊNCIA        MEMÓRIA        CONTEXTO\nATIVA                 LOCAL          WORKSPACE")
        metrics.setObjectName("MetricsLabel")
        open_ruflo = QPushButton("ABRIR CONTROLES RUFLO")
        open_ruflo.setObjectName("SecondaryButton")
        open_ruflo.clicked.connect(self._show_ruflo)
        card_layout.addWidget(self.ops_ruflo)
        card_layout.addWidget(self.ops_ruflo_detail)
        card_layout.addWidget(metrics)
        card_layout.addWidget(open_ruflo)
        operations_layout.addWidget(card)

        card, card_layout = self._operation_card("△  Swarm", "Equipe de agentes")
        self.ops_swarm = QLabel("Verificando...")
        self.ops_swarm.setObjectName("PendingBadge")
        self.ops_swarm_detail = QLabel("Estado real do workspace Ruflo")
        self.ops_swarm_detail.setObjectName("Muted")
        self.ops_swarm_detail.setWordWrap(True)
        self.swarm_progress = QProgressBar()
        self.swarm_progress.setObjectName("HudProgress")
        self.swarm_progress.setRange(0, 100)
        self.swarm_progress.setValue(0)
        self.swarm_progress.setTextVisible(False)
        card_layout.addWidget(self.ops_swarm)
        card_layout.addWidget(self.ops_swarm_detail)
        card_layout.addWidget(self.swarm_progress)
        operations_layout.addWidget(card)

        card, self.agents_card_layout = self._operation_card("♙  Agentes Ativos", "Estado real do runtime")
        self.ops_agents = QLabel("Nenhum runtime externo confirmado")
        self.ops_agents.setObjectName("Muted")
        self.ops_agents.setWordWrap(True)
        self.agents_card_layout.addWidget(self.ops_agents)
        operations_layout.addWidget(card)

        card, self.integrations_card_layout = self._operation_card("⌁  Integrações", "7 fases operacionais")
        self.ops_integrations = QLabel("0 / 7 READY")
        self.ops_integrations.setObjectName("ReadyBadge")
        self.ops_integrations_detail = QLabel("")
        self.ops_integrations_detail.setObjectName("Muted")
        self.ops_integrations_detail.setWordWrap(True)
        manage = QPushButton("GERENCIAR")
        manage.setObjectName("SecondaryButton")
        manage.clicked.connect(lambda: self._show_page("integrations"))
        self.integrations_card_layout.addWidget(self.ops_integrations)
        self.integrations_card_layout.addWidget(self.ops_integrations_detail)
        self.integrations_card_layout.addWidget(manage)
        operations_layout.addWidget(card)

        map_card = QFrame()
        map_card.setObjectName("WorldCard")
        map_layout = QHBoxLayout(map_card)
        map_layout.setContentsMargins(10, 7, 10, 7)
        msg = QLabel("INTELIGÊNCIA\nSEM FRONTEIRAS")
        msg.setObjectName("WorldLabel")
        map_layout.addWidget(msg)
        mini_eye = HudEyeWidget(compact=True)
        mini_eye.setFixedHeight(62)
        map_layout.addWidget(mini_eye, 1)
        operations_layout.addWidget(map_card)
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
        lines.append("O painel mostra somente retorno real do orquestrador; integrações externas exigem evidência real.")
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
        self.dashboard_output.setPlainText(f"> Missão recebida\n> {request}\n\n> Orquestrador em execução...")
        self.cockpit_tabs.setCurrentWidget(self.dashboard_output)
        self._run_async(partial(self.controller.run_mission, request), self._cockpit_mission_finished, self._cockpit_mission_failed)

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
            self.cockpit_mission.setText(request[:44] + ("…" if len(request) > 44 else ""))
        else:
            self.cockpit_mission.setText("Aguardando")

        ruflo_ready = bool(ruflo.get("operational"))
        self.ops_ruflo.setText("READY" if ruflo_ready else "PENDING")
        self.ops_ruflo.setObjectName("ReadyBadge" if ruflo_ready else "PendingBadge")
        self.ops_ruflo.style().unpolish(self.ops_ruflo)
        self.ops_ruflo.style().polish(self.ops_ruflo)
        self.ops_ruflo_detail.setText(str(ruflo.get("detail", "")))

        adapter = self.controller.ruflo_adapter()
        swarm_ready = bool(adapter.swarm_initialized)
        self.ops_swarm.setText("SWARM CRIADO" if swarm_ready else "NÃO CRIADO")
        self.ops_swarm.setObjectName("ReadyBadge" if swarm_ready else "PendingBadge")
        self.ops_swarm.style().unpolish(self.ops_swarm)
        self.ops_swarm.style().polish(self.ops_swarm)
        self.ops_swarm_detail.setText("Coordenação disponível · runtime externo necessário para atividade real." if swarm_ready else "Abra Ruflo para preparar o swarm.")
        self.swarm_progress.setValue(100 if swarm_ready else 0)
        self.ops_agents.setText("Ruflo coordenador: READY\nAgentes executores: aguardando runtime externo." if swarm_ready else "Nenhum runtime externo confirmado.")

        reports = data.get("integrations", [])
        operational = sum(bool(item.get("operational")) for item in reports)
        self.ops_integrations.setText(f"{operational} / {len(reports)} READY")
        state_lines = []
        for item in reports:
            state = "READY" if item.get("operational") else ("INSTALLED" if item.get("installed") else "PENDING")
            marker = "●" if item.get("operational") else "○"
            state_lines.append(f"{marker} {item.get('name')}: {state}")
        self.ops_integrations_detail.setText("\n".join(state_lines[:7]))

        logs = self.controller.storage.recent_logs(35)
        if logs:
            log_lines = []
            for item in reversed(logs):
                phase = f" [{item.get('phase')}]" if item.get("phase") else ""
                log_lines.append(f"{item.get('created_at', '')}  {item.get('level', ''):<5}  {item.get('source', '')}{phase}  {item.get('message', '')}")
            self.dashboard_logs.setPlainText("\n".join(log_lines))
        else:
            self.dashboard_logs.setPlainText("Nenhum log registrado.")

        if not self.dashboard_output.toPlainText().strip():
            self.dashboard_output.setPlainText(
                "> Olho de Deus inicializado com sucesso.\n"
                "> Cockpit operacional.\n"
                f"> Ruflo: {'READY' if ruflo_ready else 'PENDING'}\n"
                f"> Swarm: {'CRIADO' if swarm_ready else 'NÃO CRIADO'}\n"
                f"> Integrações: {operational}/{len(reports)} READY\n\n"
                "Digite uma missão no Comando Central."
            )
        if self._last_cockpit_result is None and last and last.get("result"):
            self.dashboard_results.setPlainText(json.dumps(last.get("result"), ensure_ascii=False, indent=2, default=str))
        elif self._last_cockpit_result is None:
            self.dashboard_results.setPlainText(f"Missões registradas: {summary.get('missions', 0)}\nAguardando um novo resultado no cockpit.")
