from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable, Union
from .widgetform import AbstractForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from .quickspinner import QuickSpinner


class QuickPushButton(QPushButton, AbstractForm):
    def __init__(
            self, parent=None,
            text: str = None,
            font_size: int = None,
            icon: QIcon = None,
            icon_size: QSize = QSize(21, 21),
            add_spinner: bool = False,
            spinner_radius: int = 4,
            spinner_color: QColor = QColor(Qt.GlobalColor.white),
            spinner_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignRight,
            disable_when_spinning: bool = True,
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
        super(QuickPushButton, self).__init__(
            parent, text=text, font_size=font_size, icon=icon, icon_size=icon_size, cursor=cursor,
            focus_policy=focus_policy, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )

        if add_spinner:
            layout = QHBoxLayout()
            layout.setContentsMargins(11, 0, 11, 0)
            self.setLayout(layout)

            self.spinner = QuickSpinner(
                self, center_on_parent=False, disable_parent_when_spinning=disable_when_spinning,
                radius=spinner_radius, color=spinner_color, speed=1
            )
            layout.addWidget(self.spinner, alignment=spinner_align)

    def enterEvent(self, event: QEnterEvent):
        super(QuickPushButton, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickPushButton, self).leaveEvent(a0)
        self.leave_event()

    def text_visible(self, enabled: bool):
        if enabled:
            self.setText(self.property('textValue'))
        else:
            self.setProperty('textValue', self.text())
            self.setText("")
