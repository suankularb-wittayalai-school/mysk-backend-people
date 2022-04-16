from fastapi.testclient import TestClient

from app import app
from db.curd.people import create_person


from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryPerson, QueryContact

client = TestClient(app)


def test_get_person_by_id():

    # Create a person
    person = QueryPerson(
        prefix_en="Mr.",
        prefix_th="นาย",
        first_name_en="John",
        first_name_th="จอห์น",
        last_name_en="Doe",
        last_name_th="ดอนดา",
        birthdate="2000-01-01",
        citizen_id="1234567890123",
    )
    create_person(person)

    response = client.get("/people/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "middle_name_en": None,
        "middle_name_th": None,
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890123",
        "contact": [],
    }
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_get_person_by_id_not_found():

    response = client.get("/people/99")
    assert response.status_code == 400
    assert response.json() == {"detail": "Person with id 99 not found"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_create_person_without_contact():
    response = client.post(
        "/people/",
        json={
            "prefix_en": "Mr.",
            "prefix_th": "นาย",
            "first_name_en": "John",
            "first_name_th": "จอห์น",
            "last_name_en": "Doe",
            "last_name_th": "ดอนดา",
            "birthdate": "2000-01-01",
            "citizen_id": "1234567890124",
            "contact": [],
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "middle_name_en": None,
        "middle_name_th": None,
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890124",
        "contact": [],
    }
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_create_person_with_contact():
    response = client.post(
        "/people/",
        json={
            "prefix_en": "Mr.",
            "prefix_th": "นาย",
            "first_name_en": "John",
            "first_name_th": "จอห์น",
            "last_name_en": "Doe",
            "last_name_th": "ดอนดา",
            "birthdate": "2000-01-01",
            "citizen_id": "1234567890125",
            "contact": [
                {
                    "type": "Email",
                    "value": "john@example.com",
                    "name": "John Doe",
                }
            ],
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "middle_name_en": None,
        "middle_name_th": None,
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890125",
        "contact": [
            {
                "id": "3",
                "type": "Email",
                "value": "john@example.com",
                "name": "John Doe",
            }
        ],
    }
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_person_with_contact():
    response = client.put(
        "/people/",
        json={
            "id": 3,
            "prefix_en": "Mr.",
            "prefix_th": "นาย",
            "first_name_en": "John",
            "first_name_th": "จอห์น",
            "last_name_en": "Doe",
            "last_name_th": "ดอนดา",
            "birthdate": "2000-01-01",
            "citizen_id": "1234567890125",
            "contact": [
                {
                    "id": "3",
                    "type": "Email",
                    "value": "joe@example.com",
                    "name": "Joe Doe",
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "middle_name_en": None,
        "middle_name_th": None,
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890125",
        "contact": [
            {
                "id": "3",
                "type": "Email",
                "value": "joe@example.com",
                "name": "Joe Doe",
            }
        ],
    }
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_SUCCESS.value
    )


def test_update_person_with_invalid_id():
    response = client.put(
        "/people/",
        json={
            "id": 99,
            "prefix_en": "Mr.",
            "prefix_th": "นาย",
            "first_name_en": "John",
            "first_name_th": "จอห์น",
            "last_name_en": "Doe",
            "last_name_th": "ดอนดา",
            "birthdate": "2000-01-01",
            "citizen_id": "1234567890125",
            "contact": [
                {
                    "id": "3",
                    "type": "Email",
                    "value": "john",
                    "name": "John Doe",
                }
            ],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Person with id 99 not found"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_update_person_with_invalid_contact_id():
    response = client.put(
        "/people/",
        json={
            "id": 3,
            "prefix_en": "Mr.",
            "prefix_th": "นาย",
            "first_name_en": "John",
            "first_name_th": "จอห์น",
            "last_name_en": "Doe",
            "last_name_th": "ดอนดา",
            "birthdate": "2000-01-01",
            "citizen_id": "1234567890125",
            "contact": [
                {
                    "id": "99",
                    "type": "Email",
                    "value": "john",
                    "name": "John Doe",
                }
            ],
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "'NoneType' object is not subscriptable"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )


def test_delete_person_with_contact():
    response = client.delete(
        "/people/3",
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "prefix_en": "Mr.",
        "prefix_th": "นาย",
        "first_name_en": "John",
        "first_name_th": "จอห์น",
        "last_name_en": "Doe",
        "last_name_th": "ดอนดา",
        "middle_name_en": None,
        "middle_name_th": None,
        "birthdate": "2000-01-01",
        "citizen_id": "1234567890125",
        "contact": [
            {
                "id": "3",
                "type": "Email",
                "value": "joe@example.com",
                "name": "Joe Doe",
            }
        ],
    }

    response = client.get(
        "/people/3/",
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Person with id 3 not found"}
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_GENERIC_BAD_REQUEST.value
    )
