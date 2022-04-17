from fastapi import APIRouter, Response, HTTPException
from typing import List

from db.curd.student import (
    create_student,
    get_student_by_id,
    get_students,
    update_student,
    delete_student,
)

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
            status_code=400,
            detail=f"Student with id {student_id} not found",
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


@router.put("/", response_model=Student)
def update_student_view(student: Student, response: Response):
    try:
        updated = update_student(student)

        if updated is None:
            # print("it dies")
            raise HTTPException(
                status_code=400,
                detail=f"Student with id {student.id} not found",
                headers={
                    "X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)
                },
            )

        response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )


@router.delete("/{student_id}", response_model=Student)
def delete_student_view(student_id: int, response: Response):
    try:
        deleted = delete_student(student_id)
        response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return deleted
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )
