import json

import pytest

from app.db import issue_crud, product_crud

def test_post_creates_issue_successfully_with_valid_data(test_app, monkeypatch):
    test_product = {"title": "issue on something 1", "description": "something happened 1", "id": 1, "product_owner": "foo", "createdBy": "foo",  "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000+00:00"}
    test_data = {"title": "issue title 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}

    def mock_get_product(db_session, productId):
        return test_product

    monkeypatch.setattr(product_crud, "get", mock_get_product)
    
    def mock_post(db_session, payload):
        return test_data

    monkeypatch.setattr(issue_crud, "post", mock_post)

    response = test_app.post("/products/1/issues/", data=json.dumps(test_data))
    assert response.status_code == 201
    assert response.json() == test_data

def test_post_create_issue_fails_when_product_does_not_exist(test_app, monkeypatch):
    test_data = {"title": "issue title 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}
    def mock_get_product(db_session, productId):
        return None

    monkeypatch.setattr(product_crud, "get", mock_get_product)
    
    def mock_post(db_session, payload):
        return None

    monkeypatch.setattr(issue_crud, "post", mock_post)

    response = test_app.post("/products/1/issues/", data=json.dumps(test_data))
    assert response.status_code == 404
    assert response.json()["detail"] == "product not found! Must create product first"

@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{}, 422],
        [{"title": "", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "", "status":"on hold"}, 422],
        [{"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":""}, 422],
    ],
)
def test_post_create_issue_fails_with_invalid_data(test_app, monkeypatch, payload, status_code):
    response = test_app.post("/products/1/issues/", data=json.dumps(payload))
    assert response.status_code == 422

def test_get_reads_all_issues_for_given_productId_successfully(test_app, monkeypatch):
    test_data = [
        {"title": "issue title 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"},
        {"title": "issue title 2", "description": "something happened 2", "id": 2, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}
    ]

    def mock_get_all(db_session, productId):
        return test_data

    monkeypatch.setattr(issue_crud, "get_all_by_product", mock_get_all)
    response = test_app.get("/products/1/issues")
    assert response.status_code == 200
    assert response.json() == test_data

def test_get_reads_issue_successfully_with_id(test_app, monkeypatch):
    test_data = {"title": "issue title 1","description": "something happened 1","productId": 2,"updatedBy": "foo","updatedDate": "2020-08-23T23:28:56.782000","assignedTo": "bar","status": "on hold","createdBy": "foo","id": 2,"createdDate": "2020-08-24T15:18:01.455618"}

    def mock_get(db_session, productId, id):
        return test_data

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.get("/products/2/issues/2")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_read_issue_fails_with_not_found_when_product_does_not_exist(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.get("/products/1/issues/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "issue not found"

def test_get_read_issue_fails_with_invalid_response_when_incorrect_productId(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None
    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.get("/products/0/issues/2")
    assert response.status_code == 422

def test_get_read_issue_fails_with_invalid_response_when_incorrect_issue_id(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None
    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.get("/products/1/issues/0")
    assert response.status_code == 422

def test_put_updates_issue_successfully_with_valid_data(test_app, monkeypatch):
    test_data = {"title": "issue title 1","description": "something happened 1","productId": 1,"updatedBy": "foo","updatedDate": "2020-08-23T23:28:56.782000","assignedTo": "bar","status": "on hold","createdBy": "foo","id": 2,"createdDate": "2020-08-24T15:18:01.455618"}
    test_update_data = {"title": "updated issue title","description": "updated description","productId": 1,"updatedBy": "updated foo","updatedDate": "2020-08-23T23:28:56.782000","assignedTo": "updated bar","status": "on hold","createdBy": "updated foo","id": 2,"createdDate": "2020-08-24T15:18:01.455618"}

    def mock_get(db_session,productId, id):
        return test_data

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    def mock_put(db_session, issue, title, description, productId, createdBy, updatedBy, updatedDate, assignedTo, status):
        return test_update_data

    monkeypatch.setattr(issue_crud, "put", mock_put)

    response = test_app.put("/products/2/issues/12/", data=json.dumps(test_update_data),)
    assert response.status_code == 200
    assert response.json() == test_update_data

@pytest.mark.parametrize(
    "productId, id, payload, status_code",
    [
        [1, 1, {}, 422],
        [1, 1, {"title": "", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "", "status":"on hold"}, 422],
        [1, 1, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":""}, 422],
        [999, 999, {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}, 404],
    ],
)
def test_put_update_issue_fails_with_invalid_data(test_app, monkeypatch, productId, id, payload, status_code):
    def mock_get(db_session, productId, id):
        return None

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.put(f"/products/{productId}/issues/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code

def test_delete_removes_issue_successfully_when_issue_exists(test_app, monkeypatch):
    test_data = {"title": "something happened 1", "description": "something happened 1", "id": 1, "productId": 1,  "createdBy": "foo", "updatedBy": "foo", "updatedDate": "2020-08-23T23:28:56.782000", "createdDate": "2020-08-23T23:28:56.782000", "assignedTo": "bar", "status":"on hold"}

    def mock_get(db_session, productId, id):
        return test_data

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    def mock_delete(db_session, productId, id):
        return test_data

    monkeypatch.setattr(issue_crud, "delete", mock_delete)

    response = test_app.delete("/products/1/issues/1/")
    assert response.status_code == 200
    assert response.json() == test_data

def test_delete_remove_issue_fails_when_issue_does_not_exist(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.delete("/products/999/issues/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "issue not found"

def test_delete_remove_issue_fails_when_productId_is_invalid(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.delete("/products/0/issues/1/")
    assert response.status_code == 422

def test_delete_remove_issue_fails_when_issue_id_is_invalid(test_app, monkeypatch):
    def mock_get(db_session, productId, id):
        return None

    monkeypatch.setattr(issue_crud, "get_by_id", mock_get)

    response = test_app.delete("/products/1/issues/0/")
    assert response.status_code == 422