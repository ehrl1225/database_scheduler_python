from typing import Self

class ClassTime:
    """
    각 교과목 마다 시간표를 담습니다.

    :var class_data: 교과목 번호
    :var week: 교과목 요일
    :var period: 교과목 교시
    :var building: 교과목 건물
    :var room_number: 교과목 방 번호
    """
    week: str
    period: int
    building: str
    room_number: str

    def __init__(self, class_data):
        self.class_data = class_data
        self.week = None
        self.period = None
        self.building = None
        self.room_number = None

    def set_week(self, week:str):
        self.week = week

    def set_period(self, period:int):
        if type(period) != int and period is not None:
            period = int(period)
        self.period = period

    def set_building(self, college):
        self.building = college

    def set_room_number(self, room_number):
        self.room_number = room_number

    def get_week(self, ):
        return self.week

    def get_period(self):
        return self.period

    def get_room_number(self):
        return self.room_number

    def get_building(self):
        return self.building

    def copy_self(self) -> Self:
        new_class_data = ClassTime(self.class_data)
        new_class_data.week = self.week
        new_class_data.period = self.period
        new_class_data.building = self.building
        new_class_data.room_number = self.room_number
        return new_class_data

    def get_week_period(self):
        return self.week, self.period

    def get_week_period_str(self):
        return f"{self.week}{self.period}"

    def __str__(self):
        return f"{self.week} {self.period} {self.building} {self.room_number}"

    def __repr__(self):
        return f"{self.week} {self.period} {self.building} {self.room_number}"

    def __hash__(self):
        return hash(self.class_data.get_full_class_id() + str(self))

    def set_class_data(self, class_data):
        self.class_data = class_data

    def get_class_id(self):
        return self.class_data.get_class_id()

    def get_class_number(self):
        return self.class_data.get_class_number()

    def get_class_year(self):
        return self.class_data.get_class_year()

    def get_class_semester(self):
        return self.class_data.get_class_semester()