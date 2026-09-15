from __future__ import annotations

import argparse
import sys
from typing import Sequence

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QSplashScreen, QSystemTrayIcon

from olhos_de_deus import __version__

from .cockpit_window import CockpitWindow
from .controller import DesktopController
from .ruflo_panel import install_ruflo_dock
from .theme import APP_STYLESHEET

# Qt can dispatch changeEvent while QMainWindow is still inside its base
# constructor, before the instance initializer assigns _tray_available.
CockpitWindow._tray_available = False


def build_icon(size: int = 128) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    center = size / 2.0
    path = QPainterPath()
    path.moveTo(size * 0.12, center)
    path.cubicTo(size * 0.30, size * 0.22, size * 0.70, size * 0.22, size * 0.88, center)
    path.cubicTo(size * 0.70, size * 0.78, size * 0.30, size * 0.78, size * 0.12, center)
    painter.setPen(QPen(QColor(55, 218, 255), max(2.0, size / 32)))
    painter.setBrush(QColor(7, 20, 31))
    painter.drawPath(path)
    painter.setPen(QPen(QColor(95, 244, 255), max(1.5, size / 48)))
    painter.setBrush(QColor(18, 118, 180))
    painter.drawEllipse(int(size * 0.37), int(size * 0.37), int(size * 0.26), int(size * 0.26))
    painter.setBrush(QColor(224, 252, 255))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(int(size * 0.47), int(size * 0.47), int(size * 0.06), int(size * 0.06))
    painter.end()
    return QIcon(pixmap)


def _splash(icon: QIcon) -> QSplashScreen:
    pixmap = QPixmap(620, 320)
    pixmap.fill(QColor(5, 14, 24))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor(100, 234, 255))
    painter.drawPixmap(250, 38, 120, 120, icon.pixmap(120, 120))
    painter.setPen(QColor(225, 250, 255))
    font = painter.font()
    font.setPointSize(24)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(0, 182, 620, 50, Qt.AlignmentFlag.AlignCenter, "OLHO DE DEUS")
    font.setPointSize(10)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(QColor(105, 190, 220))
    painter.drawText(0, 228, 620, 30, Qt.AlignmentFlag.AlignCenter, "COCKPIT DE INTELIGÊNCIA ARTIFICIAL")
    painter.end()
    splash = QSplashScreen(pixmap)
    splash.showMessage(
        "Inicializando cockpit · carregando núcleo · verificando integrações...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        QColor(110, 220, 245),
    )
    return splash


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="olhos-de-deus-desktop", add_help=True)
    parser.add_argument("--smoke-test", action="store_true", help="Inicializa controller/Qt, renderiza a janela e encerra")
    return parser


def _wire_ruflo(window: CockpitWindow, controller: DesktopController):
    dock = install_ruflo_dock(window, controller)
    window.set_ruflo_dock(dock)
    dock.hide()
    return dock


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    app = QApplication.instance() or QApplication(sys.argv[:1])
    app.setApplicationName("Olho de Deus")
    app.setApplicationDisplayName("Olho de Deus")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("Olho de Deus")
    app.setStyleSheet(APP_STYLESHEET)
    icon = build_icon()
    app.setWindowIcon(icon)

    controller = DesktopController()
    if args.smoke_test:
        dashboard = controller.dashboard()
        if dashboard.get("total_integrations") != 7:
            return 2
        if dashboard.get("ruflo", {}).get("phase") != 0:
            return 3
        window = CockpitWindow(controller)
        window.setWindowIcon(icon)
        ruflo_dock = _wire_ruflo(window, controller)
        window.show()
        app.processEvents()
        window.core_animation.repaint()
        ruflo_dock.widget().refresh_status()
        window._refresh_dashboard()
        app.processEvents()
        window.close()
        app.processEvents()
        return 0

    splash = _splash(icon)
    splash.show()
    app.processEvents()

    window = CockpitWindow(controller)
    window.setWindowIcon(icon)
    ruflo_dock = _wire_ruflo(window, controller)

    tray: QSystemTrayIcon | None = None
    if QSystemTrayIcon.isSystemTrayAvailable():
        tray = QSystemTrayIcon(icon, app)
        tray.setToolTip("Olho de Deus")
        menu = QMenu()
        open_action = menu.addAction("Abrir cockpit")
        status_action = menu.addAction("Status")
        doctor_action = menu.addAction("Doctor")
        ruflo_action = menu.addAction("Ruflo · Fase 0")
        menu.addSeparator()
        exit_action = menu.addAction("Sair")

        open_action.triggered.connect(lambda: (window.showNormal(), window.raise_(), window.activateWindow()))

        def show_status() -> None:
            data = controller.dashboard()
            ruflo_state = "READY" if data.get("ruflo", {}).get("operational") else "PENDING"
            tray.showMessage(
                "Olho de Deus",
                f"Núcleo online · {data['operational']}/{data['total_integrations']} fases prontas · Ruflo {ruflo_state}",
                QSystemTrayIcon.MessageIcon.Information,
                5000,
            )

        def run_doctor() -> None:
            reports = controller.doctor(probe_services=False)
            ready = sum(bool(item["operational"]) for item in reports)
            tray.showMessage(
                "System Doctor",
                f"{ready}/{len(reports)} módulos operacionais, incluindo a Fase 0",
                QSystemTrayIcon.MessageIcon.Information,
                5000,
            )

        def show_ruflo() -> None:
            window.showNormal()
            window.raise_()
            window.activateWindow()
            ruflo_dock.show()
            ruflo_dock.raise_()
            ruflo_dock.widget().refresh_status()

        status_action.triggered.connect(show_status)
        doctor_action.triggered.connect(run_doctor)
        ruflo_action.triggered.connect(show_ruflo)
        exit_action.triggered.connect(app.quit)
        tray.setContextMenu(menu)
        tray.activated.connect(
            lambda reason: open_action.trigger()
            if reason == QSystemTrayIcon.ActivationReason.DoubleClick
            else None
        )
        tray.show()
        window.set_tray_available(True)
        app.setQuitOnLastWindowClosed(False)

    window.show()
    splash.finish(window)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
