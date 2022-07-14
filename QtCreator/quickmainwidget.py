from .header import *
from .quickshadow import QuickShadow
from .quickwidget import QuickWidget


class QuickMainWidget(QuickWidget):
    def __init__(
            self, parent=None,
            flags: Qt.WindowType = Qt.WindowType.FramelessWindowHint,
            attribute: Qt.WidgetAttribute = Qt.WidgetAttribute.WA_TranslucentBackground,
            resizable: bool = True,
            margin: typing.Union[int, list] = 11,
            shadow: QGraphicsDropShadowEffect = QuickShadow(),
            focus_policy: Qt.FocusPolicy = Qt.FocusPolicy.ClickFocus,
            fixed_size: QSize = None,
            fixed_width: int = None,
            fixed_height: int = None,
            object_name: str = None
    ):
        super(QuickMainWidget, self).__init__(
            parent, flags=flags, attribute=attribute, fixed_size=fixed_size,
            fixed_width=fixed_width, fixed_height=fixed_height, object_name=object_name
        )

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
