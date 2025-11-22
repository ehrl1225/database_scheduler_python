with selected(class_id, class_number, class_year, class_semester, class_week, class_period) as (
    select sel.class_id, sel.class_number, sel.class_year, sel.class_semester, sel.class_week, sel.class_period
    from (class_data natural join class_time) as sel
    where
        (sel.class_id = '')
        or (sel.class_id='')
        --...
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
    c.class_period

from (class_data natural join class_time natural join class_names) as c
where
    (c.class_week, c.class_period) not in
    (
        select s.class_week, s.class_period
        from selected as s
    )
    and
    (c.class_id, c.class_number, c.class_year, c.class_semester) not in
    (
        select s.class_id, s.class_number, s.class_year, s.class_semester
        from selected as s
    )
    and
    (
        c.class_year = ''
        and c.class_semester = ''
        and c.class_is_closed != false
        and
        (
            (class_type = '전선'
            and class_grade = ''
            and
            (
                class_department = ''
                and
                (
                    (
                        class_major = ''
                        and class_major is not null
                    )
                    or class_major is null
                )
            ))
            or
                class_grade between 1 and ''
        )
    )
;