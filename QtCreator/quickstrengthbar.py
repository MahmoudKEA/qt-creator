from .header import *
from .quickwidget import QuickWidget
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from .quickprogressbar import QuickProgressBar
from .quicklabel import QuickLabel
from . import animation


class QuickStrengthBar(QuickWidget):
    class StrengthStatus:
        def __init__(self, text: str, color: QColor, value_range: range):
            self.text = text
            self.color = color
            self.valueRange = value_range

    veryWeakStatus = StrengthStatus(
        text="Very Weak",
        color=QColor('#FF0000'),
        value_range=range(1, 11)
    )
    weakStatus = StrengthStatus(
        text="Weak",
        color=QColor('#FF4000'),
        value_range=range(11, 31)
    )
    averageStatus = StrengthStatus(
        text="Average",
        color=QColor('#FF7000'),
        value_range=range(31, 51)
    )
    goodStatus = StrengthStatus(
        text="Good",
        color=QColor('#90FF00'),
        value_range=range(51, 76)
    )
    excellentStatus = StrengthStatus(
        text="Excellent",
        color=QColor('#00DF6C'),
        value_range=range(76, 101)
    )

    def __init__(
            self, parent=None,
            text_visible: bool = True,
            text_align: Qt.AlignmentFlag = None,
            margin: typing.Union[int, list] = 0,
            spacing: int = 6,
            font_size: int = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: typing.Callable = None,
            animation_start_value: typing.Any = None,
            animation_end_value: typing.Any = None,
            animation_duration: int = 300,
            animation_duration_bar: int = 300,
            tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None
    ):
        super(QuickStrengthBar, self).__init__(
            parent, object_name=object_name
        )

        self.__status = QuickStrengthBar.veryWeakStatus

        layout = QVBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        self.setLayout(layout)

        self.progressBar = QuickProgressBar(
            self, text_visible=False, font_size=font_size, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name='progressBar',
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )
        layout.addWidget(self.progressBar)

        self.labelText = QuickLabel(
            self, align=text_align, font_size=font_size, object_name='labelText'
        )
        self.labelText.setVisible(text_visible)
        layout.addWidget(self.labelText)

        self.__animation = animation.CustomizeMotion(
            self.progressBar, property_type=b'value', duration=animation_duration_bar
        )

    def status(self) -> StrengthStatus:
        return self.__status

    def value(self) -> int:
        return self.progressBar.value()

    def set_value(self, value: int):
        current = self.value()
        if current == value:
            return

        self.__animation.setStartValue(current)
        self.__animation.setEndValue(value)
        self.__animation.start()

        for status in (
            QuickStrengthBar.veryWeakStatus, QuickStrengthBar.weakStatus, QuickStrengthBar.averageStatus,
            QuickStrengthBar.goodStatus, QuickStrengthBar.excellentStatus
        ):
            if value in status.valueRange:
                self.labelText.setText(
                    QApplication.translate('QuickStrengthBar', status.text)
                )
                self.setStyleSheet(
                    'QLabel {color: %s;}' % status.color.name() +
                    'QProgressBar::chunk {background-color: %s;}' % status.color.name()
                )
                return

        self.labelText.setText('')
