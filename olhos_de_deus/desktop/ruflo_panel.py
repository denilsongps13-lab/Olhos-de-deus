from __future__ import annotations

import json
from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .controller import DesktopController


class _WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    finished = Signal()


class _Worker(QRunnable):
    def __init__(self, function: Callable[[], Any]) -> None:
        super().__init__()
        self.function = function
        self.signals = _WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = self.function()
        except Exception as exc:
            self.signals.error.emit(f"{type(exc).__name__}: {exc}")
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class RufloPanel(QWidget):
    """Visual control surface for the optional Ruflo phase-zero meta-harness."""

    def __init__(self, controller: DesktopController, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.thread_pool = QThreadPool.globalInstance()
        self._busy = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        heading = QLabel("FASE 0 · RUFLO")
        heading.setObjectName("PageTitle")
        layout.addWidget(heading)

        subtitle = QLabel(
            "Meta-orquestrador opcional para agentes, swarms, memória, MCP e workflows. "
            "As sete fases do Olhos de Deus continuam independentes."
        )
        subtitle.setObjectName("Muted")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        status_card = QFrame()
        status_card.setObjectName("Card")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(12, 10, 12, 10)

        row = QHBoxLayout()
        row.addWidget(QLabel("STATUS"))
        self.status = QLabel("VERIFICANDO")
        self.status.setObjectName("Pending")
        row.addStretch(1)
        row.addWidget(self.status)
        status_layout.addLayout(row)

        self.detail = QLabel("Aguardando diagnóstico...")
        self.detail.setObjectName("Muted")
        self.detail.setWordWrap(True)
        status_layout.addWidget(self.detail)

        self.workspace = QLabel("")
        self.workspace.setObjectName("Muted")
        self.workspace.setWordWrap(True)
        status_layout.addWidget(self.workspace)
        layout.addWidget(status_card)

        self.wizard = QCheckBox("Usar wizard oficial no comando de inicialização")
        self.wizard.setToolTip(
            "O wizard pode exigir interação. Para instalação automática na interface, deixe desmarcado."
        )
        layout.addWidget(self.wizard)

        actions = QHBoxLayout()
        self.refresh_button = QPushButton("VERIFICAR")
        self.refresh_button.setObjectName("SecondaryButton")
        self.refresh_button.clicked.connect(self.refresh_status)

        self.preview_button = QPushButton("PREVIEW INIT")
        self.preview_button.setObjectName("SecondaryButton")
        self.preview_button.clicked.connect(self.preview_init)

        self.init_button = QPushButton("INICIALIZAR RUFLO")
        self.init_button.setObjectName("PrimaryButton")
        self.init_button.clicked.connect(self.confirm_init)

        actions.addWidget(self.refresh_button)
        actions.addWidget(self.preview_button)
        actions.addWidget(self.init_button)
        layout.addLayout(actions)

        swarm_card = QFrame()
        swarm_card.setObjectName("Card")
        swarm_layout = QVBoxLayout(swarm_card)
        swarm_layout.addWidget(QLabel("SWARM · COORDENAÇÃO MULTIAGENTE"))

        swarm_note = QLabel(
            "O comando swarm do Ruflo prepara e coordena agentes. O Ruflo não é tratado como se "
            "sozinho executasse um modelo: execução autônoma real ainda depende do runtime de agente configurado."
        )
        swarm_note.setObjectName("Muted")
        swarm_note.setWordWrap(True)
        swarm_layout.addWidget(swarm_note)

        form = QFormLayout()
        self.topology = QComboBox()
        self.topology.addItems([
            "hierarchical",
            "hierarchical-mesh",
            "mesh",
            "ring",
            "star",
            "hybrid",
            "pheromone-adaptive",
        ])
        self.strategy = QComboBox()
        self.strategy.addItems([
            "development",
            "specialized",
            "balanced",
            "adaptive",
            "research",
            "testing",
            "optimization",
            "maintenance",
            "analysis",
        ])
        self.permissions = QComboBox()
        self.permissions.addItems(["standard", "strict", "permissive"])
        self.max_agents = QSpinBox()
        self.max_agents.setRange(1, 15)
        self.max_agents.setValue(7)
        form.addRow("Topologia", self.topology)
        form.addRow("Estratégia", self.strategy)
        form.addRow("Permissões", self.permissions)
        form.addRow("Máx. agentes", self.max_agents)
        swarm_layout.addLayout(form)

        self.objective = QPlainTextEdit()
        self.objective.setMaximumHeight(90)
        self.objective.setPlaceholderText("Objetivo do swarm. Ex.: analisar o projeto e propor correções com QA.")
        swarm_layout.addWidget(self.objective)

        swarm_actions_1 = QHBoxLayout()
        self.swarm_preview = QPushButton("PREVIEW SWARM")
        self.swarm_preview.setObjectName("SecondaryButton")
        self.swarm_preview.clicked.connect(self.preview_swarm)
        self.swarm_init = QPushButton("CRIAR SWARM")
        self.swarm_init.setObjectName("PrimaryButton")
        self.swarm_init.clicked.connect(self.confirm_swarm_init)
        self.swarm_status = QPushButton("STATUS SWARM")
        self.swarm_status.setObjectName("SecondaryButton")
        self.swarm_status.clicked.connect(self.query_swarm_status)
        swarm_actions_1.addWidget(self.swarm_preview)
        swarm_actions_1.addWidget(self.swarm_init)
        swarm_actions_1.addWidget(self.swarm_status)
        swarm_layout.addLayout(swarm_actions_1)

        self.swarm_start = QPushButton("COORDENAR OBJETIVO COM RUFLO")
        self.swarm_start.setObjectName("PrimaryButton")
        self.swarm_start.clicked.connect(self.confirm_swarm_start)
        swarm_layout.addWidget(self.swarm_start)
        layout.addWidget(swarm_card)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Status, comando e saída do Ruflo aparecerão aqui.")
        layout.addWidget(self.output, 1)

        safety = QLabel(
            "Execução real só ocorre após confirmação. O Olhos de Deus usa argumentos separados, "
            "allowlists, timeout e subprocess sem shell=True."
        )
        safety.setObjectName("Muted")
        safety.setWordWrap(True)
        layout.addWidget(safety)

        self.refresh_status()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        for button in (
            self.refresh_button,
            self.preview_button,
            self.init_button,
            self.swarm_preview,
            self.swarm_init,
            self.swarm_status,
            self.swarm_start,
        ):
            button.setEnabled(not busy)
        if busy:
            self.status.setText("EXECUTANDO")
            self.status.setObjectName("Pending")
            self.status.style().unpolish(self.status)
            self.status.style().polish(self.status)

    def _render(self, payload: Any) -> None:
        self.output.setPlainText(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        if isinstance(payload, dict) and payload.get("name") == "ruflo":
            installed = bool(payload.get("installed"))
            operational = bool(payload.get("operational"))
            if operational:
                state = "READY"
                object_name = "Ready"
            elif installed:
                state = "INSTALLED"
                object_name = "Pending"
            else:
                state = "PENDING"
                object_name = "Pending"
            self.status.setText(state)
            self.status.setObjectName(object_name)
            self.status.style().unpolish(self.status)
            self.status.style().polish(self.status)
            self.detail.setText(str(payload.get("detail", "")))

    @staticmethod
    def _completed_payload(result) -> dict[str, Any]:
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def _swarm_options(self) -> dict[str, Any]:
        return {
            "topology": self.topology.currentText(),
            "max_agents": self.max_agents.value(),
            "strategy": self.strategy.currentText(),
            "permissions": self.permissions.currentText(),
        }

    def refresh_status(self) -> None:
        payload = self.controller.ruflo_status()
        self.workspace.setText(f"Workspace: {self.controller.ruflo_workspace}")
        self._render(payload)

    def preview_init(self) -> None:
        payload = self.controller.ruflo_init(execute=False, wizard=self.wizard.isChecked())
        self.workspace.setText(f"Workspace: {self.controller.ruflo_workspace}")
        self.output.setPlainText(json.dumps(payload, ensure_ascii=False, indent=2, default=str))

    def confirm_init(self) -> None:
        if self._busy:
            return
        answer = QMessageBox.question(
            self,
            "Inicializar Ruflo",
            "Isso executará o comando oficial do Ruflo via npx neste computador e poderá acessar o npm. "
            "Deseja continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._run_async(
            lambda: self.controller.ruflo_init(execute=True, wizard=self.wizard.isChecked())
        )

    def preview_swarm(self) -> None:
        adapter = self.controller.ruflo_adapter()
        command = adapter.init_swarm(dry_run=True, **self._swarm_options())
        self.output.setPlainText(
            json.dumps(
                {
                    "phase": 0,
                    "name": "ruflo",
                    "action": "swarm-init-preview",
                    "execute": False,
                    "command": list(command),
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    def confirm_swarm_init(self) -> None:
        if self._busy:
            return
        answer = QMessageBox.question(
            self,
            "Criar swarm Ruflo",
            "Isso criará a topologia de coordenação do Ruflo no workspace usando as opções exibidas. Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        def execute() -> dict[str, Any]:
            result = self.controller.ruflo_adapter().init_swarm(dry_run=False, **self._swarm_options())
            self.controller.storage.log(
                "RUFLO",
                "Ruflo swarm initialized",
                phase="ruflo",
                payload=self._swarm_options(),
            )
            return {
                "phase": 0,
                "name": "ruflo",
                "action": "swarm-init",
                "execute": True,
                **self._completed_payload(result),
            }

        self._run_async(execute)

    def query_swarm_status(self) -> None:
        def execute() -> dict[str, Any]:
            result = self.controller.ruflo_adapter().swarm_status(dry_run=False)
            return {
                "phase": 0,
                "name": "ruflo",
                "action": "swarm-status",
                "execute": True,
                **self._completed_payload(result),
            }

        self._run_async(execute)

    def confirm_swarm_start(self) -> None:
        if self._busy:
            return
        objective = self.objective.toPlainText().strip()
        if not objective:
            QMessageBox.warning(self, "Ruflo", "Digite um objetivo para o swarm.")
            return
        answer = QMessageBox.question(
            self,
            "Coordenar objetivo",
            "O Ruflo preparará/coordenará o swarm para este objetivo. Isso não significa que um modelo externo "
            "foi executado com sucesso; o resultado exibirá exatamente o retorno real do Ruflo. Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        strategy = self.strategy.currentText()

        def execute() -> dict[str, Any]:
            result = self.controller.ruflo_adapter().start_swarm(
                objective,
                strategy=strategy,
                dry_run=False,
            )
            self.controller.storage.log(
                "RUFLO",
                "Ruflo swarm objective coordinated",
                phase="ruflo",
                payload={"objective": objective, "strategy": strategy},
            )
            return {
                "phase": 0,
                "name": "ruflo",
                "action": "swarm-start",
                "execute": True,
                "objective": objective,
                **self._completed_payload(result),
            }

        self._run_async(execute)

    def _run_async(self, function: Callable[[], Any]) -> None:
        self._set_busy(True)
        worker = _Worker(function)
        worker.signals.result.connect(self._on_result)
        worker.signals.error.connect(self._on_error)
        worker.signals.finished.connect(lambda: self._set_busy(False))
        self.thread_pool.start(worker)

    @Slot(object)
    def _on_result(self, payload: Any) -> None:
        self.output.setPlainText(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        self.refresh_status()

    @Slot(str)
    def _on_error(self, message: str) -> None:
        self.status.setText("ERRO")
        self.status.setObjectName("Pending")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.output.setPlainText(message)
        QMessageBox.critical(self, "Ruflo", message)


def install_ruflo_dock(window, controller: DesktopController) -> QDockWidget:
    """Attach the phase-zero panel to an existing Olhos de Deus main window."""
    dock = QDockWidget("Fase 0 · Ruflo", window)
    dock.setObjectName("RufloPhaseZeroDock")
    dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
    dock.setMinimumWidth(380)
    dock.setWidget(RufloPanel(controller, dock))
    window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    menu = window.menuBar().addMenu("Fase 0")
    toggle = dock.toggleViewAction()
    toggle.setText("Mostrar / ocultar Ruflo")
    menu.addAction(toggle)

    refresh_action = menu.addAction("Verificar Ruflo")
    refresh_action.triggered.connect(dock.widget().refresh_status)
    return dock
