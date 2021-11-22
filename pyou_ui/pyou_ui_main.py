import os
import json
from typing import Dict, Any

from PyQt5 import QtCore, QtGui, QtWidgets

from pyou_ui.custom_widgets import NavBar, VideoResult, VideoResultList, VideoFrame, WaitingSpinner, utils
from pyou_ui.stylesheet import StyleSheet


class MainWindow_UI(QtWidgets.QMainWindow):
    def __init__(self, title: str) -> None:
        super().__init__()

        self.settings = self.open_file("settings.json")

        self.style_sheet = StyleSheet(self.settings["theme"])

        # Window Attributes
        self.setWindowTitle(title)
        self.setMinimumSize(QtCore.QSize(640, 360))  # 16:9 aspect ratio
        # ----------------

        # Central Widget
        self.central_widget = QtWidgets.QWidget()
        self.central_layout = utils.set_vertical_layout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        # ----------------

        # Nav Bar
        self.nav_bar = NavBar(60, self.style_sheet)
        self.nav_bar.search_bar.setFont(utils.set_font("Roboto", 12))
        self.central_layout.addWidget(self.nav_bar)
        # ----------------

        # Content Frame
        self.content_frame = utils.add_frame(
            style_sheet=self.style_sheet.CONTENT_FRAME)
        self.content_frame_layout = utils.set_horizontal_layout(
            self.content_frame)
        self.central_layout.addWidget(self.content_frame)

        # Stacked Widget
        self.stack_widget = QtWidgets.QStackedWidget()
        self.content_frame_layout.addWidget(self.stack_widget)
        # ----------------

        # Waiting Spinner
        self.load_page = QtWidgets.QWidget()
        self.stack_widget.addWidget(self.load_page)

        self.waiting_spinner = WaitingSpinner(self.load_page)
        self.waiting_spinner.move(self.load_page.rect().center())
        # ----------------

        # Video Result List
        self.add_video_result_list()
        self.video_result = VideoResult
        self.stack_widget.setCurrentWidget(self.video_result_list)
        # ----------------

    def add_video_result_list(self) -> None:
        self.video_result_list = VideoResultList()
        self.stack_widget.addWidget(self.video_result_list)
        self.video_result_list.resize(
            QtCore.QSize(self.stack_widget.width(), self.stack_widget.height()))

    def remove_video_result_list(self) -> None:
        self.stack_widget.removeWidget(self.video_result_list)
        self.video_result_list.deleteLater()

    def add_video_result(self, video_result: VideoResult) -> None:
        self.video_result_list.video_result_frame_layout.addWidget(video_result)

    def add_video_frame(self, url: str, quality: int) -> None:
        self.video_frame = VideoFrame(url, quality)
        self.stack_widget.addWidget(self.video_frame)

    def remove_video_frame(self) -> None:
        if hasattr(self, "video_frame"):
            self.video_frame.player.terminate()
            self.stack_widget.removeWidget(self.video_frame)
            self.video_frame.deleteLater()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        # Search Bar
        self.nav_bar.search_bar.setFixedWidth((self.width() // 2) - 120)
        # ----------------

        # Search Button
        self.nav_bar.search_button.setFixedWidth(self.width() // 16)
        # ----------------

        # Waiting Spinner
        self.waiting_spinner.move(self.load_page.rect().center())
        # ----------------

        # Video Result List
        if self.stack_widget.currentIndex() != 0:
            self.video_result_list.video_result_frame_layout.update_widget()
        # ----------------

    @staticmethod
    def open_file(file: str) -> Dict[str, Any]:
        file = os.path.join(os.getcwd(), "pyou_ui", file)
        with open(file) as file_:
            return json.load(file_)
