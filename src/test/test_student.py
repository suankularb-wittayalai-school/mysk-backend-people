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
