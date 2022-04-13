from fastapi import APIRouter, Response

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson, Person
from typing import List


from db.database import engine


router = APIRouter()


@router.get("/")
def getPeople(response: Response) -> List[Person]:
    """
    Get all people
    TODO: Check permissions fetching people
    """
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM people")
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return [dict(row) for row in result]


@router.get("/{personId}")
def getPerson(personId: int, response: Response) -> Person:
    """
    Get a person
    TODO: Check permissions fetching person
    """
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM people WHERE id = ?", personId).fetchone()
        if result is None:
            response.headers["X-INTERNAL-CODE"] = str(
                InternalCode.IC_GENERIC_BAD_REQUEST.value
            )
            return None
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return dict(result)


@router.post("/", status_code=201)
def createPerson(person: QueryPerson, response: Response) -> Person:
    """
    Create a person
    TODO: Check permissions fetching person
    """

    with engine.connect() as conn:
        result = conn.execute(
            """
            INSERT INTO people (prefix_th, first_name_th, middle_name_th, last_name_th, prefix_en, first_name_en, middle_name_en, last_name_en, birthdate, citizen_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            person.prefix_th.value,
            person.first_name_th,
            person.middle_name_th,
            person.last_name_th,
            person.prefix_en.value,
            person.first_name_en,
            person.middle_name_en,
            person.last_name_en,
            person.birthdate,
            person.citizen_id,
        )
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return result.lastrowid


@router.put("/{personId}")
def updatePerson(personId: int):
    # TODO: update person in database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.delete("/{personId}")
def deletePerson(personId: int):
    # TODO: delete person from database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}
