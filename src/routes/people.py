from fastapi import APIRouter

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson


router = APIRouter()


@router.get("/")
def getPeople():
    # TODO: get people from database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.get("/{personId}")
def getPerson(personId: int):
    # TODO: get person from database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.post("/", status_code=201)
def createPerson(person: QueryPerson):
    # TODO: create person in database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.put("/{personId}")
def updatePerson(personId: int):
    # TODO: update person in database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}


@router.delete("/{personId}")
def deletePerson(personId: int):
    # TODO: delete person from database
    return {"internalCode": InternalCode.IC_FOR_FUTURE_IMPLEMENTATION}
