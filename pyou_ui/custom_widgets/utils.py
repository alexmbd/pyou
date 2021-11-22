from typing import List, Optional

from PyQt5 import QtCore, QtGui, QtWidgets


# Generic UI builder functions
def set_horizontal_layout(
        widget: QtWidgets.QWidget,
        contents_margin: Optional[List[int]]=None,
        spacing: int=0) -> QtWidgets.QHBoxLayout:
    horizontal_layout = QtWidgets.QHBoxLayout(widget)

    if contents_margin is not None:
        horizontal_layout.setContentsMargins(*contents_margin)
    else:
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

    horizontal_layout.setSpacing(spacing)
    return horizontal_layout


def set_vertical_layout(
        widget: QtWidgets.QWidget,
        contents_margin: Optional[List[int]]=None,
        spacing: int=0) -> QtWidgets.QVBoxLayout:
    vertical_layout = QtWidgets.QVBoxLayout(widget)

    if contents_margin is not None:
        vertical_layout.setContentsMargins(*contents_margin)
    else:
        vertical_layout.setContentsMargins(0, 0, 0, 0)

    vertical_layout.setSpacing(spacing)
    return vertical_layout


def add_frame(
        style_sheet: Optional[str]=None,
        set_width: Optional[int]=None,
        set_height: Optional[int]=None) -> QtWidgets.QFrame:
    frame = QtWidgets.QFrame()
    if style_sheet:
        frame.setStyleSheet(style_sheet)

    if set_width and set_height:
        frame.setFixedSize(QtCore.QSize(set_width, set_height))
    elif set_width:
        frame.setFixedWidth(set_width)
    elif set_height:
        frame.setFixedHeight(set_height)

    frame.setFrameShape(QtWidgets.QFrame.NoFrame)
    return frame


def set_font(family: str, size: int, set_bold: Optional[bool]=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    font.setBold(set_bold)
    return font


def add_button(
        set_width: Optional[int]=None,
        set_height: Optional[int]=None,
        icon_path: Optional[str]=None,
        icon_size: Optional[int]=None,
        icon_color: Optional[str]=None,
        style_sheet: Optional[str]=None) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton()
    if style_sheet:
        button.setStyleSheet(style_sheet)

    if set_width and set_height:
        button.setFixedSize(QtCore.QSize(set_width, set_height))
    elif set_width:
        button.setFixedWidth(set_width)
    elif set_height:
        button.setFixedHeight(set_height)

    if icon_path:
        if icon_path.split(".")[-1] == "svg":
            button.setIcon(QtGui.QIcon(
                _fill_svg(icon_path, icon_color if icon_color else "#000000")))
        else:
            button.setIcon(QtGui.QIcon(icon_path))

        if icon_size:
            button.setIconSize(QtCore.QSize(icon_size, icon_size))

    button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    return button


def _fill_svg(svg_file_path: str, color: str) -> QtGui.QPixmap:
    img = QtGui.QPixmap(svg_file_path)
    q_painter = QtGui.QPainter(img)
    q_painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    q_painter.fillRect(img.rect(), QtGui.QColor(color))
    q_painter.end()

    return img
