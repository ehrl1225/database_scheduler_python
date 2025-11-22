from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QHBoxLayout

from utils.ClassData import ClassData


class ShowClassData(QGroupBox):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.class_name_lb = QLabel()
        self.class_number_lb = QLabel()
        self.class_point_lb = QLabel()
        self.class_room_lb = QLabel()
        self.class_professor_lb = QLabel()

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(self.class_name_lb)
        hbox.addWidget(self.class_number_lb)
        vbox.addLayout(hbox)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.class_point_lb)
        hbox2.addWidget(self.class_room_lb)
        vbox.addLayout(hbox2)

        vbox.addWidget(self.class_professor_lb)

        self.setLayout(vbox)

    def set_class_data(self, class_data:ClassData, index:int):
        class_times = class_data.get_class_times()

        name_str = f"강의명 : {class_data.get_class_name()}"
        number_str = f"{class_data.get_class_number()}분반"
        point_str = f"{class_data.get_class_point()}학점"
        room_str = f"{class_times[index].building}-{class_times[index].get_room_number()}"
        professor_str = f"{class_data.get_class_professor()} 교수님"
        self.class_name_lb.setText(name_str)
        self.class_number_lb.setText(number_str)
        self.class_point_lb.setText(point_str)
        self.class_room_lb.setText(room_str)
        self.class_professor_lb.setText(professor_str)