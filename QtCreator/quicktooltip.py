from .header import *
from .quickmainwidget import QuickMainWidget


class QuickToolTip(QuickMainWidget):
    def __init__(
            self, parent=None,
            margin: typing.Union[int, list] = 11,
            shadow: QGraphicsDropShadowEffect = None,
            color: QColor = None,
            align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop,
            arrow_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
            arrow_size: QSize = QSize(15, 10),
            arrow_margin: int = 15,
            timeout: int = 5000,
            object_name: str = None
    ):
        super(QuickToolTip, self).__init__(
            parent, flags=Qt.WindowType(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint),
            resizable=False, margin=margin, shadow=shadow, object_name=object_name
        )

        self.__color = color
        self.__align = align
        self.__arrowAlign = arrow_align
        self.__arrowSize = arrow_size
        self.__arrowMargin = arrow_margin
        self.__timeout = timeout
        self.__painterPath = QPainterPath()
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__timer_call)
        self.__timerCount = 0

        self.layout().setSpacing(0)

        self.mainWidget.setMinimumSize(QSize(31, 31))
        if color:
            self.mainWidget.setStyleSheet('#mainWidget {background-color: %s;}' % color.name())

        self.labelArrow = QLabel(self)

        self.__arrow_alignment()

    def closeEvent(self, a0: QCloseEvent):
        wait = QEventLoop()
        QTimer().singleShot(150, wait.exit)
        wait.exec()

        if self.underMouse():
            a0.ignore()
            return

        super(QuickToolTip, self).closeEvent(a0)

    def hideEvent(self, a0: QHideEvent):
        super(QuickToolTip, self).hideEvent(a0)

        if self.__timeout and self.is_tooltip_mode():
            self.__timer.stop()
            self.__timerCount = 0

    def leaveEvent(self, a0: QEvent):
        super(QuickToolTip, self).leaveEvent(a0)

        if self.is_tooltip_mode():
            self.close()

    def size(self) -> QSize:
        self.adjustSize()
        return super(QuickToolTip, self).size()

    def exec(self, target=None):
        if target:
            point = target.mapToGlobal(QPoint())
            x = point.x()
            y = point.y()
            size = self.size()

            if self.__align in (Qt.AlignmentFlag.AlignTop, Qt.AlignmentFlag.AlignBottom):
                if self.__align is Qt.AlignmentFlag.AlignTop:
                    y -= size.height()
                else:
                    y += target.height()

                if self.__arrowAlign is Qt.AlignmentFlag.AlignLeft:
                    x -= self.__arrowMargin
                elif self.__arrowAlign is Qt.AlignmentFlag.AlignRight:
                    x += (target.width() + self.__arrowMargin) - size.width()
                elif self.__arrowAlign in (Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignHCenter):
                    x += (target.width() / 2) - (size.width() / 2)

            elif self.__align in (Qt.AlignmentFlag.AlignLeft, Qt.AlignmentFlag.AlignRight):
                if self.__align is Qt.AlignmentFlag.AlignLeft:
                    x -= size.width()
                else:
                    x += target.width()

                if self.__arrowAlign is Qt.AlignmentFlag.AlignTop:
                    y -= self.__arrowMargin
                elif self.__arrowAlign is Qt.AlignmentFlag.AlignBottom:
                    y += (target.height() + self.__arrowMargin) - size.height()
                elif self.__arrowAlign in (Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignVCenter):
                    y += (target.height() / 2) - (size.height() / 2)

            self.move(int(x), int(y))

        else:
            self.setWindowFlags(Qt.WindowType.SubWindow)

        self.__arrow_draw()
        self.show()

        if self.__timeout and self.is_tooltip_mode():
            self.__timer.start(1000)

    def set_align(self, alignment: Qt.AlignmentFlag):
        self.__align = alignment
        self.__arrow_alignment()

    def set_arrow_align(self, alignment: Qt.AlignmentFlag):
        self.__arrowAlign = alignment
        self.__arrow_alignment()

    def set_timeout(self, value: int):
        self.__timeout = value

    def is_tooltip_mode(self) -> bool:
        return Qt.WindowType.ToolTip in self.windowFlags()

    def __arrow_alignment(self):
        if self.__arrowAlign in (
                Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignHCenter, Qt.AlignmentFlag.AlignVCenter
        ):
            self.__arrowMargin = 0

        if self.__align is Qt.AlignmentFlag.AlignTop:
            self.__arrowSize.setWidth((self.__arrowMargin * 2) + self.__arrowSize.width())

            self.__painterPath.moveTo(self.__arrowSize.width() / 2, self.__arrowSize.height())
            self.__painterPath.lineTo(self.__arrowMargin, 0)
            self.__painterPath.lineTo(self.__arrowSize.width() - self.__arrowMargin, 0)

            self.layout().addWidget(self.mainWidget, 0, 0, 1, 1)
            self.layout().addWidget(self.labelArrow, 1, 0, 1, 1, self.__arrowAlign)

        elif self.__align is Qt.AlignmentFlag.AlignBottom:
            self.__arrowSize.setWidth((self.__arrowMargin * 2) + self.__arrowSize.width())

            self.__painterPath.moveTo(self.__arrowSize.width() / 2, 0)
            self.__painterPath.lineTo(self.__arrowMargin, self.__arrowSize.height())
            self.__painterPath.lineTo(
                self.__arrowSize.width() - self.__arrowMargin, self.__arrowSize.height()
            )

            self.layout().addWidget(self.labelArrow, 0, 0, 1, 1, self.__arrowAlign)
            self.layout().addWidget(self.mainWidget, 1, 0, 1, 1)

        elif self.__align is Qt.AlignmentFlag.AlignLeft:
            self.__arrowSize.setHeight((self.__arrowMargin * 2) + self.__arrowSize.height())

            self.__painterPath.moveTo(self.__arrowSize.width(), self.__arrowSize.height() / 2)
            self.__painterPath.lineTo(0, self.__arrowSize.height() - self.__arrowMargin)
            self.__painterPath.lineTo(0, self.__arrowMargin)

            self.layout().addWidget(self.mainWidget, 0, 0, 1, 1)
            self.layout().addWidget(self.labelArrow, 0, 1, 1, 1, self.__arrowAlign)

        elif self.__align is Qt.AlignmentFlag.AlignRight:
            self.__arrowSize.setHeight((self.__arrowMargin * 2) + self.__arrowSize.height())

            self.__painterPath.moveTo(0, self.__arrowSize.height() / 2)
            self.__painterPath.lineTo(
                self.__arrowSize.width(), self.__arrowSize.height() - self.__arrowMargin
            )
            self.__painterPath.lineTo(self.__arrowSize.width(), self.__arrowMargin)

            self.layout().addWidget(self.labelArrow, 0, 0, 1, 1, self.__arrowAlign)
            self.layout().addWidget(self.mainWidget, 0, 1, 1, 1)

        self.labelArrow.setFixedSize(self.__arrowSize)

    def __arrow_draw(self):
        color = self.__color
        if not color:
            color = self.mainWidget.palette().window().color()

        pix = QPixmap(self.labelArrow.size())
        pix.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(color)
        painter.setPen(QPen(QBrush(Qt.GlobalColor.transparent), 1))
        painter.drawPath(self.__painterPath)
        painter.end()

        self.labelArrow.setPixmap(pix)

    def __timer_call(self):
        self.__timerCount += 1000
        if self.__timerCount >= self.__timeout:
            self.close()


