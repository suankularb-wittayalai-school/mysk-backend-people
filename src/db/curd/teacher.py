# local modules
from ..database import engine, teacher_table, people_table
from db.curd.people import get_person_contact

# internal modules
from mysk_utils.schema import Teacher

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
