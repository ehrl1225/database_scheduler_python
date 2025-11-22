import psycopg2
from psycopg2.extensions import cursor, connection
from utils.ClassData import ClassData
from utils.Student import Student


class PostSQLManager:
    """
    데이터베이스에 접속하고 \n
    SQL문을 실행합니다.
    """

    database: connection = None
    cursor: cursor = None
    host: str = None
    dbname: str = None
    user: str = None
    password: str = None
    port: int = None

    def __init__(self):
        pass

    @staticmethod
    def set():
        PostSQLManager.database = psycopg2.connect(
            host=PostSQLManager.host,
            dbname=PostSQLManager.dbname,
            user=PostSQLManager.user,
            password=PostSQLManager.password,
            port=PostSQLManager.port,
            sslmode='require'
        )
        PostSQLManager.cursor = PostSQLManager.database.cursor()

    @staticmethod
    def add_attends(
            student_id,
            class_data: ClassData
    ):
        PostSQLManager.cursor.execute(
            query="""
            insert into attends(
            student_id, 
            class_data_id
            )
            values (%s,%s);
            """,
            vars=(
                student_id,
                class_data.get_class_data_id()
            )

        )
        PostSQLManager.database.commit()

    @staticmethod
    def get_salt(student_id: str):
        PostSQLManager.cursor.execute(
            query="""
            select salt
            from student
            where student_id = %s;
            """,
            vars=(student_id,)
        )
        salt: tuple[str] = PostSQLManager.cursor.fetchone()
        return bytes(salt[0])

    @staticmethod
    def add_account(
            student_id: str,
            hashed_password: hex,
            salt: str,
            admission_year,
            rest_semester_count,
            college,
            department, major
    ):
        PostSQLManager.cursor.execute(
            """
            insert into student(
                student_id, 
                password, 
                salt, 
                admission_year, 
                rest_semester_count,
                 
                college, 
                department, 
                major
            )
            values (%s, %s, %s, %s, %s, 
                %s, %s, %s);
            """,
            (student_id,
             hashed_password,
             salt,
             admission_year,
             rest_semester_count,

             college,
             department,
             major)
        )
        PostSQLManager.database.commit()

    @staticmethod
    def get_student_account(student_id:str, hashed_password:hex):
        PostSQLManager.cursor.execute(
            """
            select 
                student_id, 
                admission_year, 
                rest_semester_count,
                college,
                department,
                major
            from student
            where student.password = %s and student.student_id = %s; 
            """,
            (hashed_password, student_id)
        )
        data = PostSQLManager.cursor.fetchone()
        if data is None:
            return None
        else:
            return data

    @staticmethod
    def check_student_id(student_id):
        PostSQLManager.cursor.execute(
            """
            select count(student_id)
            from student
            where student.student_id = %s;
            """,
            (student_id,)
        )
        id = PostSQLManager.cursor.fetchone()[0]
        if id > 0:
            return True
        else:
            return False

    @staticmethod
    def check_class_data(class_data: ClassData):
        PostSQLManager.cursor.execute(
            query="""
            select *
            from class_data
            where 
                class_data.class_data_id = %s
            ;
            """,
            vars=(
                class_data.class_data_id,
            )
        )
        data = PostSQLManager.cursor.fetchone()
        if data is not None:
            return True
        else:
            return False

    @staticmethod
    def add_class_data(class_data: ClassData):
        class_name_id:int = PostSQLManager.get_class_name_id(class_data.class_name)
        PostSQLManager.cursor.execute(
            """
            insert into class_data (
            class_id,
            class_number,
            class_name_id,
            class_type, 
            class_point,
            
            class_college,
            class_department, 
            class_major, 
            class_grade, 
            class_year,
             
            class_semester, 
            class_professor, 
            class_ge_area,
            class_is_closed)
            values (%s, %s,%s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s);
            """,
            (
                class_data.class_id,
                class_data.class_number,
                class_name_id,
                class_data.class_type,
                class_data.class_point,

                class_data.class_college,
                class_data.class_department,
                class_data.class_major,
                class_data.class_grade,
                class_data.class_year,

                class_data.class_semester,
                class_data.class_professor,
                class_data.class_ge_area,
                class_data.is_closed
            )
        )
        PostSQLManager.database.commit()

        class_data_id = PostSQLManager.get_class_data_id(class_data)

        for ct in class_data.class_times:
            PostSQLManager.cursor.execute(
                """
                insert into class_time (
                    class_data_id,
                    class_building,
                    class_room_number,
                    class_week,
                    class_period
                )
                values (%s,%s, %s, %s, %s);
                """,
                (
                    class_data_id,
                    ct.building,

                    ct.room_number,
                    ct.week,
                    ct.period
                )
            )
            PostSQLManager.database.commit()

    @staticmethod
    def get_attended_time(student_id) -> list[tuple]:
        PostSQLManager.cursor.execute(
            query="""
            select distinct class_year, class_semester
            from attends natural join class_data
            where attends.student_id = %s;
            """,
            vars=(student_id,)
        )
        times = PostSQLManager.cursor.fetchall()
        return times

    @staticmethod
    def get_attended_classes(student: Student, year, semester):
        PostSQLManager.cursor.execute(
            """
            select 
                class_id, 
                class_number, 
                class_name, 
                class_type, 
                class_point, 
                
                class_college, 
                class_department,
                class_major,
                class_grade,
                class_year,
                
                class_semester,
                class_professor,
                class_ge_area,
                class_is_closed,
                class_building,
                
                class_room_number,
                class_week,
                class_period,
                class_data_id
                
            from 
                (attends natural join class_data natural join class_time natural join class_names) as c 
            where 
                c.student_id = %s
                and c.class_year = %s
                and c.class_semester = %s
            ;
            """,
            (student.get_student_id(), year, semester)
        )
        data = PostSQLManager.cursor.fetchall()
        return data

    @staticmethod
    def get_selective_classes(class_type, class_ge_area, year, semester, grade, department=None, major=None):
        sql_without_where = """
        select
            class_id, 
            class_number, 
            class_name, 
            class_type, 
            class_point,
             
            class_college, 
            class_department,
            class_major,
            class_grade,
            class_year,
            
            class_semester,
            class_professor,
            class_ge_area,
            class_is_closed,
            class_building,
            
            class_room_number,
            class_week,
            class_period,
            class_data_id
        from 
            class_data natural join class_time natural join class_names
        """
        ge_area_where = """
        where
            class_type = %s
            and class_grade between 1 and %s
            and class_ge_area = %s
            and class_year = %s
            and class_semester = %s
            and class_is_closed = %s
            ;
        """
        no_ge_area_where = """
        where
            class_type = %s
            and class_grade between 1 and %s
            and class_year = %s
            and class_semester = %s
            and class_is_closed = %s
            ;
        """
        no_ge_area_major_where = """
        where
            class_type = %s
            and class_grade = %s
            and class_year = %s
            and class_semester = %s
            and (
                    class_department = %s 
                    and (
                        (class_major = %s 
                        and class_major is not null) 
                        or class_major is null 
                    )
                )
            and class_is_closed = %s
            ;
        """
        if class_ge_area is not None and class_type == "선교":
            PostSQLManager.cursor.execute(
                query=sql_without_where + ge_area_where,
                vars=(class_type, grade, class_ge_area, year, semester, False)
            )
        else:
            if class_type == "전선":
                PostSQLManager.cursor.execute(
                    query=sql_without_where + no_ge_area_major_where,
                    vars=(class_type, grade, year, semester, department, major, False)
                )
            else:
                PostSQLManager.cursor.execute(
                    query=sql_without_where + no_ge_area_where,
                    vars=(class_type, grade, year, semester, False)
                )
        datas = PostSQLManager.cursor.fetchall()
        return datas

    @staticmethod
    def get_necessary_classes(student: Student, grade, year, semester):
        PostSQLManager.cursor.execute(
            query="""
            select 
                class_id, 
                class_number, 
                class_name, 
                class_type, 
                class_point,
                 
                class_college, 
                class_department,
                class_major,
                class_grade,
                class_year,
                
                class_semester,
                class_professor,
                class_ge_area,
                class_is_closed,
                class_building,
                class_room_number,
                class_week,
                class_period,
                class_data_id
            from class_data natural join class_time natural join class_names
            where 
                class_college = %s 
                and class_grade = %s 
                and (
                    class_department = %s 
                    and (
                        (class_major = %s 
                        and class_major is not null) 
                        or class_major is null 
                    )
                ) 
                and class_year = %s
                and class_semester = %s
                and class_is_closed = false
                and class_type != %s
                ;
            """,
            vars=(
                student.college,
                grade,
                student.department,
                student.major,
                year,
                semester,
                "전선"
            )
        )
        datas = PostSQLManager.cursor.fetchall()
        return datas

    @staticmethod
    def get_class_name_id(class_name:str) -> int:
        query = """
        select class_name_id
        from class_names
        where class_names.class_name = %s
        ;
        """
        PostSQLManager.cursor.execute(
            query=query,
            vars=(
                class_name,
            )
        )
        data = PostSQLManager.cursor.fetchone()
        if data is None:
            insert_query = """
            insert into class_names(class_name)
            values (%s)
            ;
            """
            PostSQLManager.cursor.execute(
                query=insert_query,
                vars=(class_name,)
            )
            PostSQLManager.database.commit()
            PostSQLManager.cursor.execute(
                query=query,
                vars=(class_name,)
            )
            data = PostSQLManager.cursor.fetchone()

        return data


    @staticmethod
    def get_recommend(student, selected_class_data:list[ClassData], year, semester, grade):
        '''
            selected_class_data에 값이 하나라도 있어야함
        '''
        if len(selected_class_data)==0:
            return []
        embeded_query = ""
        for class_data in selected_class_data:
            text = f"sel.class_data_id = {class_data.get_class_data_id()} or "
            embeded_query += text
        embeded_query = embeded_query.strip(" or ")
        query = f"""
        with selected(class_data_id, class_week, class_period) as (
            select sel.class_data_id, sel.class_week, sel.class_period
            from (class_data natural join class_time) as sel
            where
                {embeded_query}
        )
        select
            c.class_id,
            c.class_number,
            c.class_name,
            c.class_type,
            c.class_point,
        
            c.class_college,
            c.class_department,
            c.class_major,
            c.class_grade,
            c.class_year,
        
            c.class_semester,
            c.class_professor,
            c.class_ge_area,
            c.class_is_closed,
            c.class_building,
        
            c.class_room_number,
            c.class_week,
            c.class_period,
            c.class_data_id
        
        from (class_data natural join class_time natural join class_names) as c
        where
            c.class_data_id not in
            (
                select s.class_data_id
                from selected as s
            )
            and
            (
                c.class_year = %s
                and c.class_semester = %s
                and c.class_is_closed = false
                and
                (
                    (class_type = '전선'
                    and class_grade between 1 and %s
                    and
                    (
                        class_department = %s
                        and
                        (
                            (
                                class_major = %s
                                and class_major is not null
                            )
                            or class_major is null
                        )
                    ))
                    or
                        class_type != '전선'
                )
            )
        ;
        """
        PostSQLManager.cursor.execute(query=query, vars=(
            year,
            semester,
            grade,
            student.get_department(),
            student.get_major()
        ))
        datas = PostSQLManager.cursor.fetchall()
        return datas

    @staticmethod
    def get_class_data_id(class_data:ClassData):
        query = """
        select class_data_id
        from class_data
        where class_id = %s
            and class_number = %s
            and class_year = %s
            and class_semester = %s
        ;
        """
        PostSQLManager.cursor.execute(query=query, vars=(class_data.class_id,class_data.class_number,class_data.class_year,class_data.class_semester))
        class_data_id = PostSQLManager.cursor.fetchone()
        if class_data_id is not None:
            return class_data_id[0]
        else:
            return None

    @staticmethod
    def del_attends(student_id, year, semester):
        query = """
        delete from attends
            using class_data
        where attends.class_data_id = class_data.class_data_id
            and attends.student_id = %s
            and class_data.class_year = %s
            and class_data.class_semester =%s
        ;
        """
        PostSQLManager.cursor.execute(query=query, vars=(student_id, year,semester))
        PostSQLManager.database.commit()


def test_set():
    PostSQLManager.dbname = 'database_db'
    PostSQLManager.host = 'localhost'
    PostSQLManager.user = 'database'
    PostSQLManager.password = '19017081'
    PostSQLManager.port = 5432
    PostSQLManager.set()


def laptop_set():
    PostSQLManager.dbname = 'database_db'
    PostSQLManager.host = '192.168.0.2'
    PostSQLManager.user = 'database'
    PostSQLManager.password = '19017081'
    PostSQLManager.port = 5432
    PostSQLManager.set()


def outside_set():
    PostSQLManager.dbname = 'database_db'
    PostSQLManager.host = 'desktop.ehrl1234.kro.kr'
    PostSQLManager.user = 'database'
    PostSQLManager.password = '19017081'
    PostSQLManager.port = 23543
    PostSQLManager.set()


def db_setting():
    with open("create_db.sql", "r") as f:
        data = f.read()
        PostSQLManager.cursor.execute(data)
        PostSQLManager.database.commit()


if __name__ == '__main__':
    pass
