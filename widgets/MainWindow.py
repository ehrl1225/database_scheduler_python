from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from widgets.AccountWidget import AccountWidget
from widgets.ScheduleWidget import ScheduleWidget
from widgets.Worker import Worker

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.worker = Worker()
        self.account_wg = AccountWidget()
        self.setCentralWidget(self.account_wg)

        self.worker.start()

        self.account_wg.logined.connect(self.login)
        self.account_wg.adjust.connect(self.adjustSize)

        self.schedule_wg = ScheduleWidget()
        self.adjustSize()
        self.show()

    def login(self):
        self.account_wg.close()
        self.setCentralWidget(self.schedule_wg)
        self.schedule_wg.set_current()
