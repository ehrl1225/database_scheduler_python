from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QTabWidget
from widgets.CurrentTableWidget import CurrentTableWidget
from widgets.NewTableWidget import NewTableWidget
import sys


class ScheduleWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.main_tabs = QTabWidget()

        self.current_table_wg = CurrentTableWidget()
        self.new_table_wg = NewTableWidget()


        self.main_tabs.addTab(self.current_table_wg, "current")
        self.main_tabs.addTab(self.new_table_wg, "new")
        self.main_tabs.currentChanged.connect(self.index_changed)
        self.new_table_wg.updated.connect(self.current_table_wg.get_attends)

        vbox = QVBoxLayout()
        vbox.addWidget(self.main_tabs)

        self.setLayout(vbox)

    def index_changed(self):
        if self.main_tabs.currentIndex()==1:
            self.new_table_wg.setting()

    def set_current(self):
        self.current_table_wg.get_attends()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wg = ScheduleWidget()
    wg.show()
    sys.exit(app.exec_())
