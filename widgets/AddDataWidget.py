from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QListWidget, QHBoxLayout, \
    QCheckBox, QLineEdit, QComboBox, QMessageBox
from utils.DataManager import DataManager
from utils.PostgreSQLManager import PostSQLManager, test_set
from utils.Task import Task
from widgets.Worker import Worker
import clipboard
from functools import partial
import sys


class AddDataWidget(QWidget):

    '''

    '''

    def __init__(self):
        super().__init__()
        self.current_data = []
        self.initUI()

    def initUI(self):
        self.copy_task = None
        self.paste_btn = QPushButton("붙여넣기")
        self.clear_btn = QPushButton("clear")
        self.apply_btn = QPushButton("apply")
        self.list = QListWidget()
        self.auto_paste_chb = QCheckBox("자동 붙여넣기")
        self.cancel_btn = QPushButton("cancel")
        self.del_btn = QPushButton("del")
        self.year_le = QLineEdit()
        self.semester_cb = QComboBox()

        self.year_le.setText(str(DataManager.get_current_year()))

        for s in DataManager.get_semester_kor():
            self.semester_cb.addItem(s)
        self.semester_cb.setCurrentIndex(DataManager.get_current_semester_index())

        self.paste_btn.pressed.connect(self.paste)
        self.clear_btn.pressed.connect(self.clear_data)
        self.del_btn.pressed.connect(self.del_index)
        self.list.doubleClicked.connect(self.del_index)
        self.apply_btn.pressed.connect(self.apply)
        self.auto_paste_chb.released.connect(self.auto_copy_check)

        vbox = QVBoxLayout()

        paste_hbox = QHBoxLayout()
        paste_hbox.addWidget(self.paste_btn)
        paste_hbox.addWidget(self.auto_paste_chb)

        times_hbox = QHBoxLayout()
        times_hbox.addWidget(self.year_le)
        times_hbox.addWidget(self.semester_cb)


        vbox.addLayout(paste_hbox)
        vbox.addLayout(times_hbox)
        vbox.addWidget(self.list)
        vbox.addWidget(self.clear_btn)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.apply_btn)
        btn_hbox.addWidget(self.del_btn)

        vbox.addLayout(btn_hbox)

        vbox.addWidget(self.cancel_btn)

        self.setLayout(vbox)

    def auto_copy_check(self):
        if self.auto_paste_chb.isChecked():
            self.set_auto_copy()
        else:
            self.unset_auto_copy()

    def set_auto_copy(self):
        self.copy_task = Task(job=self.auto_copy, count=-1)
        self.copy_task()
        Worker.task_list.append(self.copy_task)

    def unset_auto_copy(self):
        Worker.del_task(self.copy_task)

    def auto_copy(self):
        if DataManager.keyboard_copy_detect():
            self.paste()

    def clear_data(self):
        self.list.clear()
        self.current_data = []

    def del_index(self):
        index = self.list.currentRow()
        del self.current_data[index]
        self.list.takeItem(index)

    def paste(self):
        text = clipboard.paste()
        data = DataManager.textToData(text)

        for d in data:
            if d not in self.current_data:
                text = f"{d.class_name} {d.class_number}분 반"
                self.current_data.append(d)
                self.list.addItem(text)

    def apply(self):
        year = self.year_le.text()
        semester = self.semester_cb.currentText()
        count = 0

        if DataManager.check_year_str(year):
            for d in self.current_data:
                eng_semester = DataManager.get_semester_kor2eng(semester)
                DataManager.set_times(d, int(year), eng_semester)
                if not PostSQLManager.check_class_data(d):
                    PostSQLManager.add_class_data(d)
                    count+=1
            QMessageBox.information(self, "업로드 완료", f"{count}개의 데이터가 업로드 되었습니다.")
            self.clear_data()


if __name__ == '__main__':
    test_set()
    app = QApplication(sys.argv)
    wg = AddDataWidget()
    wg.show()
    sys.exit(app.exec_())
