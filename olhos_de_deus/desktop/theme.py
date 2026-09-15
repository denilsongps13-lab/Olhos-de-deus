APP_STYLESHEET = r"""
QMainWindow, QWidget {
    background-color: #050d16;
    color: #dff7ff;
    font-family: "Segoe UI";
    font-size: 10pt;
}
QFrame#Sidebar {
    background-color: #06131f;
    border-right: 1px solid #0f4460;
}
QLabel#CockpitLogo {
    color: #53e7ff;
    font-size: 30pt;
    font-weight: 800;
}
QLabel#Brand {
    color: #dffaff;
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 2px;
}
QLabel#Subtitle {
    color: #4fc6ee;
    font-size: 8pt;
    letter-spacing: 2px;
}
QLabel#CockpitQuote {
    color: #77b9da;
    font-size: 9pt;
    letter-spacing: 1px;
    padding: 8px;
}
QPushButton#NavButton {
    text-align: left;
    padding: 11px 12px;
    border: 1px solid transparent;
    border-radius: 7px;
    background: transparent;
    color: #b9d8e4;
    font-size: 10pt;
}
QPushButton#NavButton:hover {
    background-color: #0b2433;
    border-color: #1f607d;
    color: #8eeeff;
}
QPushButton#NavButton:checked {
    background-color: #0a3851;
    border-color: #1fc8f0;
    color: #b7f7ff;
    font-weight: 700;
}
QPushButton#PrimaryButton {
    background-color: #0a8fbd;
    color: white;
    border: 1px solid #33dcff;
    border-radius: 7px;
    padding: 9px 16px;
    font-weight: 700;
}
QPushButton#PrimaryButton:hover { background-color: #10a9dc; }
QPushButton#PrimaryButton:disabled {
    background-color: #12303e;
    color: #5d7e8b;
    border-color: #274958;
}
QPushButton#SecondaryButton {
    background-color: #081923;
    color: #bcecff;
    border: 1px solid #25566b;
    border-radius: 7px;
    padding: 8px 14px;
}
QPushButton#SecondaryButton:hover { border-color: #34c8ec; background-color: #0b2634; }
QPushButton#SecondaryButton:disabled { color: #58717b; border-color: #193441; }
QFrame#Card,
QFrame#OperationCard,
QFrame#CommandCard,
QFrame#ResponseCard {
    background-color: #071722;
    border: 1px solid #145271;
    border-radius: 10px;
}
QFrame#CockpitTopBar {
    background-color: #071722;
    border: 1px solid #0e3c55;
    border-radius: 9px;
}
QFrame#CockpitStatusItem {
    background-color: #06141f;
    border: 1px solid #123d53;
    border-radius: 7px;
}
QLabel#CockpitStatusTitle {
    color: #6caac3;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1px;
}
QLabel#CockpitStatusValue {
    color: #dffaff;
    font-size: 11pt;
    font-weight: 700;
}
QLabel#CockpitModel {
    color: #63e6ff;
    background-color: #082131;
    border: 1px solid #1598c0;
    border-radius: 7px;
    padding: 9px 12px;
    font-weight: 700;
}
QFrame#HeroBanner {
    background-color: #061825;
    border: 1px solid #10405b;
    border-radius: 10px;
}
QLabel#HeroTitle {
    color: #a9f5ff;
    font-size: 13pt;
    font-weight: 800;
    letter-spacing: 2px;
}
QLabel#SectionTitle,
QLabel#OperationTitle {
    color: #8feeff;
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: 1px;
}
QLabel#CockpitMeta {
    color: #3d94b2;
    font-size: 7pt;
    letter-spacing: 1px;
}
QFrame#OperationsPanel {
    background-color: #06131e;
    border: 1px solid #0f4260;
    border-radius: 10px;
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
QLabel#Ready { color: #55f0ac; font-weight: 800; }
QLabel#Pending { color: #ffd166; font-weight: 800; }
QLabel#Error { color: #ff6f91; font-weight: 800; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #06111b;
    color: #dff7ff;
    border: 1px solid #1d4659;
    border-radius: 7px;
    padding: 7px;
    selection-background-color: #0f7598;
}
QPlainTextEdit#CommandInput {
    background-color: #061521;
    border: 1px solid #1f9cc6;
    font-size: 11pt;
    padding: 12px;
}
QPlainTextEdit#ConsoleOutput {
    background-color: #040d15;
    border: 1px solid #0f3f58;
    color: #b9e7f4;
    font-family: "Consolas";
    font-size: 9pt;
    padding: 9px;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
    border-color: #32d5f7;
}
QTabWidget#CockpitTabs::pane {
    border: 1px solid #0f3f58;
    border-radius: 7px;
    top: -1px;
    background: #040d15;
}
QTabBar::tab {
    background: #071826;
    color: #6fa9c0;
    padding: 8px 14px;
    border: 1px solid #113b50;
    border-bottom: none;
}
QTabBar::tab:selected {
    background: #093048;
    color: #8ff2ff;
    border-color: #1ba9d2;
}
QTableWidget {
    background-color: #06111b;
    alternate-background-color: #0a1c28;
    gridline-color: #16394a;
    border: 1px solid #173b4c;
    border-radius: 8px;
}
QHeaderView::section {
    background-color: #0b2230;
    color: #8eeeff;
    border: none;
    border-right: 1px solid #173b4c;
    padding: 7px;
    font-weight: 600;
}
QScrollBar:vertical {
    border: none;
    background: #06111b;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #17607c;
    min-height: 24px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QStatusBar {
    background-color: #06131e;
    color: #6fa6b9;
    border-top: 1px solid #12384d;
}
QDockWidget {
    color: #8feeff;
    titlebar-close-icon: none;
}
"""
