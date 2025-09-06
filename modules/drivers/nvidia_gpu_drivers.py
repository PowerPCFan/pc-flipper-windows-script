# flake8: noqa

# Version 1.0.1
# Last Edited: 21 June 2025, 00:52 UTC
# https://github.com/PowerPCFan/Nvidia-GPU-Drivers

import sys
import requests
import json
import urllib.parse
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QComboBox, QLabel, QPushButton, 
    QProgressBar, QMessageBox, QScrollArea, 
    QFrame, QSplitter, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

NUMBER_OF_RESULTS = "5"

WINDOW_DIMENSIONS = (1280, 720)

class DriverCard(QFrame):
    driver_selected = pyqtSignal(dict)
    
    def __init__(self, driver_data, driver_number, total_drivers):
        super().__init__()
        self.driver_data = driver_data
        self.driver_info = driver_data["downloadInfo"]
        
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            DriverCard {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                margin: 4px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header with driver number and name
        header_layout = QHBoxLayout()
        
        name = urllib.parse.unquote(self.driver_info.get('Name', 'N/A'))
        version = self.driver_info.get('Version', 'N/A')
        
        driver_num_label = QLabel(f"[{driver_number}/{total_drivers}] {name} version {version}")
        driver_num_label.setFont(QFont(FONT, 10, QFont.Weight.Bold))
        header_layout.addWidget(driver_num_label)
        
        header_layout.addStretch()
        
        # Choose button
        choose_button = QPushButton("Choose This Driver")
        choose_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        choose_button.clicked.connect(self.on_choose_driver)
        header_layout.addWidget(choose_button)
        
        layout.addLayout(header_layout)
        
        # Driver details
        details_layout = QGridLayout()
        
        display_version = self.driver_info.get('DisplayVersion', 'N/A')
        release_date = self.driver_info.get('ReleaseDateTime', 'N/A')
        file_size = self.driver_info.get('DownloadURLFileSize', 'N/A')
        os_name = urllib.parse.unquote(self.driver_info.get('OSName', 'N/A'))
        language_name = urllib.parse.unquote(self.driver_info.get('LanguageName', 'N/A'))
        
        # Driver flags
        flags = []
        if self.driver_info.get('IsBeta') == '1':
            flags.append("Beta")
        if self.driver_info.get('IsWHQL') == '1':
            flags.append("WHQL")
        if self.driver_info.get('IsRecommended') == '1':
            flags.append("Recommended")
        if self.driver_info.get('IsFeaturePreview') == '1':
            flags.append("Feature Preview")
        if self.driver_info.get('IsNewest') == '1':
            flags.append("Newest")
        if self.driver_info.get('IsCRD') == '1':
            flags.append("Studio Driver")
        
        driver_type = ', '.join(flags) if flags else 'Standard'
        
        # Add details to grid
        row = 0
        details = [
            ("Name:", name),
            ("Version:", f"{version}{f' (Display Version: {display_version})' if display_version else ''}"),
            ("Release Date:", release_date),
            ("File Size:", file_size),
            ("OS:", os_name),
            ("Language:", language_name),
            ("Type:", driver_type)
        ]
        
        for label_text, value_text in details:
            label = QLabel(label_text)
            label.setFont(QFont(FONT, 9, QFont.Weight.Bold))
            value = QLabel(value_text)
            value.setWordWrap(True)
            
            details_layout.addWidget(label, row, 0, Qt.AlignmentFlag.AlignTop)
            details_layout.addWidget(value, row, 1)
            row += 1
        
        details_layout.setColumnStretch(1, 1)
        layout.addLayout(details_layout)
        
        # Store the complete driver data for return
        self.complete_driver_data = {
            'name': name,
            'version': version,
            'display_version': display_version,
            'release_date': release_date,
            'file_size': file_size,
            'os_name': os_name,
            'language_name': language_name,
            'driver_type': driver_type,
            'download_url': self.driver_info.get('DownloadURL', ''),
            'details_url': self.driver_info.get('DetailsURL', ''),
            'is_beta': self.driver_info.get('IsBeta') == '1',
            'is_whql': self.driver_info.get('IsWHQL') == '1',
            'is_recommended': self.driver_info.get('IsRecommended') == '1',
            'is_feature_preview': self.driver_info.get('IsFeaturePreview') == '1',
            'is_newest': self.driver_info.get('IsNewest') == '1',
            'is_studio_driver': self.driver_info.get('IsCRD') == '1',
        }
    
    def on_choose_driver(self):
        self.driver_selected.emit(self.complete_driver_data)

class APIWorker(QThread):
    """Worker thread for API requests to prevent GUI freezing"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, request_type, params=None):
        super().__init__()
        self.request_type = request_type
        self.params = params or {}
    
    def run(self):
        try:
            if self.request_type == "menu":
                params_str = json.dumps(self.params)
                url = f"https://gfwsl.geforce.com/nvidia_web_services/controller.php?com.nvidia.services.Drivers.getMenuArrays/{params_str}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.finished.emit({"type": "menu", "data": data})
            
            elif self.request_type == "drivers":
                response = requests.get(self.params["url"], timeout=10)
                response.raise_for_status()
                data = response.json()
                self.finished.emit({"type": "drivers", "data": data})
                
        except Exception as e:
            self.error.emit(str(e))

class NvidiaDriverLookupGUI(QMainWindow):
    driver_selected = pyqtSignal(dict)  # Signal to emit selected driver data
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NVIDIA Driver Lookup")
        # self.setGeometry(100, 100, 1400, 900)
        self.setGeometry(100, 100, *WINDOW_DIMENSIONS)
        
        # Data storage
        self.product_families = []
        self.current_series = []
        self.current_products = []
        self.os_options = []
        self.language_options = []
        
        # Worker thread
        self.worker = None
        
        # Selected driver data (for return)
        self.selected_driver_data = None
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget.setLayout(QHBoxLayout())
        
        central_widget.layout().addWidget(splitter)  # type: ignore
        
        # Left panel for controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_panel.setMinimumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        
        # Title
        title = QLabel("NVIDIA Driver Lookup")
        title.setFont(QFont(FONT, 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title)
        
        # Product Family
        left_layout.addWidget(QLabel("Product Family:"))
        self.family_combo = QComboBox()
        self.family_combo.setMaxVisibleItems(10)
        self.family_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # type: ignore
        self.family_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.family_combo.currentTextChanged.connect(self.on_family_changed)
        self.family_combo.currentIndexChanged.connect(self.update_search_button_state)
        left_layout.addWidget(self.family_combo)
        
        # Product Series
        left_layout.addWidget(QLabel("Product Series:"))
        self.series_combo = QComboBox()
        self.series_combo.setMaxVisibleItems(10)
        self.series_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # type: ignore
        self.series_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.series_combo.currentTextChanged.connect(self.on_series_changed)
        self.series_combo.currentIndexChanged.connect(self.update_search_button_state)
        left_layout.addWidget(self.series_combo)
        
        # Product
        left_layout.addWidget(QLabel("Product:"))
        self.product_combo = QComboBox()
        self.product_combo.setMaxVisibleItems(10)
        self.product_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # type: ignore
        self.product_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.product_combo.currentTextChanged.connect(self.on_product_changed)
        self.product_combo.currentIndexChanged.connect(self.update_search_button_state)
        left_layout.addWidget(self.product_combo)
        
        # Operating System
        left_layout.addWidget(QLabel("Operating System:"))
        self.os_combo = QComboBox()
        self.os_combo.setMaxVisibleItems(10)
        self.os_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # type: ignore
        self.os_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.os_combo.currentIndexChanged.connect(self.update_search_button_state)
        left_layout.addWidget(self.os_combo)
        
        # Language
        left_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.language_combo.setMaxVisibleItems(10)
        self.language_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # type: ignore
        self.language_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.language_combo.currentIndexChanged.connect(self.update_search_button_state)
        left_layout.addWidget(self.language_combo)
        
        # Search button
        self.search_button = QPushButton("Search Drivers")
        self.search_button.clicked.connect(self.search_drivers)
        self.search_button.setEnabled(False)
        left_layout.addWidget(self.search_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        left_layout.addWidget(self.status_label)
        
        # Add stretch to push everything to top
        left_layout.addStretch()
        
        # Right panel for results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("Search Results:"))
        
        # Scroll area for driver cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Container widget for driver cards
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.results_container)
        right_layout.addWidget(self.scroll_area)
        
        # Initially show a message
        self.no_results_label = QLabel("Please select your GPU, OS, and Language, and click 'Search Drivers' to begin.")
        self.no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_results_label.setStyleSheet("color: #666; font-style: italic; padding: 40px;")
        self.results_layout.addWidget(self.no_results_label)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 1050])
    
    def clear_results(self):
        while self.results_layout.count() > 0:
            child = self.results_layout.takeAt(0)
            
            if child:
                widget = child.widget()
                if widget:
                    widget.deleteLater()
    
    def show_no_results_message(self, message="No drivers found for the selected configuration."):
        """Show a message when no results are found"""
        self.clear_results()
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("color: #666; font-style: italic; padding: 40px;")
        self.results_layout.addWidget(message_label)
    
    def show_loading(self, message="Loading..."):
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText(message)
        self.search_button.setEnabled(False)
    
    def hide_loading(self):
        self.progress_bar.setVisible(False)
        self.update_search_button_state()
    
    def update_search_button_state(self):
        self.search_button.setEnabled(self.can_search())
    
    def can_search(self):
        return (
            self.family_combo.currentData() is not None and
            self.series_combo.currentData() is not None and
            self.product_combo.currentData() is not None and
            self.os_combo.currentData() is not None and
            self.language_combo.currentData() is not None
        )

    def load_initial_data(self):
        self.worker = APIWorker("menu")
        self.worker.finished.connect(self.on_initial_data_loaded)
        self.worker.error.connect(self.on_api_error)
        self.worker.start()
    
    def on_initial_data_loaded(self, result):
        data = result["data"]
        if data and len(data) >= 6:
            self.product_families = data[0] if data[0] else []
            self.os_options = data[4] if data[4] else []
            self.language_options = data[5] if data[5] else []
            
            self.populate_combo(self.family_combo, self.product_families)
            self.populate_combo(self.os_combo, self.os_options)
            self.populate_combo(self.language_combo, self.language_options)
            
            self.update_search_button_state()  # Update button state after loading
        else:
            self.status_label.setText("Failed to load initial data")
            QMessageBox.critical(self, "Error", "Failed to load initial data from NVIDIA servers")
        
        self.hide_loading()
    
    def populate_combo(self, combo, items):
        combo.clear()
        combo.addItem("Select...", None)
        for item in items:
            combo.addItem(item["menutext"], item["id"])
    
    def on_family_changed(self):
        family_id = self.family_combo.currentData()
        if family_id is None:
            self.series_combo.clear()
            self.series_combo.addItem("Select...", None)
            self.product_combo.clear()
            self.product_combo.addItem("Select...", None)
            return
        
        self.worker = APIWorker("menu", {"pt": str(family_id)})
        self.worker.finished.connect(self.on_series_data_loaded)
        self.worker.error.connect(self.on_api_error)
        self.worker.start()
    
    def on_series_data_loaded(self, result):
        data = result["data"]
        if data and len(data) > 1 and data[1]:
            self.current_series = data[1]
            self.populate_combo(self.series_combo, self.current_series)
        else:
            self.current_series = []
            self.series_combo.clear()
            self.series_combo.addItem("No series available", None)
            self.status_label.setText("No series found for selected family")
        
        # Clear products when series changes
        self.product_combo.clear()
        self.product_combo.addItem("Select...", None)
        self.update_search_button_state()  # Update button state
        self.hide_loading()
    
    def on_series_changed(self):
        family_id = self.family_combo.currentData()
        series_id = self.series_combo.currentData()
        
        if family_id is None or series_id is None:
            self.product_combo.clear()
            self.product_combo.addItem("Select...", None)
            self.update_search_button_state()  # Update button state
            return
        
        self.worker = APIWorker("menu", {"pt": str(family_id), "pst": str(series_id)})
        self.worker.finished.connect(self.on_products_data_loaded)
        self.worker.error.connect(self.on_api_error)
        self.worker.start()
    
    def on_products_data_loaded(self, result):
        data = result["data"]
        if data and len(data) > 2:
            if data[2]:
                self.current_products = data[2]
                self.populate_combo(self.product_combo, self.current_products)
            else:
                self.current_products = []
                self.product_combo.clear()
                self.product_combo.addItem("No products available", None)
                self.status_label.setText("No products found")
            
            if len(data) > 4 and data[4]:
                self.os_options = data[4]
                current_os = self.os_combo.currentData()
                self.populate_combo(self.os_combo, self.os_options)
                # Try to restore selection
                for i in range(self.os_combo.count()):
                    if self.os_combo.itemData(i) == current_os:
                        self.os_combo.setCurrentIndex(i)
                        break
            
            if len(data) > 5 and data[5]:
                self.language_options = data[5]
                current_lang = self.language_combo.currentData()
                self.populate_combo(self.language_combo, self.language_options)
                # Try to restore selection
                for i in range(self.language_combo.count()):
                    if self.language_combo.itemData(i) == current_lang:
                        self.language_combo.setCurrentIndex(i)
                        break
        else:
            self.current_products = []
            self.product_combo.clear()
            self.product_combo.addItem("No products available", None)
            self.status_label.setText("Failed to load products")
        
        self.update_search_button_state()
        self.hide_loading()
    
    def on_product_changed(self):
        # Update search button state when product selection changes
        self.update_search_button_state()
    
    def search_drivers(self):
        product_id = self.product_combo.currentData()
        os_id = self.os_combo.currentData()
        lang_id = self.language_combo.currentData()
        series_id = self.series_combo.currentData()
        
        if not all([product_id, os_id, lang_id, series_id]):
            QMessageBox.warning(self, "Warning", "Please select all options before searching")
            return
        
        dch_1_oses = ["57", "135"]  # Windows 10 64-bit and Windows 11
        
        query_url = (
            f"https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php?func=DriverManualLookup"
            f"&pfid={product_id}&psid={series_id}&osID={os_id}&languageCode={lang_id}&dch={"1" if str(os_id) in dch_1_oses else "0"}&dltype=-1&numberOfResults={NUMBER_OF_RESULTS}"
        )
        
        self.show_loading("Searching for drivers...")
        self.clear_results()
        
        self.worker = APIWorker("drivers", {"url": query_url})
        self.worker.finished.connect(self.on_drivers_loaded)
        self.worker.error.connect(self.on_api_error)
        self.worker.start()
    
    def on_driver_card_selected(self, driver_data):
        self.selected_driver_data = driver_data
        self.driver_selected.emit(driver_data)
        
        # Show confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Driver Selected")
        msg.setText(f"Selected driver: {driver_data['name']}")
        msg.setDetailedText(
            f"Version: {driver_data['version']}\n"
            f"Release Date: {driver_data['release_date']}\n"
            f"Type: {driver_data['driver_type']}\n"
            f"Download URL: {driver_data['download_url']}"
        )
        msg.exec()
        
        # Close the application and return the data
        self.close()
    
    def on_drivers_loaded(self, result):
        data = result["data"]
        self.display_results(data)

        self.show_loading("Drivers loaded")
        self.hide_loading()
    
    def display_results(self, data):
        if not data or not data.get("Success") or not data.get("IDS"):
            self.show_no_results_message()
            return

        drivers = data["IDS"]
        num_drivers = len(drivers)
        
        self.clear_results()
        
        header_label = QLabel(f"{num_drivers} Result{'s' if num_drivers > 1 else ''}")
        header_label.setFont(QFont(FONT, 14, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #0078d4; padding: 10px; border-bottom: 2px solid #0078d4;")
        self.results_layout.addWidget(header_label)
        
        for idx, driver_entry in enumerate(drivers, 1):
            driver_card = DriverCard(driver_entry, idx, num_drivers)
            driver_card.driver_selected.connect(self.on_driver_card_selected)
            self.results_layout.addWidget(driver_card)
        
        self.results_layout.addStretch()
    
    def get_selected_driver_data(self):
        return self.selected_driver_data
    
    def on_api_error(self, error_message):
        self.hide_loading()
        self.status_label.setText(f"Error: {error_message}")
        QMessageBox.critical(self, "API Error", f"Failed to communicate with NVIDIA servers:\n{error_message}")

def main() -> dict | None:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    global FONT; FONT = app.font().family()
    
    window = NvidiaDriverLookupGUI()
    
    selected_driver: dict | None = None
    
    def on_driver_selected(driver_data):
        nonlocal selected_driver
        selected_driver = driver_data
        app.quit()
    
    window.driver_selected.connect(on_driver_selected)
    
    window.show()
    app.exec()
    
    return selected_driver

if __name__ == "__main__":
    try:
        result = main()
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")