from __future__ import annotations

import math
import time

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class AnimatedCoreWidget(QWidget):
    """Lightweight animated eye/neural core drawn with QPainter."""

    MODES = {"idle", "working", "success", "error"}

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(240)
        self._started = time.perf_counter()
        self._mode = "idle"
        self._flash_until = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self.update)
        self._timer.start()

    def set_activity(self, mode: str) -> None:
        if mode not in self.MODES:
            raise ValueError(f"unsupported animation mode: {mode}")
        self._mode = mode
        if mode in {"success", "error"}:
            self._flash_until = time.perf_counter() + 1.8
        self.update()

    def _palette(self) -> tuple[QColor, QColor]:
        now = time.perf_counter()
        mode = self._mode
        if mode in {"success", "error"} and now > self._flash_until:
            self._mode = "idle"
            mode = "idle"
        if mode == "working":
            return QColor(38, 220, 255), QColor(50, 140, 255)
        if mode == "success":
            return QColor(70, 255, 170), QColor(43, 205, 255)
        if mode == "error":
            return QColor(255, 85, 130), QColor(255, 145, 80)
        return QColor(35, 195, 235), QColor(64, 116, 255)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt API
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(7, 16, 24))

        width = float(self.width())
        height = float(self.height())
        center = QPointF(width / 2.0, height / 2.0)
        elapsed = time.perf_counter() - self._started
        speed = 1.9 if self._mode == "working" else 1.0
        pulse = 1.0 + 0.035 * math.sin(elapsed * 2.4 * speed)
        primary, secondary = self._palette()

        radius = min(width * 0.25, height * 0.40) * pulse
        glow = QRadialGradient(center, radius * 1.6)
        glow.setColorAt(0.0, QColor(primary.red(), primary.green(), primary.blue(), 80))
        glow.setColorAt(0.45, QColor(secondary.red(), secondary.green(), secondary.blue(), 35))
        glow.setColorAt(1.0, QColor(7, 16, 24, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(center, radius * 1.6, radius * 1.15)

        eye_width = radius * 2.25
        eye_height = radius * 1.18
        eye = QPainterPath()
        left = QPointF(center.x() - eye_width / 2.0, center.y())
        right = QPointF(center.x() + eye_width / 2.0, center.y())
        eye.moveTo(left)
        eye.cubicTo(
            QPointF(center.x() - eye_width * 0.25, center.y() - eye_height),
            QPointF(center.x() + eye_width * 0.25, center.y() - eye_height),
            right,
        )
        eye.cubicTo(
            QPointF(center.x() + eye_width * 0.25, center.y() + eye_height),
            QPointF(center.x() - eye_width * 0.25, center.y() + eye_height),
            left,
        )
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(primary, 3.0))
        painter.drawPath(eye)

        iris_radius = radius * 0.48
        painter.setPen(QPen(secondary, 2.0))
        painter.drawEllipse(center, iris_radius, iris_radius)
        pupil_radius = iris_radius * (0.42 + 0.04 * math.sin(elapsed * 3.1 * speed))
        pupil_gradient = QRadialGradient(center, pupil_radius)
        pupil_gradient.setColorAt(0.0, QColor(220, 250, 255, 245))
        pupil_gradient.setColorAt(0.25, primary)
        pupil_gradient.setColorAt(1.0, QColor(5, 26, 42, 230))
        painter.setBrush(pupil_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, pupil_radius, pupil_radius)

        node_count = 16 if self._mode == "working" else 11
        orbit_x = eye_width * 0.62
        orbit_y = eye_height * 1.0
        nodes: list[QPointF] = []
        for index in range(node_count):
            angle = (math.tau * index / node_count) + elapsed * 0.12 * speed
            wobble = 1.0 + 0.08 * math.sin(elapsed * 1.4 + index)
            point = QPointF(
                center.x() + math.cos(angle) * orbit_x * wobble,
                center.y() + math.sin(angle) * orbit_y * wobble,
            )
            nodes.append(point)

        painter.setPen(QPen(QColor(primary.red(), primary.green(), primary.blue(), 65), 1.0))
        for index, point in enumerate(nodes):
            painter.drawLine(point, nodes[(index + 3) % node_count])
            painter.drawLine(point, nodes[(index + 5) % node_count])

        painter.setPen(Qt.NoPen)
        for index, point in enumerate(nodes):
            intensity = int(150 + 95 * (0.5 + 0.5 * math.sin(elapsed * 2.2 * speed + index)))
            painter.setBrush(QColor(primary.red(), primary.green(), primary.blue(), intensity))
            painter.drawEllipse(point, 2.5, 2.5)

        painter.setPen(QColor(110, 180, 200))
        painter.setFont(QFont("Segoe UI", 9, QFont.Medium))
        label = {
            "idle": "NÚCLEO EM ESPERA",
            "working": "NÚCLEO PROCESSANDO",
            "success": "MISSÃO CONCLUÍDA",
            "error": "ATENÇÃO: FALHA DETECTADA",
        }[self._mode]
        painter.drawText(QRectF(0, height - 34, width, 24), Qt.AlignCenter, label)


class StatCard(QFrame):
    def __init__(self, title: str, value: str = "—", detail: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        self.value_label = QLabel(value)
        self.value_label.setObjectName("CardValue")
        self.detail_label = QLabel(detail)
        self.detail_label.setObjectName("Muted")
        self.detail_label.setWordWrap(True)
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.detail_label)

    def set_value(self, value: str, detail: str | None = None) -> None:
        self.value_label.setText(value)
        if detail is not None:
            self.detail_label.setText(detail)


class IntegrationCard(QFrame):
    action_requested = Signal(str)

    def __init__(self, name: str, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.name = name
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        header = QHBoxLayout()
        self.title = QLabel(title)
        self.title.setObjectName("CardTitle")
        self.status = QLabel("PENDING")
        self.status.setObjectName("Pending")
        header.addWidget(self.title)
        header.addStretch(1)
        header.addWidget(self.status)
        self.detail = QLabel("Aguardando diagnóstico")
        self.detail.setWordWrap(True)
        self.detail.setObjectName("Muted")
        self.button = QPushButton("ABRIR")
        self.button.setObjectName("SecondaryButton")
        self.button.clicked.connect(lambda: self.action_requested.emit(self.name))
        layout.addLayout(header)
        layout.addWidget(self.detail)
        layout.addWidget(self.button, 0, Qt.AlignLeft)

    def update_report(self, report: dict) -> None:
        operational = bool(report.get("operational"))
        installed = bool(report.get("installed"))
        if operational:
            self.status.setText("READY")
            self.status.setObjectName("Ready")
        elif installed:
            self.status.setText("INSTALLED")
            self.status.setObjectName("Pending")
        else:
            self.status.setText("PENDING")
            self.status.setObjectName("Error")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.detail.setText(str(report.get("detail", "")))
