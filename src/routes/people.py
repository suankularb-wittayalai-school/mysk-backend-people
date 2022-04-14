from fastapi import APIRouter, Response, HTTPException

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
from db.curd.people import (
    get_person,
    get_all_people,
    create_person,
    update_person,
    delete_person,
)

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
    try:
        inserted_data = create_person(person)
        return inserted_data
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-INTERNAL-CODE": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )


@router.put("/{personId}")
def updatePerson(personId: int, person: QueryPerson, response: Response) -> Person:
    """
    Update a person
    TODO: check permissions before updating
    """
    try:
        updated_data = update_person(personId, person)
        return updated_data
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-INTERNAL-CODE": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )

    # return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.delete("/{personId}")
def deletePerson(personId: int, response: Response) -> Person:
    """
    Delete a person
    TODO: delete person from database
    """
    try:
        deleted_data = delete_person(personId)
        return deleted_data
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-INTERNAL-CODE": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )


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
