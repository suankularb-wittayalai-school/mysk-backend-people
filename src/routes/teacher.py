# local module
from db.curd.teacher import (
    get_teacher_by_id,
    get_teachers,
    create_teacher,
    update_teacher,
)

# internal modules
from mysk_utils.schema import Teacher, QueryTeacher
from mysk_utils.response import InternalCode

# external modules
from fastapi import APIRouter, Response, HTTPException
from typing import List


router = APIRouter()


@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher_view(teacher_id: int, response: Response):
    """
    Get teacher by id
    """
    teacher = get_teacher_by_id(teacher_id)
    if teacher is None:
        raise HTTPException(
            status_code=400,
            detail=f"Teacher with id {teacher_id} not found",
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )

    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return teacher


@router.get("/", response_model=List[Teacher])
def get_teachers_view(response: Response):
    """
    Get teachers
    """
    teachers = get_teachers()
    if teachers is None:
        raise HTTPException(
            status_code=400,
            detail="Teachers not found",
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )

    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return teachers


@router.post("/", response_model=Teacher)
def create_teacher_view(teacher: QueryTeacher, response: Response):
    """
    Create teacher
    """
    teacher = create_teacher(teacher)
    if teacher is None:
        raise HTTPException(
            status_code=400,
            detail="Teacher not created",
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )

    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return teacher


@router.put("/", response_model=Teacher)
def update_teacher_view(teacher: Teacher, response: Response):
    """
    Update teacher
    """
    try:
        teacher = update_teacher(teacher)
        if teacher is None:
            raise HTTPException(
                status_code=400,
                detail="Teacher not updated",
                headers={
                    "X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)
                },
            )
        response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
        return teacher
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"X-Internal-Code": str(InternalCode.IC_GENERIC_BAD_REQUEST.value)},
        )
