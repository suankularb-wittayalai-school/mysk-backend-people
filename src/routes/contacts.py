from fastapi import APIRouter, Response, HTTPException


from mysk_utils.response import InternalCode
from mysk_utils.schema import Contact, QueryContact

from db.curd.contact import create_contact, get_contact_by_id

router = APIRouter()


@router.get("/{contactId}", response_model=Contact)
async def get_contact(contactId: int, response: Response):
    """
    Get contact by id
    """
    try:
        contact = get_contact_by_id(contactId)
        response.headers["X-Internal-Code"] = InternalCode.IC_GENERIC_SUCCESS.value
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": InternalCode.IC_GENERIC_BAD_REQUEST.value},
        )


@router.post("/")
async def create_contact_view(query: QueryContact, response: Response) -> Contact:
    """
    Create a new contact
    """
    try:
        contact = create_contact(query)
        response.status_code = 201
        response.headers["X-Internal-Code"] = InternalCode.IC_OBJECT_CREATED.value
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": InternalCode.IC_GENERIC_BAD_REQUEST.value},
        )
