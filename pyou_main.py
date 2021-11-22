import sys
from typing import Dict, Any

from PyQt5 import QtCore, QtWidgets

from pyou_ui import MainWindow_UI
from pyou import YoutubeSearch


class MainWindow(MainWindow_UI):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self.init_bindings()

    def init_bindings(self) -> None:
        self.nav_bar.setFocus()

        self.nav_bar.search_bar.returnPressed.connect(self.to_load_page)
        self.nav_bar.search_button.clicked.connect(self.to_load_page)

    def to_load_page(self) -> None:
        query = self.nav_bar.search_bar.text()
        self.stack_widget.setCurrentWidget(self.load_page)
        self.remove_video_result_list()
        self.remove_video_frame()
        self.waiting_spinner.start()
        self.start_search_thread(query, "new")

    def start_search_thread(self, query: str, action: str) -> None:
        self.thread = QtCore.QThread()
        self.worker = SearchWorker(query, action)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.search_query)
        self.worker.finished.connect(self.update_results)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.thread.finished.connect(lambda: self.display_results())

    def update_results(self, results: Dict[str, Any]) -> None:
        self.results = results

    def display_results(self) -> None:
        self.add_video_result_list()

        for item in self.results:
            result = self.video_result(
                thumbnail_path=item["thumbnail"],
                title=item["title"],
                view_count=item["viewCount"]["short"],
                upload_date=item["publishedTime"],
                channel=item["channel"]["name"],
                link=item["link"],
                channel_link=item["channel"]["link"],
                style_sheet=self.style_sheet,
                callback_func=self.selected_result)
            self.add_video_result(result)

        self.waiting_spinner.stop()
        self.stack_widget.setCurrentWidget(self.video_result_list)

    def selected_result(self, value: str) -> None:
        # self.waiting_spinner.start()
        self.add_video_frame(value, 720)
        self.stack_widget.setCurrentWidget(self.video_frame)


class SearchWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)

    def __init__(self, query: str, action: str) -> None:
        super().__init__()
        self.youtube_search = YoutubeSearch()
        self.query = query

    def search_query(self) -> None:
        results = self.youtube_search.search(self.query)
        self.finished.emit(results)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow("PYou")
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
