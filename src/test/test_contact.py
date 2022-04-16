from fastapi.testclient import TestClient
import os

from app import app
from db.curd.contact import create_contact


from mysk_utils.response import InternalCode
from mysk_utils.schema import Contact, QueryContact

client = TestClient(app)
os.environ["PYTEST_RUNNING"] = "true"


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
