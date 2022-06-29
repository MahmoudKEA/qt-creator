from apptest import *
import unittest
import sys


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_app():
        app = QApplication(sys.argv)
        main = Application()
        main.show()
        app.exec()


if __name__ == '__main__':
    unittest.main()
