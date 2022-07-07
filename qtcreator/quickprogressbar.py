from .header import *
from .widgetform import AbstractForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage


class QuickProgressBar(QProgressBar, AbstractForm):
    def __init__(
            self, parent=None,
            value: int = 0,
            minimum: int = None,
            maximum: int = None,
            text_visible: bool = True,
            text_format: str = None,
            align: Qt.AlignmentFlag = None,
            orientation: Qt.Orientation = None,
            inverted: bool = False,
            font_size: int = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: typing.Callable = None,
            animation_start_value: typing.Any = None,
            animation_end_value: typing.Any = None,
            animation_duration: int = 300,
            tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None
    ):
        super(QuickProgressBar, self).__init__(
            parent, font_size=font_size, focus_policy=focus_policy, fixed_size=fixed_size,
            fixed_width=fixed_width, fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )

        if isinstance(value, int):
            self.setValue(value)

        if minimum:
            self.setMinimum(minimum)

        if maximum:
            self.setMaximum(maximum)

        if not text_visible:
            self.setTextVisible(False)

        if text_format:
            self.setFormat(text_format)

        if align:
            self.setAlignment(align)

        if orientation:
            self.setOrientation(orientation)

        if inverted:
            self.setInvertedAppearance(inverted)

    def enterEvent(self, event: QEnterEvent):
        super(QuickProgressBar, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickProgressBar, self).leaveEvent(a0)
        self.leave_event()
