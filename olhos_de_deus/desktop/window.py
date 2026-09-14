from __future__ import annotations

import json
from functools import partial
from pathlib import Path
from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .controller import DesktopController
from .widgets import AnimatedCoreWidget, IntegrationCard, StatCard


PHASE_TITLES = {
    "graphify": "GRAPHIFY · Inteligência estrutural",
    "comfyui": "COMFYUI · Workflows visuais",
    "spec-kit": "SPEC KIT · Planejamento por especificação",
    "qa-skills": "QA GUARDIAN · Skills de qualidade",
    "i-have-adhd": "OUTPUT PROFILE · Comunicação operacional",
    "agency-agents": "AGENCY AGENTS · Equipe especializada",
    "artemis": "ARTEMIS · Operador Android",
}


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    finished = Signal()


class FunctionWorker(QRunnable):
    def __init__(self, function: Callable[[], Any]) -> None:
        super().__init__()
        self.function = function
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = self.function()
        except Exception as exc:  # UI boundary: surface cleanly instead of crashing Qt
            self.signals.error.emit(f"{type(exc).__name__}: {exc}")
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class OlhosDeDeusWindow(QMainWindow):
    def __init__(self, controller: DesktopController, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.thread_pool = QThreadPool.globalInstance()
        self.setWindowTitle("Olhos de Deus · Central de Inteligência Artificial")
        self.resize(1360, 840)
        self.setMinimumSize(1040, 680)
        self._tray_available = False
        self._current_integration = "graphify"
        self._integration_inputs: dict[str, QWidget] = {}
        self._nav_buttons: dict[str, QPushButton] = {}

        self._build_shell()
        self._refresh_all()

    def set_tray_available(self, available: bool) -> None:
        self._tray_available = bool(available)

    def changeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().changeEvent(event)
        if self._tray_available and self.isMinimized():
            QTimer.singleShot(0, self.hide)

    def _build_shell(self) -> None:
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())
        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)

        self.dashboard_page = self._build_dashboard_page()
        self.missions_page = self._build_missions_page()
        self.integrations_page = self._build_integrations_page()
        self.integration_page = self._build_integration_detail_page()
        self.doctor_page = self._build_doctor_page()
        self.logs_page = self._build_logs_page()
        self.settings_page = self._build_settings_page()

        for page in (
            self.dashboard_page,
            self.missions_page,
            self.integrations_page,
            self.integration_page,
            self.doctor_page,
            self.logs_page,
            self.settings_page,
        ):
            self.stack.addWidget(page)

        self.setCentralWidget(root)
        self.statusBar().showMessage("Núcleo pronto")

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(235)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(5)

        brand = QLabel("OLHOS DE DEUS")
        brand.setObjectName("Brand")
        subtitle = QLabel("CENTRAL DE INTELIGÊNCIA\nARTIFICIAL")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        def nav(key: str, text: str, callback: Callable[[], None]) -> None:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.clicked.connect(callback)
            self._nav_buttons[key] = button
            layout.addWidget(button)

        nav("dashboard", "Dashboard", lambda: self._show_page("dashboard"))
        nav("missions", "Missões", lambda: self._show_page("missions"))
        nav("integrations", "Integrações", lambda: self._show_page("integrations"))
        layout.addSpacing(8)
        nav("graphify", "01  Graphify", lambda: self._show_integration("graphify"))
        nav("comfyui", "02  ComfyUI", lambda: self._show_integration("comfyui"))
        nav("spec-kit", "03  Spec Kit", lambda: self._show_integration("spec-kit"))
        nav("qa-skills", "04  QA Guardian", lambda: self._show_integration("qa-skills"))
        nav("i-have-adhd", "05  Output Profile", lambda: self._show_integration("i-have-adhd"))
        nav("agency-agents", "06  Agents", lambda: self._show_integration("agency-agents"))
        nav("artemis", "07  Artemis Android", lambda: self._show_integration("artemis"))
        layout.addSpacing(8)
        nav("doctor", "System Doctor", lambda: self._show_page("doctor"))
        nav("logs", "Logs", lambda: self._show_page("logs"))
        nav("settings", "Configurações", lambda: self._show_page("settings"))
        layout.addStretch(1)

        version = QLabel("Windows Desktop")
        version.setObjectName("Muted")
        layout.addWidget(version)
        return sidebar

    @staticmethod
    def _page_container() -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)
        return page, layout

    @staticmethod
    def _title(text: str, subtitle: str | None = None) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        heading = QLabel(text)
        heading.setObjectName("PageTitle")
        layout.addWidget(heading)
        if subtitle:
            detail = QLabel(subtitle)
            detail.setObjectName("Muted")
            detail.setWordWrap(True)
            layout.addWidget(detail)
        return container

    def _build_dashboard_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("OLHOS DE DEUS", "Central de Inteligência e Orquestração"))

        metrics = QGridLayout()
        self.card_system = StatCard("SISTEMA", "ONLINE", "Núcleo carregado")
        self.card_integrations = StatCard("INTEGRAÇÕES", "0 / 7", "Aguardando diagnóstico")
        self.card_missions = StatCard("MISSÕES", "0", "Nenhuma missão registrada")
        self.card_qa = StatCard("QA", "ATIVO", "Guardian QA disponível")
        metrics.addWidget(self.card_system, 0, 0)
        metrics.addWidget(self.card_integrations, 0, 1)
        metrics.addWidget(self.card_missions, 0, 2)
        metrics.addWidget(self.card_qa, 0, 3)
        layout.addLayout(metrics)

        self.core_animation = AnimatedCoreWidget()
        layout.addWidget(self.core_animation, 1)

        command_card = QFrame()
        command_card.setObjectName("Card")
        command_layout = QHBoxLayout(command_card)
        self.quick_mission = QLineEdit()
        self.quick_mission.setPlaceholderText("O que você quer que o Olhos de Deus faça?")
        self.quick_mission.returnPressed.connect(self._run_quick_mission)
        execute = QPushButton("EXECUTAR MISSÃO")
        execute.setObjectName("PrimaryButton")
        execute.clicked.connect(self._run_quick_mission)
        command_layout.addWidget(self.quick_mission, 1)
        command_layout.addWidget(execute)
        layout.addWidget(command_card)
        return page

    def _build_missions_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("MISSÕES", "Planejamento, roteamento e validação pelo orquestrador central."))
        self.mission_input = QPlainTextEdit()
        self.mission_input.setPlaceholderText("Digite uma missão para o Olhos de Deus...")
        self.mission_input.setMaximumHeight(130)
        layout.addWidget(self.mission_input)

        actions = QHBoxLayout()
        run = QPushButton("EXECUTAR MISSÃO")
        run.setObjectName("PrimaryButton")
        run.clicked.connect(self._run_mission_page)
        self.mission_status = QLabel("AGUARDANDO")
        self.mission_status.setObjectName("Pending")
        actions.addWidget(run)
        actions.addWidget(self.mission_status)
        actions.addStretch(1)
        layout.addLayout(actions)

        self.mission_result = QPlainTextEdit()
        self.mission_result.setReadOnly(True)
        self.mission_result.setPlaceholderText("O resultado e as evidências da missão aparecerão aqui.")
        layout.addWidget(self.mission_result, 1)
        return page

    def _build_integrations_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("INTEGRAÇÕES", "Estado real das sete fases e bootstrap dos projetos externos."))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QGridLayout(content)
        grid.setSpacing(12)
        self.integration_cards: dict[str, IntegrationCard] = {}
        for index, (name, title) in enumerate(PHASE_TITLES.items()):
            card = IntegrationCard(name, title)
            card.action_requested.connect(self._show_integration)
            self.integration_cards[name] = card
            grid.addWidget(card, index // 2, index % 2)
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        actions = QHBoxLayout()
        plan = QPushButton("PLANEJAR BOOTSTRAP")
        plan.setObjectName("SecondaryButton")
        plan.clicked.connect(lambda: self._bootstrap_all(True))
        install = QPushButton("INSTALAR / ATUALIZAR TODOS")
        install.setObjectName("PrimaryButton")
        install.clicked.connect(lambda: self._bootstrap_all(False))
        actions.addWidget(plan)
        actions.addWidget(install)
        actions.addStretch(1)
        layout.addLayout(actions)
        return page

    def _build_integration_detail_page(self) -> QWidget:
        page, layout = self._page_container()
        self.integration_title = self._title(PHASE_TITLES["graphify"], "Fase independente com isolamento de falhas.")
        layout.addWidget(self.integration_title)

        status_card = QFrame()
        status_card.setObjectName("Card")
        status_layout = QHBoxLayout(status_card)
        self.integration_status = QLabel("PENDING")
        self.integration_status.setObjectName("Pending")
        self.integration_detail = QLabel("Aguardando verificação")
        self.integration_detail.setObjectName("Muted")
        self.integration_detail.setWordWrap(True)
        status_layout.addWidget(self.integration_status)
        status_layout.addWidget(self.integration_detail, 1)
        layout.addWidget(status_card)

        self.integration_form_holder = QVBoxLayout()
        layout.addLayout(self.integration_form_holder)

        action_row = QHBoxLayout()
        check = QPushButton("VERIFICAR / PREVIEW")
        check.setObjectName("SecondaryButton")
        check.clicked.connect(lambda: self._run_integration(False))
        self.integration_execute = QPushButton("EXECUTAR REAL")
        self.integration_execute.setObjectName("PrimaryButton")
        self.integration_execute.clicked.connect(lambda: self._run_integration(True))
        action_row.addWidget(check)
        action_row.addWidget(self.integration_execute)
        action_row.addStretch(1)
        layout.addLayout(action_row)

        self.integration_output = QPlainTextEdit()
        self.integration_output.setReadOnly(True)
        layout.addWidget(self.integration_output, 1)
        self._rebuild_integration_form("graphify")
        return page

    def _build_doctor_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("SYSTEM DOCTOR", "Diagnóstico das sete integrações sem esconder dependências ausentes."))
        controls = QHBoxLayout()
        run = QPushButton("EXECUTAR DIAGNÓSTICO")
        run.setObjectName("PrimaryButton")
        run.clicked.connect(lambda: self._run_doctor(False))
        probe = QPushButton("TESTAR SERVIÇOS EXTERNOS")
        probe.setObjectName("SecondaryButton")
        probe.clicked.connect(lambda: self._run_doctor(True))
        controls.addWidget(run)
        controls.addWidget(probe)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.doctor_table = QTableWidget(0, 5)
        self.doctor_table.setHorizontalHeaderLabels(["Fase", "Integração", "Modo", "Estado", "Detalhe"])
        self.doctor_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.doctor_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.doctor_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.doctor_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.doctor_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        layout.addWidget(self.doctor_table, 1)
        return page

    def _build_logs_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("LOGS", "Histórico local de missões, fases, diagnósticos e erros."))
        controls = QHBoxLayout()
        refresh = QPushButton("ATUALIZAR")
        refresh.setObjectName("SecondaryButton")
        refresh.clicked.connect(self._refresh_logs)
        self.log_filter = QLineEdit()
        self.log_filter.setPlaceholderText("Filtrar por texto...")
        self.log_filter.textChanged.connect(self._refresh_logs)
        controls.addWidget(refresh)
        controls.addWidget(self.log_filter, 1)
        layout.addLayout(controls)

        self.logs_table = QTableWidget(0, 5)
        self.logs_table.setHorizontalHeaderLabels(["Data/Hora", "Nível", "Origem", "Fase", "Mensagem"])
        self.logs_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        layout.addWidget(self.logs_table, 1)
        return page

    def _build_settings_page(self) -> QWidget:
        page, layout = self._page_container()
        layout.addWidget(self._title("CONFIGURAÇÕES", "Somente preferências não sensíveis são salvas no banco local."))
        form_card = QFrame()
        form_card.setObjectName("Card")
        form = QFormLayout(form_card)
        self.settings_external = QLineEdit()
        self.settings_comfyui = QLineEdit()
        self.settings_dry_run = QCheckBox("Usar dry-run por padrão")
        form.addRow("EXTERNAL_ROOT", self.settings_external)
        form.addRow("COMFYUI_URL", self.settings_comfyui)
        form.addRow("SEGURANÇA", self.settings_dry_run)
        layout.addWidget(form_card)
        save = QPushButton("SALVAR CONFIGURAÇÕES")
        save.setObjectName("PrimaryButton")
        save.clicked.connect(self._save_settings)
        layout.addWidget(save, 0, Qt.AlignLeft)
        self.settings_note = QLabel("")
        self.settings_note.setObjectName("Muted")
        layout.addWidget(self.settings_note)
        layout.addStretch(1)
        return page

    def _show_page(self, name: str) -> None:
        mapping = {
            "dashboard": self.dashboard_page,
            "missions": self.missions_page,
            "integrations": self.integrations_page,
            "doctor": self.doctor_page,
            "logs": self.logs_page,
            "settings": self.settings_page,
        }
        page = mapping[name]
        self.stack.setCurrentWidget(page)
        self._select_nav(name)
        if name == "dashboard":
            self._refresh_dashboard()
        elif name == "integrations":
            self._refresh_integrations()
        elif name == "doctor":
            self._populate_doctor(self.controller.doctor(probe_services=False))
        elif name == "logs":
            self._refresh_logs()
        elif name == "settings":
            self._load_settings()

    def _select_nav(self, key: str) -> None:
        for name, button in self._nav_buttons.items():
            button.setChecked(name == key)

    def _show_integration(self, name: str) -> None:
        self._current_integration = name
        self.stack.setCurrentWidget(self.integration_page)
        self._select_nav(name)
        title_widget = self.integration_title.layout().itemAt(0).widget()
        title_widget.setText(PHASE_TITLES[name])
        self.integration_output.clear()
        self._rebuild_integration_form(name)
        self._refresh_integration_status(name)

    def _rebuild_integration_form(self, name: str) -> None:
        while self.integration_form_holder.count():
            item = self.integration_form_holder.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        card = QFrame()
        card.setObjectName("Card")
        form = QFormLayout(card)
        self._integration_inputs = {}

        if name == "graphify":
            target = QLineEdit(".")
            form.addRow("Diretório / projeto", target)
            self._integration_inputs["target"] = target
        elif name == "comfyui":
            workflow = QLineEdit()
            workflow.setPlaceholderText("Selecione um workflow JSON da API do ComfyUI")
            browse = QPushButton("ARQUIVO...")
            browse.setObjectName("SecondaryButton")
            browse.clicked.connect(lambda: self._browse_file(workflow, "JSON (*.json)"))
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.addWidget(workflow, 1)
            row_layout.addWidget(browse)
            form.addRow("Workflow", row)
            self._integration_inputs["workflow_path"] = workflow
        elif name == "spec-kit":
            target = QLineEdit(".")
            integration = QComboBox()
            integration.addItems(["copilot", "codex", "claude", "gemini"])
            form.addRow("Diretório do projeto", target)
            form.addRow("Integração", integration)
            self._integration_inputs["target"] = target
            self._integration_inputs["integration"] = integration
        elif name == "qa-skills":
            skill = QLineEdit()
            skill.setPlaceholderText("Vazio = listar todas; ex.: unit-testing")
            form.addRow("Skill", skill)
            self._integration_inputs["skill"] = skill
        elif name == "i-have-adhd":
            note = QLabel("Carrega as regras oficiais do perfil operacional. Nenhum comando externo é executado.")
            note.setObjectName("Muted")
            note.setWordWrap(True)
            form.addRow(note)
        elif name == "agency-agents":
            query = QLineEdit()
            query.setPlaceholderText("Vazio = listar catálogo; ex.: backend")
            form.addRow("Buscar agente", query)
            self._integration_inputs["query"] = query
        elif name == "artemis":
            task = QLineEdit("Open Settings and report battery level")
            profile = QComboBox()
            profile.addItems(["flash", "pro"])
            form.addRow("Tarefa Android", task)
            form.addRow("Perfil", profile)
            self._integration_inputs["task"] = task
            self._integration_inputs["profile"] = profile

        self.integration_form_holder.addWidget(card)
        self.integration_execute.setEnabled(name in {"graphify", "comfyui", "spec-kit", "artemis"})

    @staticmethod
    def _browse_file(target: QLineEdit, filter_text: str) -> None:
        path, _ = QFileDialog.getOpenFileName(None, "Selecionar arquivo", "", filter_text)
        if path:
            target.setText(path)

    def _integration_kwargs(self) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for key, widget in self._integration_inputs.items():
            if isinstance(widget, QLineEdit):
                values[key] = widget.text()
            elif isinstance(widget, QComboBox):
                values[key] = widget.currentText()
        if self._current_integration == "comfyui" and not values.get("workflow_path"):
            values["probe"] = True
        return values

    def _run_integration(self, execute: bool) -> None:
        name = self._current_integration
        kwargs = self._integration_kwargs()
        if execute:
            if name == "comfyui" and not str(kwargs.get("workflow_path", "")).strip():
                QMessageBox.information(self, "ComfyUI", "Selecione um workflow JSON antes da execução real.")
                return
            answer = QMessageBox.question(
                self,
                "Confirmar execução real",
                f"Executar a fase {PHASE_TITLES[name]} fora do modo dry-run?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return

        self.integration_output.setPlainText("Executando..." if execute else "Verificando...")
        self.core_animation.set_activity("working")
        self._run_async(
            partial(self.controller.run_phase, name, execute=execute, **kwargs),
            self._integration_result,
            self._integration_error,
        )

    def _integration_result(self, result: object) -> None:
        self.integration_output.setPlainText(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        self.core_animation.set_activity("success")
        self._refresh_integration_status(self._current_integration)
        self._refresh_dashboard()
        self._refresh_logs()

    def _integration_error(self, message: str) -> None:
        self.integration_output.setPlainText(message)
        self.core_animation.set_activity("error")
        self.statusBar().showMessage(message, 8000)

    def _refresh_integration_status(self, name: str) -> None:
        report = self.controller.integration_hub().adapter(name).report(probe_services=False).to_dict()
        if report["operational"]:
            text, object_name = "READY", "Ready"
        elif report["installed"]:
            text, object_name = "INSTALLED", "Pending"
        else:
            text, object_name = "PENDING", "Error"
        self.integration_status.setText(text)
        self.integration_status.setObjectName(object_name)
        self.integration_status.style().unpolish(self.integration_status)
        self.integration_status.style().polish(self.integration_status)
        self.integration_detail.setText(report["detail"])

    def _run_quick_mission(self) -> None:
        text = self.quick_mission.text().strip()
        if not text:
            return
        self.mission_input.setPlainText(text)
        self._show_page("missions")
        self._run_mission_page()

    def _run_mission_page(self) -> None:
        request = self.mission_input.toPlainText().strip()
        if not request:
            QMessageBox.information(self, "Missões", "Digite uma missão antes de executar.")
            return
        self.mission_status.setText("EXECUTANDO")
        self.mission_status.setObjectName("Pending")
        self.mission_result.setPlainText("ORCHESTRATOR recebeu a missão. Processando...")
        self.core_animation.set_activity("working")
        self._run_async(partial(self.controller.run_mission, request), self._mission_finished, self._mission_failed)

    def _mission_finished(self, result: object) -> None:
        self.mission_status.setText("CONCLUÍDA")
        self.mission_status.setObjectName("Ready")
        self.mission_status.style().unpolish(self.mission_status)
        self.mission_status.style().polish(self.mission_status)
        self.mission_result.setPlainText(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        self.core_animation.set_activity("success")
        self._refresh_dashboard()
        self._refresh_logs()

    def _mission_failed(self, message: str) -> None:
        self.mission_status.setText("FALHOU")
        self.mission_status.setObjectName("Error")
        self.mission_status.style().unpolish(self.mission_status)
        self.mission_status.style().polish(self.mission_status)
        self.mission_result.setPlainText(message)
        self.core_animation.set_activity("error")

    def _bootstrap_all(self, dry_run: bool) -> None:
        if not dry_run:
            answer = QMessageBox.question(
                self,
                "Instalar / atualizar integrações",
                "Isso executará git clone/pull para as sete fontes em EXTERNAL_ROOT. Continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return
        self.core_animation.set_activity("working")
        self._run_async(
            partial(self.controller.bootstrap, None, dry_run=dry_run),
            lambda result: self._bootstrap_result(result, dry_run),
            self._integration_error,
        )

    def _bootstrap_result(self, result: object, dry_run: bool) -> None:
        self.core_animation.set_activity("success")
        self.statusBar().showMessage("Bootstrap planejado" if dry_run else "Bootstrap concluído", 6000)
        QMessageBox.information(
            self,
            "Bootstrap",
            ("Plano gerado sem alterações.\n\n" if dry_run else "Operação concluída.\n\n")
            + json.dumps(result, ensure_ascii=False, indent=2, default=str)[:5000],
        )
        self._refresh_all()

    def _run_doctor(self, probe_services: bool) -> None:
        self.statusBar().showMessage("Executando System Doctor...")
        self._run_async(
            partial(self.controller.doctor, probe_services=probe_services),
            self._doctor_result,
            lambda message: self.statusBar().showMessage(message, 8000),
        )

    def _doctor_result(self, result: object) -> None:
        self._populate_doctor(result if isinstance(result, list) else [])
        self._refresh_integrations()
        self._refresh_dashboard()
        self.statusBar().showMessage("System Doctor concluído", 5000)

    def _populate_doctor(self, reports: list[dict[str, Any]]) -> None:
        self.doctor_table.setRowCount(len(reports))
        for row, report in enumerate(reports):
            if report.get("operational"):
                state = "READY"
            elif report.get("installed"):
                state = "INSTALLED"
            else:
                state = "PENDING"
            values = [report.get("phase"), report.get("name"), report.get("mode"), state, report.get("detail")]
            for column, value in enumerate(values):
                self.doctor_table.setItem(row, column, QTableWidgetItem(str(value)))

    def _refresh_dashboard(self) -> None:
        data = self.controller.dashboard()
        self.card_system.set_value("ONLINE", f"v{data['version']} · dados em {data['data_root']}")
        self.card_integrations.set_value(
            f"{data['operational']} / {data['total_integrations']}",
            f"{data['installed']} repositórios detectados",
        )
        summary = data["summary"]
        last = data.get("last_mission")
        last_text = "Nenhuma missão registrada"
        if last:
            last_text = f"Última: {last['status']} · {last.get('duration_ms') or 0} ms"
        self.card_missions.set_value(str(summary["missions"]), last_text)
        self.card_qa.set_value("ATIVO", "Gate Guardian QA carregado")

    def _refresh_integrations(self) -> None:
        reports = self.controller.dashboard()["integrations"]
        for report in reports:
            card = self.integration_cards.get(report["name"])
            if card:
                card.update_report(report)

    def _refresh_logs(self) -> None:
        logs = self.controller.storage.recent_logs(400)
        needle = self.log_filter.text().casefold().strip() if hasattr(self, "log_filter") else ""
        if needle:
            logs = [
                item for item in logs
                if needle in " ".join(str(item.get(key, "")) for key in ("level", "source", "phase", "message")).casefold()
            ]
        self.logs_table.setRowCount(len(logs))
        for row, item in enumerate(logs):
            values = [item["created_at"], item["level"], item["source"], item.get("phase") or "", item["message"]]
            for column, value in enumerate(values):
                self.logs_table.setItem(row, column, QTableWidgetItem(str(value)))

    def _load_settings(self) -> None:
        self.settings_external.setText(str(self.controller.external_root))
        self.settings_comfyui.setText(self.controller.comfyui_url)
        self.settings_dry_run.setChecked(bool(self.controller.storage.get_setting("dry_run_default", True)))
        self.settings_note.setText(f"Dados locais: {self.controller.paths.root}")

    def _save_settings(self) -> None:
        try:
            settings = self.controller.save_settings(
                external_root=self.settings_external.text(),
                comfyui_url=self.settings_comfyui.text(),
                dry_run_default=self.settings_dry_run.isChecked(),
            )
        except Exception as exc:
            QMessageBox.warning(self, "Configurações", str(exc))
            return
        self.settings_note.setText("Configurações salvas: " + json.dumps(settings, ensure_ascii=False))
        self._refresh_all()

    def _refresh_all(self) -> None:
        self._refresh_dashboard()
        self._refresh_integrations()
        self._refresh_logs()
        self._load_settings()
        reports = self.controller.doctor(probe_services=False)
        self._populate_doctor(reports)
        self._select_nav("dashboard")
        self.stack.setCurrentWidget(self.dashboard_page)

    def _run_async(
        self,
        function: Callable[[], Any],
        on_result: Callable[[object], None],
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        worker = FunctionWorker(function)
        worker.signals.result.connect(on_result)
        worker.signals.error.connect(on_error or (lambda message: self.statusBar().showMessage(message, 8000)))
        self.thread_pool.start(worker)
