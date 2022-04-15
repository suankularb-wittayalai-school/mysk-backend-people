from fastapi import APIRouter, Response, HTTPException
from typing import List

from db.curd.student import create_student, get_student_by_id, get_students

from mysk_utils.schema import Student, QueryStudent
from mysk_utils.response import InternalCode


router = APIRouter()


@router.get("/", response_model=List[Student])
async def get_students_view(response: Response):
    """
    Get all students
    """
    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return get_students()


@router.get("/{student_id}", response_model=Student)
def get_student_view(student_id: int, response: Response):
    """
    Get student by id
    """
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )

    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return student


@router.post("/", response_model=Student)
def create_student_view(student: QueryStudent, response: Response):
    try:
        student = create_student(student)
        response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return student

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )
