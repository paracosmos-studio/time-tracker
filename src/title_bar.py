from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QIcon
from style import Style
import sys
import os


class CustomTitleBar(QWidget):
    def __init__(self, parent=None, allow_fullscreen=True):
        super().__init__(parent)
        self.parent = parent
        self.custom_style = Style()

        if getattr(sys, 'frozen', False):
            script_dir = sys._MEIPASS
            close_icon = os.path.join(script_dir, 'resources/close.svg')
            minimize_icon = os.path.join(script_dir, 'resources/minimize.svg')
            fullscreen_icon = os.path.join(script_dir, 'resources/fullscreen.svg')
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            close_icon = os.path.join(script_dir, '../resources/close.svg')
            minimize_icon = os.path.join(script_dir, '../resources/minimize.svg')
            fullscreen_icon = os.path.join(script_dir, '../resources/fullscreen.svg')

        # Variables to track dragging
        self.dragging = False
        self.drag_start_position = QPoint()

        # Add custom styling to the title bar
        self.setFixedHeight(30)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            background-color:#090909;
            border-top-left-radius:10px;
            border-top-right-radius:10px;
            border: none;
        """)

        # Create title bar layout
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 10, 0, 0)
        title_bar_layout.setSpacing(3)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add close button to the title bar
        close_button = QPushButton()
        close_button.setIcon(QIcon(close_icon))
        close_button.setIconSize(QSize(10, 10))
        close_button.setStyleSheet(self.custom_style.button_title_bar + "background-color:#BF616A;}")
        close_button.setFont(self.custom_style.bold_font)

        # Add minimize button to the title bar
        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(minimize_icon))
        minimize_button.setIconSize(QSize(10, 10))
        minimize_button.setStyleSheet(self.custom_style.button_title_bar + "background-color:#EBCB8B;}")
        minimize_button.setFont(self.custom_style.bold_font)

        # Add buttons to layout
        title_bar_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignLeft)
        title_bar_layout.addWidget(minimize_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(title_bar_layout)

        # Connect button functionality
        close_button.clicked.connect(self.parent.close)
        minimize_button.clicked.connect(self.parent.showMinimized)

        # Add fullscreen button to the title bar
        if allow_fullscreen:
            fullscreen_button = QPushButton()
            fullscreen_button.setIcon(QIcon(fullscreen_icon))
            fullscreen_button.setIconSize(QSize(10, 10))
            fullscreen_button.setStyleSheet(self.custom_style.button_title_bar + "background-color:#A3BE8C;}")
            fullscreen_button.setFont(self.custom_style.bold_font)
            
            title_bar_layout.addWidget(fullscreen_button, alignment=Qt.AlignmentFlag.AlignLeft)
            fullscreen_button.clicked.connect(self.parent.toggle_fullscreen)

        # Enable dragging from the custom title bar
        self.mousePressEvent = self.mouse_press_event
        self.mouseMoveEvent = self.mouse_move_event
        self.mouseReleaseEvent = self.mouse_release_event


    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()


    def mouse_move_event(self, event):
        if self.dragging:
            self.parent.move(event.globalPosition().toPoint() - self.drag_start_position)
            event.accept()


    def mouse_release_event(self, event):
        self.dragging = False
