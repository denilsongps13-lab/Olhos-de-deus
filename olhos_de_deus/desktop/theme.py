APP_STYLESHEET = r"""
QMainWindow, QWidget {
    background-color: #030914;
    color: #dff7ff;
    font-family: "Segoe UI";
    font-size: 10pt;
}
QFrame#Sidebar {
    background-color: #04101d;
    border-right: 1px solid #0b4e70;
}
QLabel#Brand {
    color: #ecfdff;
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 2px;
}
QLabel#Subtitle {
    color: #3fcfff;
    font-size: 8pt;
    letter-spacing: 2px;
}
QLabel#CockpitQuote {
    color: #6bbce0;
    font-size: 9pt;
    letter-spacing: 2px;
    padding: 8px 10px;
    border-left: 2px solid #1aaee0;
}
QLabel#SidebarFooter {
    color: #557f95;
    font-size: 7pt;
    letter-spacing: 1px;
    padding: 8px;
}
QPushButton#NavButton {
    text-align: left;
    padding: 13px 14px;
    border: 1px solid transparent;
    border-left: 3px solid transparent;
    border-radius: 4px;
    background: transparent;
    color: #9fc5d5;
    font-size: 10pt;
}
QPushButton#NavButton:hover {
    background-color: #082439;
    border-color: #145d7e;
    color: #93eeff;
}
QPushButton#NavButton:checked {
    background-color: #083a5d;
    border: 1px solid #18b9ef;
    border-left: 3px solid #2fe5ff;
    color: #c7faff;
    font-weight: 700;
}
QPushButton#PrimaryButton {
    background-color: #10b8e8;
    color: #00111c;
    border: 1px solid #73edff;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 800;
}
QPushButton#PrimaryButton:hover { background-color: #35d8ff; }
QPushButton#PrimaryButton:disabled {
    background-color: #12303e;
    color: #5d7e8b;
    border-color: #274958;
}
QPushButton#SecondaryButton {
    background-color: #061521;
    color: #a8ddf2;
    border: 1px solid #1b5572;
    border-radius: 6px;
    padding: 9px 15px;
    font-weight: 600;
}
QPushButton#SecondaryButton:hover { border-color: #36d9ff; background-color: #0a2940; color: #d9f9ff; }
QPushButton#SecondaryButton:disabled { color: #58717b; border-color: #193441; }
QPushButton#SendButton {
    min-width: 42px;
    max-width: 42px;
    background-color: #092942;
    color: #61eaff;
    border: 1px solid #1d6f92;
    border-radius: 5px;
    padding: 8px;
    font-weight: 800;
}
QFrame#Card,
QFrame#OperationCard,
QFrame#CommandCard,
QFrame#ResponseCard {
    background-color: #04111e;
    border: 1px solid #0f5c82;
    border-radius: 8px;
}
QFrame#CommandCard, QFrame#ResponseCard {
    border: 1px solid #147ba6;
}
QFrame#CockpitTopBar {
    background-color: #04101c;
    border: 1px solid #0b4c6a;
    border-radius: 7px;
}
QFrame#CockpitStatusItem {
    background-color: #03101c;
    border-right: 1px solid #15506a;
}
QLabel#StatusIcon {
    color: #35dfff;
    font-size: 15pt;
    font-weight: 800;
}
QLabel#CockpitStatusTitle {
    color: #6b98ad;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1px;
}
QLabel#CockpitStatusValue {
    color: #e6fbff;
    font-size: 10pt;
    font-weight: 700;
}
QLabel#CockpitModel {
    color: #67e9ff;
    background-color: #061b2c;
    border: 1px solid #1189b4;
    border-radius: 5px;
    padding: 10px 14px;
    font-weight: 700;
}
QFrame#HeroBanner {
    background-color: #04111d;
    border: 1px solid #0d4260;
    border-radius: 7px;
}
QLabel#HeroTitle {
    color: #9eeeff;
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: 3px;
}
QLabel#HeroQuote {
    color: #6ca9c9;
    font-size: 8pt;
    font-weight: 600;
    letter-spacing: 2px;
}
QLabel#SectionTitle,
QLabel#OperationTitle {
    color: #7eeaff;
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: 1px;
}
QLabel#OperationSubtitle {
    color: #628ea3;
    font-size: 8pt;
}
QLabel#CockpitMeta {
    color: #4287a4;
    font-size: 7pt;
    letter-spacing: 1px;
}
QFrame#OperationsPanel {
    background-color: #030d17;
    border: 1px solid #0d4563;
    border-radius: 7px;
}
QFrame#OperationCard {
    background-color: #041421;
    border: 1px solid #125a7c;
    border-radius: 7px;
}
QFrame#WorldCard {
    background-color: #031421;
    border: 1px solid #0c3e59;
    border-radius: 7px;
}
QLabel#WorldLabel {
    color: #5aaed2;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#MetricsLabel {
    color: #5aa2c1;
    font-size: 7pt;
    letter-spacing: 1px;
    padding: 6px 0;
    border-top: 1px solid #123d53;
}
QLabel#OperationRowName { color: #a8cedd; }
QLabel#DotReady { color: #29efb3; }
QLabel#DotPending { color: #ffd45c; }
QLabel#ReadyBadge {
    color: #4ef5ba;
    background-color: #063226;
    border: 1px solid #10865f;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 8pt;
    font-weight: 800;
}
QLabel#PendingBadge {
    color: #ffd45c;
    background-color: #302708;
    border: 1px solid #826d16;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 8pt;
    font-weight: 800;
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
QLabel#CommandBar {
    background-color: #03101a;
    color: #567f92;
    border: 1px solid #0d3b54;
    border-radius: 5px;
    padding: 9px 11px;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #03101a;
    color: #dff7ff;
    border: 1px solid #174c65;
    border-radius: 6px;
    padding: 7px;
    selection-background-color: #0f7598;
}
QPlainTextEdit#CommandInput {
    background-color: #031522;
    border: 1px solid #19a8d8;
    border-radius: 6px;
    font-size: 11pt;
    padding: 13px;
}
QPlainTextEdit#ConsoleOutput {
    background-color: #020b13;
    border: 1px solid #0c3e58;
    color: #a7dcea;
    font-family: "Consolas";
    font-size: 9pt;
    padding: 10px;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
    border-color: #36dcff;
}
QTabWidget#CockpitTabs::pane {
    border: 1px solid #0c3e58;
    border-radius: 5px;
    top: -1px;
    background: #020b13;
}
QTabBar::tab {
    background: #041422;
    color: #628da2;
    padding: 8px 13px;
    border: 1px solid #103b52;
    border-bottom: none;
    font-size: 8pt;
    font-weight: 700;
}
QTabBar::tab:selected {
    background: #062c45;
    color: #75efff;
    border-color: #1794bd;
}
QProgressBar#HudProgress {
    background: #071722;
    border: 1px solid #163e50;
    border-radius: 4px;
    min-height: 7px;
    max-height: 7px;
}
QProgressBar#HudProgress::chunk {
    background-color: #19c8ef;
    border-radius: 3px;
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
    background: #03101a;
    width: 9px;
}
QScrollBar::handle:vertical {
    background: #17607c;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QStatusBar {
    background-color: #03101a;
    color: #5f8798;
    border-top: 1px solid #10384e;
}
QDockWidget {
    color: #8feeff;
    titlebar-close-icon: none;
}
"""
