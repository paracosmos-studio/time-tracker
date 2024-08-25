from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QListWidget,
    QDialog,
    QInputDialog
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from tracker import Timer
from file_handler import CSVHandler
from title_bar import CustomTitleBar
from style import Style
from project_manager import ProjectManager
from datetime import datetime, timedelta
import os
import csv

class MainWindow(QMainWindow):
    """
    Main application window for the Timer.
    """

    def __init__(self):
        super().__init__()

        self.project_manager = ProjectManager()
        self.csv_handler = CSVHandler(self.project_manager)
        self.timer = Timer()

        # Apply the custom style
        self.custom_style = Style()
        self.setStyleSheet("background:transparent;border:none;")
        self.setFont(self.custom_style.regular_font)
        self.setMaximumWidth(300)
        self.setMinimumWidth(300)
        self.setMaximumHeight(210)
        self.setMinimumHeight(210)

        self.setWindowTitle("Timer")
        
        # Remove the default title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # UI Elements
        self.timer_label = QLabel("0:00:00", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size:35px;margin-bottom:10px;color:#FFFFFF;")
        self.timer_label.setFont(self.custom_style.medium_font)

        self.toggle_button = QPushButton("START")
        self.toggle_button.setStyleSheet(
            self.custom_style.button_primary + "background-color:#A3BE8C;color:#090909;}"
        )
        self.toggle_button.clicked.connect(self.toggle_timer)
        self.toggle_button.setFont(self.custom_style.bold_font)

        self.project_combo = QComboBox()
        self.project_combo.setStyleSheet(self.custom_style.combo_box)
        self.project_combo.addItems(self.project_manager.projects)
        self.project_combo.currentTextChanged.connect(self.project_changed)
        self.project_combo.setFont(self.custom_style.regular_font)

        initial_project = self.project_combo.currentText()
        if initial_project:
            self.project_changed(initial_project)

        self.settings_button = QPushButton("Settings")
        self.view_log_button = QPushButton("Timesheet")

        self.settings_button.setStyleSheet(self.custom_style.button_navigation_left)
        self.settings_button.setFont(self.custom_style.regular_font)
        self.view_log_button.setStyleSheet(self.custom_style.button_navigation_right)
        self.view_log_button.setFont(self.custom_style.regular_font)

        # Timer Update
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timer_label)

        # Main App
        app_layout = QVBoxLayout()
        app_layout.setSpacing(5)
        app_layout.addWidget(self.timer_label)
        app_layout.addWidget(self.project_combo)
        app_layout.addWidget(self.toggle_button)

        app_sub_layout = QHBoxLayout()
        app_sub_layout.addWidget(self.settings_button)
        app_sub_layout.addWidget(self.view_log_button)
        app_layout.addLayout(app_sub_layout)

        app = QWidget()
        app.setLayout(app_layout)
        app.setStyleSheet(self.custom_style.widget + "border-top-left-radius:0px; \
                          border-top-right-radius:0px; \
                          border-bottom-left-radius:10px; \
                          border-bottom-right-radius:10px;}")

        # Set the custom title bar
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        self.setCentralWidget(app)

        # Connections
        self.settings_button.clicked.connect(self.open_settings)
        self.view_log_button.clicked.connect(self.view_log)


    def toggle_timer(self):
        if self.timer.start_time is None:
            self.start_timer()
        else:
            self.stop_timer()


    def start_timer(self):
        if self.project_combo.currentText():
            self.timer.start()
            self.update_timer.start(1000)
            self.toggle_button.setText("STOP")
            self.toggle_button.setStyleSheet(
                self.custom_style.button_primary + "background-color:#BF616A;color:#FFFFFF;}"
            )
            self.project_combo.setDisabled(True)
            self.settings_button.setDisabled(True)
        else:
            QMessageBox.warning(self, "Warning", "Please select a project first.")


    def stop_timer(self):
        end_time, total_time = self.timer.stop()
        self.update_timer.stop()

        if end_time:
            description = QInputDialog(self)
            description.setWindowTitle("Summary")
            description.setLabelText(f'Add a short summary (optional):')
            description.setStyleSheet(self.custom_style.input_dialog)
            description.setFont(self.custom_style.regular_font)
            description.setFixedWidth(300)
            description.setMaximumHeight(200)
            ok = description.exec()

            self.csv_handler.write_log_entry(
                self.project_combo.currentText(), 
                datetime.now() - total_time, 
                end_time, 
                total_time, 
                description.textValue() if ok else ""
            )

        self.toggle_button.setText("START")
        self.toggle_button.setStyleSheet(
            self.custom_style.button_primary + "background-color:#A3BE8C;color:#090909;}"
        )
        self.project_combo.setDisabled(False)
        self.settings_button.setDisabled(False)
        self.update_timer_label()


    def update_timer_label(self):
        elapsed_time = self.timer.get_elapsed_time()
        self.timer_label.setText(str(elapsed_time).split(".")[0])  # Display HH:MM:SS


    def project_changed(self, project_name):
        total_seconds = self.csv_handler.read_project_time(project_name)
        total_time = timedelta(seconds=total_seconds)
        self.timer.reset()
        self.timer.total_time = total_time
        self.update_timer_label()


    def open_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setStyleSheet(self.custom_style.dialog)

        dialog.setFixedWidth(300)
        dialog.setMinimumHeight(230)
        dialog.setMaximumHeight(280)

        layout = QVBoxLayout()
        layout.setSpacing(5)

        # Display current CSV file location
        self.path_label = QLabel("Save Directory")
        self.path_label.setFont(self.custom_style.medium_font)
        self.path_label.setStyleSheet("color:#ffffff;margin-bottom:0px;")
        layout.addWidget(self.path_label)

        self.csv_path_label = QLabel(f"{self.project_manager.csv_file_path}")
        self.csv_path_label.setFont(self.custom_style.regular_font)
        self.csv_path_label.setWordWrap(True)
        self.csv_path_label.setStyleSheet("color:#cacaca;margin-bottom:10px;")
        self.csv_path_label.setMinimumHeight(65)
        self.csv_path_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.csv_path_label)

        # Directory Change Button
        directory_button = QPushButton("Change Directory")
        directory_button.setStyleSheet(self.custom_style.button_secondary)
        directory_button.clicked.connect(self.change_directory)
        directory_button.setFont(self.custom_style.regular_font)
        layout.addWidget(directory_button)

        # Project Management
        project_button = QPushButton("Manage Projects")
        project_button.setStyleSheet(self.custom_style.button_secondary)
        project_button.clicked.connect(self.manage_projects)
        project_button.setFont(self.custom_style.regular_font)
        layout.addWidget(project_button)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(0)
        sub_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Display version
        self.version_label = QLabel(f'Version: {self.project_manager.version}')
        self.version_label.setStyleSheet("color:#5f5f5f;font-size:11px;margin-top:10px;")
        self.version_label.setFont(self.custom_style.regular_font)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_layout.addWidget(self.version_label)

        # Display Company
        self.version_label = QLabel(f'2024 © Paracosmos Studio Inc.')
        self.version_label.setStyleSheet("color:#5f5f5f;font-size:11px;margin-bottom:10px;")
        self.version_label.setFont(self.custom_style.regular_font)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_layout.addWidget(self.version_label)

        layout.addLayout(sub_layout)

        dialog.setLayout(layout)
        dialog.exec()


    def change_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            file_path = os.path.join(directory, "timesheet.csv")
            self.project_manager.set_csv_file_path(file_path)
            self.csv_handler = CSVHandler(self.project_manager)
            self.csv_path_label.setText(f"{file_path}")
            QMessageBox.information(
                self,
                "Directory Changed",
                f"CSV file location changed to: {file_path}"
            )
            self.refresh_ui()


    def manage_projects(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Projects")
        dialog.setStyleSheet(self.custom_style.dialog)
        dialog.setFixedWidth(300)
        dialog.setMinimumHeight(230)

        layout = QVBoxLayout()
        layout.setSpacing(5)

        project_list = QListWidget()
        project_list.addItems(self.project_manager.projects)
        project_list.setStyleSheet(self.custom_style.list_widget)
        project_list.setFont(self.custom_style.regular_font)

        add_button = QPushButton("Add")
        add_button.setStyleSheet(self.custom_style.button_secondary)
        add_button.setFont(self.custom_style.regular_font)
        add_button.clicked.connect(
            lambda: self.add_project(form_input.text(), project_list)
        )

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(self.custom_style.button_secondary)
        edit_button.setFont(self.custom_style.regular_font)
        edit_button.clicked.connect(
            lambda: self.edit_project(project_list.currentItem())
        )

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(self.custom_style.button_secondary)
        delete_button.setFont(self.custom_style.regular_font)
        delete_button.clicked.connect(
            lambda: self.delete_project(project_list.currentItem(), project_list)
        )

        form_input = QLineEdit()
        form_input.setStyleSheet(self.custom_style.line_edit)
        form_input.setFont(self.custom_style.regular_font)
        form_input.setPlaceholderText("Enter a new project")
        form_input.setMinimumWidth(260)

        form_layout = QVBoxLayout()
        form_layout.addWidget(form_input)
        form_layout.addWidget(add_button)
        form_layout.setSpacing(5)

        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        layout.addWidget(project_list)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec()
        self.refresh_ui()


    def add_project(self, project_name, project_list):
        if project_name:
            self.project_manager.add_project(project_name)
            project_list.addItem(project_name)
            self.project_combo.addItem(project_name)


    def edit_project(self, item):
        if item:
            input_dialog = QInputDialog(self)
            input_dialog.setWindowTitle("Edit Project")
            input_dialog.setLabelText(f'Rename "{item.text()}" to:')
            input_dialog.setStyleSheet(self.custom_style.input_dialog)
            input_dialog.setFont(self.custom_style.regular_font)
            input_dialog.setFixedWidth(300)
            input_dialog.setMaximumHeight(200)
            ok = input_dialog.exec()

            if ok:
                new_name = input_dialog.textValue()
                if new_name:
                    old_name = item.text()
                    self.project_manager.edit_project(old_name, new_name)
                    item.setText(new_name)
                    index = self.project_combo.findText(old_name)
                    if index >= 0:
                        self.project_combo.setItemText(index, new_name)
                    self.replace_project_name_in_csv(old_name, new_name)


    def replace_project_name_in_csv(self, old_name, new_name):
        temp_file_path = self.project_manager.csv_file_path + ".tmp"
        with open(self.project_manager.csv_file_path, 'r') as file, open(
            temp_file_path,
            'w',
            newline=''
        ) as temp_file:
            reader = csv.reader(file)
            writer = csv.writer(temp_file)
            for row in reader:
                if row[4] == old_name:
                    row[4] = new_name
                writer.writerow(row)
        os.replace(temp_file_path, self.project_manager.csv_file_path)


    def delete_project(self, item, project_list):
        if item:
            self.project_manager.delete_project(item.text())
            project_list.takeItem(project_list.row(item))
            index = self.project_combo.findText(item.text())
            if index >= 0:
                self.project_combo.removeItem(index)


    def view_log(self):
        csv_file_path = self.csv_handler.file_path
        if os.path.exists(csv_file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(csv_file_path))
        else:
            QMessageBox.warning(self, "Error", f"CSV file not found: {csv_file_path}")


    def refresh_ui(self):
        self.project_combo.clear()
        self.project_combo.addItems(self.project_manager.projects)


    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.setMaximumWidth(300)
            self.setMinimumWidth(300)
            self.setMaximumHeight(210)
            self.setMinimumHeight(210)
            self.timer_label.setStyleSheet("font-size:35px;margin-bottom:10px;color:#FFFFFF;")
        else:
            self.showFullScreen()
            self.setMaximumWidth(9999)
            self.setMaximumHeight(9999)
            self.timer_label.setStyleSheet("font-size:300px;margin-bottom:10px;color:#FFFFFF;")
