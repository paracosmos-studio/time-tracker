from PyQt6.QtGui import QFont, QFontDatabase
import os
import sys

class Style:
    """
    Class to manage the application's style.  

    Note that some of the styles are missing `}` at the end. It was
    done intentionally to allow for further customization of the
    styles in the `interface.py` module.
    """

    def __init__(self):
        super().__init__()

        # Determine if the application is running as a bundled executable
        if getattr(sys, 'frozen', False):
            script_dir = sys._MEIPASS
            font_dir = os.path.join(script_dir, 'resources/fonts')
            dropdown_icon = os.path.join(script_dir, 'resources/dropdown.svg')
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            font_dir = os.path.join(script_dir, '../resources/fonts')
            dropdown_icon = os.path.join(script_dir, '../resources/dropdown.svg')

        self.regular_font_id = QFontDatabase.addApplicationFont(os.path.join(font_dir, "satoshi_regular.otf"))
        self.medium_font_id = QFontDatabase.addApplicationFont(os.path.join(font_dir, "satoshi_medium.otf"))
        self.bold_font_id = QFontDatabase.addApplicationFont(os.path.join(font_dir, "satoshi_bold.otf"))

        if self.regular_font_id == -1:
            print("Failed to load font.")

        font_family = QFontDatabase.applicationFontFamilies(self.regular_font_id)[0]
        self.regular_font = QFont(font_family)
        self.bold_font = QFont(font_family, weight=QFont.Weight.Bold)
        self.medium_font = QFont(font_family, weight=QFont.Weight.Medium)

        self.button_primary = """
            QPushButton {
                border: none;
                padding: 10px 5px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 15px;
        """
        self.button_secondary = """
            QPushButton {
                background-color: #383838;
                color: #CACACA;
                border: none;
                padding: 6px 4px;
                border-radius: 4px;
                font-size: 13px;
            }
        """
        self.button_title_bar = """
            QPushButton {
                color: #FFFFFF;
                border: none;
                padding: 0px;
                border-radius: 8px;
                font-size: 10px;
                width: 16px;
                height: 16px;
                margin: 0;
        """
        self.button_navigation_left = """
            QPushButton {
                background-color: none;
                color: #CACACA;
                border: none;
                padding: 10px 0px 5px 0px;
                border-radius: 4px;
                font-size: 13px;
                text-align: left;
            }
        """
        self.button_navigation_right = """
            QPushButton {
                background-color: none;
                color: #CACACA;
                border: none;
                padding: 10px 0px 5px 0px;
                border-radius: 4px;
                font-size: 13px;
                text-align: right;
            }
        """
        self.combo_box = f"""
            QComboBox {{
                background-color: #383838;
                color: #CACACA;
                border: none;
                padding: 5px 8px;
                border-radius: 4px;
                font-size: 14px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #383838;
                color: #ffffff;
                padding: 5px 1px;
                border: 1px solid #4F4F4F;
                border-radius: 4px;
                margin: 0px;
            }}
            QComboBox::drop-down {{
                padding-right: 8px;
                border: none;
                border-radius: 4px;
            }}
            QComboBox::down-arrow {{
                image: url({dropdown_icon});
            }}
        """
        self.widget = """
            QWidget {
                background-color: #090909;
                color: #CACACA;
        """
        self.dialog = """
            QDialog {
                background-color: #090909;
                color: #CACACA;
            }
        """
        self.list_widget = """
            QListWidget {
                background-color: #090909;
                color: #CACACA;
                border: 1px solid #383838;
                border-radius: 4px;
                font-size: 15px;
            }
            QListWidget::item {
                padding: 2px 1px;
            }
            QListWidget::item:selected {
                background-color: #EBCB8B;
                color: #090909;
            }
            QScrollBar:vertical {
                border: none;
                border-left: 1px solid #090909;
                background: #383838;
                width: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #A3BE8C;
                min-height: 0px;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        self.line_edit = """
            QLineEdit {
                border: 1px solid #383838;
                color: #CACACA;
                padding: 5px;
                border-radius: 4px;
                font-size: 15px;
                margin-top: 10px;
            }
        """
        self.input_dialog = """
            QInputDialog {
                background-color: #090909;
                color: #CACACA;
                width: 300px;
                max-height: 200px;
            }
            QInputDialog QLineEdit {
                border: 1px solid #383838;
                color: #CACACA;
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
            }
        """