APP_STYLESHEET = r"""
QMainWindow, QWidget {
    background-color: #030914;
    color: #dff7ff;
    font-family: "Segoe UI";
    font-size: 10pt;
}
QWidget#CockpitPage { background-color: #020814; }
QFrame#Sidebar {
    background-color: #04111f;
    border-right: 1px solid #0b79a8;
}
QFrame#SidebarLogoBox {
    background-color: #03101d;
    border: 1px solid #0a3852;
    border-radius: 9px;
}
QLabel#Brand {
    color: #e6fbff;
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 2px;
}
QLabel#Subtitle {
    color: #3ec8f4;
    font-size: 8pt;
    letter-spacing: 2px;
}
QLabel#CockpitQuote {
    color: #76b7d5;
    font-size: 9pt;
    letter-spacing: 2px;
    padding: 10px 6px;
    border-left: 2px solid #0c81b5;
}
QLabel#SidebarVersion {
    color: #5f8fa8;
    font-size: 7pt;
    letter-spacing: 1px;
    padding: 5px;
}
QPushButton#NavButton {
    text-align: left;
    padding: 12px 12px;
    border: 1px solid transparent;
    border-radius: 6px;
    background: transparent;
    color: #a8d0df;
    font-size: 10pt;
}
QPushButton#NavButton:hover {
    background-color: #08243a;
    border-color: #0d6e99;
    color: #8eeeff;
}
QPushButton#NavButton:checked {
    background-color: #07365a;
    border: 1px solid #1ec9ff;
    color: #c8f9ff;
    font-weight: 700;
}
QFrame#CockpitTopBar {
    background-color: #041321;
    border: 1px solid #0e4566;
    border-radius: 8px;
}
QFrame#CockpitStatusItem {
    background-color: #03101c;
    border-right: 1px solid #0a4b70;
}
QLabel#StatusIcon {
    color: #20d8ff;
    font-size: 16pt;
    font-weight: 700;
}
QLabel#CockpitStatusTitle {
    color: #5797b7;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1px;
}
QLabel#CockpitStatusValue {
    color: #dffaff;
    font-size: 10pt;
    font-weight: 700;
}
QLabel#CockpitModel {
    min-width: 145px;
    color: #59e4ff;
    background-color: #041c30;
    border: 1px solid #148eb8;
    border-radius: 6px;
    padding: 10px 12px;
    font-weight: 700;
}
QFrame#HeroBanner {
    background-color: #03101d;
    border: 1px solid #0d4160;
    border-radius: 8px;
}
QLabel#HeroTitle {
    background: transparent;
    color: #9aefff;
    font-size: 12pt;
    font-weight: 800;
    letter-spacing: 3px;
}
QLabel#HeroSub {
    background: transparent;
    color: #397fa1;
    font-size: 7pt;
    letter-spacing: 1px;
}
QFrame#CommandCard, QFrame#ResponseCard {
    background-color: #04111d;
    border: 1px solid #0d6f97;
    border-radius: 8px;
}
QLabel#SectionTitle {
    color: #93efff;
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: 1px;
}
QLabel#CockpitMeta {
    color: #4388a5;
    font-size: 7pt;
    letter-spacing: 1px;
}
QLabel#CockpitMetaBright {
    color: #42efc4;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 1px;
}
QPlainTextEdit#CommandInput {
    background-color: #03101b;
    color: #dbf7ff;
    border: 1px solid #159ac9;
    border-radius: 7px;
    padding: 13px;
    font-size: 11pt;
    selection-background-color: #086990;
}
QPlainTextEdit#CommandInput:focus { border-color: #3de6ff; }
QPushButton#PrimaryButton {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0aa8d5, stop:1 #16d7f3);
    color: #00131e;
    border: 1px solid #58efff;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 800;
}
QPushButton#PrimaryButton:hover { background-color: #32e9ff; }
QPushButton#PrimaryButton:disabled {
    background-color: #12303e;
    color: #5d7e8b;
    border-color: #274958;
}
QPushButton#SecondaryButton, QPushButton#CompactButton {
    background-color: #051522;
    color: #aee9f7;
    border: 1px solid #1c5672;
    border-radius: 6px;
    padding: 9px 14px;
    font-weight: 600;
}
QPushButton#CompactButton { padding: 7px 9px; font-size: 8pt; }
QPushButton#SecondaryButton:hover, QPushButton#CompactButton:hover {
    background-color: #08283b;
    border-color: #2ad7ff;
    color: #dffcff;
}
QPushButton#SecondaryButton:disabled, QPushButton#CompactButton:disabled {
    color: #58717b;
    border-color: #193441;
}
QTabWidget#CockpitTabs::pane {
    border: 1px solid #0d4a67;
    border-radius: 6px;
    top: -1px;
    background: #020b13;
}
QTabBar::tab {
    background: #041421;
    color: #5f9eb8;
    padding: 8px 13px;
    border: 1px solid #0d3850;
    border-bottom: none;
}
QTabBar::tab:selected {
    background: #062b42;
    color: #86efff;
    border-color: #18a7d4;
}
QPlainTextEdit#ConsoleOutput {
    background-color: #020a12;
    border: none;
    color: #9fd8e8;
    font-family: "Consolas";
    font-size: 9pt;
    padding: 9px;
    selection-background-color: #0d5472;
}
QWidget#ExecutionEye { background-color: #020a12; }
QLineEdit#FollowupInput {
    background-color: #03101b;
    border: 1px solid #0e4662;
    border-radius: 6px;
    color: #dff7ff;
    padding: 9px;
}
QPushButton#SendButton {
    background-color: #05243a;
    border: 1px solid #1bbfe9;
    border-radius: 6px;
    color: #7eefff;
    font-size: 14pt;
    font-weight: 800;
}
QFrame#OperationsPanel {
    background-color: #03101c;
    border: 1px solid #0c4667;
    border-radius: 8px;
}
QFrame#OperationCard {
    background-color: #041420;
    border: 1px solid #0e4c6e;
    border-radius: 8px;
}
QLabel#OperationIcon {
    color: #26d9ff;
    font-size: 14pt;
    font-weight: 800;
}
QLabel#OperationTitle {
    color: #d4f8ff;
    font-size: 10pt;
    font-weight: 800;
}
QFrame#MiniMetric {
    background-color: #03101a;
    border: 1px solid #0b354c;
    border-radius: 5px;
}
QLabel#MiniMetricTitle {
    color: #4e8aa5;
    font-size: 6pt;
    font-weight: 700;
}
QLabel#MiniMetricValue {
    color: #64e8ff;
    font-size: 7pt;
    font-weight: 700;
}
QLabel#TinyMuted { color: #648ea1; font-size: 7pt; }
QLabel#MiniInfo { color: #5fa0b9; font-size: 7pt; }
QLabel#AgentDot { color: #25e6bc; font-size: 8pt; }
QLabel#AgentName, QLabel#IntegrationName { color: #b7dbe7; font-size: 8pt; }
QLabel#CockpitChipReady {
    color: #35f0b8;
    background-color: #043326;
    border: 1px solid #139d78;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 7pt;
    font-weight: 800;
}
QLabel#CockpitChipPending {
    color: #ffd166;
    background-color: #33270a;
    border: 1px solid #927221;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 7pt;
    font-weight: 800;
}
QLabel#CockpitChipInfo {
    color: #4fd9ff;
    background-color: #06263a;
    border: 1px solid #147ca3;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 7pt;
    font-weight: 800;
}
QProgressBar#SwarmProgress {
    background-color: #03101a;
    border: 1px solid #0c3e56;
    border-radius: 4px;
    height: 8px;
}
QProgressBar#SwarmProgress::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0a92c4, stop:1 #27e6ff);
    border-radius: 3px;
}
QFrame#WorldFooterCard {
    background-color: #03101a;
    border: 1px solid #0b3a54;
    border-radius: 8px;
}
QLabel#WorldFooterText {
    color: #4f9dbb;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#CardTitle { color: #80eaff; font-size: 9pt; font-weight: 600; }
QLabel#CardValue { color: #f3fdff; font-size: 20pt; font-weight: 700; }
QLabel#PageTitle { color: #e8fbff; font-size: 20pt; font-weight: 700; }
QLabel#Muted { color: #6f9bac; }
QLabel#Ready { color: #55f0ac; font-weight: 800; }
QLabel#Pending { color: #ffd166; font-weight: 800; }
QLabel#Error { color: #ff6f91; font-weight: 800; }
QFrame#Card {
    background-color: #06131f;
    border: 1px solid #16445d;
    border-radius: 9px;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #04101a;
    color: #dff7ff;
    border: 1px solid #1a465b;
    border-radius: 6px;
    padding: 7px;
    selection-background-color: #0f7598;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus { border-color: #32d5f7; }
QTableWidget {
    background-color: #04101a;
    alternate-background-color: #071b27;
    gridline-color: #12384a;
    border: 1px solid #173b4c;
    border-radius: 8px;
}
QHeaderView::section {
    background-color: #082131;
    color: #8eeeff;
    border: none;
    border-right: 1px solid #173b4c;
    padding: 7px;
    font-weight: 600;
}
QScrollBar:vertical { border: none; background: #03101a; width: 9px; }
QScrollBar::handle:vertical { background: #145675; min-height: 24px; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QStatusBar {
    background-color: #03101c;
    color: #5f91a5;
    border-top: 1px solid #0d3950;
}
QDockWidget { color: #8feeff; titlebar-close-icon: none; }
"""
