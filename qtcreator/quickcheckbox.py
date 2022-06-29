from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable, Union
from .widgetform import AbstractForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage


class QuickCheckBox(QCheckBox, AbstractForm):
    def __init__(
            self, parent=None,
            text: str = None,
            font_size: int = None,
            icon: QIcon = None,
            icon_size: QSize = QSize(21, 21),
            checked: bool = False,
            cursor: Qt.CursorShape = Qt.CursorShape.PointingHandCursor,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: Callable = None,
            animation_start_value: Any = None,
            animation_end_value: Any = None,
            animation_duration: int = 300,
            tooltip: Union[QuickToolTip, QuickToolTipMessage] = None
    ):
        super(QuickCheckBox, self).__init__(
            parent, text=text, font_size=font_size, icon=icon, icon_size=icon_size, checked=checked,
            cursor=cursor, focus_policy=focus_policy, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )

    def enterEvent(self, event: QEnterEvent):
        super(QuickCheckBox, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickCheckBox, self).leaveEvent(a0)
        self.leave_event()
