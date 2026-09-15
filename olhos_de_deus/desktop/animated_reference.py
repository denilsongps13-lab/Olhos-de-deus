from __future__ import annotations

import math
import time

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QPlainTextEdit, QWidget


class AnimatedEye(QWidget):
    def __init__(self, compact: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.compact = compact
        self._started = time.perf_counter()
        self._working = False
        self.setMinimumSize(100 if compact else 190, 74 if compact else 150)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self.update)
        self._timer.start()

    def set_working(self, working: bool) -> None:
        self._working = working
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = float(self.width()), float(self.height())
        cx, cy = w / 2.0, h / 2.0
        s = min(w, h)
        t = time.perf_counter() - self._started
        speed = 1.6 if self._working else 1.0
        pulse = 1.0 + 0.075 * math.sin(t * 2.7 * speed)

        glow = QRadialGradient(QPointF(cx, cy), s * 0.48 * pulse)
        glow.setColorAt(0.0, QColor(83, 235, 255, 88))
        glow.setColorAt(0.45, QColor(0, 143, 255, 44))
        glow.setColorAt(1.0, QColor(0, 45, 100, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glow)
        p.drawEllipse(QPointF(cx, cy), s * 0.48 * pulse, s * 0.36 * pulse)

        for i, factor in enumerate((0.78, 0.60, 0.43)):
            alpha = 90 + int(45 * (0.5 + 0.5 * math.sin(t * 2.0 + i)))
            p.setPen(QPen(QColor(0, 174, 255, alpha), 1.0))
            r = s * factor * 0.5 * pulse
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QPointF(cx, cy), r, r)

        ew, eh = s * 0.88, s * 0.34
        eye = QPainterPath()
        eye.moveTo(cx - ew / 2.0, cy)
        eye.cubicTo(cx - ew * 0.28, cy - eh, cx + ew * 0.28, cy - eh, cx + ew / 2.0, cy)
        eye.cubicTo(cx + ew * 0.28, cy + eh, cx - ew * 0.28, cy + eh, cx - ew / 2.0, cy)
        p.setPen(QPen(QColor(45, 225, 255, 245), 2.4 if not self.compact else 1.8))
        p.drawPath(eye)

        iris = s * 0.18 * pulse
        iris_glow = QRadialGradient(QPointF(cx, cy), iris * 1.6)
        iris_glow.setColorAt(0.0, QColor(235, 255, 255, 255))
        iris_glow.setColorAt(0.2, QColor(48, 230, 255, 245))
        iris_glow.setColorAt(0.58, QColor(0, 117, 255, 190))
        iris_glow.setColorAt(1.0, QColor(0, 30, 80, 0))
        p.setBrush(iris_glow)
        p.setPen(QPen(QColor(87, 239, 255, 210), 1.2))
        p.drawEllipse(QPointF(cx, cy), iris * 1.45, iris * 1.45)
        p.setBrush(QColor(1, 12, 25, 245))
        p.drawEllipse(QPointF(cx, cy), iris * 0.56, iris * 0.56)

        p.setPen(QPen(QColor(40, 205, 255, 120), 1.0))
        for i in range(16):
            a = i * math.tau / 16.0 + t * 0.22 * speed
            r1, r2 = s * 0.29, s * (0.37 + 0.015 * math.sin(t * 2.1 + i))
            p.drawLine(QPointF(cx + math.cos(a) * r1, cy + math.sin(a) * r1), QPointF(cx + math.cos(a) * r2, cy + math.sin(a) * r2))
        p.end()


