from PyQt5 import QtCore, QtGui, QtWidgets
import mpv


class VideoFrame(QtWidgets.QWidget):
    def __init__(self, url: str, quality: int) -> None:
        super().__init__()

        # This is necessary since PyQT stomps over the locale settings needed by libmpv.
        # This needs to happen after importing PyQT before creating the first mpv.MPV instance.
        import locale
        locale.setlocale(locale.LC_NUMERIC, 'C')

        self.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(QtCore.Qt.WA_NativeWindow)

        self.player = mpv.MPV(
            wid=str(int(self.winId())),
            ytdl=True,
            ytdl_format=f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]")
        self.player.play(url)
        self.is_playing = True

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.player.pause = self.is_playing
        self.is_playing = not self.is_playing
