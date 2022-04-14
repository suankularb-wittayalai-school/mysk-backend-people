from sqlalchemy import select, insert, update, delete
from typing import List

from ..database import (
    engine,
    people_table,
    contact_table,
    contact_type_table,
    person_contact_table,
)
from mysk_utils.schema import Person, Contact


def get_person(person_id: int) -> Person:
    """
    Get a person from the database.
    """
    conn = engine.connect()
    result = conn.execute(
        people_table.select().where(people_table.c.id == person_id)
    ).fetchone()

    if result is None:
        return None

    person = Person(**dict(result))

    contacts = conn.execute(
        select([contact_table, person_contact_table, contact_type_table])
        .join(contact_table, person_contact_table.c.contact_id == contact_table.c.id)
        .join(contact_type_table, contact_type_table.c.id == contact_table.c.type)
        .where(person_contact_table.c.person_id == person_id)
        .order_by(contact_table.c.id)
    ).fetchall()

    formatted_contact = [
        Contact(
            **{
                "id": contact.id,
                "type": contact["name_1"],
                "value": contact.value,
                "name": contact.name,
            }
        )
        for contact in contacts
    ]

    person.contact = formatted_contact
    conn.close()
    return person


def get_all_people() -> List[Person]:
    """
    Get all people from the database.
    """
    conn = engine.connect()
    result = conn.execute(people_table.select()).fetchall()

    people = [Person(**dict(person)) for person in result]

    for person in people:
        contacts = conn.execute(
            select([contact_table, person_contact_table, contact_type_table])
            .join(
                contact_table, person_contact_table.c.contact_id == contact_table.c.id
            )
            .join(contact_type_table, contact_type_table.c.id == contact_table.c.type)
            .where(person_contact_table.c.person_id == person.id)
            .order_by(contact_table.c.id)
        ).fetchall()

        formatted_contact = [
            Contact(
                **{
                    "id": contact.id,
                    "type": contact["name_1"],
                    "value": contact.value,
                    "name": contact.name,
                }
            )
            for contact in contacts
        ]

        person.contact = formatted_contact

    conn.close()
    return people
