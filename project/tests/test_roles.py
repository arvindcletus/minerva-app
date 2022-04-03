# project/tests/test_roles.py


import json

from faker import Faker


def generate_same_role_name(faker):
    return faker.bothify(text="????-########")


def generate_new_role_name():
    fake = Faker()
    return fake.bothify(text="????-########")


def test_create_role_unique(faker, test_app_with_db):
    role_name = generate_same_role_name(faker)
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))

    assert response.status_code == 201
    assert response.json()["name"] == role_name


def test_create_role_duplicate(faker, test_app_with_db):
    role_name = generate_same_role_name(faker)
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))

    assert response.status_code == 422
    response_dict = response.json()["detail"][0]
    assert response_dict["loc"] == []
    assert response_dict["type"] == "IntegrityError"


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
    role_name = generate_new_role_name()
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


def test_view_all_roles(test_app_with_db):
    role_name = generate_new_role_name()
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))
    role_id = response.json()["id"]

    response = test_app_with_db.get("/roles/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == role_id, response_list))) == 1


def test_remove_role(test_app_with_db):
    role_name = generate_new_role_name()
    response = test_app_with_db.post("/roles/", data=json.dumps({"name": role_name}))
    role_id = response.json()["id"]

    response = test_app_with_db.delete(f"/roles/{role_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": role_id, "name": role_name}


def test_remove_role_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/roles/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"
