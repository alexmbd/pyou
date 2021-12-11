from PyQt5 import QtWidgets

from pyou_ui.custom_widgets import utils


class VideoResultList(QtWidgets.QScrollArea):
    def __init__(self, widget_width: int) -> None:
        super().__init__()

        self.setWidgetResizable(True)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.video_result_frame = utils.add_frame()
        self.video_result_frame_layout = _GridLayout(
            self, self.video_result_frame, widget_width)
        self.setWidget(self.video_result_frame)


class _GridLayout(QtWidgets.QGridLayout):
    def __init__(self, parent_: QtWidgets.QWidget, widget_: QtWidgets.QWidget, widget_width: int) -> None:
        super().__init__(widget_)

        self.parent_ = parent_
        self.widget_width = widget_width
        self.widget_list = []

        self.setVerticalSpacing(40)

    def addWidget(self, widget: QtWidgets.QWidget) -> None:
        if len(self.widget_list) == 0:
            self._add_new_row(widget, 0)
            return

        current_row = len(self.widget_list) - 1
        if not self._can_add_to_current_row(current_row):
            self._add_new_row(widget, current_row + 1)
            return

        self.widget_list[current_row].append(widget)
        super().addWidget(
            widget, current_row, len(self.widget_list[current_row]))

    def clear_widget(self) -> None:
        self.widget_list = []
        self._remove_widgets()

    def update_widget(self) -> None:
        self._remove_widgets()

        widget_list_copy = [
            widget for row in self.widget_list for widget in row]
        self.widget_list = []

        for widget in widget_list_copy:
            self.addWidget(widget)

    def _add_new_row(self, widget: QtWidgets.QWidget, row: int) -> None:
        self.widget_list.append([widget])
        super().addWidget(widget, row, 0)

    def _can_add_to_current_row(self, row: int) -> bool:
        parent_width = self.parent_.width() - 2
        total_widget_len = (len(self.widget_list[row]) + 1) * self.widget_width

        return (parent_width - total_widget_len) > 104

    def _remove_widgets(self) -> None:
        for index in reversed(range(self.count())):
            item = self.itemAt(index).widget()
            self.removeWidget(item)
            item.setParent(None)
