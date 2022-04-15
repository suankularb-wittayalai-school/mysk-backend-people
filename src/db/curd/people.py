from sqlalchemy import select
from typing import List

from ..database import (
    engine,
    people_table,
    person_contact_table,
)
from mysk_utils.schema import Person, Contact, QueryPerson
from .contact import get_contacts_by_id, create_contact


def get_person_contact(person_id: int) -> List[Contact]:
    """
    Get all contacts of a person from the database.
    """
    conn = engine.connect()
    result = conn.execute(
        select([person_contact_table]).where(
            person_contact_table.c.person_id == person_id
        )
    ).fetchall()

    contact_ids = [contact.contact_id for contact in result]
    conn.close()
    return get_contacts_by_id(contact_ids)


def get_person(person_id: int) -> Person:
    """
    Get a person from the database.
    """
    conn = engine.connect()
    result = conn.execute(
        people_table.select().where(people_table.c.id == person_id)
    ).fetchone()

    if result is None:
        raise Exception(f"Person with id {person_id} not found")

    person = Person(**dict(result))

    # contacts = conn.execute(
    #     select([contact_table, person_contact_table, contact_type_table])
    #     .join(contact_table, person_contact_table.c.contact_id == contact_table.c.id)
    #     .join(contact_type_table, contact_type_table.c.id == contact_table.c.type)
    #     .where(person_contact_table.c.person_id == person_id)
    #     .order_by(contact_table.c.id)
    # ).fetchall()

    # formatted_contact = [
    #     Contact(
    #         **{
    #             "id": contact.id,
    #             "type": contact["name_1"],
    #             "value": contact.value,
    #             "name": contact.name,
    #         }
    #     )
    #     for contact in contacts
    # ]

    # same as above
    person.contact = get_person_contact(person_id)

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
        # contacts = conn.execute(
        #     select([contact_table, person_contact_table, contact_type_table])
        #     .join(
        #         contact_table, person_contact_table.c.contact_id == contact_table.c.id
        #     )
        #     .join(contact_type_table, contact_type_table.c.id == contact_table.c.type)
        #     .where(person_contact_table.c.person_id == person.id)
        #     .order_by(contact_table.c.id)
        # ).fetchall()

        # formatted_contact = [
        #     Contact(
        #         **{
        #             "id": contact.id,
        #             "type": contact["name_1"],
        #             "value": contact.value,
        #             "name": contact.name,
        #         }
        #     )
        #     for contact in contacts
        # ]

        person.contact = get_person_contact(person.id)

    conn.close()
    return people


def create_person(person: QueryPerson) -> Person:
    """
    Create a person in the database.
    """
    # print("hi")
    conn = engine.connect()
    person_id = conn.execute(
        people_table.insert().values(
            prefix_th=person.prefix_th.value,
            first_name_th=person.first_name_th,
            middle_name_th=person.middle_name_th,
            last_name_th=person.last_name_th,
            prefix_en=person.prefix_en.value,
            first_name_en=person.first_name_en,
            middle_name_en=person.middle_name_en,
            last_name_en=person.last_name_en,
            birthdate=person.birthdate,
            citizen_id=person.citizen_id,
        )
    ).inserted_primary_key[0]

    if person.contact is not None and len(person.contact) > 0:
        for contact in person.contact:
            contacts = create_contact(contact)
            conn.execute(
                person_contact_table.insert().values(
                    person_id=person_id, contact_id=contacts.id
                )
            )
    conn.close()
    created_person = get_person(person_id)
    return created_person


def update_person(person_id: int, person: QueryPerson) -> Person:
    """
    Update a person in the database.
    """
    conn = engine.connect()

    updating = get_person(person_id)

    if updating is None:
        raise Exception(f"Person with id {person_id} not found")

    conn.execute(
        people_table.update()
        .where(people_table.c.id == person_id)
        .values(
            prefix_th=person.prefix_th.value,
            first_name_th=person.first_name_th,
            middle_name_th=person.middle_name_th,
            last_name_th=person.last_name_th,
            prefix_en=person.prefix_en.value,
            first_name_en=person.first_name_en,
            middle_name_en=person.middle_name_en,
            last_name_en=person.last_name_en,
            birthdate=person.birthdate,
            citizen_id=person.citizen_id,
        ),
    )

    conn.close()
    updated_person = get_person(person_id)
    return updated_person


def delete_person(person_id: int) -> Person:
    """
    Delete a person from the database.
    """
    conn = engine.connect()
    deleting = get_person(person_id)
    if deleting is None:
        raise Exception(f"Person with id {person_id} not found")
    conn.execute(people_table.delete().where(people_table.c.id == person_id))
    conn.close()
    return deleting
