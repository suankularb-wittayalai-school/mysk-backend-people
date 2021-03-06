from fastapi.testclient import TestClient

from app import app
from db.curd.student import create_student

from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryStudent, Student

client = TestClient(app)


def test_get_student_by_id():
    student = QueryStudent(
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="John",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890126",
        std_id="88888",
    )
    created = create_student(student)
    response = client.get("/student/1")
    assert response.status_code == 200
    assert Student(**response.json()) == created
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_get_student_by_id_not_found():
    response = client.get("/student/99")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student with id 99 not found"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_create_student_without_contact():
    studentjson = {
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890127",
        "std_id": "88889",
    }
    response = client.post("/student/", json=studentjson)
    assert response.status_code == 200
    assert Student(**response.json()) == Student(**studentjson, id=2)
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_create_student_with_contact():
    studentjson = {
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890128",
        "std_id": "88880",
        "contact": [
            {
                "type": "Email",
                "value": "john@example.com",
                "name": "John Doe",
            }
        ],
    }
    response = client.post("/student/", json=studentjson)

    studentjson["contact"][0]["id"] = 4

    expected = Student(**studentjson, id=3)

    assert response.status_code == 200
    assert Student(**response.json()) == expected
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_student_with_contact():
    studentjson = {
        "id": 3,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890128",
        "std_id": "88880",
        "contact": [
            {
                "id": "4",
                "type": "Email",
                "value": "john@example.com",
                "name": "John Doe",
            }
        ],
    }

    studentjson["contact"][0]["value"] = "john"
    studentjson["last_name_th"] = "ดอนดากุน"
    after = Student(**studentjson)

    response = client.put("/student/", json=studentjson)
    assert response.status_code == 200
    assert Student(**response.json()) == after
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_student_with_invalid_id():
    studentjson = {
        "id": 99,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890128",
        "std_id": "88880",
    }

    response = client.put("/student/", json=studentjson)
    assert response.status_code == 400
    assert response.json()["detail"] is not None
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_update_student_with_invalid_contact_id():
    studentjson = {
        "id": 3,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890128",
        "std_id": "88880",
        "contact": [
            {
                "id": "99",
                "type": "Email",
                "value": "john@example.com",
                "name": "John Doe",
            }
        ],
    }

    response = client.put("/student/", json=studentjson)
    assert response.status_code == 400
    assert response.json()["detail"] is not None
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_delete_student_with_invalid_id():
    response = client.delete("/student/99")
    assert response.status_code == 400
    assert response.json()["detail"] is not None
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_delete_student_with_valid_id():

    response = client.delete("/student/3")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )

    response = client.get(
        "/student/3/",
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Student with id 3 not found"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )
