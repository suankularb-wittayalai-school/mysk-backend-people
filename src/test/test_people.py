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
