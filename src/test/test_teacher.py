# local modules
from app import app
from db.curd.teacher import create_teacher

# internal modules
from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryTeacher, Teacher


# external modules
from fastapi.testclient import TestClient


client = TestClient(app)


def test_create_teacher():
    """
    Test create teacher
    """
    teacher_json = {
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890126",
        "teacher_id": "skt888",
    }
    response = client.post("/teacher/", json=teacher_json)
    assert response.status_code == 200
    assert Teacher(**response.json()) == Teacher(**teacher_json, id=1)
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_get_teachers():
    """
    Test get all teacher
    """
    response = client.get("/teacher/")
    assert response.status_code == 200
    assert [Teacher(**teacher) for teacher in response.json()] == [
        Teacher(
            id=1,
            prefix_en="Mr.",
            prefix_th="นาย",
            first_name_en="John",
            first_name_th="จอห์น",
            last_name_en="Doe",
            last_name_th="ดอนดา",
            birthdate="2000-01-01",
            citizen_id="1234567890126",
            teacher_id="skt888",
        )
    ]
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_get_teacher_by_id():
    """
    Test get teacher by id
    """
    response = client.get("/teacher/1")
    assert response.status_code == 200
    assert Teacher(**response.json()) == Teacher(
        id=1,
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="John",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890126",
        teacher_id="skt888",
    )
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_get_teacher_by_id_not_found():
    """
    Test get teacher by id not found
    """
    response = client.get("/teacher/2")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Teacher with id 2 not found",
    }
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )
