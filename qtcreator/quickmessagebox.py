from .header import *
from .quickdialog import QuickDialog
from .quickwidget import QuickWidget
from .quicklabel import QuickLabel
from .quickpushbutton import QuickPushButton


class QuickMessageBox(QuickDialog):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
            ),
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_TranslucentBackground,
            title: str = None,
            title_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignHCenter,
            title_font_size: int = None,
            add_close: bool = True,
            close_icon: QIcon = None,
            close_icon_size: QSize = QSize(21, 21),
            close_size: QSize = QSize(24, 24),
            add_icon: bool = False,
            icon: QPixmap = None,
            icon_scaled: bool = False,
            icon_size: QSize = None,
            add_text: bool = True,
            text: str = None,
            text_format: Qt.TextFormat = None,
            text_align: Qt.AlignmentFlag = None,
            text_font_size: int = None,
            selectable: bool = False,
            accept_button: str = None,
            cancel_button: str = None,
            inputs: list = None,
            resizable: bool = False,
            margin: typing.Union[int, list] = 11,
            spacing: int = 11,
            shadow: QGraphicsDropShadowEffect = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.ClickFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None
    ):
        super(QuickMessageBox, self).__init__(
            parent, flags=flags, attribute=attribute, closeable=add_close, resizable=resizable,
            margin=margin, shadow=shadow, focus_policy=focus_policy, fixed_size=fixed_size,
            fixed_width=fixed_width, fixed_height=fixed_height, object_name=object_name
        )

        self.__leftClickPressed = None
        self.__clickPressedX = None
        self.__clickPressedY = None
        self.clickedOn = None

        layout = QGridLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        self.mainWidget.setLayout(layout)

        if title:
            self.labelTitle = QuickLabel(
                self, title, align=title_align, font_size=title_font_size, object_name='labelTitle'
            )
            self.labelTitle.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            )
            layout.addWidget(self.labelTitle, 0, 0, 1, 1)

        if add_close:
            self.pushButtonClose = QuickPushButton(
                self, icon=close_icon, icon_size=close_icon_size, fixed_size=close_size,
                object_name='pushButtonClose'
            )
            self.pushButtonClose.clicked.connect(self.button_clicked)
            layout.addWidget(self.pushButtonClose, 0, 0, 1, 1, Qt.AlignmentFlag(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
            ))

        if add_icon or add_text:
            content_layout = QHBoxLayout()
            content_layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
            content_layout.setSpacing(spacing)
            content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.contentWidget = QuickWidget(
                self, focus_policy=focus_policy, object_name='contentWidget'
            )
            self.contentWidget.setLayout(content_layout)
            layout.addWidget(self.contentWidget, 1, 0, 1, 1)

            if add_icon:
                self.labelIcon = QuickLabel(
                    self, scaled=icon_scaled, pixmap=icon, fixed_size=icon_size, object_name='labelIcon'
                )
                content_layout.addWidget(self.labelIcon)

            if add_text:
                self.labelText = QuickLabel(
                    self, text=text, text_format=text_format, align=text_align, selectable=selectable,
                    word_warp=True, font_size=text_font_size, object_name='labelText'
                )
                content_layout.addWidget(self.labelText)

        if inputs or accept_button or cancel_button:
            input_layout = QHBoxLayout()
            input_layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
            input_layout.setSpacing(spacing)
            self.inputWidget = QuickWidget(
                self, focus_policy=focus_policy, object_name='inputWidget'
            )
            self.inputWidget.setLayout(input_layout)
            layout.addWidget(self.inputWidget, 2, 0, 1, 1)

            if inputs:
                for item in inputs:
                    self.add_input(item)

            if accept_button:
                self.pushButtonAccept = QuickPushButton(
                    self, text=accept_button, fixed_height=31, object_name='pushButtonAccept'
                )
                self.pushButtonAccept.clicked.connect(self.button_clicked)
                self.add_input(self.pushButtonAccept)

            if cancel_button:
                self.pushButtonCancel = QuickPushButton(
                    self, text=cancel_button, fixed_height=31, object_name='pushButtonCancel'
                )
                self.pushButtonCancel.clicked.connect(self.button_clicked)
                self.add_input(self.pushButtonCancel)

    def closeEvent(self, a0: QCloseEvent) -> None:
        if not self.clickedOn:
            a0.ignore()
            return

        super(QuickMessageBox, self).closeEvent(a0)

    def showEvent(self, a0: QShowEvent):
        super(QuickMessageBox, self).showEvent(a0)
        try:
            self.clickedOn = self.pushButtonClose
        except AttributeError:
            self.clickedOn = None

    def mousePressEvent(self, event):
        super(QuickMessageBox, self).mousePressEvent(event)

        is_maximized = self.isMaximized()

        if event.button() == Qt.MouseButton.LeftButton and self.underMouse() and not is_maximized:
            self.__clickPressedX = event.pos().x()
            self.__clickPressedY = event.pos().y()
            self.__leftClickPressed = True

    def mouseReleaseEvent(self, event):
        super(QuickMessageBox, self).mouseReleaseEvent(event)

        self.__leftClickPressed = False

    def mouseMoveEvent(self, event):
        super(QuickMessageBox, self).mouseMoveEvent(event)

        if self.__leftClickPressed:
            x = int(event.globalPosition().x() - self.__clickPressedX)
            y = int(event.globalPosition().y() - self.__clickPressedY)
            self.move(x, y)

    def add_input(self, widget: typing.Any):
        self.inputWidget.layout().addWidget(widget)
        widget.show()

    def replace_input(self, current_widget: typing.Any, new_widget: typing.Any, delete: bool = False):
        self.inputWidget.layout().replaceWidget(current_widget, new_widget)
        new_widget.show()
        if delete:
            current_widget.deleteLater()
        else:
            current_widget.hide()

    def remove_input(self, widget: typing.Any, delete: bool = False):
        self.inputWidget.layout().removeWidget(widget)
        if delete:
            widget.deleteLater()
        else:
            widget.hide()

    def clear_inputs(self, delete: bool = False):
        while self.inputWidget.layout().count() > 0:
            widget = self.inputWidget.layout().itemAt(0).widget()
            self.inputWidget.layout().removeWidget(widget)
            if delete:
                widget.deleteLater()
            else:
                widget.hide()

    def button_clicked(self):
        self.clickedOn = self.sender()
        self.close()
