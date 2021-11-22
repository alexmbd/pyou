# https://github.com/z3ntu/QtWaitingSpinner
import math
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets


class _QtWaitingSpinner(QtWidgets.QWidget):
    def __init__(
            self,
            parent: QtWidgets.QWidget,
            centerOnParent: Optional[bool]=True,
            disableParentWhenSpinning: Optional[bool]=False,
            modality: Optional[QtCore.Qt.WindowModality]=QtCore.Qt.NonModal) -> None:
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        # WAS IN initialize()
        self._color = QtGui.QColor(QtCore.Qt.black)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()
        # END initialize()

        self.setWindowModality(modality)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent: QtGui.QPaintEvent) -> None:
        self.updatePosition()
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(QtCore.Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength,
                              self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(
                i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                                          self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            painter.drawRoundedRect(QtCore.QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth), self._roundness,
                                    self._roundness, QtCore.Qt.RelativeSize)
            painter.restore()

    def start(self) -> None:
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self) -> None:
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines: int) -> None:
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length: int) -> None:
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width: int) -> None:
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius: int) -> None:
        self._innerRadius = radius
        self.updateSize()

    def color(self) -> QtGui.QColor:
        return self._color

    def roundness(self) -> float:
        return self._roundness

    def minimumTrailOpacity(self) -> float:
        return self._minimumTrailOpacity

    def trailFadePercentage(self) -> float:
        return self._trailFadePercentage

    def revolutionsPersSecond(self) -> float:
        return self._revolutionsPerSecond

    def numberOfLines(self) -> int:
        return self._numberOfLines

    def lineLength(self) -> int:
        return self._lineLength

    def lineWidth(self) -> int:
        return self._lineWidth

    def innerRadius(self) -> int:
        return self._innerRadius

    def isSpinning(self) -> bool:
        return self._isSpinning

    def setRoundness(self, roundness: float) -> None:
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color: Optional[QtGui.QColor]=QtCore.Qt.black) -> None:
        self._color = QtGui.QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond: float) -> None:
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail: float) -> None:
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity: float) -> None:
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self) -> None:
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self) -> None:
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self) -> None:
        self._timer.setInterval(
            1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self) -> None:
        if self.parentWidget() and self._centerOnParent:
            self.move(self.parentWidget().width() / 2 - self.width() / 2,
                      self.parentWidget().height() / 2 - self.height() / 2)

    def lineCountDistanceFromPrimary(self, current: int, primary: int, totalNrOfLines: int) -> int:
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(
            self,
            countDistance: int,
            totalNrOfLines: int,
            trailFadePerc: float,
            minOpacity: float,
            colorinput: QtGui.QColor) -> QtGui.QColor:
        color = QtGui.QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(
            math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color


class WaitingSpinner(_QtWaitingSpinner):
    def __init__(
            self,
            parent: QtWidgets.QWidget,
            color: Optional[QtGui.QColor]=QtGui.QColor(255, 255, 255)) -> None:
        super().__init__(parent)

        self.setRoundness(70.0)
        self.setMinimumTrailOpacity(15.0)
        self.setTrailFadePercentage(70.0)
        self.setNumberOfLines(12)
        self.setLineLength(10)
        self.setLineWidth(5)
        self.setInnerRadius(10)
        self.setRevolutionsPerSecond(1)
        self.setColor(color)
