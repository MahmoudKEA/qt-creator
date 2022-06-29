from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable


class StandardForm(QObject):
    def __init__(
            self, parent,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: Callable = None,
            animation_start_value: Any = None,
            animation_end_value: Any = None,
            animation_duration: int = 300
    ):
        super(StandardForm, self).__init__(parent)

        self.__animationCallback = animation_value_changed

        if isinstance(focus_policy, Qt.FocusPolicy):
            self.setFocusPolicy(focus_policy)

        if fixed_size:
            self.setFixedSize(fixed_size)
        else:
            if fixed_width:
                self.setFixedWidth(fixed_width)
            if fixed_height:
                self.setFixedHeight(fixed_height)

        if object_name:
            self.setObjectName(object_name)
        if callable(self.__animationCallback):
            self.__animation = QVariantAnimation(self)
            self.__animation.valueChanged.connect(self.__animation_value_changed)
            self.__animation.setStartValue(animation_start_value)
            self.__animation.setEndValue(animation_end_value)
            self.__animation.setDuration(animation_duration)

    def enter_event(self):
        if callable(self.__animationCallback):
            self.__animation.setDirection(QAbstractAnimation.Direction.Forward)
            self.__animation.start()

    def leave_event(self):
        if callable(self.__animationCallback):
            self.__animation.setDirection(QAbstractAnimation.Direction.Backward)
            self.__animation.start()

    def __animation_value_changed(self, value: Any):
        if not isinstance(self.sender(), QVariantAnimation):
            return

        self.__animationCallback(value)


class AbstractForm(StandardForm):
    def __init__(
            self, parent,
            text: str = None,
            font_size: int = None,
            icon: QIcon = None,
            icon_size: QSize = None,
            checked: bool = False,
            cursor: Qt.CursorShape = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: Callable = None,
            animation_start_value: Any = None,
            animation_end_value: Any = None,
            animation_duration: int = 300,
            tooltip: QWidget = None
    ):
        super(AbstractForm, self).__init__(
            parent, focus_policy=focus_policy, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration
        )

        if text:
            self.setText(text)

        if font_size:
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        if icon:
            self.setIcon(icon)

        if icon_size:
            self.setIconSize(icon_size)

        if checked:
            self.setChecked(True)

        if cursor:
            self.setCursor(cursor)

        self.tooltip = tooltip

    def enter_event(self):
        super(AbstractForm, self).enter_event()

        if self.tooltip:
            self.tooltip.exec(self)

    def leave_event(self):
        super(AbstractForm, self).leave_event()

        if self.tooltip:
            self.tooltip.close()
