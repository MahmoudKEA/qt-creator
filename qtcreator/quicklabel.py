from .header import *
from .widgetform import AbstractForm
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from .quickwidget import QuickWidget
from .quickpushbutton import QuickPushButton
from . import utility


class QuickLabel(QLabel, AbstractForm):
    def __init__(
            self, parent=None,
            text: str = None,
            text_format: Qt.TextFormat = None,
            align: Qt.AlignmentFlag = None,
            selectable: bool = False,
            word_warp: bool = False,
            scaled: bool = False,
            pixmap: QPixmap = None,
            font_size: int = None,
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
        super(QuickLabel, self).__init__(
            parent, text=text, font_size=font_size, fixed_size=fixed_size, fixed_width=fixed_width,
            fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )

        if text_format:
            self.setTextFormat(text_format)

        if align:
            self.setAlignment(align)

        if selectable:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.setCursor(Qt.CursorShape.IBeamCursor)

        if word_warp:
            self.setWordWrap(True)

        if scaled:
            self.setScaledContents(scaled)

        if pixmap:
            self.setPixmap(pixmap)

    def enterEvent(self, event: QEnterEvent):
        super(QuickLabel, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickLabel, self).leaveEvent(a0)
        self.leave_event()

    def setText(
            self, text: str, url: str = None, url_color: QColor = QColor(Qt.GlobalColor.blue),
            elided_mode: Qt.TextElideMode = None
    ):
        if elided_mode:
            width = self.width()
            metrics = QFontMetrics(self.font())
            if metrics.horizontalAdvance(text) > width:
                text = metrics.elidedText(text, elided_mode, width)

        if url:
            self.setOpenExternalLinks(True)
            text = f'<a href="{url}" style="color: {url_color.name()};">{text}</a>'

        super(QuickLabel, self).setText(text)


class QuickLabelAddress(QuickWidget):
    def __init__(
            self, parent=None,
            address: str = None,
            explorer_url: str = None,
            add_copy: bool = True,
            copy_icon: QIcon = None,
            copy_tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None,
            add_browse: bool = False,
            browse_icon: QIcon = None,
            browse_tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None,
            margin: typing.Union[int, list] = 0,
            spacing: int = 11,
            selectable: bool = False,
            word_warp: bool = False,
            font_size: int = None,
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
        super(QuickLabelAddress, self).__init__(
            parent, object_name=object_name, animation_value_changed=animation_value_changed,
            animation_start_value=animation_start_value, animation_end_value=animation_end_value,
            animation_duration=animation_duration
        )

        self.__address = address
        self.__explorerURL = explorer_url

        layout = QHBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        self.setLayout(layout)

        self.labelText = QuickLabel(
            self, selectable=selectable, word_warp=word_warp, font_size=font_size,
            fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name='labelText', tooltip=tooltip
        )
        self.set_address(address, explorer_url)
        layout.addWidget(self.labelText)

        if add_copy:
            self.pushButtonCopy = QuickPushButton(
                self, icon=copy_icon, icon_size=QSize(21, 21), fixed_size=QSize(21, 21),
                object_name='pushButtonCopy', tooltip=copy_tooltip
            )
            self.pushButtonCopy.clicked.connect(self.copy_clicked)
            layout.addWidget(self.pushButtonCopy)

        if add_browse:
            self.pushButtonBrowse = QuickPushButton(
                self, icon=browse_icon, icon_size=QSize(21, 21), fixed_size=QSize(21, 21),
                object_name='pushButtonBrowse', tooltip=browse_tooltip
            )
            self.pushButtonBrowse.clicked.connect(self.browse_clicked)
            layout.addWidget(self.pushButtonBrowse)

    @pyqtSlot()
    def copy_clicked(self):
        utility.clipboard(self.__address)

    @pyqtSlot()
    def browse_clicked(self):
        utility.url_open(f'{self.__explorerURL}/{self.__address}')

    def address(self) -> str:
        return self.__address

    def set_address(
            self, address: str, explorer_url: str,
            elided_mode: Qt.TextElideMode = Qt.TextElideMode.ElideMiddle
    ):
        self.__address = address
        self.__explorerURL = explorer_url
        self.labelText.setText(address, elided_mode=elided_mode)

    def clear(self):
        self.__address = ''
        self.__explorerURL = ''
        self.labelText.clear()
