import datetime

from utils.ClassData import ClassData



class Student:
    """
    로그인한 계정의 필요한 데이터를 담습니다.(비밀번호 제외)\n

    """

    student_id: str
    admission_year: int
    rest_semester_count: int
    classes: dict[str, list[ClassData]]
    max_class_point: int
    college: str
    department: str
    major: str

    def __init__(self):
        self.student_id = None
        self.admission_year = None
        self.rest_semester_count = None
        self.classes = dict()
        self.college = None
        self.department = None
        self.major = None

    def get_student_id(self):
        return self.student_id

    def get_department(self):
        return self.department

    def get_college(self):
        return self.college

    def get_major(self):
        return self.major

    def get_current_grade(self):
        today = datetime.datetime.today()
        return int(today.year - self.admission_year - (self.rest_semester_count // 2)) + 1

    def set_classes(self, semester: str, classes):
        self.classes[semester] = classes

    def set_student_id(self, student_id):
        self.student_id = student_id

    def set_admission_year(self, admission_year):
        self.admission_year = admission_year

    def set_rest_semester_count(self, rest_semester_count):
        self.rest_semester_count = rest_semester_count

    def set_college(self, college):
        self.college = college

    def set_department(self, department):
        self.department = department

    def set_major(self, major):
        self.major = major


if __name__ == '__main__':
    pass
