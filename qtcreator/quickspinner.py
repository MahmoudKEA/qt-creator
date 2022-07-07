"""
Forked from:
https://github.com/fbjorn/QtWaitingSpinner
"""

from .header import *


class QuickSpinner(QWidget):
    def __init__(
            self, parent,
            center_on_parent: bool = True,
            disable_parent_when_spinning: bool = False,
            modality: Qt.WindowModality = Qt.WindowModality.NonModal,
            roundness: typing.Union[int, float] = 100,
            fade: typing.Union[int, float] = 50,
            lines: int = 12,
            line_length: int = 10,
            line_width: int = 2,
            radius: int = 10,
            speed: typing.Union[int, float] = math.pi / 2,
            color: QColor = QColor(Qt.GlobalColor.black)
    ):
        super().__init__(parent)

        self.__centerOnParent = center_on_parent
        self.__disableParentWhenSpinning = disable_parent_when_spinning

        self.__color = QColor(color)
        self.__roundness = roundness
        self.__minimumTrailOpacity = math.pi
        self.__trailFadePercentage = fade
        self.__revolutionsPerSecond = speed
        self.__numberOfLines = lines
        self.__lineLength = line_length
        self.__lineWidth = line_width
        self.__innerRadius = radius
        self.__currentCounter = 0
        self.__isSpinning = False

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.rotate)
        self.update_size()
        self.update_timer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, a0: QPaintEvent):
        super(QuickSpinner, self).paintEvent(a0)

        self.update_position()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        if self.__currentCounter >= self.__numberOfLines:
            self.__currentCounter = 0

        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(self.__numberOfLines):
            painter.save()
            painter.translate(self.__innerRadius + self.__lineLength, self.__innerRadius + self.__lineLength)
            rotate_angle = float(360 * i) / float(self.__numberOfLines)
            painter.rotate(rotate_angle)
            painter.translate(self.__innerRadius, 0)
            distance = self.line_count_distance_from_primary(i, self.__currentCounter, self.__numberOfLines)
            color = self.current_line_color(
                distance,
                self.__numberOfLines,
                self.__trailFadePercentage,
                self.__minimumTrailOpacity,
                self.__color
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(0, -int(self.__lineWidth / 2), self.__lineLength, self.__lineWidth),
                self.__roundness,
                self.__roundness,
                Qt.SizeMode.RelativeSize
            )
            painter.restore()

    def start(self):
        self.update_position()
        self.__isSpinning = True
        self.show()

        if self.parentWidget and self.__disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self.__timer.isActive():
            self.__timer.start()
            self.__currentCounter = 0

    def stop(self):
        self.__isSpinning = False
        self.hide()

        if self.parentWidget() and self.__disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self.__timer.isActive():
            self.__timer.stop()
            self.__currentCounter = 0

    def set_number_of_lines(self, lines: int):
        self.__numberOfLines = lines
        self.__currentCounter = 0
        self.update_timer()

    def set_line_length(self, length: int):
        self.__lineLength = length
        self.update_size()

    def set_line_width(self, width: int):
        self.__lineWidth = width
        self.update_size()

    def set_inner_radius(self, radius: int):
        self.__innerRadius = radius
        self.update_size()

    @property
    def color(self) -> QColor:
        return self.__color

    @property
    def roundness(self) -> typing.Union[int, float]:
        return self.__roundness

    @property
    def minimum_trail_opacity(self) -> typing.Union[int, float]:
        return self.__minimumTrailOpacity

    @property
    def trail_fade_percentage(self) -> typing.Union[int, float]:
        return self.__trailFadePercentage

    @property
    def revolutions_pers_second(self) -> typing.Union[int, float]:
        return self.__revolutionsPerSecond

    @property
    def number_of_lines(self) -> int:
        return self.__numberOfLines

    @property
    def line_length(self) -> int:
        return self.__lineLength

    @property
    def line_width(self) -> int:
        return self.__lineWidth

    @property
    def inner_radius(self) -> int:
        return self.__innerRadius

    @property
    def is_spinning(self) -> bool:
        return self.__isSpinning

    def set_roundness(self, roundness: typing.Union[int, float]):
        self.__roundness = max(0.0, min(100.0, roundness))

    def set_color(self, color: QColor = QColor(Qt.GlobalColor.black)):
        self.__color = color

    def set_revolutions_per_second(self, revolutions_per_second: typing.Union[int, float]):
        self.__revolutionsPerSecond = revolutions_per_second
        self.update_timer()

    def set_trail_fade_percentage(self, trail: typing.Union[int, float]):
        self.__trailFadePercentage = trail

    def set_minimum_trail_opacity(self, minimum_trail_opacity: typing.Union[int, float]):
        self.__minimumTrailOpacity = minimum_trail_opacity

    def rotate(self):
        self.__currentCounter += 1
        if self.__currentCounter >= self.__numberOfLines:
            self.__currentCounter = 0
        self.update()

    def update_size(self):
        size = (self.__innerRadius + self.__lineLength) * 2
        self.setFixedSize(size, size)

    def update_timer(self):
        self.__timer.setInterval(int(1000 / (self.__numberOfLines * self.__revolutionsPerSecond)))

    def update_position(self):
        if self.parentWidget() and self.__centerOnParent:
            self.move(QPoint(
                int(self.parentWidget().width() / 2 - self.width() / 2),
                int(self.parentWidget().height() / 2 - self.height() / 2)
            ))

    @staticmethod
    def line_count_distance_from_primary(current: int, primary: int, total_number_of_lines: int) -> int:
        distance = primary - current
        if distance < 0:
            distance += total_number_of_lines

        return distance

    @staticmethod
    def current_line_color(
            count_distance: int, total_number_of_lines: int,
            trail_fade_percentage: typing.Union[int, float],
            min_opacity: typing.Union[int, float], color_input: QColor
    ) -> QColor:
        color = QColor(color_input)
        if count_distance == 0:
            return color

        min_alpha_f = min_opacity / 100.0
        distance_threshold = int(math.ceil((total_number_of_lines - 1) * trail_fade_percentage / 100.0))

        if count_distance > distance_threshold:
            color.setAlphaF(min_alpha_f)
        else:
            alpha_diff = color.alphaF() - min_alpha_f
            gradient = alpha_diff / float(distance_threshold + 1)
            result_alpha = color.alphaF() - gradient * count_distance
            # If alpha is out of bounds, clip it.
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.setAlphaF(result_alpha)

        return color
