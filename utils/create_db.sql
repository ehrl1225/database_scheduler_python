drop table class_time;
drop table attends;
drop table student;
drop table class_data;
drop table class_names;


create table student
(
    student_id  varchar(8) unique , -- 학번
    password    bytea, -- 비밀번호
    salt        bytea, -- salt 값
    admission_year  numeric(4,0), -- 입학년도
    rest_semester_count numeric(2), -- 휴학 학기 수
    college varchar(20), -- 대학
    department    varchar(10), -- 학부
    major varchar(10), -- 전공
    primary key (student_id)
);

create table class_names
(
    class_name_id integer generated always as identity primary key, -- 수업 이름 id
    class_name varchar(80) -- 수업 이름
);

create table class_data
(
    class_data_id integer generated always as identity primary key,
    class_id varchar(5), -- 수업 id
    class_number varchar(4), -- 수업 분반
    class_name_id integer, -- 수업 이름 id
    class_type  varchar(2), --
    class_point numeric(2,0), -- 수업 학점
    class_college   varchar(10), --
    class_department    varchar(10),
    class_major varchar(10),
    class_grade numeric(1,0),
    class_year  numeric(4,0),
    class_semester varchar(6)
        check (class_semester in ('spring', 'summer', 'fall', 'winter')),
    class_professor varchar(10),
    class_ge_area numeric(1,0),
    class_is_closed bool,
    foreign key (class_name_id) references class_names(class_name_id)
);

create table attends
(
    student_id  varchar(8),
    class_data_id   integer,

    foreign key (student_id) references student(student_id)
        on delete cascade,
    foreign key (class_data_id) references class_data(class_data_id)
);


create table class_time
(
    class_data_id   integer,
    class_building    varchar(10),
    class_room_number   varchar(8),
    class_week  varchar(1),
    class_period    numeric(2),
    foreign key (class_data_id) references class_data(class_data_id)
        on delete cascade
);
