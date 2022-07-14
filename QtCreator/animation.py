from .header import *


class Property:
    OPACITY = QByteArray(b'opacity')
    WINDOW_OPACITY = QByteArray(b'windowOpacity')
    MAXIMUM_SIZE = QByteArray(b'maximumWidth')
    GEOMETRY = QByteArray(b'geometry')


class CustomizeMotion(QPropertyAnimation):
    def __init__(
            self, parent, property_type: typing.Union[bytes, QByteArray], duration: int,
            start_value: typing.Any = None, end_value: typing.Any = None, finished: typing.Callable = None
    ):
        super(CustomizeMotion, self).__init__(parent, property_type)

        self.setDuration(duration)

        if start_value:
            self.setStartValue(start_value)

        if end_value:
            self.setEndValue(end_value)

        if callable(finished):
            self.finished.connect(finished)


class OpacityMotion(QPropertyAnimation):
    def __init__(self, parent, property_type: typing.Union[bytes, QByteArray] = None):
        if property_type is Property.OPACITY or not property_type and parent.parent():
            effect = QGraphicsOpacityEffect(parent)
            parent.setGraphicsEffect(effect)
            super(OpacityMotion, self).__init__(effect, Property.OPACITY)

        else:
            super(OpacityMotion, self).__init__(parent, Property.WINDOW_OPACITY)

    def temp_show(self, duration: int = 300, finished: typing.Callable = None) -> QPropertyAnimation:
        self.setDuration(duration)
        self.setStartValue(0)
        self.setEndValue(1)
        self.finished.connect(lambda: self.__finished(finished))

        return self

    def temp_hide(self, duration: int = 500, finished: typing.Callable = None) -> QPropertyAnimation:
        self.setDuration(duration)
        self.setStartValue(1)
        self.setEndValue(0)
        self.finished.connect(lambda: self.__finished(finished))

        return self

    def __finished(self, callback: typing.Callable):
        try:
            self.targetObject().parent().setGraphicsEffect(None)
        except (AttributeError, RuntimeError):
            pass

        if callable(callback):
            callback()


class GeometryMotion(QPropertyAnimation):
    def __init__(self, parent):
        super(GeometryMotion, self).__init__(parent, Property.GEOMETRY)
        self.__parent = parent

    def temp_x(
            self, start_x: int = None, end_x: int = None,
            duration: int = 500, finished: typing.Callable = None
    ) -> QPropertyAnimation:
        rect = self.__parent.geometry()
        if not start_x:
            start_x = rect.x()

        self.setDuration(duration)
        self.setStartValue(QRect(start_x, rect.y(), rect.width(), rect.height()))
        self.setEndValue(QRect(end_x, rect.y(), rect.width(), rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_y(
            self, start_y: int = None, end_y: int = None,
            duration: int = 500, finished: typing.Callable = None
    ) -> QPropertyAnimation:
        rect = self.__parent.geometry()
        if not start_y:
            start_y = rect.y()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), start_y, rect.width(), rect.height()))
        self.setEndValue(QRect(rect.x(), end_y, rect.width(), rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_show(
            self, width: int, duration: int = 500, finished: typing.Callable = None
    ) -> QPropertyAnimation:
        rect = self.__parent.geometry()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), rect.y(), 0, rect.height()))
        self.setEndValue(QRect(rect.x(), rect.y(), width, rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_hide(self, duration: int = 500, finished: typing.Callable = None) -> QPropertyAnimation:
        rect = self.__parent.geometry()

        self.setDuration(duration)
        self.setStartValue(QRect(rect.x(), rect.y(), rect.width(), rect.height()))
        self.setEndValue(QRect(rect.x(), rect.y(), 0, rect.height()))

        if callable(finished):
            self.finished.connect(finished)

        return self


class MaximumWidthMotion(QPropertyAnimation):
    def __init__(self, parent):
        super(MaximumWidthMotion, self).__init__(parent, Property.MAXIMUM_SIZE)
        self.__parent = parent

    def temp_show(
            self, width: int, duration: int = 1000, finished: typing.Callable = None
    ) -> QPropertyAnimation:
        self.setDuration(duration)
        self.setStartValue(0)
        self.setEndValue(width)

        if callable(finished):
            self.finished.connect(finished)

        return self

    def temp_hide(self, duration: int = 500, finished: typing.Callable = None) -> QPropertyAnimation:
        self.setDuration(duration)
        self.setStartValue(self.__parent.width())
        self.setEndValue(0)

        if callable(finished):
            self.finished.connect(finished)

        return self
