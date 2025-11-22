from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout
from utils.PostgreSQLManager import PostSQLManager
from utils.DataManager import DataManager
from widgets.ScheduleTable import ScheduleTable
from widgets.ShowClassData import ShowClassData


class CurrentTableWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(ScheduleTable(), "빈 스케줄")
        self.refresh_btn = QPushButton("불러오기")
        self.show_class_data_wg = ShowClassData()
        self.refresh_btn.pressed.connect(self.get_attends)

        main_hbox = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(self.refresh_btn)
        main_hbox.addLayout(vbox)

        main_hbox.addWidget(self.show_class_data_wg)

        self.setLayout(main_hbox)

    def get_attends(self):
        if DataManager.has_login():
            self.tabs.clear()
            student = DataManager.get_current_student()
            times = PostSQLManager.get_attended_time(student.student_id)
            if times == []:
                self.tabs.addTab(ScheduleTable(), "빈 스케줄")
                return
            times.sort(key=lambda x: (x[0], DataManager.get_eng_semester_index(x[1])))
            for year, semester in times:
                data = PostSQLManager.get_attended_classes(
                    student=student,
                    year=year,
                    semester=semester
                )
                class_datas = DataManager.datas2classDatas(data)
                self.add_table(year, semester, class_datas)

    def add_table(self, year, semester, class_datas):
        table = ScheduleTable()
        table.set_class_datas(class_datas)
        kor_semester = DataManager.get_semester_eng2kor(semester)
        name = f"{year}-{kor_semester}"
        self.tabs.addTab(table, name)
        table.cellClicked.connect(self.show_class_data)

    @pyqtSlot(int, int)
    def show_class_data(self, row, col):
        table: ScheduleTable = self.tabs.currentWidget()
        class_datas = table.get_class_datas()
        class_data, index = DataManager.rowcol2class_data(row, col, class_datas)
        if class_data is not None:
            self.show_class_data_wg.set_class_data(class_data, index)
