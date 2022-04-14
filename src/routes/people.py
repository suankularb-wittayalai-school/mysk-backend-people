from fastapi import APIRouter, Response, HTTPException

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson, Person, QueryContact
from typing import List


from db.database import (
    engine,
    person_contact_table,
)
from db.curd.people import (
    get_person,
    get_all_people,
    create_person,
    update_person,
    delete_person,
)

from db.curd.contact import (
    create_contact,
)


router = APIRouter()


@router.get("/")
def get_people_view(response: Response) -> List[Person]:
    """
    Get all people

    TODO: Check permissions fetching people
    """

    return get_all_people()


@router.get("/{personId}")
def get_person_view(personId: int, response: Response) -> Person:
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
def create_person_view(person: QueryPerson, response: Response) -> Person:
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
def update_person_view(
    personId: int, person: QueryPerson, response: Response
) -> Person:
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
def delete_person_view(personId: int, response: Response) -> Person:
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
def create_contact_view(
    personId: int, contact: QueryContact, response: Response
) -> Person:
    """
    Create a contact

    TODO: check permissions before creating
    """

    try:
        person = get_person(personId)
        inserted_data = create_contact(personId, contact)

        with engine.connect() as conn:
            conn.execute(
                person_contact_table.insert().values(
                    person_id=person.id, contact_id=inserted_data.id
                )
            )

        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return get_person(personId)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-INTERNAL-CODE": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )
