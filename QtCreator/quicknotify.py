from .header import *
from .quickwidget import QuickWidget
from .quicklabel import QuickLabel
from .quickpushbutton import QuickPushButton


class QuickNotifyListWidgetItem(QuickWidget):
    def __init__(
            self, parent=None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            graphic_effect: QGraphicsEffect = None,
            animation_value_changed: typing.Callable = None,
            animation_start_value: typing.Any = None,
            animation_end_value: typing.Any = None,
            animation_duration: int = 300
    ):
        super(QuickNotifyListWidgetItem, self).__init__(
            parent, fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name, graphic_effect=graphic_effect,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration,
        )

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)


class QuickNotifyMessageListWidgetItem(QuickNotifyListWidgetItem):
    def __init__(
            self, parent=None,
            text: str = None,
            text_format: Qt.TextFormat = None,
            text_align: Qt.AlignmentFlag = None,
            selectable: bool = False,
            add_icon: bool = False,
            icon: QPixmap = None,
            icon_scaled: bool = False,
            icon_size: QSize = None,
            add_close: bool = False,
            close_icon: QIcon = None,
            close_icon_size: QSize = QSize(16, 16),
            close_size: QSize = QSize(21, 21),
            margin: typing.Union[int, list] = 11,
            graphic_effect: QGraphicsEffect = None,
            font_size: int = None,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: typing.Callable = None,
            animation_start_value: typing.Any = None,
            animation_end_value: typing.Any = None,
            animation_duration: int = 300
    ):
        super(QuickNotifyMessageListWidgetItem, self).__init__(
            parent, graphic_effect=graphic_effect, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        self.setLayout(layout)

        if add_icon:
            self.labelIcon = QuickLabel(
                self, scaled=icon_scaled, pixmap=icon, fixed_size=icon_size, object_name='labelIcon'
            )
            layout.addWidget(self.labelIcon, alignment=Qt.AlignmentFlag.AlignTop)

        if text:
            self.labelText = QuickLabel(
                self, text=text, text_format=text_format, align=text_align, selectable=selectable,
                word_warp=True, font_size=font_size, object_name='labelText'
            )
            layout.addWidget(self.labelText, stretch=True)

        if add_close:
            self.pushButtonClose = QuickPushButton(
                self, icon=close_icon, icon_size=close_icon_size, fixed_size=close_size,
                object_name='pushButtonClose'
            )
            self.pushButtonClose.clicked.connect(self.close)
            layout.addWidget(self.pushButtonClose, alignment=Qt.AlignmentFlag.AlignTop)


class QuickNotifyListWidget(QuickWidget):
    class Mode:
        INTERNAL = 1
        EXTERNAL = 2

    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType.FramelessWindowHint,
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_TranslucentBackground,
            align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight,
            mode: int = Mode.INTERNAL,
            max_visible: int = 5,
            timeout: int = 5000,
            margin: typing.Union[int, list] = 11,
            spacing: int = 11,
            object_name: str = None
    ):
        super(QuickNotifyListWidget, self).__init__(
            parent, flags=flags, attribute=attribute, object_name=object_name
        )

        self.__mode = mode
        self.__maxVisible = max_visible
        self.__timeout = timeout
        self.__items = {}
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__timer_call)

        if mode == QuickNotifyListWidget.Mode.EXTERNAL:
            self.setWindowFlags(Qt.WindowType(
                self.windowFlags() | Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
            ))
            self.setFixedSize(self.screen().size())
        else:
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        layout = QVBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        layout.setAlignment(align)
        self.setLayout(layout)

        self.close()

    def add_item(self, item: QuickNotifyListWidgetItem):
        self.__items.update({item: 0})

        if self.layout().count() < self.__maxVisible:
            self.layout().addWidget(item)
            self.show()

        if self.__timeout and not self.__timer.isActive():
            self.__timer.start(1000)

    def remove_item(self, item: QuickNotifyListWidgetItem):
        del self.__items[item]
        self.layout().removeWidget(item)

        if self.layout().count() <= 0:
            if self.__timeout:
                self.__timer.stop()

            self.close()

    def __timer_call(self):
        items = self.__items.copy()
        for item in items:
            try:
                if item.underMouse():
                    return
            except RuntimeError:
                continue

        for item, sec in items.items():
            try:
                if sec >= self.__timeout:
                    self.remove_item(item)
                elif item.isVisible():
                    self.__items[item] += 1000
                else:
                    self.add_item(item)
            except RuntimeError:
                continue
