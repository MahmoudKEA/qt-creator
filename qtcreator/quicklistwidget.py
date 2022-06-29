from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Any, Callable, Union
from .widgetform import StandardForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from .quickwidget import QuickWidget
from .quicklabel import QuickLabel
from . import utility


class EmptyListWidget(QuickWidget):
    def __init__(
            self, parent=None,
            scaled: bool = False,
            illustration: QPixmap = None,
            title: str = None,
            description: str = None,
            margin: Union[int, list] = 11,
            spacing: int = 11,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None
    ):
        super(EmptyListWidget, self).__init__(
            parent, fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        if illustration:
            self.labelIllustration = QuickLabel(
                self, align=Qt.AlignmentFlag.AlignHCenter, scaled=scaled, pixmap=illustration,
                object_name='labelIllustration'
            )
            self.labelIllustration.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            )
            layout.addWidget(self.labelIllustration)

        if title:
            self.labelTitle = QuickLabel(
                self, text=title, align=Qt.AlignmentFlag.AlignHCenter, object_name='labelTitle'
            )
            layout.addWidget(self.labelTitle)

        if description:
            self.labelDescription = QuickLabel(
                self, text=description, align=Qt.AlignmentFlag.AlignHCenter, word_warp=True,
                object_name='labelDescription'
            )
            layout.addWidget(self.labelDescription)


class QuickListWidgetItem(QuickWidget):
    def __init__(
            self, parent=None,
            cursor: Qt.CursorShape = None,
            graphic_effect: QGraphicsEffect = None,
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
        super(QuickListWidgetItem, self).__init__(
            parent, graphic_effect=graphic_effect, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration
        )

        if cursor:
            self.setCursor(cursor)

        self.listWidgetItem = QListWidgetItem()

        self.tooltip = tooltip

    def enterEvent(self, event: QEnterEvent):
        super(QuickListWidgetItem, self).enterEvent(event)

        if self.tooltip:
            self.tooltip.exec(self)

    def leaveEvent(self, a0: QEvent):
        super(QuickListWidgetItem, self).leaveEvent(a0)

        if self.tooltip:
            self.tooltip.close()

    def size_update(self):
        self.adjustSize()
        self.listWidgetItem.setSizeHint(self.sizeHint())


class QuickListWidget(QListWidget, StandardForm):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType.SubWindow,
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_StyledBackground,
            edit_triggers: QAbstractItemView.EditTrigger = QAbstractItemView.EditTrigger.NoEditTriggers,
            selection_mode: QAbstractItemView.SelectionMode = QAbstractItemView.SelectionMode.NoSelection,
            scroll_mode: QAbstractItemView.ScrollMode = QAbstractItemView.ScrollMode.ScrollPerPixel,
            resize_mode: QListView.ResizeMode = QListView.ResizeMode.Fixed,
            view_mode: QListView.ViewMode = QListView.ViewMode.ListMode,
            movement: QListView.Movement = QListView.Movement.Static,
            icon_size: QSize = QSize(21, 21),
            grid_size: QSize = None,
            spacing: int = 0,
            scroll_step: int = 10,
            empty_list_widget: QWidget = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: Callable = None,
            animation_start_value: Any = None,
            animation_end_value: Any = None,
            animation_duration: int = 300
    ):
        super(QuickListWidget, self).__init__(
            parent, fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name, animation_value_changed=animation_value_changed,
            animation_start_value=animation_start_value, animation_end_value=animation_end_value,
            animation_duration=animation_duration
        )

        self.setWindowFlags(Qt.WindowType(self.windowFlags() | flags))
        self.setAttribute(attribute, True)
        self.setEditTriggers(edit_triggers)
        self.setSelectionMode(selection_mode)
        self.setVerticalScrollMode(scroll_mode)
        self.setHorizontalScrollMode(scroll_mode)
        self.setResizeMode(resize_mode)
        self.setViewMode(view_mode)
        self.setMovement(movement)
        self.horizontalScrollBar().setCursor(Qt.CursorShape.PointingHandCursor)
        self.verticalScrollBar().setCursor(Qt.CursorShape.PointingHandCursor)
        self.model().rowsInserted.connect(self.model_changed)
        self.model().rowsRemoved.connect(self.model_changed)
        self.model().modelReset.connect(self.model_changed)

        if icon_size:
            self.setIconSize(icon_size)

        if grid_size:
            self.setGridSize(grid_size)

        if spacing:
            self.setSpacing(spacing)

        if scroll_step:
            utility.scroll_step(self, step=scroll_step)

        self.__emptyListWidget = empty_list_widget
        if empty_list_widget:
            layout = QGridLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(empty_list_widget, 0, 0, 1, 1)
            self.setLayout(layout)

    def enterEvent(self, event: QEnterEvent):
        super(QuickListWidget, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickListWidget, self).leaveEvent(a0)
        self.leave_event()

    def model_changed(self):
        if not self.__emptyListWidget:
            return

        is_exists = self.count() > 0
        self.__emptyListWidget.setHidden(is_exists)

    def add_item(self, item: QuickListWidgetItem):
        self.addItem(item.listWidgetItem)
        self.setItemWidget(item.listWidgetItem, item)
