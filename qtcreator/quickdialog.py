from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import Union
from .widgetform import StandardForm
from .quickwidget import QuickWidget


class QuickDialog(QDialog, StandardForm):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType.FramelessWindowHint,
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_TranslucentBackground,
            closeable: bool = True,
            resizable: bool = True,
            margin: Union[int, list] = 11,
            shadow: QGraphicsDropShadowEffect = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.ClickFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None
    ):
        super(QuickDialog, self).__init__(
            parent, fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name
        )

        self.__closeable = closeable
        self.__geometry = None

        self.setWindowFlags(Qt.WindowType(self.windowFlags() | flags))
        self.setAttribute(attribute, True)

        layout = QGridLayout()
        layout.setContentsMargins(*margin if isinstance(margin, list) else [margin] * 4)
        self.setLayout(layout)

        self.mainWidget = QuickWidget(
            self, graphic_effect=shadow, focus_policy=focus_policy, object_name='mainWidget'
        )
        layout.addWidget(self.mainWidget, 0, 0, 1, 1)

        if resizable and not fixed_size:
            self.sizeGrip = QSizeGrip(self)
            self.sizeGrip.setFixedSize(QSize(24, 24))
            layout.addWidget(self.sizeGrip, 0, 0, 1, 1, Qt.AlignmentFlag(
                Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
            ))

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key.Key_Escape:
            if not self.__closeable:
                a0.ignore()
                return

        super(QuickDialog, self).keyPressEvent(a0)

    def exec(self) -> int:
        self.adjustSize()

        if not self.__geometry:
            self.__geometry = self.geometry()

        parent = self.nativeParentWidget()
        self.move(parent.geometry().center() - self.__geometry.center())

        return super(QuickDialog, self).exec()
