from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import io
import pyqrcode


def text_ellipsis(
        target, mode: Qt.TextElideMode = Qt.TextElideMode.ElideRight,
        tooltip: bool = False, width: int = None
):
    text = target.text()
    if not width:
        width = target.contentsRect().width()

    metrics = QFontMetrics(target.font())
    if metrics.horizontalAdvance(text) > width:
        elided = metrics.elidedText(text, mode, width)
        target.setText(elided)

        if tooltip:
            target.setToolTip(text)


def scroll_step(target, step: int = 8):
    target.verticalScrollBar().setSingleStep(step)
    target.horizontalScrollBar().setSingleStep(step)


def view_list_style(target, icon_size: QSize = QSize(21, 21), no_shadow: bool = False):
    flags = Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
    if no_shadow:
        flags |= Qt.WindowType.NoDropShadowWindowHint
    list_view = QListView()
    list_view.setIconSize(icon_size)
    target.setView(list_view)
    target.view().window().setWindowFlags(flags)
    target.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)


def update_polish(target):
    target.style().unpolish(target)
    target.style().polish(target)


def translator(text: str):
    QApplication.translate('Form', text)


def clipboard(text: str):
    if not text:
        return

    clip = QApplication.clipboard()
    clip.clear(mode=clip.Mode.Clipboard)
    clip.setText(text, mode=clip.Mode.Clipboard)


def url_open(url: str):
    if not url:
        return

    _url = QUrl(url)
    QDesktopServices().openUrl(_url)


def qr_creator(
        text: str, size: QSize, font_color: QColor = QColor(Qt.GlobalColor.black),
        background_color: QColor = QColor(Qt.GlobalColor.transparent)
) -> QPixmap:
    image_file = io.BytesIO()

    generator = pyqrcode.create(text, error='L', mode='binary')
    generator.png(
        image_file, scale=7, module_color=font_color.getRgb(), background=background_color.getRgb()
    )

    image = QImage.fromData(image_file.getvalue(), 'png').scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
    return QPixmap.fromImage(image)