class QuickToolTipMessage(QuickToolTip):
    def __init__(
            self, parent=None,
            text: str = None,
            text_format: Qt.TextFormat = None,
            text_align: Qt.AlignmentFlag = None,
            font_size: int = None,
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
            shadow: QGraphicsDropShadowEffect = None,
            color: QColor = None,
            align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop,
            arrow_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
            arrow_size: QSize = QSize(15, 10),
            arrow_margin: int = 15,
            timeout: int = 5000,
            object_name: str = None
    ):
        super(QuickToolTipMessage, self).__init__(
            parent, margin=margin, shadow=shadow, color=color, align=align, arrow_align=arrow_align,
            arrow_size=arrow_size, arrow_margin=arrow_margin, timeout=timeout, object_name=object_name
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        self.mainWidget.setLayout(layout)

        if add_icon:
            self.labelIcon = QLabel(self)
            self.labelIcon.setScaledContents(icon_scaled)
            self.labelIcon.setPixmap(icon)
            self.labelIcon.setObjectName('labelIcon')
            if icon_size:
                self.labelIcon.setFixedSize(icon_size)
            layout.addWidget(self.labelIcon, alignment=Qt.AlignmentFlag.AlignTop)

        if text:
            self.labelText = QLabel(self)
            self.labelText.setText(text)
            self.labelText.setWordWrap(True)
            self.labelText.setObjectName('labelText')
            if text_format:
                self.labelText.setTextFormat(text_format)
            if text_align:
                self.labelText.setAlignment(text_align)
            if font_size:
                font = self.labelText.font()
                font.setPointSize(font_size)
                self.labelText.setFont(font)
            if selectable:
                self.labelText.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                self.labelText.setCursor(Qt.CursorShape.IBeamCursor)
            layout.addWidget(self.labelText)

        if add_close:
            self.pushButtonClose = QPushButton(self)
            self.pushButtonClose.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.pushButtonClose.setCursor(Qt.CursorShape.PointingHandCursor)
            self.pushButtonClose.clicked.connect(self.close)
            self.pushButtonClose.setObjectName('pushButtonClose')
            if close_icon:
                self.pushButtonClose.setIcon(close_icon)
            if close_icon_size:
                self.pushButtonClose.setIconSize(close_icon_size)
            if close_size:
                self.pushButtonClose.setFixedSize(close_size)
            layout.addWidget(self.pushButtonClose, alignment=Qt.AlignmentFlag.AlignTop)

    def closeEvent(self, a0: QCloseEvent):
        try:
            if self.sender() is self.pushButtonClose:
                super(QuickToolTip, self).closeEvent(a0)
                return
        except AttributeError:
            pass

        super(QuickToolTipMessage, self).closeEvent(a0)
