from .header import *
from .widgetform import StandardForm
from .quickwidget import QuickWidget


class QuickMenu(QMenu, StandardForm):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType(
                Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.Popup
                | Qt.WindowType.NoDropShadowWindowHint
            ),
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_TranslucentBackground,
            position: QPoint = QPoint(11, 11),
            resizable: bool = False,
            margin: typing.Union[int, list] = 11,
            shadow: QGraphicsDropShadowEffect = None,
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.ClickFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None
    ):
        super(QuickMenu, self).__init__(
            parent, fixed_size=fixed_size, fixed_width=fixed_width, fixed_height=fixed_height,
            object_name=object_name
        )

        self.__position = position

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

    def exec(self, *__args):
        point = None
        __args = list(__args)

        for i in __args:
            if isinstance(i, QPoint):
                point = i
                break

        self.mainWidget.adjustSize()
        self.adjustSize()

        if not point:
            point = QCursor().pos()
            desktop_geometry = self.screen().geometry()

            if (desktop_geometry.width() - point.x()) < self.width():
                point.setX(point.x() - self.width())
            else:
                point.setX(point.x() + self.__position.x())

            if (desktop_geometry.height() - point.y()) < self.height():
                point.setY(point.y() - self.height())
            else:
                point.setY(point.y() + self.__position.y())

            __args.append(point)

        super(QuickMenu, self).exec(*__args)
