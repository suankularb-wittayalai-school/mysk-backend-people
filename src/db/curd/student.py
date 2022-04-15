from turtle import st
from typing import List
from ..database import engine, student_table, people_table, person_contact_table

from sqlalchemy import select

from db.curd.people import create_person, get_person_contact, update_person


from mysk_utils.schema import Student, QueryStudent, QueryPerson


def get_student_by_id(id: int) -> Student:
    """
    Get student by id
    """
    conn = engine.connect()
    query = conn.execute(
        select([student_table, people_table])
        .where(student_table.c.id == id)
        .join(people_table, student_table.c.person_id == people_table.c.id)
    ).fetchone()

    if query is None:
        return None
    # print(dict(query))
    student = Student(**dict(query), std_id=query["student_id"])
    student.contact = get_person_contact(query["person_id"])
    conn.close()
    return student


def get_students() -> List[Student]:
    """
    Get all students
    """
    conn = engine.connect()
    query = conn.execute(
        select([student_table, people_table])
        .where(student_table.c.person_id == people_table.c.id)
        .order_by(student_table.c.id)
        .join(people_table, student_table.c.person_id == people_table.c.id)
    ).fetchall()

    students = []
    for row in query:
        student = Student(**dict(row), std_id=row["student_id"])
        student.contact = get_person_contact(row["person_id"])
        students.append(student)

    conn.close()
    return students


def create_student(student: QueryStudent) -> Student:
    """
    Create student
    """
    conn = engine.connect()
    person = QueryPerson(
        prefix_th=student.prefix_th.value,
        prefix_en=student.prefix_en.value,
        first_name_th=student.first_name_th,
        first_name_en=student.first_name_en,
        last_name_th=student.last_name_th,
        last_name_en=student.last_name_en,
        middle_name_th=student.middle_name_th,
        middle_name_en=student.middle_name_en,
        contact=student.contact,
        birthdate=student.birthdate,
        citizen_id=student.citizen_id,
    )

    person_id = create_person(person)

    student_id = conn.execute(
        student_table.insert().values(person_id=person_id.id, student_id=student.std_id)
    ).inserted_primary_key[0]

    student = get_student_by_id(student_id)
    conn.close()
    return student


def update_student(student: Student) -> Student:
    """
    Update student
    """
    conn = engine.connect()
    person = conn.execute(
        select([people_table])
        .where(
            people_table.c.first_name_th == student.first_name_th
            and people_table.c.last_name_th == student.last_name_th
        )
        .limit(1)
    ).fetchone()

    if person is None:
        return None

    person_id = person["id"]
    person = QueryPerson(
        prefix_th=student.prefix_th.value,
        prefix_en=student.prefix_en.value,
        first_name_th=student.first_name_th,
        first_name_en=student.first_name_en,
        last_name_th=student.last_name_th,
        last_name_en=student.last_name_en,
        middle_name_th=student.middle_name_th,
        middle_name_en=student.middle_name_en,
        contact=student.contact,
        birthdate=student.birthdate,
        citizen_id=student.citizen_id,
    )

    person_id = update_person(person_id, person)

    conn.execute(
        student_table.update()
        .where(student_table.c.id == student.id)
        .values(person_id=person_id.id, student_id=student.std_id)
    )

    student = get_student_by_id(student.id)
    conn.close()
    return student
