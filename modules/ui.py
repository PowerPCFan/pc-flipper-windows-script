import re as regexp
import sys

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFont, QScreen
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QScrollArea, QVBoxLayout,
    QWidget
)

from modules.apps import APP_DEFINITIONS
from modules.misc.models import (
    ActivationChoice, AppDefinition,
    AppId, FurmarkAntiAliasing,
    FurmarkOptions, FurmarkResolution,
    ScriptOptions
)


class ScriptOptionsWindow(QMainWindow):
    def __init__(self, font: str = "Segoe UI"):
        super().__init__()
        self.task_options = ScriptOptions(
            selected_apps={app.app_id: app.selected_by_default for app in APP_DEFINITIONS}
        )
        self.app_checkboxes: dict[AppId, QCheckBox] = {}

        self.init_ui(font)
        self.setup_connections()

    def init_ui(self, font: str):
        self.setWindowTitle("Script Options")
        self.setMinimumSize(500, 400)
        self.resize(850, 650)
        self.setStyleSheet(f"font-family: {font};")
        self.center_window()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("Script Options")
        title_label.setFont(QFont(font, 16, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Select the tasks you would like to run.")
        subtitle_label.setFont(QFont(font, 10, QFont.Weight.Bold))
        main_layout.addWidget(subtitle_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.Box)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        self.create_driver_section(scroll_layout)
        self.create_system_section(scroll_layout)
        self.create_app_section(scroll_layout)

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.continue_button = QPushButton("Start Script")
        self.continue_button.clicked.connect(self.on_continue_clicked)
        button_layout.addWidget(self.continue_button)
        main_layout.addLayout(button_layout)

    def center_window(self):
        primary_screen: QScreen | None = QApplication.primaryScreen()
        if primary_screen is not None:
            screen: QRect = primary_screen.geometry()
            window = self.geometry()
            x = (screen.width() - window.width()) // 2
            y = (screen.height() - window.height()) // 2
            self.move(x, y)

    def create_driver_section(self, layout: QVBoxLayout):
        header = QLabel("Driver Installation")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        self.install_gpu_drivers = QCheckBox("Install GPU Drivers")
        self.install_gpu_drivers.setChecked(True)
        layout.addWidget(self.install_gpu_drivers)

        desc_label = QLabel("Detects your GPU and installs the appropriate drivers")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.install_chipset_drivers = QCheckBox("Install Chipset Drivers")
        self.install_chipset_drivers.setChecked(True)
        layout.addWidget(self.install_chipset_drivers)

        desc_label = QLabel("Installs the appropriate chipset drivers for your CPU")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.show_motherboard_driver_page = QCheckBox("Open Motherboard Driver Page")
        self.show_motherboard_driver_page.setChecked(True)
        layout.addWidget(self.show_motherboard_driver_page)

        desc_label = QLabel("Opens your motherboard's driver page to download additional drivers or software")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

    def create_system_section(self, layout: QVBoxLayout):
        header = QLabel("System Configuration")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        self.run_windows_tweaks = QCheckBox("Tweak Windows")
        layout.addWidget(self.run_windows_tweaks)

        desc_label = QLabel("Applies basic Windows tweaks such as disabling location services or disabling telemetry")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.save_spec_sheet = QCheckBox("Save System Spec Sheet to Desktop")
        layout.addWidget(self.save_spec_sheet)

        desc_label = QLabel("Saves a HTML file containing your system specifications to the desktop")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.generate_ai_description = QCheckBox("Generate AI Listing Description")
        layout.addWidget(self.generate_ai_description)

        desc_label = QLabel("Opens an AI description generator window with detected specs")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.activate_windows = QCheckBox("Activate Windows")
        layout.addWidget(self.activate_windows)

        desc_label = QLabel("Activate your Windows installation")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.activate_windows_panel = QWidget()
        self.activate_windows_panel.setVisible(False)
        activate_layout = QVBoxLayout(self.activate_windows_panel)
        activate_layout.setContentsMargins(25, 0, 0, 15)

        self.activation_group = QButtonGroup()

        self.activate_windows_massgrave = QRadioButton("Massgrave (Free Activation Tool)")
        self.activate_windows_massgrave.setChecked(True)
        self.activation_group.addButton(self.activate_windows_massgrave)
        activate_layout.addWidget(self.activate_windows_massgrave)

        self.activate_windows_key = QRadioButton("Authentic Key")
        self.activation_group.addButton(self.activate_windows_key)
        activate_layout.addWidget(self.activate_windows_key)

        self.authentic_key_panel = QWidget()
        self.authentic_key_panel.setVisible(False)
        key_layout = QVBoxLayout(self.authentic_key_panel)
        key_layout.setContentsMargins(25, 5, 0, 0)

        key_label = QLabel("Enter your Windows Product Key:")
        key_layout.addWidget(key_label)

        self.windows_product_key = QLineEdit()
        self.windows_product_key.setFixedWidth(300)
        self.windows_product_key.textChanged.connect(self.format_product_key)
        key_layout.addWidget(self.windows_product_key)

        activate_layout.addWidget(self.authentic_key_panel)
        layout.addWidget(self.activate_windows_panel)

    def create_app_section(self, layout: QVBoxLayout):
        header = QLabel("Application Management")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        self.run_app_installer = QCheckBox("Install Applications")
        self.run_app_installer.setChecked(True)
        layout.addWidget(self.run_app_installer)

        desc_label = QLabel("Choose applications to install on this system")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.app_installer_panel = QWidget()
        app_layout = QVBoxLayout(self.app_installer_panel)
        app_layout.setContentsMargins(25, 0, 0, 15)

        app_header = QLabel("Available Applications")
        app_header.setFont(QFont(app_header.font().family(), 10, QFont.Weight.Bold))
        app_layout.addWidget(app_header)

        self.create_app_checkboxes(app_layout)
        layout.addWidget(self.app_installer_panel)

    def _add_app_checkbox(self, layout: QVBoxLayout, app: AppDefinition):
        checkbox = QCheckBox(app.label)
        checkbox.setChecked(app.selected_by_default)
        self.app_checkboxes[app.app_id] = checkbox
        layout.addWidget(checkbox)

    def create_app_checkboxes(self, layout: QVBoxLayout):
        for app in APP_DEFINITIONS:
            if app.app_id == AppId.FURMARK:
                self.furmark_checkbox = QCheckBox(app.label)
                self.furmark_checkbox.setChecked(app.selected_by_default)
                self.app_checkboxes[app.app_id] = self.furmark_checkbox
                layout.addWidget(self.furmark_checkbox)

                self.furmark_sub_options = QWidget()
                furmark_layout = QVBoxLayout(self.furmark_sub_options)
                furmark_layout.setContentsMargins(25, 0, 0, 0)

                self.run_furmark_test = QCheckBox("Run FurMark Stress Test after installation")
                self.run_furmark_test.setChecked(True)
                furmark_layout.addWidget(self.run_furmark_test)

                desc_label = QLabel("Runs a GPU stress test using FurMark")
                desc_label.setStyleSheet("color: gray; margin-left: 25px;")
                desc_label.setWordWrap(True)
                furmark_layout.addWidget(desc_label)

                self.furmark_test_options = QWidget()
                test_layout = QVBoxLayout(self.furmark_test_options)
                test_layout.setContentsMargins(25, 0, 0, 10)

                duration_label = QLabel("Test Duration (minutes):")
                test_layout.addWidget(duration_label)

                self.furmark_duration = QLineEdit(str(FurmarkOptions().duration_minutes))
                self.furmark_duration.setFixedWidth(100)
                test_layout.addWidget(self.furmark_duration)

                resolution_label = QLabel("Resolution:")
                test_layout.addWidget(resolution_label)

                self.furmark_resolution = QComboBox()
                self.furmark_resolution.addItems([res.value for res in FurmarkResolution])
                self.furmark_resolution.setCurrentText(FurmarkResolution.P1080.value)
                self.furmark_resolution.setFixedWidth(150)
                test_layout.addWidget(self.furmark_resolution)

                aa_label = QLabel("Anti-Aliasing:")
                test_layout.addWidget(aa_label)

                self.furmark_anti_aliasing = QComboBox()
                self.furmark_anti_aliasing.addItems([aa.value for aa in FurmarkAntiAliasing])
                self.furmark_anti_aliasing.setCurrentText(FurmarkAntiAliasing.MSAA_4X.value)
                self.furmark_anti_aliasing.setFixedWidth(150)
                test_layout.addWidget(self.furmark_anti_aliasing)

                furmark_layout.addWidget(self.furmark_test_options)
                layout.addWidget(self.furmark_sub_options)
                continue

            self._add_app_checkbox(layout, app)

    def setup_connections(self):
        self.activate_windows.toggled.connect(self.activate_windows_panel.setVisible)
        self.activate_windows_key.toggled.connect(self.authentic_key_panel.setVisible)
        self.run_app_installer.toggled.connect(self.app_installer_panel.setVisible)
        self.furmark_checkbox.toggled.connect(self.toggle_furmark_options)
        self.run_furmark_test.toggled.connect(self.furmark_test_options.setVisible)

    def toggle_furmark_options(self, checked):
        self.furmark_sub_options.setVisible(checked)
        if not checked:
            self.run_furmark_test.setChecked(False)
            self.run_furmark_test.setEnabled(False)
            self.run_furmark_test.setToolTip("Enable FurMark installation to enable stress testing")
        else:
            self.run_furmark_test.setEnabled(True)
            self.run_furmark_test.setToolTip("")

    def format_product_key(self, text):
        raw = regexp.sub(r"[^A-Za-z0-9]", "", text).upper()
        raw = raw[:25]

        chunks = [raw[i:i + 5] for i in range(0, len(raw), 5)]
        formatted = "-".join(chunks)
        cursor_position = len(formatted)

        self.windows_product_key.blockSignals(True)
        self.windows_product_key.setText(formatted)
        self.windows_product_key.setCursorPosition(cursor_position)
        self.windows_product_key.blockSignals(False)

    def _parse_duration_minutes(self) -> int:
        raw = self.furmark_duration.text().strip()
        if raw.isdigit():
            return max(1, int(raw))
        return FurmarkOptions().duration_minutes

    def on_continue_clicked(self):
        options = ScriptOptions()
        options.install_gpu_drivers = self.install_gpu_drivers.isChecked()
        options.install_chipset_drivers = self.install_chipset_drivers.isChecked()
        options.show_motherboard_driver_page = self.show_motherboard_driver_page.isChecked()
        options.run_windows_tweaks = self.run_windows_tweaks.isChecked()
        options.save_spec_sheet = self.save_spec_sheet.isChecked()
        options.generate_ai_description = self.generate_ai_description.isChecked()
        options.run_app_installer = self.run_app_installer.isChecked()
        options.activate_windows = self.activate_windows.isChecked()

        if options.activate_windows:
            if self.activate_windows_massgrave.isChecked():
                options.activation_choice = ActivationChoice.MASSGRAVE
            elif self.activate_windows_key.isChecked():
                options.activation_choice = ActivationChoice.PRODUCT_KEY
                options.windows_product_key = self.windows_product_key.text()
        else:
            options.activation_choice = ActivationChoice.NONE

        options.selected_apps = {}
        for app_id, checkbox in self.app_checkboxes.items():
            options.selected_apps[app_id] = checkbox.isChecked() if options.run_app_installer else False

        if (
            options.run_app_installer
            and options.selected_apps.get(AppId.FURMARK, False)
            and self.run_furmark_test.isChecked()
        ):
            options.furmark.enabled = True
            options.furmark.duration_minutes = self._parse_duration_minutes()
            options.furmark.resolution = FurmarkResolution.from_display_text(self.furmark_resolution.currentText())
            options.furmark.anti_aliasing = FurmarkAntiAliasing.from_display_text(
                self.furmark_anti_aliasing.currentText()
            )

        self.task_options = options
        self.close()


def show_script_options_window() -> ScriptOptions:
    app = QApplication(sys.argv)
    window = ScriptOptionsWindow(font="Segoe UI")
    window.show()
    app.exec()
    return window.task_options
