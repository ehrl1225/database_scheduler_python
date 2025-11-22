from utils.ClassTime import ClassTime
from typing import Self

class ClassData:
    '''
    교과목 정보를 담습니다.

    \b
    :var class_id: 교과목 번호
    :var class_number: 분반
    :var class_name: 교과목 명
    :var class_type: 이수구분
    :var class_point: 학점
    :var class_ge_area: 교양영역
    :var class_grade: 대상 학년
    :var class_room: 강의실
    :var class_time: 시간
    :var class_professor: 대표교수
    :var is_closed: 폐강 여부
    :var class_college: 대학
    :var class_department: 학부
    :var class_major: 학과
    '''
    class_data_id: int
    class_id: str
    class_number: str
    class_name: str
    class_type: str
    class_point: int
    class_ge_area: int
    class_grade: int
    class_year: int
    class_semester:int
    class_times: list[ClassTime]
    class_professor: str
    is_closed: bool
    class_college: str
    class_department: str
    class_major: str

    def __init__(self) -> None:
        self.class_data_id = None
        self.class_id = None
        self.class_number = None
        self.class_type = None
        self.class_point = None
        self.class_ge_area = None
        self.class_grade = None
        self.class_year = None
        self.class_semester = None
        self.class_times = []
        self.class_professor = None


    def equals(self, other:Self) -> bool:
        if self.class_id != other.get_class_id():
            return False
        if self.class_number != other.get_class_number():
            return False
        if self.class_year != other.get_class_year():
            return False
        if self.class_semester != other.get_class_semester():
            return False
        return True

    def get_class_name(self):
        return self.class_name

    def get_class_id(self):
        return self.class_id

    def get_class_number(self):
        return self.class_number

    def get_class_type(self):
        return self.class_type

    def get_class_point(self):
        return self.class_point

    def get_class_ge_area(self):
        return self.class_ge_area

    def get_class_grade(self):
        return self.class_grade

    def get_class_year(self):
        return self.class_year

    def get_class_semester(self):
        return self.class_semester

    def get_class_room(self):
        return self.class_room

    def get_class_times(self):
        return self.class_times

    def get_class_professor(self):
        return self.class_professor

    def add_class_time(self, class_time:ClassTime):
        class_time.set_class_data(self)
        self.class_times.append(class_time)

    def set_class_id(self, class_id):
        self.class_id = class_id

    def set_class_number(self, class_number):
        self.class_number = class_number

    def set_class_name(self, class_name) -> None:
        self.class_name = class_name

    def set_class_type(self, class_type) -> None:
        self.class_type = class_type

    def set_class_point(self, class_point) -> None:
        self.class_point = class_point

    def set_class_ge_area(self, class_ge_area) -> None:
        self.class_ge_area = class_ge_area

    def set_class_times(self, class_times) -> None:
        self.class_times = class_times

    def set_class_professor(self, class_professor) -> None:
        self.class_professor = class_professor

    def set_is_closed(self, is_closed) -> None:
        self.is_closed = is_closed

    def set_class_college(self, class_college) -> None:
        self.class_college = class_college

    def set_class_department(self, class_department) -> None:
        self.class_department = class_department

    def set_class_major(self, class_major) -> None:
        self.class_major = class_major

    def set_class_grade(self, class_grade) -> None:
        self.class_grade=class_grade

    def set_class_year(self, class_year):
        self.class_year = class_year

    def set_class_semester(self, class_semester):
        self.class_semester = class_semester

    def get_full_class_id(self):
        return f"{self.class_id}{self.class_number}{self.class_year}{self.class_semester}"

    def get_full_name(self) -> str:
        return f"{self.class_name} {self.class_number}분반"

    def get_class_times_tuple(self):
        data = []
        for class_time in self.class_times:
            data.append(class_time.get_week_period())
        return data

    def has_class_time(self):
        for class_time in self.class_times:
            if class_time.get_week() is None and class_time.get_period() is None:
                return False
        else:
            return True

    def get_class_times_str(self):
        location:dict[str, dict[str,list[int]]] = {}
        if self.has_class_time():
            for class_time in self.class_times:
                building = class_time.get_building()
                week = class_time.get_week()
                period = class_time.get_period()
                if building in location:
                    if week in location[building]:
                        location[building][week].append(period)
                    else:
                        location[building][week] = [period]
                else:
                    location[building] = {week:[period]}
            text = ""
            for building in location:
                text += f"{building} ("
                for week in location[building]:
                    text += f"{week} "
                    for period in location[building][week]:
                        text+=f"{period},"
                    text = text.strip(",") + " "
                text += ")"
            return text
        else:
            return ""

    def __str__(self) -> str:
        return f"{self.class_name} {self.class_number}분반"

    def __repr__(self) -> str:
        return f"{self.class_name} {self.class_number}분반"

    def __eq__(self, other):
        if isinstance(other, ClassData):
            if self.class_id != other.class_id:
                return False
            if self.class_number != other.class_number:
                return False
            if self.class_year != other.class_year:
                return False
            if self.class_semester != other.class_semester:
                return False
            return True

    def __hash__(self):
        return hash(self.get_full_class_id())

    def set_class_data_id(self, class_data_id):
        self.class_data_id = class_data_id

    def get_class_data_id(self):
        return self.class_data_id

