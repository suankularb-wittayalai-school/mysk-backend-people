# local modules
from ..database import engine, teacher_table, people_table
from db.curd.people import get_person_contact, create_person, update_person

# internal modules
from mysk_utils.schema import Teacher, QueryTeacher, QueryPerson, Person

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
    print(dict(query))
    teacher = Teacher(**dict(query))
    teacher.contact = get_person_contact(query["person_id"])
    conn.close()
    return teacher


def get_teachers() -> List[Teacher]:
    """
    Get teachers
    """
    conn = engine.connect()
    queries = conn.execute(
        select([teacher_table, people_table])
        .where(teacher_table.c.id == people_table.c.id)
        .join(people_table, teacher_table.c.person_id == people_table.c.id)
    ).fetchall()

    if queries is None:
        return None
    # print(dict(query))
    teachers = []
    for query in queries:
        teacher = Teacher(**dict(query))
        teacher.contact = get_person_contact(query["person_id"])
        teachers.append(teacher)
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


def update_teacher(teacher: Teacher) -> Teacher:
    """
    Update teacher
    """
    conn = engine.connect()

    try:
        person_id = conn.execute(
            select([teacher_table.c.person_id]).where(teacher_table.c.id == teacher.id)
        ).fetchone()[0]
    except IndexError:
        return None

    person = Person(
        id=person_id,
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

    update_person(person)

    conn.execute(
        teacher_table.update()
        .where(teacher_table.c.id == teacher.id)
        .values(person_id=person_id, teacher_id=teacher.teacher_id)
    )
    conn.close()
    return get_teacher_by_id(teacher.id)
