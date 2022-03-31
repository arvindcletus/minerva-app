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
