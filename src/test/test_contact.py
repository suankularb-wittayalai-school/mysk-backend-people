from fastapi.testclient import TestClient

from app import app
from db.curd.contact import create_contact


from mysk_utils.response import InternalCode
from mysk_utils.schema import QueryContact

client = TestClient(app)


def test_create_contact():

    response = client.post(
        "/contacts/", json={"name": "test", "type": "Line", "value": "test"}
    )

    assert response.status_code == 201
    assert response.headers["X-Internal-Code"] == str(
        InternalCode.IC_OBJECT_CREATED.value
    )
    assert response.json() == {
        "id": "1",
        "name": "test",
        "type": "Line",
        "value": "test",
    }


def test_create_contact_with_invalid_type():
    response = client.post(
        "/contacts/", json={"name": "test", "type": "Invalid", "value": "test"}
    )
    assert response.status_code == 422


def test_get_contact():
    contact = QueryContact(name="test", type="Line", value="test")
    create_contact(contact)
    response = client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "test",
        "type": "Line",
        "value": "test",
    }


def test_get_contact_with_invalid_id():
    response = client.get("/contacts/99")
    assert response.status_code == 200
    assert response.json() == None


def test_update_contact():
    response = client.put(
        "/contacts/",
        json={"id": "1", "name": "test2", "type": "Line", "value": "test2"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "test2",
        "type": "Line",
        "value": "test2",
    }


def test_update_contact_with_invalid_id():
    response = client.put(
        "/contacts/",
        json={"id": "99", "name": "test2", "type": "Line", "value": "test2"},
    )
    assert response.status_code == 400
    assert response.json().get("detail") is not None


def test_delete_contact():
    deleting = client.get("/contacts/1")

    response = client.delete("/contacts/1")
    assert response.status_code == 200
    assert response.json() == deleting.json()

    response = client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json() == None


def test_delete_contact_with_invalid_id():
    response = client.delete("/contacts/99")
    assert response.status_code == 200
    assert response.json() == None
