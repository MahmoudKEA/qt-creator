# Qt Creator Library
#### This library is designed to build Qt6 applications more easily, quickly and flexibly
- It provides more professional tools as well
- Designed by: Mahmoud Khalid

## Requirements for Python 3
    pip install PyQt6
    pip install pyqrcode
    pip install password_strength

## Usage
```python
import QtCreator


# Create main widget
class Application(QtCreator.QuickMainWidget):
    def __init__(self, parent):
        super(Application, self).__init__(
            parent=parent,
            flags=QtCreator.Qt.WindowType.SubWindow,
            attribute=QtCreator.Qt.WidgetAttribute.WA_StyledBackground,
            resizable=True,
            object_name="mainWidget"
        )

        # Create layout
        layout = QtCreator.QHBoxLayout()
        self.mainWidget.setLayout(layout)
        self.resize(300, 450)

        # Create lineEdit object
        self.lineEdit = QtCreator.QuickLineEdit(
            parent=self,
            placeholder_text="Username",
            clearable=True,
            add_icon=True,
            icon=QtCreator.QPixmap('userIcon.png'),
            fixed_height=41,
            object_name="lineEdit"
        )
        layout.addWidget(self.lineEdit)

        # Create pushButton object
        self.pushButton = QtCreator.QuickPushButton(
            parent=self,
            text="Login",
            font_size=14,
            fixed_height=41,
            object_name="pushButton"
        )
        layout.addWidget(self.pushButton)
```

### Go to the test folder to check full application built by QtCreator
    python test/qtcreator_unittesting.py

<a href="https://ibb.co/HXbM0Hj">
    <img src="https://i.ibb.co/V3zhdqs/2022-07-07-225608.png" alt="2022-07-07-225608" border="0">
</a>
