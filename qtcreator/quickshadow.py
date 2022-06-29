from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class QuickShadow(QGraphicsDropShadowEffect):
    def __init__(
            self, parent=None,
            color: QColor = QColor(0, 0, 0, 150),
            radius: int = 20,
            offset: int = 0,
            offset_x: int = 0,
            offset_y: int = 0
    ):
        super(QuickShadow, self).__init__(parent)

        self.setBlurRadius(radius)
        self.setColor(color)

        if offset_x or offset_y:
            self.setXOffset(offset_x)
            self.setYOffset(offset_y)
        else:
            self.setOffset(offset)
