from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable, Union
from .widgetform import AbstractForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from . import utility


class QuickComboBox(QComboBox, AbstractForm):
    def __init__(
            self, parent=None,
            items: list = None,
            editable: bool = False,
            current_text: str = None,
            current_index: int = None,
            max_visible_items: int = None,
            max_count: int = None,
            list_view_mode: bool = True,
            no_shadow: bool = False,
            anti_wheel: bool = True,
            font_size: int = None,
            icon_size: QSize = QSize(21, 21),
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
        super(QuickComboBox, self).__init__(
            parent, font_size=font_size, icon_size=icon_size, cursor=cursor, focus_policy=focus_policy,
            fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name, animation_value_changed=animation_value_changed,
            animation_start_value=animation_start_value, animation_end_value=animation_end_value,
            animation_duration=animation_duration, tooltip=tooltip
        )

        self.__antiWheel = anti_wheel

        if items:
            self.addItems(items)

        if editable:
            self.setEditable(True)

        if current_text:
            self.setCurrentText(current_text)

        if current_index:
            self.setCurrentIndex(current_index)

        if max_visible_items:
            self.setMaxVisibleItems(max_visible_items)

        if max_count:
            self.setMaxCount(max_count)

        if list_view_mode:
            utility.view_list_style(
                self, icon_size=icon_size, no_shadow=no_shadow
            )

    def enterEvent(self, event: QEnterEvent):
        super(QuickComboBox, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickComboBox, self).leaveEvent(a0)
        self.leave_event()

    def wheelEvent(self, e: QWheelEvent):
        if self.__antiWheel:
            return

        super(QuickComboBox, self).wheelEvent(e)
