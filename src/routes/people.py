from fastapi import APIRouter, Response

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson, Person, QueryContact, Contact
from typing import List

from sqlalchemy import insert, update, delete, select


from db.database import (
    engine,
    people_table,
    contact_table,
    contact_type_table,
    person_contact_table,
)
from db.curd.people import get_person, get_all_people, create_person

router = APIRouter()


@router.get("/")
def getPeople(response: Response) -> List[Person]:
    """
    Get all people
    TODO: Check permissions fetching people
    """

    return get_all_people()


@router.get("/{personId}")
def getPerson(personId: int, response: Response) -> Person:
    """
    Get a person
    TODO: Check permissions fetching person
    """
    person = get_person(personId)

    if person is None:
        response.headers["X-INTERNAL-CODE"] = str(
            InternalCode.IC_GENERIC_BAD_REQUEST.value
        )
        return None

    response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return person


@router.post("/", status_code=201)
def createPerson(person: QueryPerson, response: Response) -> Person:
    """
    Create a person
    TODO: Check permissions fetching person
    """

    inserted_data = create_person(person)
    return inserted_data


@router.put("/{personId}")
def updatePerson(personId: int, person: QueryPerson, response: Response) -> Person:
    """
    Update a person
    TODO: check permissions before updating
    """

    with engine.connect() as conn:
        result = conn.execute(
            update(people_table)
            .where(people_table.c.id == personId)
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
            )
        )
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        # print(result.lastrowid)
        return result.lastrowid

    # return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.delete("/{personId}")
def deletePerson(personId: int, response: Response) -> Person:
    """
    Delete a person
    TODO: delete person from database
    """

    with engine.connect() as conn:
        deleting = conn.execute(
            select(people_table).where(people_table.c.id == personId)
        ).fetchone()

        if deleting is None:
            response.headers["X-INTERNAL-CODE"] = str(
                InternalCode.IC_GENERIC_BAD_REQUEST.value
            )
            return None

        result = conn.execute(delete(people_table).where(people_table.c.id == personId))
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return deleting


@router.post("/{personId}/contact")
def createContact(personId: int, contact: QueryContact, response: Response) -> Person:
    """
    Create a contact
    TODO: create a entry in contact table and forign key in people table
    """

    with engine.connect() as conn:
        person: Person = conn.execute(
            select(people_table).where(people_table.c.id == personId)
        ).fetchone()

        if person is None:
            response.headers["X-INTERNAL-CODE"] = str(
                InternalCode.IC_GENERIC_BAD_REQUEST.value
            )
            return None

        contact_type = conn.execute(
            select(contact_type_table).where(
                contact_type_table.c.name == contact.type.value
            )
        ).fetchone()
        if contact_type is None:
            response.headers["X-INTERNAL-CODE"] = str(
                InternalCode.IC_GENERIC_BAD_REQUEST.value
            )
            return None
        contact = conn.execute(
            insert(contact_table).values(
                type=contact_type.id,
                value=contact.value,
                name=contact.name,
            )
        )

        person_contact_type = conn.execute(
            insert(person_contact_table).values(
                person_id=personId,
                contact_id=contact.inserted_primary_key[0],
            )
        )

        contacts = conn.execute(
            select(person_contact_table).where(
                person_contact_table.c.person_id == personId
            )
        ).fetchall()

        contact_id = [contact.contact_id for contact in contacts]

        contact_data = conn.execute(
            select(
                contact_table.c.id,
                contact_type_table.c.name,
                contact_table.c.value,
                contact_table.c.name,
            )
            .join(contact_type_table, contact_type_table.c.id == contact_table.c.type)
            .where(contact_table.c.id.in_(contact_id))
            .order_by(contact_table.c.id)
        ).fetchall()

        # print contact type
        contact_data = [
            Contact(
                id=contact["id"],
                name=contact["name_1"],
                type=contact["name"],
                value=contact["value"],
            )
            for contact in [dict(contact) for contact in contact_data]
        ]
        person = Person(**dict(person))
        person.contact = contact_data

        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return person
