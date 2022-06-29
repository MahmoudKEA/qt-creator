from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable
from .widgetform import StandardForm


class QuickWidget(QWidget, StandardForm):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType.SubWindow,
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_StyledBackground,
            graphic_effect: QGraphicsEffect = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.ClickFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: Callable = None,
            animation_start_value: Any = None,
            animation_end_value: Any = None,
            animation_duration: int = 300
    ):
        super(QuickWidget, self).__init__(
            parent, focus_policy=focus_policy, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration
        )

        self.setWindowFlags(Qt.WindowType(self.windowFlags() | flags))
        self.setAttribute(attribute, True)

        if graphic_effect:
            self.setGraphicsEffect(graphic_effect)

    def enterEvent(self, event: QEnterEvent):
        super(QuickWidget, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickWidget, self).leaveEvent(a0)
        self.leave_event()