class AnimatedPlanet(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._started = time.perf_counter()
        self._working = False
        self.setMinimumHeight(128)
        self.setMaximumHeight(150)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self.update)
        self._timer.start()

    def set_working(self, working: bool) -> None:
        self._working = working
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = float(self.width()), float(self.height())
        t = time.perf_counter() - self._started
        speed = 1.65 if self._working else 1.0
        pulse = 1.0 + 0.035 * math.sin(t * 2.35 * speed)

        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0.0, QColor(2, 12, 25))
        bg.setColorAt(0.5, QColor(3, 29, 55))
        bg.setColorAt(1.0, QColor(1, 10, 24))
        p.fillRect(self.rect(), bg)

        source = QPointF(w * 0.08, h * 0.56)
        gc = QPointF(w * 0.66, h * 1.10)
        radius = h * 0.98 * pulse

        eye = QPainterPath()
        ew, eh = h * 0.34, h * 0.12
        eye.moveTo(source.x() - ew / 2, source.y())
        eye.cubicTo(source.x() - ew * .25, source.y() - eh, source.x() + ew * .25, source.y() - eh, source.x() + ew / 2, source.y())
        eye.cubicTo(source.x() + ew * .25, source.y() + eh, source.x() - ew * .25, source.y() + eh, source.x() - ew / 2, source.y())
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(42, 218, 255, 190), 1.3))
        p.drawPath(eye)
        eg = QRadialGradient(source, h * 0.10 * pulse)
        eg.setColorAt(0, QColor(220, 255, 255, 230))
        eg.setColorAt(.25, QColor(38, 225, 255, 225))
        eg.setColorAt(1, QColor(0, 92, 220, 0))
        p.setBrush(eg)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(source, h * .10 * pulse, h * .10 * pulse)

        bridge = QPainterPath(source)
        bridge.cubicTo(QPointF(w * .30, h * .02), QPointF(w * .52, h * .15), QPointF(gc.x(), h * .48))
        alpha = 105 + int(70 * (0.5 + 0.5 * math.sin(t * 2.2 * speed)))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(36, 190, 255, alpha), 1.4))
        p.drawPath(bridge)
        for i in range(7):
            pos = (t * 0.16 * speed + i / 7.0) % 1.0
            pt = bridge.pointAtPercent(pos)
            dg = QRadialGradient(pt, 8.0)
            dg.setColorAt(0, QColor(220, 255, 255, 255))
            dg.setColorAt(.35, QColor(41, 218, 255, 220))
            dg.setColorAt(1, QColor(0, 100, 255, 0))
            p.setBrush(dg)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(pt, 8.0, 8.0)

        globe = QRadialGradient(gc, radius)
        globe.setColorAt(0.0, QColor(8, 105, 190, 230))
        globe.setColorAt(0.5, QColor(0, 64, 130, 200))
        globe.setColorAt(0.86, QColor(0, 31, 77, 160))
        globe.setColorAt(1.0, QColor(0, 13, 35, 0))
        p.setBrush(globe)
        p.setPen(QPen(QColor(38, 186, 255, 195), 1.4))
        p.drawEllipse(gc, radius, radius)

        p.save()
        p.translate(gc)
        p.rotate((t * 2.7 * speed) % 360.0)
        p.translate(-gc)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(57, 190, 250, 88), 0.8))
        for xo in (-.48, -.25, 0.0, .25, .48):
            rw = radius * (0.62 + abs(xo) * .52)
            p.drawArc(QRectF(gc.x() - rw / 2, gc.y() - radius, rw, radius * 2), 90 * 16, 180 * 16)
        p.restore()
        p.setPen(QPen(QColor(61, 197, 255, 90), .8))
        for yf in (.28, .44, .60, .74):
            p.drawArc(QRectF(gc.x() - radius, gc.y() - radius * yf, radius * 2, radius * .34), 0, 180 * 16)

        for i in range(3):
            phase = (t * .42 * speed + i / 3.0) % 1.0
            rr = radius * (.77 + phase * .34)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(27, 196, 255, int(100 * (1.0 - phase))), 1.0))
            p.drawEllipse(gc, rr, rr)
        p.end()


class ConsoleEye(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._started = time.perf_counter()
        self._working = False
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self.viewport().update)
        self._timer.start()

    def set_working(self, working: bool) -> None:
        self._working = working
        self.viewport().update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        p = QPainter(self.viewport())
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = float(self.viewport().width()), float(self.viewport().height())
        if w < 520 or h < 140:
            p.end(); return
        t = time.perf_counter() - self._started
        speed = 1.7 if self._working else 1.0
        pulse = 1.0 + .055 * math.sin(t * 2.8 * speed)
        cx, cy = w * .82, h * .58
        s = min(w * .25, h * .72)
        glow = QRadialGradient(QPointF(cx, cy), s * .72)
        glow.setColorAt(0, QColor(38, 214, 255, 55)); glow.setColorAt(.48, QColor(0, 100, 230, 28)); glow.setColorAt(1, QColor(0, 30, 80, 0))
        p.setPen(Qt.PenStyle.NoPen); p.setBrush(glow); p.drawEllipse(QPointF(cx, cy), s * .72, s * .72)
        for i, factor in enumerate((.92,.70,.52,.34)):
            p.setBrush(Qt.BrushStyle.NoBrush); p.setPen(QPen(QColor(34, 195, 255, 68 + int(35 * (.5 + .5 * math.sin(t * 2.1 + i)))), 1.0))
            r = s * factor * .5 * pulse; p.drawEllipse(QPointF(cx, cy), r, r)
        ew, eh = s * .95, s * .32
        path = QPainterPath(); path.moveTo(cx-ew/2,cy); path.cubicTo(cx-ew*.27,cy-eh,cx+ew*.27,cy-eh,cx+ew/2,cy); path.cubicTo(cx+ew*.27,cy+eh,cx-ew*.27,cy+eh,cx-ew/2,cy)
        p.setPen(QPen(QColor(54,225,255,175),1.7)); p.drawPath(path)
        iris = s * .13 * pulse
        ig = QRadialGradient(QPointF(cx,cy),iris*1.8); ig.setColorAt(0,QColor(235,255,255,220)); ig.setColorAt(.25,QColor(49,229,255,210)); ig.setColorAt(1,QColor(0,80,230,0))
        p.setBrush(ig); p.setPen(Qt.PenStyle.NoPen); p.drawEllipse(QPointF(cx,cy),iris*1.8,iris*1.8); p.setBrush(QColor(0,10,24,230)); p.drawEllipse(QPointF(cx,cy),iris*.60,iris*.60)
        beam = QPainterPath(QPointF(cx,cy-iris*1.8)); beam.cubicTo(QPointF(cx+s*.18,cy-s*.35),QPointF(cx-s*.12,h*.18),QPointF(cx,2.0)); p.setBrush(Qt.BrushStyle.NoBrush); p.setPen(QPen(QColor(38,196,255,95),1.1)); p.drawPath(beam)
        for i in range(5):
            pt = beam.pointAtPercent(1.0-((t*.19*speed+i/5.0)%1.0)); p.setBrush(QColor(106,242,255,185)); p.setPen(Qt.PenStyle.NoPen); p.drawEllipse(pt,1.8,1.8)
        p.end()
