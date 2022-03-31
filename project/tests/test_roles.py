# project/tests/test_roles.py


import json
import pytest

from faker import Faker


def test_create_role_unique(faker, test_app_with_db):
    role_name = faker.bothify(text="????-########")
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))

    assert response.status_code == 201
    assert response.json()["name"] == role_name


def test_create_role_duplicate(faker, test_app_with_db):
    role_name = faker.bothify(text="????-########")
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [],
                "msg": f'duplicate key value violates unique constraint "roles_name_key"\nDETAIL:  Key (name)=({role_name}) already exists.',
                "type": "IntegrityError",
            }
        ]
    }


def test_create_role_invalid_json(test_app):
    response = test_app.post("/roles/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_view_role(test_app_with_db):
    fake = Faker()
    role_name = fake.bothify(text="????-########")
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))
    role_id = response.json()["id"]

    response = test_app_with_db.get(f"/roles/{role_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == role_id
    assert response_dict["name"] == role_name
    assert response_dict["created_at"]


def test_view_role_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/roles/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"
