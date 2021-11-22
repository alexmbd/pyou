import os
import json
from typing import Dict, Any


class StyleSheet:
    def __init__(self, file: str) -> None:
        self.style_sheet = self.open_file(file)
        self.generate_style_sheet()

    def generate_style_sheet(self) -> None:
        # NAVBAR STYLESHEET
        self.NAVBAR = f"""
            QFrame {{
                color: {self.style_sheet['NavBar']['color']};
                background-color: {self.style_sheet['NavBar']['background-color']};
            }}

            QLineEdit {{
                color: {self.style_sheet['NavBar']['color']};
                background-color: {self.style_sheet['NavBar']['search-bar-background-color']};
                border: 1px solid;
                border-color: {self.style_sheet['NavBar']['search-bar-border-color']};
                border-top-left-radius: 2px;
                border-bottom-left-radius: 2px;
                padding-left: 8px;
                padding-right: 8px;
            }}

            QPushButton {{
                background-color: transparent;
                border: none;
            }}
        """

        self.NAVBAR_SEARCH_BUTTON_BG_COLOR = f"""
            QPushButton {{
                background-color: {self.style_sheet['NavBar']['search-button-background-color']};
                border: none;
                border-top-right-radius: 2px;
                border-bottom-right-radius: 2px;
            }}
        """

        self.NAVBAR_ICON_COLOR = self.style_sheet['NavBar']['color']
        # ----------------

        # CONTENT FRAME STYLESHEET
        self.CONTENT_FRAME = f"""
            QFrame {{
                color: {self.style_sheet['ContentFrame']['color']};
                background-color: {self.style_sheet['ContentFrame']['background-color']};
            }}
        """
        # ----------------

        # VIDEO RESULT STYLESHEET
        self.VIDEO_RESULT = f"""
            QFrame {{
                background-color: {self.style_sheet['VideoResult']['card-background-color']};
                border-radius: 4px;
            }}
        """
        # ----------------

        # VIDEO RESULT TITLE TEXT STYLESHEET
        self.VIDEO_RESULT_TITLE_TEXT = f"""
            QLabel {{
                margin-left: 1px;
            }}
        """
        # ----------------

        # VIDEO RESULT TEXT STYLESHEET
        self.VIDEO_RESULT_TEXT = f"""
            QLabel {{
                color: {self.style_sheet['VideoResult']['channel-views-upload-date-color']};
                margin-left: 1px;
            }}
        """
        # ----------------

    @staticmethod
    def open_file(file: str) -> Dict[str, Any]:
        file = os.path.join(os.getcwd(), "pyou_ui", "themes", file)
        with open(file) as file_:
            return json.load(file_)
