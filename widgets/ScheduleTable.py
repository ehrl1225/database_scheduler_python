from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QToolTip
from utils.DataManager import DataManager
from utils.ClassData import ClassData
from utils.ClassTime import ClassTime


class ScheduleTable(QTableWidget):

    def __init__(self):
        super().__init__()
        self.non_selected_color = QColor(255, 255, 255)
        self.selected_color = QColor(255, 215, 0)
        self.redundant_color = QColor(255, 0, 0)
        self.same_name_color = QColor(255, 127, 39)
        self.class_datas:list[ClassData] = []

        self.initUI()

    def initUI(self):
        self.setMinimumWidth(700)
        self.setMinimumHeight(370)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(DataManager.get_weeks())
        self.setRowCount(11)
        self.setVerticalHeaderLabels(DataManager.get_times())
        for i in range(11):
            for j in range(6):
                item = QTableWidgetItem()
                item.setBackground(self.non_selected_color)
                self.setItem(i, j, item)

    def set_class_datas(self, class_datas: list[ClassData]):
        same_names = DataManager.get_same_names(class_datas=class_datas)
        self.class_datas = []
        for class_data in class_datas:
            name = class_data.get_class_name()
            self.class_datas.append(class_data)
            if name in same_names:
                self.set_class_data(class_data, self.same_name_color)
            else:
                self.set_class_data(class_data, self.selected_color)

    def get_class_datas(self):
        return self.class_datas

    def set_class_data(self, class_data: ClassData, color):

        class_times = class_data.get_class_times()
        first_times = DataManager.separate_times(class_data)
        for class_time in class_times:
            if class_time in first_times:
                self.paint_class_time(class_time, color, class_data.class_name)
            else:
                self.paint_class_time(class_time, color)

    def paint_class_time(self, class_time: ClassTime, color: QColor, text=None):
        if class_time.get_week() is not None and class_time.get_period() is not None:
            col = DataManager.get_week_index(class_time.week)
            row = class_time.get_period() - 1
            item = self.item(row, col)
            current_color = item.background().color()
            if current_color == self.non_selected_color:
                item.setBackground(color)
            elif current_color == self.selected_color:
                item.setBackground(self.redundant_color)
            if text is not None:
                item.setText(text)

    def paint_row_col(self, row: int, col: int, color: QColor):
        item = self.item(row, col)
        item.setBackground(color)

    def set_non_selected_color(self, color: QColor):
        self.non_selected_color = color

    def set_selected_color(self, color: QColor):
        self.selected_color = color

    def set_redundant_color(self, color: QColor):
        self.redundant_color = color

    def clear(self):
        for col in range(6):
            for row in range(11):
                item = self.item(row, col)
                item.setBackground(self.non_selected_color)
                item.setText("")
