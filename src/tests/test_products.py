import json

import pytest

from app.db import product_crud


def test_post_creates_product_successfully_with_valid_data(test_app, monkeypatch):
    test_data = {"title": "issue on something 1", "description": "something happened 1", "id": 1, "productOwner": "foo", "createdBy": "foo",  "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000+00:00"}

    def mock_post(db_session, payload):
        return test_data

    monkeypatch.setattr(product_crud, "post", mock_post)

    response = test_app.post("/products/", data=json.dumps(test_data))
    assert response.status_code == 201
    assert response.json() == test_data

@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{}, 422],
        [{"title": "1", "description": "bar", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [{"title": "foo", "description": "1", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [{"title": "foo", "description": "bar", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [{"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [{"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "foo", "updatedBy": "", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [{"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": ""}, 422],
    ],
)
def test_post_create_product_fails_with_invalid_data(test_app, monkeypatch, payload, status_code):
    response = test_app.post("/products/", data=json.dumps(payload))
    assert response.status_code == 422


def test_get_reads_product_successfully_with_id(test_app, monkeypatch):
    test_data = {"title": "issue on something 1", "description": "something happened 1", "id": 1, "productOwner": "foo", "createdBy": "foo",  "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000+00:00"}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.get("/products/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_read_product_fails_with_not_found_when_product_does_not_exist(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.get("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "product not found"

def test_get_read_product_fails_with_invalid_response_when_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.get("/products/0")
    assert response.status_code == 422

def test_get_reads_all_products_successfully(test_app, monkeypatch):
    test_data = [
        {"title": "issue on something 1", "description": "something happened 1", "id": 1, "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00", "createdDate": "2020-08-23T23:28:56.782000+00:00"},
        {"title": "issue on something 2", "description": "something happened 2", "id": 2, "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00", "createdDate": "2020-08-23T23:28:56.782000+00:00"},
    ]

    def mock_get_all(db_session):
        return test_data

    monkeypatch.setattr(product_crud, "get_all", mock_get_all)

    response = test_app.get("/products/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_put_updates_product_successfully_with_valid_data(test_app, monkeypatch):
    test_data = {"title": "issue on something 1", "description": "something happened 1", "id": 1, "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00", "createdDate": "2020-08-23T23:28:56.782000+00:00"}
    test_update_data = {"title": "issue updated", "description": "updated", "id": 1, "productOwner": "foo", "createdBy": "foo", "updatedBy": "bar", "updatedDate": "2020-08-24T11:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000+00:00"}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(product_crud, "get", mock_get)

    def mock_put(db_session, product, title, description, productOwner, createdBy, updatedBy, updatedDate):
        return test_update_data

    monkeypatch.setattr(product_crud, "put", mock_put)

    response = test_app.put("/products/1/", data=json.dumps(test_update_data),)
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
        [1, {"title": "1", "description": "bar", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [1, {"title": "foo", "description": "1", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [1, {"title": "foo", "description": "bar", "productOwner": "", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [1, {"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [1, {"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "foo", "updatedBy": "", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 422],
        [1, {"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": ""}, 422],
        [999, {"title": "foo", "description": "bar", "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00"}, 404],
    ],
)
def test_put_update_product_fails_with_invalid_data(test_app, monkeypatch, id, payload, status_code):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.put(f"/products/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_delete_removes_product_successfully_when_product_exists(test_app, monkeypatch):
    test_data = {"title": "issue on something 1", "description": "something happened 1", "id": 1, "productOwner": "foo", "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000+00:00", "createdDate": "2020-08-23T23:28:56.782000+00:00"}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(product_crud, "get", mock_get)

    def mock_delete(db_session, id):
        return test_data

    monkeypatch.setattr(product_crud, "delete", mock_delete)

    response = test_app.delete("/products/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_delete_remove_product_fails_when_product_does_not_exist(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.delete("/products/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "product not found"

def test_delete_remove_product_fails_with_invalid_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get)

    response = test_app.delete("/products/0/")
    assert response.status_code == 422
