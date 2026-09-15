from __future__ import annotations

import json
from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
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

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Status, comando e saída do Ruflo aparecerão aqui.")
        layout.addWidget(self.output, 1)

        safety = QLabel(
            "Execução real só ocorre após confirmação. O Olhos de Deus usa argumentos separados, "
            "timeout e subprocess sem shell=True."
        )
        safety.setObjectName("Muted")
        safety.setWordWrap(True)
        layout.addWidget(safety)

        self.refresh_status()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.refresh_button.setEnabled(not busy)
        self.preview_button.setEnabled(not busy)
        self.init_button.setEnabled(not busy)
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
    dock.setMinimumWidth(340)
    dock.setWidget(RufloPanel(controller, dock))
    window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    menu = window.menuBar().addMenu("Fase 0")
    toggle = dock.toggleViewAction()
    toggle.setText("Mostrar / ocultar Ruflo")
    menu.addAction(toggle)

    refresh_action = menu.addAction("Verificar Ruflo")
    refresh_action.triggered.connect(dock.widget().refresh_status)
    return dock
