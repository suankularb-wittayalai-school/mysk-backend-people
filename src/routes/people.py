from fastapi import APIRouter, Response

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson, Person
from typing import List

from sqlalchemy import insert, update, delete, select


from db.database import engine, people_table


router = APIRouter()


@router.get("/")
def getPeople(response: Response) -> List[Person]:
    """
    Get all people
    TODO: Check permissions fetching people
    """
    with engine.connect() as conn:
        result = conn.execute(select(people_table)).fetchall()
        response.headers["X-INTERNAL-CODE"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return result


@router.get("/{personId}")
def getPerson(personId: int, response: Response) -> Person:
    """
    Get a person
    TODO: Check permissions fetching person
    """
    with engine.connect() as conn:
        result = conn.execute(
            select(people_table).where(people_table.c.id == personId)
        ).fetchone()
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
            insert(people_table).values(
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
        return dict(result.lastrowid)


@router.put("/{personId}")
def updatePerson(personId: int, person: QueryPerson, response: Response) -> Person:
    """
    Update a person
    TODO: make all fields in QueryPerson optional
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
def deletePerson(personId: int):
    # TODO: delete person from database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}
