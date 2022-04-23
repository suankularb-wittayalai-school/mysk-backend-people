# local modules
from ..database import engine, teacher_table, people_table
from db.curd.people import get_person_contact, create_person

# internal modules
from mysk_utils.schema import Teacher, QueryTeacher, QueryPerson

# external modules
from sqlalchemy import select
from typing import List


def get_teacher_by_id(id: int) -> Teacher:
    """
    Get teacher by id
    """
    conn = engine.connect()
    query = conn.execute(
        select([teacher_table, people_table])
        .where(teacher_table.c.id == id)
        .join(people_table, teacher_table.c.person_id == people_table.c.id)
    ).fetchone()

    if query is None:
        return None
    # print(dict(query))
    teacher = Teacher(**dict(query), teacher_id=query["teacher_id"])
    teacher.contact = get_person_contact(query["person_id"])
    conn.close()
    return teacher


def get_teachers() -> List[Teacher]:
    """
    Get teachers
    """
    conn = engine.connect()
    query = conn.execute(
        select([teacher_table, people_table])
        .where(teacher_table.c.id == id)
        .join(people_table, teacher_table.c.person_id == people_table.c.id)
    ).fetchall()

    if query is None:
        return None
    # print(dict(query))
    teachers = [
        Teacher(**dict(query), teacher_id=query["teacher_id"]) for query in query
    ]
    conn.close()
    return teachers


def create_teacher(teacher: QueryTeacher) -> Teacher:
    """
    Create teacher
    """
    conn = engine.connect()

    person = QueryPerson(
        prefix_th=teacher.prefix_th.value,
        prefix_en=teacher.prefix_en.value,
        first_name_th=teacher.first_name_th,
        first_name_en=teacher.first_name_en,
        last_name_th=teacher.last_name_th,
        last_name_en=teacher.last_name_en,
        middle_name_th=teacher.middle_name_th,
        middle_name_en=teacher.middle_name_en,
        contact=teacher.contact,
        birthdate=teacher.birthdate,
        citizen_id=teacher.citizen_id,
    )

    person_id = create_person(person).id

    teacher_id = conn.execute(
        teacher_table.insert().values(
            person_id=person_id, teacher_id=teacher.teacher_id
        )
    ).inserted_primary_key[0]
    conn.close()
    return get_teacher_by_id(teacher_id)
