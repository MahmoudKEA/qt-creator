from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Union
from .quicktooltip import QuickToolTip, QuickToolTipMessage


class QSwitch(QAbstractButton):
    def __init__(self, parent=None, track_radius=10, thumb_radius=8):
        super(QSwitch, self).__init__(parent=parent)

        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        self.__trackRadius = track_radius
        self.__thumbRadius = thumb_radius

        self.__margin = max(0, self.__thumbRadius - self.__trackRadius)
        self.__baseOffset = max(self.__thumbRadius, self.__trackRadius)
        self.__endOffset = {
            True: lambda: self.width() - self.__baseOffset,
            False: lambda: self.__baseOffset,
        }
        self.__offset = self.__baseOffset

        palette = self.palette()
        if self.__thumbRadius > self.__trackRadius:
            self.__trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self.__thumbColor = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self.__trackOpacity = 0.5
        else:
            self.__trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self.__thumbColor = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self.__trackOpacity = 1

    @pyqtProperty(int)
    def offset(self) -> int:
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self.__offset = value
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(
            (4 * self.__trackRadius) + (2 * self.__margin),
            (2 * self.__trackRadius) + (2 * self.__margin),
        )

    def setChecked(self, checked: bool):
        super(QSwitch, self).setChecked(checked)
        self.offset = self.__endOffset[checked]()

    def resizeEvent(self, a0: QResizeEvent):
        super(QSwitch, self).resizeEvent(a0)
        self.offset = self.__endOffset[self.isChecked()]()

    def paintEvent(self, e: QPaintEvent):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(Qt.PenStyle.NoPen)

        track_opacity = self.__trackOpacity
        thumb_opacity = 1.0
        if self.isEnabled():
            track_brush = self.__trackColor[self.isChecked()]
            thumb_brush = self.__thumbColor[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self.__margin,
            self.__margin,
            self.width() - (2 * self.__margin),
            self.height() - (2 * self.__margin),
            self.__trackRadius,
            self.__trackRadius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset - self.__thumbRadius,
            self.__baseOffset - self.__thumbRadius,
            2 * self.__thumbRadius,
            2 * self.__thumbRadius
        )

    def mouseReleaseEvent(self, e: QMouseEvent):
        super(QSwitch, self).mouseReleaseEvent(e)

        if e.button() == Qt.MouseButton.LeftButton:
            animation = QPropertyAnimation(self, QByteArray(b'offset'), self)
            animation.setDuration(200)
            animation.setStartValue(self.offset)
            animation.setEndValue(self.__endOffset[self.isChecked()]())
            animation.start()

    def set_track_color_on(self, color: QColor):
        self.__trackColor[True] = color

    def set_thumb_color_on(self, color: QColor):
        self.__thumbColor[True] = color

    def set_track_color_off(self, color: QColor):
        self.__trackColor[False] = color

    def set_thumb_color_off(self, color: QColor):
        self.__thumbColor[False] = color


class QuickSwitch(QSwitch):
    def __init__(
            self, parent=None,
            checked: bool = False,
            track_radius=10,
            thumb_radius=8,
            track_color_on: QColor = None,
            thumb_color_on: QColor = None,
            track_color_off: QColor = None,
            thumb_color_off: QColor = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
            cursor: Qt.CursorShape = Qt.CursorShape.PointingHandCursor,
            object_name: str = None,
            tooltip: Union[QuickToolTip, QuickToolTipMessage] = None
    ):
        super(QuickSwitch, self).__init__(
            parent, track_radius=track_radius, thumb_radius=thumb_radius
        )

        if checked:
            self.setChecked(True)

        if track_color_on:
            self.set_track_color_on(track_color_on)

        if thumb_color_on:
            self.set_thumb_color_on(thumb_color_on)

        if track_color_off:
            self.set_track_color_off(track_color_off)

        if thumb_color_off:
            self.set_thumb_color_off(thumb_color_off)

        if isinstance(focus_policy, Qt.FocusPolicy):
            self.setFocusPolicy(focus_policy)

        if cursor:
            self.setCursor(cursor)

        if object_name:
            self.setObjectName(object_name)

        self.tooltip = tooltip

    def enterEvent(self, event: QEnterEvent):
        super(QuickSwitch, self).enterEvent(event)

        if self.tooltip:
            self.tooltip.exec(self)

    def leaveEvent(self, a0: QEvent):
        super(QuickSwitch, self).leaveEvent(a0)

        if self.tooltip:
            self.tooltip.close()
