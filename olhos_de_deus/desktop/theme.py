APP_STYLESHEET = r"""
QMainWindow, QWidget {
    background-color: #071018;
    color: #dff7ff;
    font-family: "Segoe UI";
    font-size: 10pt;
}
QFrame#Sidebar {
    background-color: #08141f;
    border-right: 1px solid #12384d;
}
QLabel#Brand {
    color: #69e7ff;
    font-size: 18pt;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#Subtitle {
    color: #73a9bd;
    font-size: 9pt;
}
QPushButton#NavButton {
    text-align: left;
    padding: 10px 12px;
    border: 1px solid transparent;
    border-radius: 8px;
    background: transparent;
    color: #b9d8e4;
}
QPushButton#NavButton:hover {
    background-color: #0e2432;
    border-color: #1f607d;
    color: #8eeeff;
}
QPushButton#NavButton:checked {
    background-color: #0c2d40;
    border-color: #1fc8f0;
    color: #9cf4ff;
    font-weight: 600;
}
QPushButton#PrimaryButton {
    background-color: #0e6f94;
    color: white;
    border: 1px solid #27d8ff;
    border-radius: 8px;
    padding: 9px 16px;
    font-weight: 600;
}
QPushButton#PrimaryButton:hover { background-color: #1289b6; }
QPushButton#SecondaryButton {
    background-color: #0d1c27;
    color: #bcecff;
    border: 1px solid #25566b;
    border-radius: 8px;
    padding: 8px 14px;
}
QPushButton#SecondaryButton:hover { border-color: #34c8ec; }
QFrame#Card {
    background-color: #0b1822;
    border: 1px solid #173b4c;
    border-radius: 12px;
}
QLabel#CardTitle {
    color: #80eaff;
    font-size: 9pt;
    font-weight: 600;
}
QLabel#CardValue {
    color: #f3fdff;
    font-size: 20pt;
    font-weight: 700;
}
QLabel#PageTitle {
    color: #e8fbff;
    font-size: 20pt;
    font-weight: 700;
}
QLabel#Muted { color: #6f9bac; }
QLabel#Ready { color: #55f0ac; font-weight: 700; }
QLabel#Pending { color: #ffd166; font-weight: 700; }
QLabel#Error { color: #ff6f91; font-weight: 700; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #09131c;
    color: #dff7ff;
    border: 1px solid #1d4659;
    border-radius: 7px;
    padding: 7px;
    selection-background-color: #0f7598;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
    border-color: #32d5f7;
}
QTableWidget {
    background-color: #09131c;
    alternate-background-color: #0c1c27;
    gridline-color: #16394a;
    border: 1px solid #173b4c;
    border-radius: 8px;
}
QHeaderView::section {
    background-color: #0d2230;
    color: #8eeeff;
    border: none;
    border-right: 1px solid #173b4c;
    padding: 7px;
    font-weight: 600;
}
QScrollBar:vertical {
    border: none;
    background: #08131c;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #1b5268;
    min-height: 24px;
    border-radius: 5px;
}
QStatusBar {
    background-color: #08131c;
    color: #6fa6b9;
    border-top: 1px solid #12384d;
}
"""
