from __future__ import annotations

import json
import math
from functools import partial
from typing import Any

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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


class DigitalEyeWidget(QWidget):
    """Native Qt HUD eye used by the cockpit; no external image dependency."""

    def __init__(self, compact: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.compact = compact
        self.setMinimumSize(120 if compact else 190, 80 if compact else 150)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w * 0.52, h * 0.50
        base = min(w, h)

        glow = QRadialGradient(QPointF(cx, cy), base * 0.45)
        glow.setColorAt(0.0, QColor(0, 218, 255, 95))
        glow.setColorAt(0.35, QColor(0, 126, 255, 35))
        glow.setColorAt(1.0, QColor(0, 20, 40, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glow)
        p.drawEllipse(QPointF(cx, cy), base * 0.44, base * 0.44)

        p.setBrush(Qt.BrushStyle.NoBrush)
        for i, alpha in ((1, 190), (2, 105), (3, 65)):
            r = base * (0.22 + i * 0.065)
            p.setPen(QPen(QColor(34, 201, 255, alpha), 1.2))
            p.drawEllipse(QPointF(cx, cy), r, r)

        eye = QPainterPath()
        eye.moveTo(cx - base * 0.34, cy)
        eye.cubicTo(cx - base * 0.17, cy - base * 0.22, cx + base * 0.17, cy - base * 0.22, cx + base * 0.34, cy)
        eye.cubicTo(cx + base * 0.17, cy + base * 0.22, cx - base * 0.17, cy + base * 0.22, cx - base * 0.34, cy)
        p.setPen(QPen(QColor(66, 220, 255, 230), 2.0))
        p.drawPath(eye)

        iris = QRadialGradient(QPointF(cx, cy), base * 0.14)
        iris.setColorAt(0.0, QColor(225, 252, 255))
        iris.setColorAt(0.2, QColor(0, 229, 255))
        iris.setColorAt(0.62, QColor(0, 104, 220))
        iris.setColorAt(1.0, QColor(1, 21, 42))
        p.setPen(QPen(QColor(71, 229, 255, 230), 1.5))
        p.setBrush(iris)
        p.drawEllipse(QPointF(cx, cy), base * 0.12, base * 0.12)
        p.setBrush(QColor(1, 10, 22))
        p.drawEllipse(QPointF(cx, cy), base * 0.045, base * 0.045)

        p.setPen(QPen(QColor(45, 192, 255, 145), 1.0))
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            r1, r2 = base * 0.34, base * 0.40
            x1, y1 = cx + math.cos(a) * r1, cy + math.sin(a) * r1
            x2, y2 = cx + math.cos(a) * r2, cy + math.sin(a) * r2
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            p.setBrush(QColor(37, 220, 255, 220))
            p.drawEllipse(QPointF(x2, y2), 2.4, 2.4)
        p.end()


class NetworkGlobeWidget(QWidget):
    """Painted globe/network banner matching the selected sci-fi cockpit."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(118)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0.0, QColor(4, 20, 37))
        bg.setColorAt(0.55, QColor(5, 31, 55))
        bg.setColorAt(1.0, QColor(3, 12, 25))
        p.fillRect(self.rect(), bg)

        p.setPen(QPen(QColor(13, 91, 146, 85), 1))
        for y in range(15, h, 22):
            p.drawLine(0, y, w, y)
        for x in range(12, w, 44):
            p.drawLine(x, 0, x + int(h * 0.35), h)

        cx, cy = w * 0.70, h * 0.98
        radius = min(w * 0.37, h * 1.18)
        halo = QRadialGradient(QPointF(cx, cy), radius * 1.15)
        halo.setColorAt(0, QColor(0, 116, 255, 70))
        halo.setColorAt(0.58, QColor(0, 80, 190, 34))
        halo.setColorAt(1, QColor(0, 0, 0, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(halo)
        p.drawEllipse(QPointF(cx, cy), radius * 1.12, radius * 1.12)

        p.setBrush(QColor(3, 29, 58, 235))
        p.setPen(QPen(QColor(19, 141, 245, 185), 1.4))
        p.drawEllipse(QPointF(cx, cy), radius, radius)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(24, 120, 213, 92), 1))
        for scale in (0.34, 0.60, 0.82):
            p.drawEllipse(QPointF(cx, cy), radius * scale, radius)
        for offset in (-0.55, -0.25, 0.0, 0.25, 0.55):
            yy = cy + radius * offset
            half = math.sqrt(max(radius * radius - (yy - cy) ** 2, 0))
            p.drawLine(QPointF(cx - half, yy), QPointF(cx + half, yy))

        nodes = [(-0.61,-0.35),(-0.43,-0.18),(-0.26,-0.48),(-0.06,-0.28),(0.13,-0.47),(0.29,-0.22),(0.47,-0.39),(0.61,-0.14),(-0.30,0.01),(0.03,-0.03),(0.34,0.02)]
        pts = [QPointF(cx + dx * radius, cy + dy * radius) for dx, dy in nodes]
        p.setPen(QPen(QColor(32, 179, 255, 105), 1))
        for a, b in ((0,1),(1,2),(1,3),(2,4),(3,4),(3,8),(4,5),(5,6),(5,9),(6,7),(8,9),(9,10),(7,10)):
            p.drawLine(pts[a], pts[b])
        p.setPen(Qt.PenStyle.NoPen)
        for pt in pts:
            dot = QRadialGradient(pt, 6)
            dot.setColorAt(0, QColor(210, 250, 255, 255))
            dot.setColorAt(0.25, QColor(21, 210, 255, 240))
            dot.setColorAt(1, QColor(0, 80, 180, 0))
            p.setBrush(dot)
            p.drawEllipse(pt, 6, 6)
        p.end()


class CockpitWindow(OlhosDeDeusWindow):
    """High-fidelity Modelo 2 cockpit shell over the existing real controller."""

    def __init__(self, *args, **kwargs) -> None:
        self.ruflo_dock = None
        self._last_cockpit_result: dict[str, Any] | None = None
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Olho de Deus · Cockpit de Inteligência Artificial")
        self.resize(1600, 960)
        self.setMinimumSize(1180, 720)

    def set_ruflo_dock(self, dock) -> None:
        self.ruflo_dock = dock

    @staticmethod
    def _status_chip(text: str, state: str = "Ready") -> QLabel:
        label = QLabel(text)
        label.setObjectName(f"CockpitChip{state}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame(); sidebar.setObjectName("Sidebar"); sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar); layout.setContentsMargins(14,14,14,14); layout.setSpacing(5)
        logo_box = QFrame(); logo_box.setObjectName("SidebarLogoBox")
        logo_layout = QVBoxLayout(logo_box); logo_layout.setContentsMargins(8,6,8,10)
        eye = DigitalEyeWidget(compact=True); eye.setMaximumHeight(108)
        brand = QLabel("OLHO DE DEUS"); brand.setObjectName("Brand"); brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("INTELIGÊNCIA EM AÇÃO"); subtitle.setObjectName("Subtitle"); subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(eye); logo_layout.addWidget(brand); logo_layout.addWidget(subtitle)
        layout.addWidget(logo_box); layout.addSpacing(10)

        def nav(key: str, text: str, callback) -> None:
            button = QPushButton(text); button.setObjectName("NavButton"); button.setCheckable(True)
            button.clicked.connect(callback); self._nav_buttons[key] = button; layout.addWidget(button)

        nav("dashboard", "⌂   Dashboard", lambda: self._show_page("dashboard"))
        nav("missions", "◎   Missões", lambda: self._show_page("missions"))
        nav("integrations", "△   Integrações", lambda: self._show_page("integrations"))
        nav("ruflo", "◉   Ruflo", self._show_ruflo)
        nav("doctor", "⊞   Doctor", lambda: self._show_page("doctor"))
        nav("logs", "▤   Logs", lambda: self._show_page("logs"))
        nav("settings", "⚙   Configurações", lambda: self._show_page("settings"))
        layout.addStretch(1)
        quote = QLabel("“MAIS INTELIGÊNCIA\nPARA UM\nMUNDO MELHOR”"); quote.setObjectName("CockpitQuote"); quote.setWordWrap(True)
        layout.addWidget(quote); layout.addSpacing(8)
        version = QLabel(f"◉  OLHO DE DEUS v{__version__}\nSISTEMA OPERACIONAL DE INTELIGÊNCIA")
        version.setObjectName("SidebarVersion"); version.setWordWrap(True); layout.addWidget(version)
        return sidebar

    def _status_item(self, icon: str, title: str, value: str) -> tuple[QFrame, QLabel]:
        frame = QFrame(); frame.setObjectName("CockpitStatusItem")
        row = QHBoxLayout(frame); row.setContentsMargins(11,7,11,7); row.setSpacing(8)
        icon_label = QLabel(icon); icon_label.setObjectName("StatusIcon"); row.addWidget(icon_label)
        texts = QVBoxLayout(); texts.setContentsMargins(0,0,0,0); texts.setSpacing(1)
        title_label = QLabel(title); title_label.setObjectName("CockpitStatusTitle")
        value_label = QLabel(value); value_label.setObjectName("CockpitStatusValue"); value_label.setWordWrap(False)
        texts.addWidget(title_label); texts.addWidget(value_label); row.addLayout(texts,1)
        return frame, value_label

    def _operation_card(self, title: str, icon: str = "◈") -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame(); frame.setObjectName("OperationCard")
        layout = QVBoxLayout(frame); layout.setContentsMargins(12,10,12,10); layout.setSpacing(6)
        head = QHBoxLayout(); glyph = QLabel(icon); glyph.setObjectName("OperationIcon")
        heading = QLabel(title); heading.setObjectName("OperationTitle"); head.addWidget(glyph); head.addWidget(heading,1); layout.addLayout(head)
        return frame, layout

    @staticmethod
    def _metric_row(items: list[tuple[str, str]]) -> QWidget:
        box = QWidget(); row = QHBoxLayout(box); row.setContentsMargins(0,0,0,0); row.setSpacing(4)
        for title, value in items:
            item = QFrame(); item.setObjectName("MiniMetric")
            lay = QVBoxLayout(item); lay.setContentsMargins(6,4,6,4)
            a = QLabel(title); a.setObjectName("MiniMetricTitle"); b = QLabel(value); b.setObjectName("MiniMetricValue")
            lay.addWidget(a); lay.addWidget(b); row.addWidget(item,1)
        return box

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget(); page.setObjectName("CockpitPage")
        outer = QHBoxLayout(page); outer.setContentsMargins(10,10,10,10); outer.setSpacing(10)
        center = QVBoxLayout(); center.setSpacing(8); outer.addLayout(center,1)

        top = QFrame(); top.setObjectName("CockpitTopBar")
        top_layout = QHBoxLayout(top); top_layout.setContentsMargins(6,5,6,5); top_layout.setSpacing(4)
        item, self.cockpit_system = self._status_item("●","STATUS GERAL","ONLINE"); top_layout.addWidget(item)
        item, self.cockpit_version = self._status_item("◉","VERSÃO",f"v{__version__}"); top_layout.addWidget(item)
        item, self.cockpit_agent = self._status_item("♟","AGENTE ATIVO","Ruflo"); top_layout.addWidget(item)
        item, self.cockpit_mission = self._status_item("◎","MISSÃO ATUAL","Aguardando"); top_layout.addWidget(item,2)
        model = QLabel("MODELO 2 — COCKPIT"); model.setObjectName("CockpitModel"); model.setAlignment(Qt.AlignmentFlag.AlignCenter); top_layout.addWidget(model)
        center.addWidget(top)

        hero = QFrame(); hero.setObjectName("HeroBanner")
        hero_layout = QHBoxLayout(hero); hero_layout.setContentsMargins(0,0,0,0)
        globe = NetworkGlobeWidget(); globe_layer = QHBoxLayout(globe); globe_layer.setContentsMargins(18,10,18,8)
        copy = QVBoxLayout(); copy.addStretch(1)
        hero_title = QLabel("VER MAIS.\nPENSAR MAIS.\nREALIZAR MAIS."); hero_title.setObjectName("HeroTitle"); copy.addWidget(hero_title)
        hero_sub = QLabel("COORDENAR  •  CONECTAR  •  COMPREENDER  •  TRANSFORMAR"); hero_sub.setObjectName("HeroSub"); copy.addWidget(hero_sub); copy.addStretch(1)
        globe_layer.addLayout(copy,1); globe_layer.addStretch(2); hero_layout.addWidget(globe); center.addWidget(hero)

        command = QFrame(); command.setObjectName("CommandCard")
        command_layout = QVBoxLayout(command); command_layout.setContentsMargins(13,10,13,10); command_layout.setSpacing(7)
        command_head = QHBoxLayout(); command_title = QLabel("✣  COMANDO CENTRAL"); command_title.setObjectName("SectionTitle")
        command_meta = QLabel("LINGUAGEM NATURAL   •   MULTIAGENTES   •   RESULTADOS REAIS"); command_meta.setObjectName("CockpitMeta")
        command_head.addWidget(command_title); command_head.addStretch(1); command_head.addWidget(command_meta); command_layout.addLayout(command_head)
        self.quick_mission = QPlainTextEdit(); self.quick_mission.setObjectName("CommandInput"); self.quick_mission.setMaximumHeight(118)
        self.quick_mission.setPlaceholderText("O que você quer que o Olho de Deus faça?"); command_layout.addWidget(self.quick_mission)
        buttons = QHBoxLayout(); buttons.setSpacing(8)
        execute = QPushButton("▶   EXECUTAR"); execute.setObjectName("PrimaryButton"); execute.clicked.connect(self._run_quick_mission)
        plan = QPushButton("▣   PLANEJAR"); plan.setObjectName("SecondaryButton"); plan.clicked.connect(lambda: self._prepare_mission(""))
        research = QPushButton("⌕   PESQUISAR"); research.setObjectName("SecondaryButton"); research.clicked.connect(lambda: self._prepare_mission("Pesquisar e analisar: "))
        create = QPushButton("＋   CRIAR"); create.setObjectName("SecondaryButton"); create.clicked.connect(lambda: self._prepare_mission("Criar: "))
        more = QPushButton("•••"); more.setObjectName("SecondaryButton"); more.setFixedWidth(64); more.clicked.connect(lambda: self._show_page("missions"))
        for btn in (execute,plan,research,create): buttons.addWidget(btn)
        buttons.addStretch(1); buttons.addWidget(more); command_layout.addLayout(buttons); center.addWidget(command)

        response = QFrame(); response.setObjectName("ResponseCard")
        response_layout = QVBoxLayout(response); response_layout.setContentsMargins(12,9,12,9); response_layout.setSpacing(5)
        response_head = QHBoxLayout(); response_title = QLabel(">_  RESPOSTA / EXECUÇÃO"); response_title.setObjectName("SectionTitle")
        self.cockpit_execution_state = QLabel("● PRONTO"); self.cockpit_execution_state.setObjectName("Ready")
        realtime = QLabel("●  EXECUÇÃO EM TEMPO REAL"); realtime.setObjectName("CockpitMetaBright")
        response_head.addWidget(response_title); response_head.addStretch(1); response_head.addWidget(realtime); response_head.addWidget(self.cockpit_execution_state); response_layout.addLayout(response_head)
        self.cockpit_tabs = QTabWidget(); self.cockpit_tabs.setObjectName("CockpitTabs")
        history_panel = QWidget(); history_layout = QHBoxLayout(history_panel); history_layout.setContentsMargins(0,0,0,0)
        self.dashboard_output = QPlainTextEdit(); self.dashboard_output.setReadOnly(True); self.dashboard_output.setObjectName("ConsoleOutput"); history_layout.addWidget(self.dashboard_output,1)
        history_eye = DigitalEyeWidget(); history_eye.setObjectName("ExecutionEye"); history_eye.setMinimumWidth(210); history_eye.setMaximumWidth(275); self.core_animation = history_eye; history_layout.addWidget(history_eye)
        self.dashboard_logs = QPlainTextEdit(); self.dashboard_logs.setReadOnly(True); self.dashboard_logs.setObjectName("ConsoleOutput")
        self.dashboard_results = QPlainTextEdit(); self.dashboard_results.setReadOnly(True); self.dashboard_results.setObjectName("ConsoleOutput")
        self.dashboard_files = QPlainTextEdit(); self.dashboard_files.setReadOnly(True); self.dashboard_files.setObjectName("ConsoleOutput"); self.dashboard_files.setPlainText("Arquivos produzidos por execuções reais aparecerão aqui.")
        self.dashboard_activity = QPlainTextEdit(); self.dashboard_activity.setReadOnly(True); self.dashboard_activity.setObjectName("ConsoleOutput")
        self.dashboard_activity.setPlainText("Atividade dos agentes\n\nO painel mostra estados, evidências e tarefas observáveis. Raciocínio interno privado não é exibido.")
        self.cockpit_tabs.addTab(history_panel,"HISTÓRICO"); self.cockpit_tabs.addTab(self.dashboard_logs,"LOGS"); self.cockpit_tabs.addTab(self.dashboard_results,"RESULTADOS"); self.cockpit_tabs.addTab(self.dashboard_files,"ARQUIVOS"); self.cockpit_tabs.addTab(self.dashboard_activity,"ATIVIDADE DOS AGENTES")
        response_layout.addWidget(self.cockpit_tabs,1)
        bottom_command = QHBoxLayout(); self.followup_input = QLineEdit(); self.followup_input.setObjectName("FollowupInput"); self.followup_input.setPlaceholderText("Digite uma mensagem ou comando..."); self.followup_input.returnPressed.connect(self._run_followup)
        send = QPushButton("➤"); send.setObjectName("SendButton"); send.setFixedWidth(52); send.clicked.connect(self._run_followup)
        bottom_command.addWidget(self.followup_input,1); bottom_command.addWidget(send); response_layout.addLayout(bottom_command); center.addWidget(response,1)

        operations = QFrame(); operations.setObjectName("OperationsPanel"); operations.setFixedWidth(330)
        operations_layout = QVBoxLayout(operations); operations_layout.setContentsMargins(10,10,10,10); operations_layout.setSpacing(7)
        panel_title = QLabel("⌁  PAINEL DE OPERAÇÕES"); panel_title.setObjectName("SectionTitle"); operations_layout.addWidget(panel_title)

        card, card_layout = self._operation_card("Ruflo","♟"); head = QHBoxLayout(); desc = QLabel("Agente principal / Fase 0"); desc.setObjectName("Muted")
        self.ops_ruflo = self._status_chip("VERIFICANDO","Pending"); head.addWidget(desc,1); head.addWidget(self.ops_ruflo); card_layout.addLayout(head)
        self.ops_ruflo_metrics = self._metric_row([("INTELIGÊNCIA","ORQUESTRAÇÃO"),("SWARM","—"),("WORKSPACE","LOCAL")]); card_layout.addWidget(self.ops_ruflo_metrics)
        self.ops_ruflo_detail = QLabel(""); self.ops_ruflo_detail.setObjectName("TinyMuted"); self.ops_ruflo_detail.setWordWrap(True); card_layout.addWidget(self.ops_ruflo_detail)
        open_ruflo = QPushButton("ABRIR CONTROLES RUFLO"); open_ruflo.setObjectName("CompactButton"); open_ruflo.clicked.connect(self._show_ruflo); card_layout.addWidget(open_ruflo); operations_layout.addWidget(card)

        card, card_layout = self._operation_card("Swarm","△"); row = QHBoxLayout(); swarm_desc = QLabel("Equipe de agentes"); swarm_desc.setObjectName("Muted")
        self.ops_swarm = self._status_chip("VERIFICANDO","Pending"); row.addWidget(swarm_desc,1); row.addWidget(self.ops_swarm); card_layout.addLayout(row)
        self.ops_swarm_detail = QLabel("Estado real do workspace Ruflo"); self.ops_swarm_detail.setObjectName("TinyMuted"); self.ops_swarm_detail.setWordWrap(True); card_layout.addWidget(self.ops_swarm_detail)
        self.swarm_progress = QProgressBar(); self.swarm_progress.setObjectName("SwarmProgress"); self.swarm_progress.setTextVisible(False); self.swarm_progress.setRange(0,100); self.swarm_progress.setValue(0); card_layout.addWidget(self.swarm_progress)
        self.ops_swarm_metrics = QLabel("AGENTES: runtime externo não confirmado"); self.ops_swarm_metrics.setObjectName("MiniInfo"); card_layout.addWidget(self.ops_swarm_metrics); operations_layout.addWidget(card)

        card, card_layout = self._operation_card("Agentes Ativos","◎"); self.ops_agents = QVBoxLayout(); card_layout.addLayout(self.ops_agents); self.agent_labels = {}
        for name in ("Ruflo coord.","Planner","Router","Guardian QA","Runtime externo"):
            row = QHBoxLayout(); dot = QLabel("●"); dot.setObjectName("AgentDot"); name_label = QLabel(name); name_label.setObjectName("AgentName"); state = self._status_chip("PENDING","Pending")
            row.addWidget(dot); row.addWidget(name_label,1); row.addWidget(state); self.agent_labels[name] = state; self.ops_agents.addLayout(row)
        operations_layout.addWidget(card)

        card, card_layout = self._operation_card("Integrações","⊞"); self.ops_integrations = QLabel("0 / 7 READY"); self.ops_integrations.setObjectName("Ready"); card_layout.addWidget(self.ops_integrations)
        self.ops_integrations_detail = QVBoxLayout(); self.integration_rows = {}
        for name in ("Graphify","ComfyUI","Spec Kit","QA Skills","Output Profile","Agency Agents","Artemis"):
            row = QHBoxLayout(); nm = QLabel(name); nm.setObjectName("IntegrationName"); st = self._status_chip("PENDING","Pending"); row.addWidget(nm,1); row.addWidget(st); self.ops_integrations_detail.addLayout(row); self.integration_rows[name] = st
        card_layout.addLayout(self.ops_integrations_detail)
        manage = QPushButton("GERENCIAR INTEGRAÇÕES"); manage.setObjectName("CompactButton"); manage.clicked.connect(lambda: self._show_page("integrations")); card_layout.addWidget(manage); operations_layout.addWidget(card,1)

        world = QFrame(); world.setObjectName("WorldFooterCard"); world_lay = QHBoxLayout(world); world_lay.setContentsMargins(10,7,10,7)
        text = QLabel("INTELIGÊNCIA\nSEM FRONTEIRAS"); text.setObjectName("WorldFooterText"); mini_eye = DigitalEyeWidget(compact=True); mini_eye.setMaximumHeight(68)
        world_lay.addWidget(text); world_lay.addWidget(mini_eye,1); operations_layout.addWidget(world)
        outer.addWidget(operations); return page

    def _run_followup(self) -> None:
        text = self.followup_input.text().strip()
        if not text: return
        self.quick_mission.setPlainText(text); self.followup_input.clear(); self._run_quick_mission()

    def _show_ruflo(self) -> None:
        self._select_nav("ruflo")
        if self.ruflo_dock is None:
            self.statusBar().showMessage("Painel Ruflo ainda não foi anexado à janela",5000); return
        self.ruflo_dock.show(); self.ruflo_dock.raise_(); widget = self.ruflo_dock.widget()
        if widget is not None and hasattr(widget,"refresh_status"): widget.refresh_status()

    def _prepare_mission(self, prefix: str) -> None:
        text = self.quick_mission.toPlainText().strip()
        if prefix and not text: text = prefix.rstrip()
        elif prefix and text: text = prefix + text
        self.mission_input.setPlainText(text); self._show_page("missions"); self.mission_input.setFocus()

    def _format_mission_result(self, result: dict[str, Any]) -> str:
        mission = result.get("mission",{}) if isinstance(result,dict) else {}
        lines = [f"> EXECUTION ID   {result.get('execution_id','-')}",f"> DURAÇÃO        {result.get('duration_ms',0)} ms",f"> STATUS          {mission.get('status','-')}",""]
        for step in mission.get("steps",[]):
            status = str(step.get("status","")).upper(); lines.append(f"[{status:<8}]  {step.get('name','')}  ·  {step.get('capability','')}")
            for evidence in step.get("evidence",[]) or []: lines.append(f"             ↳ {evidence}")
            if step.get("error"): lines.append(f"             ERRO: {step['error']}")
        lines.extend(["","Retorno fiel do orquestrador. Integrações externas só contam como executadas quando produzem evidência real."])
        return "\n".join(lines)

    def _run_quick_mission(self) -> None:
        request = self.quick_mission.toPlainText().strip()
        if not request:
            QMessageBox.information(self,"Comando central","Digite uma missão antes de executar."); return
        self.mission_input.setPlainText(request); self.cockpit_execution_state.setText("● EXECUTANDO"); self.cockpit_execution_state.setObjectName("Pending")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state); self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.dashboard_output.setPlainText(f"> Missão recebida\n> {request}\n\n> Orquestrador em execução...")
        self.dashboard_activity.setPlainText("Atividade observável\n\nRuflo / Planner / Router serão atualizados conforme o fluxo real retornar evidências.")
        self.cockpit_tabs.setCurrentIndex(0); self._run_async(partial(self.controller.run_mission,request),self._cockpit_mission_finished,self._cockpit_mission_failed)

    def _cockpit_mission_finished(self, result: object) -> None:
        payload = result if isinstance(result,dict) else {"result":result}; self._last_cockpit_result = payload; pretty = self._format_mission_result(payload)
        self.dashboard_output.setPlainText(pretty); self.dashboard_results.setPlainText(json.dumps(payload,ensure_ascii=False,indent=2,default=str)); self.mission_result.setPlainText(json.dumps(payload,ensure_ascii=False,indent=2,default=str))
        self.mission_status.setText("CONCLUÍDA"); self.mission_status.setObjectName("Ready"); self.cockpit_execution_state.setText("● CONCLUÍDO"); self.cockpit_execution_state.setObjectName("Ready")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state); self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.dashboard_activity.setPlainText(self._format_agent_activity(payload)); self._refresh_dashboard(); self._refresh_logs()

    def _format_agent_activity(self, payload: dict[str, Any]) -> str:
        mission = payload.get("mission",{}) if isinstance(payload,dict) else {}; lines = ["ATIVIDADE OBSERVÁVEL DOS AGENTES",""]
        for step in mission.get("steps",[]): lines.append(f"{step.get('capability','NÚCLEO')}: {step.get('name','etapa')} → {str(step.get('status','')).upper()}")
        lines.extend(["","Este painel exibe atividade, estado e evidências observáveis.","Raciocínio interno privado não é exibido."]); return "\n".join(lines)

    def _cockpit_mission_failed(self, message: str) -> None:
        self.dashboard_output.setPlainText(f"FALHA NA EXECUÇÃO\n\n{message}"); self.dashboard_results.setPlainText(message); self.mission_result.setPlainText(message)
        self.mission_status.setText("FALHOU"); self.mission_status.setObjectName("Error"); self.cockpit_execution_state.setText("● ERRO"); self.cockpit_execution_state.setObjectName("Error")
        self.cockpit_execution_state.style().unpolish(self.cockpit_execution_state); self.cockpit_execution_state.style().polish(self.cockpit_execution_state)
        self.dashboard_activity.setPlainText(f"Execução interrompida.\n\n{message}"); self._refresh_dashboard()

    @staticmethod
    def _set_chip(label: QLabel, text: str, state: str) -> None:
        label.setText(text); label.setObjectName(f"CockpitChip{state}"); label.style().unpolish(label); label.style().polish(label)

    def _refresh_dashboard(self) -> None:
        data = self.controller.dashboard(); ruflo = data.get("ruflo",{}); summary = data.get("summary",{}); last = data.get("last_mission")
        self.cockpit_system.setText("ONLINE"); self.cockpit_version.setText(f"v{data.get('version',__version__)}"); self.cockpit_agent.setText("Ruflo" if ruflo.get("operational") else "Núcleo local")
        if last:
            request = str(last.get("request","Última missão")); self.cockpit_mission.setText(request[:46] + ("…" if len(request)>46 else ""))
        else: self.cockpit_mission.setText("Aguardando")
        ruflo_ready = bool(ruflo.get("operational")); self._set_chip(self.ops_ruflo,"READY" if ruflo_ready else "PENDING","Ready" if ruflo_ready else "Pending")
        detail = str(ruflo.get("detail","")); self.ops_ruflo_detail.setText(detail[:115] + ("…" if len(detail)>115 else ""))
        adapter = self.controller.ruflo_adapter(); swarm_ready = bool(adapter.swarm_initialized)
        self._set_chip(self.ops_swarm,"CRIADO" if swarm_ready else "PENDING","Ready" if swarm_ready else "Pending")
        self.ops_swarm_detail.setText("Coordenação disponível. Execução autônoma real depende do runtime de agente." if swarm_ready else "Abra Ruflo para preparar o swarm.")
        self.swarm_progress.setValue(100 if swarm_ready else 0); self.ops_swarm_metrics.setText("ESTADO: swarm preparado · runtime externo: não confirmado" if swarm_ready else "ESTADO: aguardando configuração")
        self._set_chip(self.agent_labels["Ruflo coord."],"READY" if ruflo_ready else "PENDING","Ready" if ruflo_ready else "Pending")
        for local in ("Planner","Router","Guardian QA"): self._set_chip(self.agent_labels[local],"READY","Ready")
        self._set_chip(self.agent_labels["Runtime externo"],"PENDING","Pending")
        reports = data.get("integrations",[]); operational = sum(bool(item.get("operational")) for item in reports); self.ops_integrations.setText(f"{operational} / {len(reports)} READY")
        aliases = {"graphify":"Graphify","comfyui":"ComfyUI","spec-kit":"Spec Kit","qa-skills":"QA Skills","i-have-adhd":"Output Profile","agency-agents":"Agency Agents","artemis":"Artemis"}
        for item in reports:
            key = str(item.get("key") or item.get("slug") or "").lower(); display = aliases.get(key)
            if display is None:
                raw = str(item.get("name","")); display = aliases.get(raw.lower(), next((v for v in aliases.values() if v.lower()==raw.lower()),raw))
            target = self.integration_rows.get(display)
            if target is None: continue
            if item.get("operational"): state, style = "READY", "Ready"
            elif item.get("installed"): state, style = "INSTALLED", "Info"
            else: state, style = "PENDING", "Pending"
            self._set_chip(target,state,style)
        logs = self.controller.storage.recent_logs(45)
        if logs:
            log_lines = []
            for item in reversed(logs):
                phase = f" [{item.get('phase')}]" if item.get("phase") else ""; log_lines.append(f"{item.get('created_at','')}  {item.get('level',''):<7}  {item.get('source','')}{phase}  {item.get('message','')}")
            self.dashboard_logs.setPlainText("\n".join(log_lines))
        else: self.dashboard_logs.setPlainText("Nenhum log registrado.")
        if not self.dashboard_output.toPlainText().strip():
            self.dashboard_output.setPlainText("> Olho de Deus inicializado com sucesso.\n> Cockpit Modelo 2 ativo.\n" + f"> Ruflo: {'READY' if ruflo_ready else 'PENDING'}\n> Swarm: {'CRIADO' if swarm_ready else 'NÃO CRIADO'}\n> Integrações: {operational}/{len(reports)} READY\n\nDigite uma missão no Comando Central.")
        if self._last_cockpit_result is None and last and last.get("result"):
            self.dashboard_results.setPlainText(json.dumps(last.get("result"),ensure_ascii=False,indent=2,default=str))
        elif self._last_cockpit_result is None:
            self.dashboard_results.setPlainText(f"Missões registradas: {summary.get('missions',0)}\nAguardando um novo resultado no cockpit.")
