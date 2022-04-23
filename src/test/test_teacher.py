# local modules
from app import app

# internal modules
from mysk_utils.response import InternalCode
from mysk_utils.schema import Teacher, Contact


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
        "citizen_id": "1234567890129",
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
            citizen_id="1234567890129",
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
        citizen_id="1234567890129",
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


def test_create_teacher_with_contact():
    """
    Test create teacher with contact
    """
    teacher_json = {
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890120",
        "teacher_id": "skt889",
        "contact": [
            {
                "type": "Email",
                "value": "john@example.com",
                "name": "John Doe",
            }
        ],
    }
    expected = Teacher(
        id=2,
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="John",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890120",
        teacher_id="skt889",
        contact=[
            Contact(id=5, type="Email", value="john@example.com", name="John Doe")
        ],
    )
    response = client.post("/teacher/", json=teacher_json)
    assert response.status_code == 200
    assert Teacher(**response.json()) == expected
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_teacher():
    """
    Test update teacher
    """
    teacher_json = {
        "id": 1,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "Joe",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890129",
        "teacher_id": "skt888",
    }

    response = client.put("/teacher/", json=teacher_json)
    assert response.status_code == 200
    assert Teacher(**response.json()) == Teacher(
        id=1,
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="Joe",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890129",
        teacher_id="skt888",
    )


def test_update_teacher_with_contact():
    """
    Test update teacher with contact
    """
    teacher_json = {
        "id": 2,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "Joe",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890120",
        "teacher_id": "skt889",
        "contact": [
            {
                "id": 5,
                "type": "Email",
                "value": "john@example.com",
                "name": "John",
            }
        ],
    }

    expected = Teacher(
        id=2,
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="Joe",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890120",
        teacher_id="skt889",
        contact=[Contact(id=5, type="Email", value="john@example.com", name="John")],
    )

    response = client.put("/teacher/", json=teacher_json)
    assert response.status_code == 200
    assert Teacher(**response.json()) == expected
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_teacher_not_found():
    """
    Test update teacher not found
    """
    teacher_json = {
        "id": 99,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "Joe",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890120",
        "teacher_id": "skt889",
    }

    response = client.put("/teacher/", json=teacher_json)
    assert response.status_code == 400
    assert response.json()["detail"] is not None
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )
