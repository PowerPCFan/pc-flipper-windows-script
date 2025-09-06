import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QCheckBox, QPushButton,
    QScrollArea, QFrame, QLineEdit, QRadioButton,
    QButtonGroup, QComboBox
)
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFont, QScreen
import re as regexp

# i hate this code


class ScriptOptionsWindow(QMainWindow):
    def __init__(self, font="Segoe UI"):
        super().__init__()
        # self.task_options: dict[str, str | bool | dict] = {}
        self.task_options: dict[str, str | bool | dict] = {
            "install_gpu_drivers": False,
            "install_chipset_drivers": False,
            "show_motherboard_driver_page": False,
            "run_windows_tweaks": False,
            "save_spec_sheet": False,
            "run_app_installer": False,
            "apps": {},
            "activate_windows": False,
            "activate_windows_massgrave": False,
            "activate_windows_key": False,
            "windows_product_key": "",
            "run_furmark_test": False,
            "furmark_duration": "",
            "furmark_resolution": "",
            "furmark_anti_aliasing": ""
        }

        self.init_ui(font)
        self.setup_connections()

    def init_ui(self, font):
        self.setWindowTitle("Script Options")

        self.setMinimumSize(500, 400)
        self.resize(850, 650)

        self.setStyleSheet(f"font-family: {font};")

        # Center the window
        self.center_window()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("Script Options")
        title_label.setFont(QFont(font, 16, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Select the tasks you would like to run.")
        subtitle_label.setFont(QFont(font, 10, QFont.Weight.Bold))
        main_layout.addWidget(subtitle_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.Box)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        self.create_driver_section(scroll_layout)
        self.create_system_section(scroll_layout)
        self.create_app_section(scroll_layout)

        # consumes extra vertical space to preserve layout
        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Continue button
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
        # Driver Installation header
        header = QLabel("Driver Installation")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        # GPU Drivers
        self.install_gpu_drivers = QCheckBox("Install GPU Drivers")
        self.install_gpu_drivers.setChecked(True)
        layout.addWidget(self.install_gpu_drivers)

        desc_label = QLabel("Detects your GPU and installs the appropriate drivers")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Chipset Drivers
        self.install_chipset_drivers = QCheckBox("Install Chipset Drivers")
        self.install_chipset_drivers.setChecked(True)
        layout.addWidget(self.install_chipset_drivers)

        desc_label = QLabel("Installs the appropriate chipset drivers for your CPU")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Motherboard Driver Page
        self.show_motherboard_driver_page = QCheckBox("Open Motherboard Driver Page")
        self.show_motherboard_driver_page.setChecked(True)
        layout.addWidget(self.show_motherboard_driver_page)

        desc_label = QLabel("Opens your motherboard's driver page to download additional drivers or software")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

    def create_system_section(self, layout: QVBoxLayout):
        # System Configuration header
        header = QLabel("System Configuration")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        # Windows Tweaks
        self.run_windows_tweaks = QCheckBox("Tweak Windows")
        layout.addWidget(self.run_windows_tweaks)

        desc_label = QLabel("Applies basic Windows tweaks such as disabling location services or disabling telemetry")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Spec sheet
        self.save_spec_sheet = QCheckBox("Save System Spec Sheet to Desktop")
        layout.addWidget(self.save_spec_sheet)

        desc_label = QLabel("Saves a HTML file containing your system specifications to the desktop")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Windows Activation
        self.activate_windows = QCheckBox("Activate Windows")
        layout.addWidget(self.activate_windows)

        desc_label = QLabel("Activate your Windows installation")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Windows Activation Panel
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

        # Authentic Key Panel
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
        # Application Management header
        header = QLabel("Application Management")
        header.setFont(QFont(header.font().family(), 12, QFont.Weight.Bold))
        layout.addWidget(header)

        # Install Applications
        self.run_app_installer = QCheckBox("Install Applications")
        self.run_app_installer.setChecked(True)
        layout.addWidget(self.run_app_installer)

        desc_label = QLabel("Choose applications to install on this system")
        desc_label.setStyleSheet("color: gray; margin-left: 25px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # App Installer Panel
        self.app_installer_panel = QWidget()
        app_layout = QVBoxLayout(self.app_installer_panel)
        app_layout.setContentsMargins(25, 0, 0, 15)

        app_header = QLabel("Available Applications")
        app_header.setFont(QFont(app_header.font().family(), 10, QFont.Weight.Bold))
        app_layout.addWidget(app_header)

        # Create application checkboxes
        self.create_app_checkboxes(app_layout)
        layout.addWidget(self.app_installer_panel)

    def create_app_checkboxes(self, layout: QVBoxLayout):
        # recommended apps - checked by default
        apps = [
            ("redist", "Visual C++ Redist Runtimes (Recommended)", True),
            ("dotnet", "Microsoft .NET Runtimes (Recommended)", True),
            ("sevenzip", "7-Zip (Recommended)", True),
        ]

        self.app_checkboxes: dict[str, QCheckBox] = {}

        for app_id, app_name, checked in apps:
            checkbox = QCheckBox(app_name)
            checkbox.setChecked(checked)
            self.app_checkboxes[app_id] = checkbox
            layout.addWidget(checkbox)

        # FurMark with special handling
        self.furmark_checkbox = QCheckBox("FurMark (Recommended)")
        self.furmark_checkbox.setChecked(True)
        self.app_checkboxes["furmark"] = self.furmark_checkbox
        layout.addWidget(self.furmark_checkbox)

        # FurMark sub-options
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

        # FurMark test options
        self.furmark_test_options = QWidget()
        test_layout = QVBoxLayout(self.furmark_test_options)
        test_layout.setContentsMargins(25, 0, 0, 10)

        # Duration
        duration_label = QLabel("Test Duration (minutes):")
        test_layout.addWidget(duration_label)

        self.furmark_duration = QLineEdit("5")
        self.furmark_duration.setFixedWidth(100)
        test_layout.addWidget(self.furmark_duration)

        # Resolution
        resolution_label = QLabel("Resolution:")
        test_layout.addWidget(resolution_label)

        self.furmark_resolution = QComboBox()
        self.furmark_resolution.addItems([
            "720p (1280x720)",
            "1080p (1920x1080)",
            "1440p (2560x1440)"
        ])
        self.furmark_resolution.setCurrentIndex(1)
        self.furmark_resolution.setFixedWidth(150)
        test_layout.addWidget(self.furmark_resolution)

        # Anti-Aliasing
        aa_label = QLabel("Anti-Aliasing:")
        test_layout.addWidget(aa_label)

        self.furmark_anti_aliasing = QComboBox()
        self.furmark_anti_aliasing.addItems([
            "None",
            "MSAA 2x",
            "MSAA 4x",
            "MSAA 8x"
        ])
        self.furmark_anti_aliasing.setCurrentIndex(2)
        self.furmark_anti_aliasing.setFixedWidth(150)
        test_layout.addWidget(self.furmark_anti_aliasing)

        furmark_layout.addWidget(self.furmark_test_options)
        layout.addWidget(self.furmark_sub_options)

        # the rest of the apps
        other_apps = [
            ("firefox", "Firefox", False),
            ("chrome", "Chrome", False),
            ("steam", "Steam", False),
            ("discord", "Discord", False),
            ("epic_games_launcher", "Epic Games Launcher", False),
            ("openrgb", "OpenRGB", False),
            ("signalrgb", "SignalRGB", False),
            ("vlc", "VLC Media Player", False),
            ("malwarebytes", "Malwarebytes", False),
            ("hwmonitor", "HWMonitor", False),
            ("msi_afterburner", "MSI Afterburner", False),
            ("occt", "OCCT", False),
            ("cinebench", "Cinebench R23", False),
            ("crystaldiskmark", "CrystalDiskMark", False),
            ("crystaldiskinfo", "CrystalDiskInfo", False),
            ("aida64", "AIDA64", False),
            ("fancontrol", "FanControl", False),
            ("cpuz", "CPU-Z", False),
            ("gpuz", "GPU-Z", False),
            ("heaven", "Unigine Heaven Benchmark", False),
            ("valley", "Unigine Valley Benchmark", False),
            ("superposition", "Unigine Superposition Benchmark", False),
            ("revo", "Revo Uninstaller", False),
        ]

        for app_id, app_name, checked in other_apps:
            checkbox = QCheckBox(app_name)
            checkbox.setChecked(checked)
            self.app_checkboxes[app_id] = checkbox
            layout.addWidget(checkbox)

    def setup_connections(self):
        # Windows activation panel visibility
        self.activate_windows.toggled.connect(self.activate_windows_panel.setVisible)

        # Authentic key panel visibility
        self.activate_windows_key.toggled.connect(self.authentic_key_panel.setVisible)

        # App installer panel visibility
        self.run_app_installer.toggled.connect(self.app_installer_panel.setVisible)

        # FurMark sub-options visibility
        self.furmark_checkbox.toggled.connect(self.toggle_furmark_options)

        # FurMark test options visibility
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
        # Remove non-alphanumeric characters and convert to uppercase
        raw = regexp.sub(r'[^A-Za-z0-9]', '', text).upper()
        raw = raw[:25]  # Limit to 25 characters

        # Split into chunks of 5
        chunks = [raw[i: i + 5] for i in range(0, len(raw), 5)]
        formatted = '-'.join(chunks)
        cursor_position = len(formatted)

        # update text field
        self.windows_product_key.blockSignals(True)  # stop input temporarily
        self.windows_product_key.setText(formatted)  # update text to the formatted string
        self.windows_product_key.setCursorPosition(cursor_position)  # set cursor position to the end of string
        self.windows_product_key.blockSignals(False)  # re-enable input

    def on_continue_clicked(self):
        # Collect all options
        self.task_options = {
            "install_gpu_drivers": self.install_gpu_drivers.isChecked(),
            "install_chipset_drivers": self.install_chipset_drivers.isChecked(),
            "show_motherboard_driver_page": self.show_motherboard_driver_page.isChecked(),
            "run_windows_tweaks": self.run_windows_tweaks.isChecked(),
            "save_spec_sheet": self.save_spec_sheet.isChecked(),
            "run_app_installer": self.run_app_installer.isChecked(),
            "activate_windows": self.activate_windows.isChecked(),
        }

        # Windows activation options
        if self.activate_windows.isChecked():
            self.task_options["activate_windows_massgrave"] = self.activate_windows_massgrave.isChecked()
            self.task_options["activate_windows_key"] = self.activate_windows_key.isChecked()
            if self.activate_windows_key.isChecked():
                self.task_options["windows_product_key"] = self.windows_product_key.text()
        else:
            self.task_options["activate_windows_massgrave"] = False
            self.task_options["activate_windows_key"] = False
            self.task_options["windows_product_key"] = ""

        self.task_options["apps"] = {}

        # Application installation options
        if self.run_app_installer.isChecked():
            for app_id, checkbox in self.app_checkboxes.items():
                self.task_options["apps"][app_id] = checkbox.isChecked()

            # FurMark specific options
            if self.furmark_checkbox.isChecked():
                self.task_options["run_furmark_test"] = self.run_furmark_test.isChecked()
                if self.run_furmark_test.isChecked():
                    self.task_options["furmark_duration"] = self.furmark_duration.text()
                    self.task_options["furmark_resolution"] = self.furmark_resolution.currentText()
                    self.task_options["furmark_anti_aliasing"] = self.furmark_anti_aliasing.currentText()
            else:
                self.task_options["run_furmark_test"] = False
                self.task_options["furmark_duration"] = ""
                self.task_options["furmark_resolution"] = ""
                self.task_options["furmark_anti_aliasing"] = ""
        else:
            # Clear all app options if app installer is unchecked
            for app_id in self.app_checkboxes.keys():
                self.task_options["apps"][app_id] = False
            self.task_options["run_furmark_test"] = False
            self.task_options["furmark_duration"] = ""
            self.task_options["furmark_resolution"] = ""
            self.task_options["furmark_anti_aliasing"] = ""

        self.close()


def show_script_options_window():
    """
    Shows the GUI window for selecting script options.

    :return: The task options selected by the user, in a Python dictionary

    ## Example usage
    ```python
    import modules.ui as ui
    options = ui.show_script_options_window()
    print(options)  # prints the selected options as a dictionary
    ```

    """
    app = QApplication(sys.argv)
    window = ScriptOptionsWindow(font="Segoe UI")
    window.show()
    app.exec()
    return window.task_options
