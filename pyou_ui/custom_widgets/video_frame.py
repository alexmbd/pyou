from PyQt5 import QtCore, QtGui, QtWidgets
import mpv


class VideoFrame(QtWidgets.QWidget):
    now_playing = QtCore.pyqtSignal()
    set_fullscreen = QtCore.pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()

        # This is necessary since PyQT stomps over the locale settings needed by libmpv.
        # This needs to happen after importing PyQT before creating the first mpv.MPV instance.
        import locale
        locale.setlocale(locale.LC_NUMERIC, "C")

        self.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(QtCore.Qt.WA_NativeWindow)

        self.is_playing = False
        self.is_fullscreen = False

    def play(self, url: str, quality: int) -> None:
        self.player = mpv.MPV(
            wid=str(int(self.winId())),
            ytdl=True,
            ytdl_format=f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]")
        self.player.play(url)
        self.start_wait_thread()

    def stop(self) -> None:
        if hasattr(self, "player"):
            self.player.terminate()
            self.is_playing = False

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.player.pause = self.is_playing
        self.is_playing = not self.is_playing

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.is_fullscreen = not self.is_fullscreen
        self.set_fullscreen.emit(self.is_fullscreen)

    def start_wait_thread(self) -> None:
        self.thread = QtCore.QThread()
        self.worker = VideoPlaybackWorker(self.player)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.wait)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.thread.finished.connect(lambda: self.now_playing.emit())
        self.is_playing = True


class VideoPlaybackWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, player: mpv.MPV) -> None:
        super().__init__()
        self.player = player

    def wait(self) -> None:
        self.player.wait_until_playing()
        self.finished.emit()
