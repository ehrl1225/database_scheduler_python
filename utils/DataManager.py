import time

import clipboard

from utils.ClassData import ClassData
from utils.ClassTime import ClassTime
from utils.GraduationCredit import GraduationCredit
from utils.Student import Student
import hashlib
import bcrypt
import keyboard
import datetime
import pickle
import os

GEClassAreas = [
    "언어와 소통(1영역)",
    "세계와 문명(2영역)",
    "역사와 사회(3영역)",
    "문화와 철학(4영역)",
    "기술과 정보(5영역)",
    "건강과 예술(6영역)",
    "자연과 과학(7영역)"
]

weeks = ["월", "화", "수", "목", "금", "토"]

times = ("9:30 ~ 10:20 : 10:30 ~ 11:20 : 11:30 ~ 12:20 : 12:30 ~ 1:20 : 1:30 ~ 2:20 : 2:30 ~ 3:20 : 3:30 ~ 4:20 : 4:30 "
         "~ 5:20 : 5:30 ~ 6:20 : 6:30 ~ 7:20 : 7:30 ~ 8:20").split(" : ")

semester_eng = ["spring", "summer", "fall", "winter"]
semester_kor = ["1학기", "여름학기", "2학기", "겨울학기"]

selective_type = [
    "전공",
    "전선",
    "선교",
    "중핵",
    "소교"
]
majors: dict[str, dict[str, list[str]]] = {
    "국제대학": {
        "자유전공학부": ["전체"]
    },
    "인문사회대학": {
        "인문학부": {},
        "외국어학부": {},
        "법학과": {},
        "행정학과": {},
        "언론정보학과": {},
        "행정학과(야)": {},
        "법·행정학부": {},
        "미디어커뮤니케이션학과": {},
        "소방행정학과": {}
    },
    "경상대학": {},
    "공과대학": {},
    "건강과과학대학": {},
    "미술대학": {},
    "ICT융합대학": {},
    "음악대학": {}
}
account_file_path = "cache.pkg"


