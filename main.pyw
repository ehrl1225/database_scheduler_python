from widgets.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from utils.PostgreSQLManager import test_set, outside_set, laptop_set

if __name__ == '__main__':
    laptop_set()
    # outside_set()
    app = QApplication(sys.argv)
    wg = MainWindow()
    sys.exit(app.exec_())