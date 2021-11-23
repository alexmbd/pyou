from typing import Optional, Any, Callable

from PyQt5 import QtCore, QtGui, QtWidgets

from pyou_ui.custom_widgets import utils


class VideoResult(QtWidgets.QFrame):
    def __init__(
            self,
            children_width: int,
            children_height: int,
            thumbnail_path: str,
            title: str,
            view_count: str,
            upload_date: str,
            channel: str,
            link: str,
            channel_link: str,
            style_sheet: Any,
            callback_func: Callable[[str], None]) -> None:
        super().__init__()

        self.setStyleSheet(style_sheet.VIDEO_RESULT)

        self.setFixedSize(QtCore.QSize(
            children_width, children_height + (children_height // 2.75)))

        self.video_result_layout = utils.set_vertical_layout(self)

        # Thumbnail Result
        # 16:9 aspect ratio
        self.thumbnail_button = _ClickableLabel(
            children_width, children_height, thumbnail_path=thumbnail_path, emitted_value=link)
        self.thumbnail_button.setStyleSheet("margin-bottom: 4px;")
        # ----------------

        class _VideoResultMetaDataFrame(QtWidgets.QFrame):
            def __init__(
                    self,
                    title_font: QtGui.QFont,
                    text_font: QtGui.QFont,
                    style_sheet: Any) -> None:
                super().__init__()

                width_ = children_width - 14
                height_ = children_height // 2.75

                self.setFixedSize(QtCore.QSize(width_, height_))

                self.meta_data_frame_layout = utils.set_vertical_layout(self)

                self.video_title_button = _ClickableLabel(
                    width_, height_ // 3, text=self.format_text(title), 
                    tooltip_text=title, font=title_font, emitted_value=link)
                self.video_title_button.setStyleSheet(
                    style_sheet.VIDEO_RESULT_TITLE_TEXT)

                self.meta_data_frame_layout.addWidget(
                    self.video_title_button)
                # ----------------

                self.channel_button = _ClickableLabel(
                    width_, height_ // 3, text=self.format_text(channel), 
                    tooltip_text=channel, font=text_font, emitted_value=channel_link)
                self.channel_button.setStyleSheet(style_sheet.VIDEO_RESULT_TEXT)

                self.meta_data_frame_layout.addWidget(self.channel_button)
                # ----------------

                self.view_count_upload_date_frame = utils.add_frame(
                    set_width=width_, set_height=height_ // 3)
                self.view_count_upload_date_frame_layout = utils.set_horizontal_layout(
                    self.view_count_upload_date_frame)
                self.view_count_upload_date_frame_layout.setAlignment(
                    QtCore.Qt.AlignLeft)

                self.view_count_button = _ClickableLabel(
                    (len(view_count) + int(width_ * 0.22)), height_ // 3, text=view_count, 
                    tooltip_text=view_count, font=text_font, emitted_value=link)
                self.view_count_button.setStyleSheet(style_sheet.VIDEO_RESULT_TEXT)

                self.upload_date_button = _ClickableLabel(
                    (len(upload_date) + int(width_ * 0.4)), height_ // 3, text=upload_date, 
                    tooltip_text=upload_date, font=text_font, emitted_value=link)
                self.upload_date_button.setStyleSheet(style_sheet.VIDEO_RESULT_TEXT)

                self.view_count_upload_date_frame_layout.addWidget(
                    self.view_count_button)
                self.view_count_upload_date_frame_layout.addWidget(
                    self.upload_date_button)

                self.meta_data_frame_layout.addWidget(
                    self.view_count_upload_date_frame)
                # ----------------

            @staticmethod
            def format_text(text: str) -> str:
                if len(text) > 25:
                    text = f"{text[:24]}..."
                return text

        # Text Result
        self.video_result_meta_data_frame = _VideoResultMetaDataFrame(
            utils.set_font("Roboto", 14), utils.set_font("Roboto", 10), style_sheet)

        self.video_result_layout.addWidget(self.thumbnail_button)
        self.video_result_layout.addWidget(self.video_result_meta_data_frame)
        # ----------------

        # Bind ClickableLabels to callback_func
        self.thumbnail_button.clicked.connect(callback_func)
        self.video_result_meta_data_frame.video_title_button.clicked.connect(callback_func)
        self.video_result_meta_data_frame.channel_button.clicked.connect(callback_func)
        self.video_result_meta_data_frame.view_count_button.clicked.connect(callback_func)
        self.video_result_meta_data_frame.upload_date_button.clicked.connect(callback_func)
        # ----------------


class _ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    def __init__(
            self,
            width_: int,
            height_: int,
            text: Optional[str]=None,
            tooltip_text: Optional[str]=None,
            font: Optional[QtGui.QFont]=None,
            thumbnail_path: Optional[str]=None,
            emitted_value: Optional[Any]=None) -> None:
        super().__init__()

        self.width_ = width_
        self.height_ = height_
        self.thumbnail_path = thumbnail_path
        self.emitted_value = emitted_value

        self.setFixedSize(width_, height_)

        self.setText(text)
        self.setToolTip(tooltip_text)

        if font:
            self.setFont(font)

        if thumbnail_path:
            self.add_image()

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def add_image(self) -> None:
        pixmap = QtGui.QPixmap(self.thumbnail_path)
        pixmap = pixmap.scaled(
            self.width_, self.height_, transformMode=QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.clicked.emit(self.emitted_value)