class DataManager:
    """
    데이터를 관리합니다.
    """

    current_student: Student = Student()
    classes: list[ClassData] = list()
    graduationCredits: list[GraduationCredit] = list()
    maxGrade: int = 4
    logined: bool = False

    def __init__(self):
        pass

    @staticmethod
    def keyboard_copy_detect():
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
            return True
        else:
            return False

    @staticmethod
    def has_same_name(class_datas: list[ClassData]):
        name_set = set()
        for class_data in class_datas:
            name = class_data.get_class_name()
            if name in name_set:
                return True
            else:
                name_set.add(name)
        else:
            return False

    @staticmethod
    def get_same_names(class_datas: list[ClassData]) -> set[ClassData]:
        name_set = set()
        answer = set()
        for class_data in class_datas:
            name = class_data.get_class_name()
            if name in name_set:
                answer.add(name)
            else:
                name_set.add(name)
        return answer

    @staticmethod
    def has_account():
        return os.path.isfile(account_file_path)

    @staticmethod
    def save_account(id, pw):
        with open(account_file_path, "wb") as f:
            account_dict = dict()
            account_dict["id"] = id
            account_dict["pw"] = pw
            pickle.dump(account_dict, f)

    @staticmethod
    def load_account():
        with open(account_file_path, "rb") as f:
            account_dict = pickle.load(f)
            return account_dict

    @staticmethod
    def del_account():
        if os.path.isfile(account_file_path):
            os.remove(account_file_path)

    @staticmethod
    def get_selective_types() -> list[str]:
        return selective_type

    @staticmethod
    def get_weeks() -> list[str]:
        return weeks

    @staticmethod
    def get_times():
        return times

    @staticmethod
    def get_week_index(week):
        if week is not None:
            return weeks.index(week)

    @staticmethod
    def login(account):
        DataManager.logined = True
        DataManager.set_current_student(account)

    @staticmethod
    def set_current_student(account):
        DataManager.current_student = account

    @staticmethod
    def get_current_student():
        return DataManager.current_student

    @staticmethod
    def has_login():
        return DataManager.logined

    @staticmethod
    def logoff():
        DataManager.logined = False
        DataManager.current_student = Student()

    @staticmethod
    def get_ge_areas():
        return GEClassAreas

    @staticmethod
    def get_current_year():
        return datetime.datetime.today().year

    @staticmethod
    def check_year_str(year_str: str):
        if year_str.isdecimal() and len(year_str) == 4:
            return True
        else:
            return False

    @staticmethod
    def get_semester_eng():
        return semester_eng

    @staticmethod
    def get_semester_kor():
        return semester_kor

    @staticmethod
    def get_semester_kor2eng(kor_semester):
        index = semester_kor.index(kor_semester)
        return semester_eng[index]

    @staticmethod
    def get_semester_eng2kor(eng_semester):
        index = semester_eng.index(eng_semester)
        return semester_kor[index]

    @staticmethod
    def get_current_semester():
        today = datetime.datetime.today()
        month = today.month
        if month < 3:
            semester = "winter"
        elif month < 6:
            semester = "spring"
        elif month < 9:
            semester = "summer"
        elif month < 12:
            semester = "fall"
        elif month == 12:
            semester = "winter"
        else:
            return ""
        return semester

    @staticmethod
    def get_current_semester_index():
        eng_semester = DataManager.get_current_semester()
        return semester_eng.index(eng_semester)

    @staticmethod
    def get_eng_semester_index(eng_semester):
        return semester_eng.index(eng_semester)

    @staticmethod
    def addClass(class_data):
        DataManager.classes.append(class_data)

    @staticmethod
    def delClass(class_data):
        DataManager.classes.remove(class_data)

    @staticmethod
    def getClass(class_id, class_number):
        for c in DataManager.classes:
            if c.class_id == class_id and c.class_number == class_number:
                return c

    # 데이터 분별을 위해
    # 이후에 좀더 정확히 분별하게 만들 계획 있음
    @staticmethod
    def checkText(split_text: str) -> bool:
        if len(split_text) == 23:
            if not split_text[0].isdecimal():
                return False
            if not split_text[1] == "":
                return False
            if not split_text[2].isdecimal():
                return False
            if not split_text[3] != "":
                return False
            if not split_text[4].isdecimal():
                return False
            if not split_text[5] == "":
                return False
            if not split_text[6] != "":
                return False
            if not split_text[7].isdecimal():
                return False
            if not split_text[8].isdecimal():
                return False
            if not split_text[9].isdecimal():
                return False


        elif len(split_text) == 17:
            pass

    @staticmethod
    def check_splited_text(split_text:list[str]):
        if len(split_text)==23:
            if not split_text[0].isdecimal():
                return False
            if split_text[1] != "":
                return False
            if not split_text[2].isdecimal():
                return False
            if split_text[3].isdecimal():
                return False
            if not split_text[4].isdecimal():
                return False
            if split_text[6].isdecimal():
                return False
            if not split_text[7].isdecimal():
                return False
            if not split_text[8].isdecimal():
                return False
            if not split_text[9].isdecimal():
                return False
            if split_text[10].isdecimal():
                return False
            if not split_text[11].isdecimal():
                return False
            if split_text[13].isdecimal():
                return False
            if split_text[18].isdecimal():
                return False
            if split_text[19].isdecimal():
                return False
            return True

        else:
            return False

    @staticmethod
    def textToData(text) -> list[ClassData]:
        data = list()
        for t in text.split("\n"):
            split_text:list[str] = t.split("\t")
            len_blocks = len(split_text)
            if len_blocks == 23:
                if DataManager.check_splited_text(split_text):
                    data.append(DataManager.analyze_line(split_text))
            elif len_blocks == 21:
                # 나중에 이것 보다는 더 정확한 판별 시스템 추가할 것
                first:str = t[1]
                first.isdecimal()
                data2 = ["0", ""] + split_text
                if DataManager.check_splited_text(data2):
                    data.append(DataManager.analyze_line(data2))
        return data

    # 공과511(목7),종합409(월7 목6)
    # 종합210-2(화5,6)
    # 미술야외실기장(화6,7,8,9)
    # (금12,13,14 토15)
    # 1공학114(월2,3,4)
    # 미래B202(목6,7,8)
    # 휴.... 위 조건 다 만족시키면서 에러가 안나는 방식을 결국 해냄
    # 프로그램 언어에서 문법 검사기 방식으로 만들어냄
    @staticmethod
    def split_place_time(text, class_data: ClassData) -> list[ClassTime]:
        data = []
        buffer = ""
        class_time: ClassTime = ClassTime(class_data)
        index = 0
        t = ""

        def go_next() -> bool:
            nonlocal index, t

            index += 1
            if index >= len(text):
                return False
            else:
                t = text[index]
                return True

        def get_week_period() -> None:
            nonlocal buffer, index, class_time, t, data
            while True:
                go_next()
                if t in weeks:
                    class_time.set_week(t)
                elif t.isdecimal():
                    buffer += t
                elif t in [",", ")", " "]:
                    class_time.set_period(buffer)
                    data.append(class_time)
                    class_time = class_time.copy_self()
                    buffer = ""
                    if t == ")":
                        return

        def get_num() -> None:
            nonlocal buffer, index, class_time, t
            while True:
                if t == "(":
                    class_time.set_room_number(buffer)

                    buffer = ""
                    get_week_period()
                    return
                elif t.isdecimal() or t == "B" or t == "-":
                    buffer += t
                go_next()

        def get_data() -> None:
            nonlocal buffer, index, class_time, t
            t = text[index]
            while True:
                if buffer != "" and (t.isdecimal() or t == "B"):
                    class_time.set_building(buffer)
                    buffer = ""
                    get_num()
                elif t == "(":

                    class_time.set_building(buffer)
                    buffer = ""
                    get_week_period()
                elif t == ",":
                    pass
                else:
                    buffer += t
                status = go_next()
                if not status:
                    break

        if text == "":
            return [class_time]
        else:
            get_data()
            return data

    @staticmethod
    def analyze_line(split_text: list[str]) -> ClassData:
        class_data = ClassData()

        class_id = split_text[2]
        class_name = split_text[3]
        class_number = split_text[4]
        class_type = split_text[6]
        class_point = split_text[7]
        class_college_data = split_text[10].split(">>")
        class_college = class_college_data[0]
        if class_college_data[1][-1] == "부":
            class_department = class_college_data[1]
            if len(class_college_data) > 2:
                class_major = class_college_data[2]
            else:
                class_major = None
        else:
            class_department = None
            class_major = class_college_data[1]
        class_grade = split_text[11]

        place_and_time = split_text[13]
        class_times: list[ClassTime] = DataManager.split_place_time(place_and_time, class_data)
        class_professor = split_text[19]
        ge_class_area_text = split_text[20]
        if ge_class_area_text in GEClassAreas:
            ge_class_area = GEClassAreas.index(ge_class_area_text) + 1
        else:
            ge_class_area = 0
        is_closed_text = split_text[22]
        if len(is_closed_text) > 1:
            is_closed = True
        else:
            is_closed = False
        class_data.set_class_id(class_id)
        class_data.set_class_number(class_number)
        class_data.set_class_name(class_name)
        class_data.set_class_type(class_type)
        class_data.set_class_point(class_point)
        class_data.set_class_times(class_times)
        class_data.set_class_professor(class_professor)
        class_data.set_class_ge_area(ge_class_area)
        class_data.set_is_closed(is_closed)
        class_data.set_class_college(class_college)
        class_data.set_class_department(class_department)
        class_data.set_class_major(class_major)
        class_data.set_class_grade(class_grade)
        return class_data

    @staticmethod
    def filter_classes(filters):
        classes = []
        for c in DataManager.classes:
            for f in filters:
                pass
        return classes

    @staticmethod
    def get_intersections(class_datas: list[ClassData]) -> dict[tuple, set[ClassData]]:

        times: dict[tuple, set[ClassData]] = dict()

        for class_data in class_datas:
            for class_time_tuple in class_data.get_class_times_tuple():
                if class_time_tuple in times:
                    times[class_time_tuple].add(class_data)
                else:
                    times[class_time_tuple] = {class_data}
        keys = list(times.keys())
        for t in keys:
            if len(times[t]) == 1:
                del times[t]
        return times

    @staticmethod
    def get_not_intersections(class_data, intersections):
        temp = set()
        for i in intersections:
            for j in i:
                temp.add(j)
        class_data_set = set(class_data)
        return class_data_set - temp

    @staticmethod
    def get_salt():
        return bcrypt.gensalt()

    @staticmethod
    def hash_pw(user_pw: str, salt: bytes) -> hex:
        encoded_pw = user_pw.encode()
        pw = encoded_pw + salt
        hexDigest = hashlib.sha256(pw).hexdigest()
        return hexDigest

    @staticmethod
    def datas2student(data: list[tuple]):
        student = Student()

        student_id = data[0]
        admission_year = int(data[1])
        rest_semester_count = data[2]
        college = data[3]
        department = data[4]
        major = data[5]

        student.set_student_id(student_id)
        student.set_admission_year(admission_year)
        student.set_rest_semester_count(rest_semester_count)
        student.set_college(college)
        student.set_department(department)
        student.set_major(major)

        return student

    @staticmethod
    def datas2classDatas(data: list[tuple]):
        class_datas: dict[str, ClassData] = dict()
        for d in data:
            class_id = d[0]
            class_number = d[1]
            class_name = d[2]
            class_type = d[3]
            class_point = d[4]
            class_college = d[5]
            class_department = d[6]
            class_major = d[7]
            class_grade = d[8]
            class_year = d[9]
            class_semester = d[10]
            class_professor = d[11]
            class_ge_area = d[12]
            class_is_closed = d[13]
            class_building = d[14]
            class_room_number = d[15]
            class_week = d[16]
            class_period = d[17]
            class_data_id = d[18]

            class_data = ClassData()
            class_data.set_class_id(class_id)
            class_data.set_class_number(class_number)
            class_data.set_class_name(class_name)
            class_data.set_class_type(class_type)
            class_data.set_class_point(class_point)
            class_data.set_class_college(class_college)
            class_data.set_class_department(class_department)
            class_data.set_class_major(class_major)
            class_data.set_class_grade(class_grade)
            class_data.set_class_year(class_year)
            class_data.set_class_semester(class_semester)
            class_data.set_class_professor(class_professor)
            class_data.set_class_ge_area(class_ge_area)
            class_data.set_is_closed(class_is_closed)
            class_data.set_class_data_id(class_data_id)

            class_time = ClassTime(class_data)
            class_time.set_building(class_building)
            class_time.set_room_number(class_room_number)
            class_time.set_week(class_week)
            class_time.set_period(class_period)

            class_data.add_class_time(class_time)

            full_id = class_data.get_full_class_id()
            if full_id in class_datas:
                class_datas[full_id].add_class_time(class_time)
            else:
                class_datas[full_id] = class_data
        for class_data in class_datas:
            cd = class_datas[class_data]
            times:list[ClassTime] = cd.get_class_times()
            times.sort(key=lambda time: f"{weeks.index(time.get_week())}{time.get_period():02d}" if (time.get_week() is not None) and (time.get_period() is not None) else "000")
            cd.set_class_times(times)
        return list(class_datas.values())

    @staticmethod
    def set_times(class_data, year, semester):
        class_data.set_class_year(year)
        class_data.set_class_semester(semester)

    @staticmethod
    def separate_times(class_data:ClassData):
        class_times = class_data.get_class_times()
        first_times: set[ClassTime] = set()
        week_class_times: dict[str, list[ClassTime]] = {}
        for class_time in class_times:
            week = class_time.get_week()
            if week in week_class_times:
                pre_time = week_class_times[week][-1]
                if pre_time.get_period()+1 != class_time.get_period():
                    first_times.add(class_time)
                week_class_times[week].append(class_time)
            else:
                first_times.add(class_time)
                week_class_times[week] = [class_time]
        return first_times

    @staticmethod
    def subtract_time(selected_datas:list[ClassData], recommend_datas:list[ClassData]):
        answer:list[ClassData] = []
        class_times: set[str] = set()
        for selected_data in selected_datas:
            times = selected_data.get_class_times()
            for time in times:
                class_times.add(time.get_week_period_str())
        for recommend_data in recommend_datas:
            times = recommend_data.get_class_times()
            for time in times:
                if time.get_week_period_str() in class_times:
                    break
            else:
                answer.append(recommend_data)
        return answer

    @staticmethod
    def rowcol2class_data(row:int, col:int, class_datas:list[ClassData]):
        period = row+1
        week = weeks[col]
        week_period_tuple = (week, period)
        for class_data in class_datas:
            week_period_tuples = class_data.get_class_times_tuple()
            if week_period_tuple in week_period_tuples:
                index = week_period_tuples.index(week_period_tuple)
                return class_data, index
        else:
            return None, None

    @staticmethod
    def sum_points(class_datas:list[ClassData]):
        total = 0
        for class_data in class_datas:
            total += class_data.get_class_point()
        return total

data = """18		10853	도전과창조-기업가정신	018		중핵	2	2	0	교양대학>>교양	1		미래521(수1,2)					ABCDF	정형철		2023-08-30	수강인원 미달에 의한 폐강
19		10853	도전과창조-기업가정신	019		중핵	2	2	0	교양대학>>교양	1		미래521(수3,4)					ABCDF	정형철			
53		00506	결혼과가족	001		선교	3	3	0	교양대학>>교양	1		종합507(목5,6,7)					ABCDF	고선주	역사와 사회(3영역)		
"""
data2 = """1	교양	1학년	10864	094	CSL중국어2(재수강_92합반)		기교	고건혁	법정508(목7,8,9)	출력	입력	입력				
2	교양	1학년	10853	039	도전과창조-기업가정신		중핵	연경열	미래104(목5,6)	출력	입력	입력				
3	교양	1학년	10853	040	도전과창조-기업가정신		중핵	조희근	미래104(수5,6)	출력	입력	입력				
4	교양	1학년	10853	041	도전과창조-기업가정신		중핵	신동수	미래521(화5,6)	출력	입력	입력				
"""
# 테스트 용으로 사용할 것
if __name__ == '__main__':
    pass
