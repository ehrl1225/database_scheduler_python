from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QCheckBox, QLabel, \
    QSpinBox, QMessageBox
from utils.DataManager import DataManager
from utils.PostgreSQLManager import PostSQLManager
from widgets.ClassDataGroupBox import ClassDataGroupBox
from widgets.ScheduleTable import ScheduleTable
from widgets.AddDataWidget import AddDataWidget
from widgets.ShowClassData import ShowClassData


class NewTableWidget(QWidget):
    updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.schedule_table = ScheduleTable()
        self.show_class_data = ShowClassData()

        self.class_type_cb = QComboBox()
        self.GE_area_cb = QComboBox()
        self.year_le = QLineEdit()
        self.semester_cb = QComboBox()
        self.point_lb = QLabel("최대 학점")
        self.point_spinbox = QSpinBox()
        self.grade_lb = QLabel("학년")
        self.grade_spinbox = QSpinBox()

        self.selective_list = ClassDataGroupBox()
        self.recommend_list = ClassDataGroupBox()
        self.get_necessary_btn = QPushButton("get")
        self.get_selective_btn = QPushButton("get")
        self.clear_necessart_btn = QPushButton("clear")
        self.clear_selective_btn = QPushButton("clear")
        self.apply_selected_btn = QPushButton("apply")
        self.add_data_wg = AddDataWidget()
        self.add_data_btn = QPushButton("add data", self)

        self.selective_chb = QCheckBox()
        self.recommend_chb = QCheckBox()

        self.current_point_lb = QLabel("현재 학점 : 0")

        self.point_spinbox.setValue(21)
        self.grade_spinbox.setValue(1)
        self.grade_spinbox.setMinimum(1)
        self.class_type_cb.currentIndexChanged.connect(self.class_type_cb_work)
        self.add_data_btn.pressed.connect(self.add_data_wg.show)
        self.year_le.setText(str(DataManager.get_current_year()))
        self.schedule_table.cellClicked.connect(self.selected_table)

        for s in DataManager.get_semester_kor():
            self.semester_cb.addItem(s)
        self.semester_cb.setCurrentIndex(DataManager.get_current_semester_index())

        for st in DataManager.get_selective_types():
            self.class_type_cb.addItem(st)

        self.GE_area_cb.addItem("전체")
        for gea in DataManager.get_ge_areas():
            self.GE_area_cb.addItem(gea)

        self.selective_list.check_changed.connect(self.set_table)
        self.recommend_list.check_changed.connect(self.set_table)

        self.get_necessary_btn.pressed.connect(self.get_selective)
        self.get_selective_btn.pressed.connect(self.get_recommend)
        self.clear_necessart_btn.pressed.connect(self.selective_list.clear)
        self.clear_selective_btn.pressed.connect(self.recommend_list.clear)

        self.apply_selected_btn.pressed.connect(self.apply)

        self.selective_chb.stateChanged.connect(self.set_selective_all)
        self.recommend_chb.stateChanged.connect(self.set_recommend_all)

        main_hbox = QHBoxLayout()

        table_vbox = QVBoxLayout()
        table_vbox.addWidget(self.schedule_table)
        table_vbox.addWidget(self.show_class_data)

        main_hbox.addLayout(table_vbox)

        vbox = QVBoxLayout()

        vbox.addWidget(self.add_data_btn)

        cb_hbox = QHBoxLayout()
        cb_hbox.addWidget(self.class_type_cb)
        cb_hbox.addWidget(self.GE_area_cb)
        vbox.addLayout(cb_hbox)

        time_hbox = QHBoxLayout()
        time_hbox.addWidget(self.year_le)
        time_hbox.addWidget(self.semester_cb)
        vbox.addLayout(time_hbox)

        point_hbox = QHBoxLayout()
        point_hbox.addWidget(self.current_point_lb)
        point_hbox.addWidget(self.point_lb)
        point_hbox.addWidget(self.point_spinbox)
        vbox.addLayout(point_hbox)

        grade_hbox = QHBoxLayout()
        grade_hbox.addWidget(self.grade_lb)
        grade_hbox.addWidget(self.grade_spinbox)
        vbox.addLayout(grade_hbox)

        chb_hbox = QHBoxLayout()
        chb_hbox.addWidget(self.selective_chb)
        chb_hbox.addWidget(self.recommend_chb)
        vbox.addLayout(chb_hbox)

        list_hbox = QHBoxLayout()
        list_hbox.addWidget(self.selective_list)
        list_hbox.addWidget(self.recommend_list)
        vbox.addLayout(list_hbox)

        get_hbox = QHBoxLayout()
        get_hbox.addWidget(self.get_necessary_btn)
        get_hbox.addWidget(self.get_selective_btn)
        vbox.addLayout(get_hbox)

        clear_hbox = QHBoxLayout()
        clear_hbox.addWidget(self.clear_necessart_btn)
        clear_hbox.addWidget(self.clear_selective_btn)
        vbox.addLayout(clear_hbox)


        vbox.addWidget(self.apply_selected_btn)

        main_hbox.addLayout(vbox)

        self.setLayout(main_hbox)

    def set_current_point_lb(self):
        total = 0
        total += DataManager.sum_points(self.selective_list.get_data())
        total += DataManager.sum_points(self.recommend_list.get_data())
        self.current_point_lb.setText(f"현재 학점 : {total}")

    def set_selective_all(self):
        if self.selective_chb.isChecked():
            self.selective_list.check_all()

    def set_recommend_all(self):
        if self.recommend_chb.isChecked():
            self.recommend_list.check_all()

    @pyqtSlot(int, int)
    def selected_table(self, row, col):
        datas = self.selective_list.get_data()
        datas2 = self.recommend_list.get_data()
        class_datas = datas + datas2
        class_data, index = DataManager.rowcol2class_data(row, col, class_datas)
        if class_data is not None:
            self.show_class_data.set_class_data(class_data, index)


    def setting(self):
        if DataManager.has_login():
            student = DataManager.current_student
            self.grade_spinbox.setValue(student.get_current_grade())

    def class_type_cb_work(self):
        if self.class_type_cb.currentText() != "선교":
            self.GE_area_cb.setDisabled(True)
        else:
            self.GE_area_cb.setEnabled(True)

    def set_table(self):
        self.set_current_point_lb()
        self.schedule_table.clear()
        self.schedule_table.set_class_datas(self.selective_list.get_data())
        self.schedule_table.set_class_datas(self.recommend_list.get_data())

    def get_selective(self):
        if DataManager.has_login():
            student = DataManager.get_current_student()
            department = student.get_department()
            major = student.get_major()
            class_type = self.class_type_cb.currentText()
            year = self.year_le.text()
            if not DataManager.check_year_str(year):
                return
            year = int(year)
            semester = self.semester_cb.currentText()
            eng_semester = DataManager.get_semester_kor2eng(semester)
            grade = self.grade_spinbox.value()
            if self.GE_area_cb.currentIndex() == 0:
                ge_area = None
            else:
                ge_area = self.GE_area_cb.currentIndex()
            if class_type == "전공":
                datas = PostSQLManager.get_necessary_classes(student, grade, year, eng_semester)

            else:
                datas = PostSQLManager.get_selective_classes(class_type, ge_area, year, eng_semester, grade,
                                                             department=department, major=major)
            class_datas = DataManager.datas2classDatas(datas)


            self.selective_list.del_not_checked()
            if class_datas is not None:
                self.selective_list.set_items(class_datas)

    def get_recommend(self):
        if DataManager.has_login():
            student = DataManager.get_current_student()
            self.recommend_list.del_not_checked()
            year = self.year_le.text()
            semester = self.semester_cb.currentText()
            grade = self.grade_spinbox.value()
            eng_semester = DataManager.get_semester_kor2eng(semester)
            selected_class_data = self.selective_list.get_data() + self.recommend_list.get_data()
            if not DataManager.check_year_str(year):
                return
            year = int(year)
            datas = PostSQLManager.get_recommend(
                student=student,
                selected_class_data=selected_class_data,
                year = year,
                semester = eng_semester,
                grade=grade
            )
            class_datas = DataManager.datas2classDatas(datas)
            if class_datas is not None:
                class_datas = DataManager.subtract_time(selected_class_data, class_datas)
                self.recommend_list.set_items(class_datas)


    def apply(self):
        if DataManager.has_login():
            student = DataManager.get_current_student()
            datas = self.selective_list.get_data()
            datas2 = self.recommend_list.get_data()
            class_datas = datas + datas2
            intersections = DataManager.get_intersections(class_datas)
            year = self.year_le.text()
            semester = self.semester_cb.currentText()
            eng_semester = DataManager.get_semester_kor2eng(semester)
            if not DataManager.check_year_str(year):
                return
            year = int(year)
            PostSQLManager.del_attends(
                student.get_student_id(),
                year,
                eng_semester
            )
            if len(intersections)>1:
                QMessageBox.warning(self, "경고", "겹치는 시간이 존재합니다.")
                return
            if DataManager.has_same_name(class_datas):
                QMessageBox.warning(self, "경고", "겹치는 과목이 존재합니다.")
                return
            if DataManager.sum_points(class_datas)>self.point_spinbox.value():
                QMessageBox.warning(self, "경고", "최대 학점을 넘었습니다.")
            for class_data in class_datas:
                PostSQLManager.add_attends(
                    student.get_student_id(),
                    class_data
                )
            self.updated.emit()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = NewTableWidget()
    wg.show()
    sys.exit(app.exec_())
