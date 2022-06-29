from qtcreator import *


class SettingsDialog(QuickDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(
            parent, shadow=QuickShadow()
        )

        self.labelTitle = QuickLabel(
            self, "Settings Window", font_size=14, fixed_height=31
        )

        self.pushButtonClose = QuickPushButton(
            self, icon=QIcon('styles/close.png'), icon_size=QSize(16, 16), fixed_size=QSize(24, 24),
            object_name='pushButtonClose'
        )
        self.pushButtonClose.clicked.connect(self.close)

        self.lineEditUsername = QuickLineEdit(
            self, "Mahmoud", font_size=12, fixed_height=41
        )

        tooltip_show = QuickToolTipMessage(
            self, "Show / Hide Text", font_size=10
        )

        self.lineEditPassword = QuickLineEditPassword(
            self, font_size=12, fixed_height=41, eye_tooltip=tooltip_show
        )
        self.lineEditPassword.lineEdit.setText('123456789')
        self.lineEditPassword.set_eye_icon(
            show=QIcon('styles/eye-visible.png'), hidden=QIcon('styles/eye-invisible.png')
        )

        tooltip = QuickToolTipMessage(
            self, "OTP Confirmation Code", font_size=10
        )

        self.lineEditOTP = QuickLineEditMultiple(
            self, count=6, space_index=3, placeholder_text='-', font_size=16,
            fixed_size=QSize(21, 31), margin=21, mode=QLineEdit.EchoMode.Password,
            add_eye=True, eye_tooltip=tooltip_show, tooltip=tooltip
        )
        self.lineEditOTP.set_eye_icon(
            show=QIcon('styles/eye-visible.png'), hidden=QIcon('styles/eye-invisible.png')
        )

        self.comboboxTheme = QuickComboBox(
            self, ['Light Mode', 'Dark Mode'], font_size=12, fixed_height=51, no_shadow=True
        )

        self.labelAutoBackup = QuickLabel(
            self, "Backup Automatically", font_size=12, fixed_height=21
        )

        self.checkboxAutoBackup = QuickCheckBox(
            self, checked=True, fixed_size=QSize(21, 21)
        )

        tooltip = QuickToolTipMessage(
            self, "Backup is disabled", font_size=10
        )

        self.switchAutoBackup = QuickSwitch(
            self, thumb_radius=12, track_color_on=QColor('#fec202'), thumb_color_on=QColor('orange'),
            track_color_off=QColor('gray'), thumb_color_off=QColor('black'), tooltip=tooltip
        )
        self.switchAutoBackup.clicked.connect(self.switch_clicked)

        self.labelProxy = QuickLabel(
            self, "Would you like to use a proxy?", font_size=12, fixed_height=21
        )

        self.radioButtonProxyEnabled = QuickRadioButton(
            self, "Proxy Enabled", checked=True, font_size=10, fixed_height=21
        )

        self.radioButtonProxyDisabled = QuickRadioButton(
            self, "Proxy Disabled", font_size=10, fixed_height=21
        )

        address_text = '0x0000000000000000000000000000000000000000'
        qr_image = utility.qr_creator(
            address_text, QSize(200, 200), font_color=QColor(Qt.GlobalColor.white)
        )
        tooltip_address = QuickToolTipMessage(
            self, color=QColor(Qt.GlobalColor.gray), add_icon=True, icon=qr_image
        )

        self.labelAddress = QuickLabelAddress(
            self, address_text, 'https://bscscan.com/address',
            add_copy=True, add_browse=True, font_size=12, fixed_width=151, tooltip=tooltip_address,
            copy_icon=QIcon('styles/copy.png'), browse_icon=QIcon('styles/browse.png')
        )
        self.labelAddress.pushButtonCopy.clicked.connect(self.copy_clicked)

        layout = QGridLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setVerticalSpacing(21)
        layout.addWidget(self.labelTitle, 0, 0, 1, 2)
        layout.addWidget(self.pushButtonClose, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.lineEditUsername, 1, 0, 1, 2)
        layout.addWidget(self.lineEditPassword, 2, 0, 1, 2)
        layout.addWidget(self.lineEditOTP, 3, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.comboboxTheme, 4, 0, 1, 2)
        layout.addWidget(self.labelAutoBackup, 5, 0, 1, 2)
        layout.addWidget(self.checkboxAutoBackup, 5, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.switchAutoBackup, 5, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.labelProxy, 6, 0, 1, 2)
        layout.addWidget(self.radioButtonProxyEnabled, 7, 0, 1, 1)
        layout.addWidget(self.radioButtonProxyDisabled, 7, 1, 1, 1)
        layout.addWidget(self.labelAddress, 8, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        self.mainWidget.setLayout(layout)

        self.__animate = None
        self.__leftClickPressed = None
        self.__clickPressedX = None
        self.__clickPressedY = None

    def showEvent(self, a0: QShowEvent):
        super(SettingsDialog, self).showEvent(a0)

        self.__animate = animation.OpacityMotion(
            self, property_type=animation.Property.OPACITY
        )
        self.__animate.temp_show(1000).start()

    def mousePressEvent(self, event):
        super(QuickDialog, self).mousePressEvent(event)

        is_maximized = self.isMaximized()

        if event.button() == Qt.MouseButton.LeftButton and self.underMouse() and not is_maximized:
            self.__clickPressedX = event.pos().x()
            self.__clickPressedY = event.pos().y()
            self.__leftClickPressed = True

    def mouseReleaseEvent(self, event):
        super(QuickDialog, self).mouseReleaseEvent(event)

        self.__leftClickPressed = False

    def mouseMoveEvent(self, event):
        super(QuickDialog, self).mouseMoveEvent(event)

        if self.__leftClickPressed:
            x = int(event.globalPosition().x() - self.__clickPressedX)
            y = int(event.globalPosition().y() - self.__clickPressedY)
            self.move(x, y)

    @pyqtSlot(bool)
    def switch_clicked(self, checked: bool):
        if checked:
            self.switchAutoBackup.tooltip.labelText.setText("Backup is enabled")
        else:
            self.switchAutoBackup.tooltip.labelText.setText("Backup is disabled")

    @pyqtSlot()
    def copy_clicked(self):
        notify = QuickNotifyMessageListWidgetItem(
            self, "Copied Successfully", font_size=12,
            add_icon=True, icon=QPixmap('styles/ok.png'), icon_scaled=True, icon_size=QSize(31, 31),
            fixed_size=QSize(301, 51)
        )
        self.parent().parent().parent().notifyListWidget.add_item(notify)


class MenuWidget(QuickMenu):
    def __init__(self, parent):
        super(MenuWidget, self).__init__(
            parent, fixed_width=201
        )

        self.pushButtonAbout = QuickPushButton(
            self, "About", font_size=12, icon=QIcon('styles/info.png'), fixed_height=41
        )
        self.pushButtonAbout.clicked.connect(self.about_clicked)

        self.pushButtonExit = QuickPushButton(
            self, "Exit", font_size=12, icon=QIcon('styles/close.png'), fixed_height=41
        )
        self.pushButtonExit.clicked.connect(self.close_clicked)

        layout = QVBoxLayout()
        layout.setContentsMargins(11, 11, 11, 11)
        layout.addWidget(self.pushButtonAbout)
        layout.addWidget(self.pushButtonExit)
        self.mainWidget.setLayout(layout)

    def showEvent(self, a0: QShowEvent):
        super(MenuWidget, self).showEvent(a0)

        animate = animation.OpacityMotion(
            self, property_type=animation.Property.OPACITY
        )
        animate.temp_show().start()

    def about_clicked(self):
        self.close()

    def close_clicked(self):
        self.nativeParentWidget().close()


class HeaderWidget(QuickWidget):
    def __init__(self, parent):
        super(HeaderWidget, self).__init__(
            parent, fixed_height=81,
            animation_value_changed=self.background_color_changed,
            animation_start_value=QColor(0, 0, 0, 200), animation_end_value=QColor(0, 0, 0, 255),
            animation_duration=500
        )

        self.labelAvatar = QuickLabel(
            self, fixed_size=QSize(51, 51), scaled=True, pixmap=QPixmap('styles/avatar.png'),
            animation_value_changed=self.size_changed,
            animation_start_value=QSize(51, 51), animation_end_value=QSize(71, 71)
        )

        self.labelUsername = QuickLabel(
            self, "Hi, Mahmoud!", font_size=16, fixed_size=QSize(140, 21), object_name='labelUsername'
        )

        self.labelStatus = QuickLabel(
            self, "Online", font_size=10, fixed_size=QSize(140, 21), object_name='labelStatus'
        )

        self.dialogSettings = SettingsDialog(self)

        self.pushButtonSettings = QuickPushButton(
            self, "Settings", font_size=10, fixed_size=QSize(81, 31), object_name='pushButtonSettings'
        )
        self.pushButtonSettings.clicked.connect(self.settings_clicked)

        self.menuWidget = MenuWidget(self)

        self.pushButtonMenu = QuickPushButton(
            self, icon=QIcon('styles/menu.png'), fixed_size=QSize(31, 31)
        )
        self.pushButtonMenu.clicked.connect(self.menu_clicked)

        layout = QGridLayout()
        layout.setContentsMargins(21, 0, 11, 0)
        layout.addWidget(self.labelAvatar, 0, 0, 2, 1)
        layout.addWidget(self.labelUsername, 0, 1, 1, 1, Qt.AlignmentFlag(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        ))
        layout.addWidget(self.labelStatus, 1, 1, 1, 1, Qt.AlignmentFlag(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        ))
        layout.addWidget(self.pushButtonSettings, 0, 2, 2, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.pushButtonMenu, 0, 3, 2, 1)
        self.setLayout(layout)

        self.__leftClickPressed = None
        self.__clickPressedX = None
        self.__clickPressedY = None

    def mousePressEvent(self, event):
        super(HeaderWidget, self).mousePressEvent(event)

        is_maximized = self.nativeParentWidget().isMaximized()

        if event.button() == Qt.MouseButton.LeftButton and self.underMouse() and not is_maximized:
            margin = self.nativeParentWidget().layout().contentsRect()
            self.__clickPressedX = event.pos().x() + margin.x()
            self.__clickPressedY = event.pos().y() + margin.y()
            self.__leftClickPressed = True

    def mouseReleaseEvent(self, event):
        super(HeaderWidget, self).mouseReleaseEvent(event)

        self.__leftClickPressed = False

    def mouseMoveEvent(self, event):
        super(HeaderWidget, self).mouseMoveEvent(event)

        if self.__leftClickPressed:
            x = int(event.globalPosition().x() - self.__clickPressedX)
            y = int(event.globalPosition().y() - self.__clickPressedY)
            self.nativeParentWidget().move(x, y)

    def settings_clicked(self):
        self.dialogSettings.exec()

    def menu_clicked(self):
        point = self.pushButtonMenu.mapToGlobal(QPoint())
        point.setY(point.y() + 41)
        self.menuWidget.exec(point)

    def background_color_changed(self, value: QColor):
        css = '''
        HeaderWidget
        {
            background-color: rgba%s;
        }
        ''' % str(value.getRgb())
        self.sender().parent().setStyleSheet(css)

    def size_changed(self, value: QSize):
        self.sender().parent().setFixedSize(value)


class MessageWidget(QuickListWidgetItem):
    def __init__(self, parent, message: str, align: Qt.AlignmentFlag):
        super(MessageWidget, self).__init__(parent)

        if align is Qt.AlignmentFlag.AlignLeft:
            alignment = Qt.AlignmentFlag.AlignRight
            color = QColor(Qt.GlobalColor.gray)
        else:
            alignment = Qt.AlignmentFlag.AlignLeft
            color = QColor('#fec202')

        tooltip = QuickToolTipMessage(
            self, message, font_size=12, align=alignment, arrow_size=QSize(10, 15), color=color,
            margin=[21, 11, 21, 11], arrow_align=Qt.AlignmentFlag.AlignBottom
        )
        tooltip.setMaximumWidth(301)
        tooltip.exec()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(tooltip, alignment=align)
        self.setLayout(layout)

        self.size_update()


class ChatWidget(QuickListWidget):
    def __init__(self, parent):
        empty_widget = EmptyListWidget(
            parent, illustration=QPixmap('styles/message.png'),
            title="no messages has been sent yet!".capitalize(),
            description="let's send your first message now.".capitalize(), spacing=6
        )
        font = QFont()
        font.setPointSize(12)
        empty_widget.labelDescription.setFont(font)
        font.setPointSize(14)
        font.setBold(True)
        empty_widget.labelTitle.setFont(font)

        super(ChatWidget, self).__init__(
            parent, empty_list_widget=empty_widget
        )

        self.pushButtonHistory = QuickPushButton(
            self, "Get History", font_size=12, add_spinner=True, fixed_size=QSize(201, 41),
            object_name='pushButtonHistory'
        )
        self.pushButtonHistory.clicked.connect(self.pushButtonHistory.spinner.start)
        empty_widget.layout().addWidget(self.pushButtonHistory, alignment=Qt.AlignmentFlag.AlignHCenter)

    def model_changed(self):
        super(ChatWidget, self).model_changed()

        is_exists = self.count() > 0
        self.setProperty('hasContent', is_exists)
        utility.update_polish(self)


class SendBarWidget(QuickWidget):
    def __init__(self, parent):
        super(SendBarWidget, self).__init__(
            parent, fixed_height=81, animation_value_changed=self.background_color_changed,
            animation_start_value=QColor(0, 0, 0, 200), animation_end_value=QColor(0, 0, 0, 255),
            animation_duration=500
        )

        self.lineEditMessage = QuickLineEdit(
            self, placeholder_text="What's on your mind?", font_size=12, length=200,
            fixed_height=41, clearable=True
        )

        self.pushButtonEmoji = QuickPushButton(
            self, icon=QIcon('styles/emoji.png'), icon_size=QSize(24, 24), fixed_size=QSize(31, 31)
        )
        self.pushButtonEmoji.clicked.connect(self.emoji_clicked)

        tooltip = QuickToolTipMessage(
            self, "Publish your message to everyone.", shadow=QuickShadow(color=QColor('#fec202')),
            font_size=10, margin=[21, 11, 11, 11], add_close=True, close_icon=QIcon('styles/close.png')
        )

        self.pushButtonSend = QuickPushButton(
            self, icon=QIcon('styles/send.png'), icon_size=QSize(24, 24),
            fixed_size=QSize(31, 31), tooltip=tooltip
        )
        self.pushButtonSend.clicked.connect(self.send_message_clicked)

        layout = QHBoxLayout()
        layout.setContentsMargins(11, 11, 11, 21)
        layout.addWidget(self.lineEditMessage)
        layout.addWidget(self.pushButtonEmoji)
        layout.addWidget(self.pushButtonSend)
        self.setLayout(layout)

        self.nextAlign = None

    def emoji_clicked(self):
        change_button = QuickPushButton(
            self, "Change", font_size=10, fixed_size=QSize(101, 31)
        )

        messagebox = QuickMessageBox(
            self, title="Chat Message", title_align=Qt.AlignmentFlag.AlignHCenter, title_font_size=12,
            close_icon=QIcon('styles/close.png'), close_icon_size=QSize(16, 16), add_icon=True,
            text="This is chat interface for testing PyQt SDK development", text_font_size=12,
            accept_button="Accept", cancel_button="Cancel", inputs=[change_button], shadow=QuickShadow()
        )
        change_button.clicked.connect(lambda: messagebox.labelIcon.setPixmap(QPixmap('styles/ok.png')))
        messagebox.exec()

        notify = QuickNotifyMessageListWidgetItem(
            self, f"Clicked On: {messagebox.clickedOn.objectName()}", font_size=12,
            add_icon=True, icon=QPixmap('styles/ok.png'), icon_scaled=True, icon_size=QSize(31, 31),
            fixed_size=QSize(301, 51)
        )
        self.parent().parent().notifyListWidget.add_item(notify)

    def send_message_clicked(self):
        if self.nextAlign is Qt.AlignmentFlag.AlignLeft:
            self.nextAlign = Qt.AlignmentFlag.AlignRight
        else:
            self.nextAlign = Qt.AlignmentFlag.AlignLeft

        text = self.lineEditMessage.text()
        message = MessageWidget(
            self, message=text, align=self.nextAlign
        )
        self.parent().parent().chatWidget.add_item(message)

        notify = QuickNotifyMessageListWidgetItem(
            self, "The message sent successfully", font_size=12,
            add_icon=True, icon=QPixmap('styles/ok.png'), icon_scaled=True, icon_size=QSize(31, 31),
            fixed_size=QSize(301, 51)
            # , add_close=True, close_icon=QIcon('styles/close.png')
        )
        self.parent().parent().notifyListWidget.add_item(notify)

        self.lineEditMessage.clear()

    def background_color_changed(self, value: QColor):
        css = '''
        SendBarWidget
        {
            background-color: rgba%s;
        }
        ''' % str(value.getRgb())
        self.sender().parent().setStyleSheet(css)


class Application(QuickMainWidget):
    def __init__(self, parent=None):
        super(Application, self).__init__(
            parent, resizable=True
        )

        self.resize(400, 650)
        self.set_stylesheet()

        self.headerWidget = HeaderWidget(self)
        self.chatWidget = ChatWidget(self)
        self.sendBarWidget = SendBarWidget(self)
        self.notifyListWidget = QuickNotifyListWidget(
            self, mode=QuickNotifyListWidget.Mode.INTERNAL,
            align=Qt.AlignmentFlag(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        )

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.headerWidget, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.chatWidget, 1, 0, 1, 1)
        layout.addWidget(self.sendBarWidget, 2, 0, 1, 1, Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.notifyListWidget, 0, 0, 3, 1)
        self.mainWidget.setLayout(layout)

    def set_stylesheet(self):
        with open('styles/stylesheet.css', 'r') as file:
            self.setStyleSheet(file.read())
