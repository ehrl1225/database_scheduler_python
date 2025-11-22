from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QCheckBox, QPushButton, QScrollArea, QWidget
from utils.ClassData import ClassData


class ClassDataGroupBoxItem(QGroupBox):
    x_pressed = pyqtSignal()
    check_changed = pyqtSignal()
    def __init__(self, class_data: ClassData, func):
        super().__init__()
        self.class_data = class_data
        self.func = func
        self.initUI()

    def initUI(self):

        self.chb = QCheckBox(f"{self.class_data.get_full_name()}\n{self.class_data.get_class_times_str()}")
        self.x_btn = QPushButton("X")

        self.x_btn.setMaximumHeight(100)

        self.x_btn.pressed.connect(self.del_self)
        self.chb.stateChanged.connect(self.check_changed.emit)

        hbox = QHBoxLayout()
        hbox.addWidget(self.chb)
        hbox.addWidget(self.x_btn)
        self.setLayout(hbox)

    def del_self(self):
        if self.chb.isChecked():
            self.chb.setCheckState(False)
        self.func(self)

    def isChecked(self) -> bool:
        return self.chb.isChecked()

    def get_class_data(self):
        return self.class_data

    def set_checked(self):
        self.chb.setCheckState(2)

    def set_uncheck(self):
        self.chb.setCheckState(False)

class ClassDataGroupBox(QGroupBox):
    check_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_wg = QWidget()
        self.scroll_area_vbox = QVBoxLayout()

        self.scroll_area_vbox.setAlignment(Qt.AlignTop)

        self.scroll_area_wg.setLayout(self.scroll_area_vbox)
        self.scroll_area.setWidget(self.scroll_area_wg)

        vbox = QVBoxLayout()
        vbox.addWidget(self.scroll_area)

        self.setLayout(vbox)

    def set_items(self, class_datas: list[ClassData]):
        checked_class_datas = self.get_checked_class_data()
        class_datas.sort(key=lambda class_data:str(class_data))
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(i).widget()
            if not wg.isChecked():
                self.delete_item(wg)
        for class_data in class_datas:
            if class_data not in checked_class_datas:
                self.add_item(class_data)

    def add_item(self, class_data: ClassData):
        class_data_item = ClassDataGroupBoxItem(class_data, self.delete_item)
        class_data_item.check_changed.connect(self.check_changed.emit)
        self.scroll_area_vbox.addWidget(class_data_item)

    def delete_item(self, wg:ClassDataGroupBoxItem):
        wg.close()
        self.scroll_area_vbox.removeWidget(wg)

    def get_data(self):
        data = []
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(i).widget()
            if wg.isChecked():
                data.append(wg.get_class_data())
        return data

    def get_not_checked_wg(self):
        wgs:list[ClassDataGroupBoxItem] = []
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(i).widget()
            if not wg.isChecked():
                wgs.append(wg)
        return wgs

    def get_checked_wg(self):
        wgs: list[ClassDataGroupBoxItem] = []
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(i).widget()
            if wg.isChecked():
                wgs.append(wg)
        return wgs

    def get_checked_class_data(self):
        wgs: set[ClassData] = set()
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(i).widget()
            if wg.isChecked():
                wgs.add(wg.get_class_data())
        return wgs

    def del_not_checked(self):
        for wg in self.get_not_checked_wg():
            wg.close()
            self.scroll_area_vbox.removeWidget(wg)

    def clear(self):
        for i in range(self.scroll_area_vbox.count()):
            wg: ClassDataGroupBoxItem = self.scroll_area_vbox.itemAt(0).widget()
            self.delete_item(wg)

    def check_all(self):
        wgs = self.get_not_checked_wg()
        for wg in wgs:
            wg.set_checked()

    def uncheck_all(self):
        wgs = self.get_checked_wg()
        for wg in wgs:
            wg.set_uncheck()

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = ClassDataGroupBox()
    wg.show()
    sys.exit(app.exec_())