from .header import *
from .widgetform import AbstractForm
from .quickwidget import QuickWidget
from .quicktooltip import QuickToolTip, QuickToolTipMessage
from .quicklabel import QuickLabel
from .quickpushbutton import QuickPushButton
from .quickstrengthbar import QuickStrengthBar


class QuickLineEdit(QLineEdit, AbstractForm):
    def __init__(
            self, parent=None,
            text: str = None,
            placeholder_text: str = None,
            align: Qt.AlignmentFlag = None,
            writable: bool = True,
            numeric: bool = False,
            length: int = 64,
            mode: QLineEdit.EchoMode = None,
            menu_policy: Qt.ContextMenuPolicy = None,
            clearable: bool = False,
            add_layout: bool = False,
            add_icon: bool = False,
            icon: QPixmap = None,
            icon_scaled: bool = False,
            icon_size: QSize = QSize(21, 21),
            icon_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
            font_size: int = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.StrongFocus,
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
        super(QuickLineEdit, self).__init__(
            parent, text=text, font_size=font_size, focus_policy=focus_policy, fixed_size=fixed_size,
            fixed_width=fixed_width, fixed_height=fixed_height, object_name=object_name,
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )

        if placeholder_text:
            self.setPlaceholderText(placeholder_text)

        if align:
            self.setAlignment(align)

        if writable:
            self.setMaxLength(length)
            if numeric:
                self.setValidator(
                    QRegularExpressionValidator(QRegularExpression('[0-9]{%s}' % length))
                )
        else:
            self.setReadOnly(True)

        if mode:
            self.setEchoMode(mode)

        if menu_policy:
            self.setContextMenuPolicy(menu_policy)

        if clearable:
            self.setClearButtonEnabled(True)

        if add_layout or add_icon:
            layout = QHBoxLayout()
            layout.setContentsMargins(11, 0, 11, 0)
            self.setLayout(layout)

            if add_icon:
                self.labelIcon = QuickLabel(
                    self, scaled=icon_scaled, pixmap=icon, fixed_size=icon_size, object_name='labelIcon'
                )
                layout.addWidget(self.labelIcon, alignment=icon_align)

    def enterEvent(self, event: QEnterEvent):
        super(QuickLineEdit, self).enterEvent(event)
        self.enter_event()

    def leaveEvent(self, a0: QEvent):
        super(QuickLineEdit, self).leaveEvent(a0)
        self.leave_event()


class QuickLineEditMultiple(QuickWidget):
    def __init__(
            self, parent=None,
            count: int = 6,
            space_index: int = None,
            placeholder_text: str = None,
            numeric: bool = True,
            mode: QLineEdit.EchoMode = None,
            menu_policy: Qt.ContextMenuPolicy = None,
            margin: typing.Union[int, list] = 0,
            spacing: int = 11,
            add_eye: bool = False,
            eye_one_click: bool = True,
            eye_show_icon: QIcon = None,
            eye_hidden_icon: QIcon = None,
            eye_icon_size: QSize = QSize(21, 21),
            eye_tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None,
            font_size: int = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.StrongFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None,
            animation_value_changed: typing.Callable = None,
            animation_start_value: typing.Any = None,
            animation_end_value: typing.Any = None,
            animation_duration: int = 300,
            tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None,
            text_changed: typing.Callable = None
    ):
        super(QuickLineEditMultiple, self).__init__(
            parent, object_name=object_name, animation_value_changed=animation_value_changed,
            animation_start_value=animation_start_value, animation_end_value=animation_end_value,
            animation_duration=animation_duration
        )

        self.__eyeShowIcon = eye_show_icon
        self.__eyeHiddenIcon = eye_hidden_icon
        self.__textChanged = text_changed
        self.__lineEditFields = []
        self.__isTyping = False
        self.__text = ''

        layout = QHBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        for i in range(count):
            line_edit = QuickLineEdit(
                self, placeholder_text=placeholder_text, align=Qt.AlignmentFlag.AlignHCenter,
                numeric=numeric, length=count, mode=mode, menu_policy=menu_policy, font_size=font_size,
                focus_policy=focus_policy, fixed_size=fixed_size, fixed_width=fixed_width,
                fixed_height=fixed_height, object_name='lineEdit'
            )
            line_edit.textChanged.connect(self.__text_changed)
            layout.addWidget(line_edit)
            self.__lineEditFields.append(line_edit)

        if space_index:
            space_widget = QuickWidget(
                self, attribute=Qt.WidgetAttribute.WA_TranslucentBackground, fixed_width=11
            )
            layout.insertWidget(space_index, space_widget)

        if add_eye:
            self.pushButtonEye = QuickPushButton(
                self, icon=eye_show_icon, icon_size=eye_icon_size, fixed_size=eye_icon_size,
                object_name='pushButtonEye', tooltip=eye_tooltip
            )
            layout.addWidget(self.pushButtonEye)

            if eye_one_click:
                self.pushButtonEye.pressed.connect(self.__eye_clicked)
                self.pushButtonEye.released.connect(self.__eye_clicked)
            else:
                self.pushButtonEye.clicked.connect(self.__eye_clicked)

        self.tooltip = tooltip

    def enterEvent(self, event: QEnterEvent):
        super(QuickLineEditMultiple, self).enterEvent(event)

        if self.tooltip:
            self.tooltip.exec(self)

    def leaveEvent(self, a0: QEvent):
        super(QuickLineEditMultiple, self).leaveEvent(a0)

        if self.tooltip:
            self.tooltip.close()

    def text(self) -> str:
        return self.__text

    @pyqtSlot(str)
    def __text_changed(self, text: str):
        if self.__isTyping:
            return

        self.__isTyping = True
        count = len(self.__lineEditFields)

        if len(text) == count:
            self.__text = text
        elif text:
            self.__text = (self.__text + text[-1:])[:count]
        else:
            self.__text = self.__text[:-1]

        for index, lineEdit in enumerate(self.__lineEditFields):
            try:
                lineEdit.setText(self.__text[index])
                lineEdit.setFocus()
            except IndexError:
                lineEdit.clear()

        self.__isTyping = False

        if callable(self.__textChanged):
            self.__textChanged(self.__text)

    def set_eye_icon(self, show: QIcon, hidden: QIcon):
        self.__eyeShowIcon = show
        self.__eyeHiddenIcon = hidden
        self.pushButtonEye.setIcon(show)

    @pyqtSlot()
    def __eye_clicked(self):
        if self.__lineEditFields[0].echoMode() is QLineEdit.EchoMode.Password:
            mode = QLineEdit.EchoMode.Normal
            self.pushButtonEye.setIcon(self.__eyeHiddenIcon)
        else:
            mode = QLineEdit.EchoMode.Password
            self.pushButtonEye.setIcon(self.__eyeShowIcon)

        for lineEdit in self.__lineEditFields:
            lineEdit.setEchoMode(mode)


class QuickLineEditPassword(QuickWidget):
    def __init__(
            self, parent=None,
            text: str = None,
            placeholder_text: str = None,
            align: Qt.AlignmentFlag = None,
            writable: bool = True,
            numeric: bool = False,
            length: int = 64,
            menu_policy: Qt.ContextMenuPolicy = None,
            margin: typing.Union[int, list] = 0,
            spacing: int = 11,
            clearable: bool = False,
            add_icon: bool = False,
            icon: QPixmap = None,
            icon_scaled: bool = False,
            icon_size: QSize = QSize(21, 21),
            icon_align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
            add_eye: bool = True,
            eye_one_click: bool = True,
            eye_show_icon: QIcon = None,
            eye_hidden_icon: QIcon = None,
            eye_icon_size: QSize = QSize(21, 21),
            eye_tooltip: typing.Union[QuickToolTip, QuickToolTipMessage] = None,
            add_strength_bar: bool = True,
            strength_bar_text_visible: bool = True,
            strength_bar_text_align: Qt.AlignmentFlag = None,
            strength_bar_font_size: int = None,
            font_size: int = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.StrongFocus,
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
        super(QuickLineEditPassword, self).__init__(
            parent, object_name=object_name
        )

        self.__eyeShowIcon = eye_show_icon
        self.__eyeHiddenIcon = eye_hidden_icon

        layout = QVBoxLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        layout.setSpacing(spacing)
        self.setLayout(layout)

        self.lineEdit = QuickLineEdit(
            self, text=text, placeholder_text=placeholder_text, align=align, font_size=font_size,
            numeric=numeric, writable=writable, length=length, mode=QLineEdit.EchoMode.Password,
            focus_policy=focus_policy, menu_policy=menu_policy, clearable=clearable, add_layout=True,
            add_icon=add_icon, icon=icon, icon_scaled=icon_scaled, icon_size=icon_size, icon_align=icon_align,
            fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height, object_name='lineEdit',
            animation_value_changed=animation_value_changed, animation_start_value=animation_start_value,
            animation_end_value=animation_end_value, animation_duration=animation_duration, tooltip=tooltip
        )
        layout.addWidget(self.lineEdit)

        if add_eye:
            self.pushButtonEye = QuickPushButton(
                self, icon=eye_show_icon, icon_size=eye_icon_size, fixed_size=eye_icon_size,
                object_name='pushButtonEye', tooltip=eye_tooltip
            )
            self.lineEdit.layout().addWidget(self.pushButtonEye, alignment=Qt.AlignmentFlag.AlignRight)

            if eye_one_click:
                self.pushButtonEye.pressed.connect(self.__eye_clicked)
                self.pushButtonEye.released.connect(self.__eye_clicked)
            else:
                self.pushButtonEye.clicked.connect(self.__eye_clicked)

        if add_strength_bar:
            self.strengthBar = QuickStrengthBar(
                self, text_visible=strength_bar_text_visible, text_align=strength_bar_text_align,
                font_size=strength_bar_font_size, fixed_height=8, object_name='strengthBar'
            )
            layout.addWidget(self.strengthBar)
            self.lineEdit.textChanged.connect(self.__text_changed)

    def set_eye_icon(self, show: QIcon, hidden: QIcon):
        self.__eyeShowIcon = show
        self.__eyeHiddenIcon = hidden
        self.pushButtonEye.setIcon(show)

    @pyqtSlot(str)
    def __text_changed(self, text: str):
        try:
            percent = int(PasswordStats(text).strength() * 100)
        except ValueError:
            percent = 0

        self.strengthBar.set_value(percent)

    @pyqtSlot()
    def __eye_clicked(self):
        if self.lineEdit.echoMode() is QLineEdit.EchoMode.Password:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.pushButtonEye.setIcon(self.__eyeHiddenIcon)
        else:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            self.pushButtonEye.setIcon(self.__eyeShowIcon)
