import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..dependencies.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_order():
    response = client.post(
        "/orders/",
        json={
            "customer_name": "John Doe",
            "description": "Test order",
            "status": "pending",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "pending"


def test_read_all_orders():
    client.post("/orders/", json={"customer_name": "Alice"})
    client.post("/orders/", json={"customer_name": "Bob"})
    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_one_order_not_found():
    response = client.get("/orders/9999")
    assert response.status_code == 404


def test_update_order():
    create_resp = client.post(
        "/orders/", json={"customer_name": "Dave", "description": "Old"}
    )
    order_id = create_resp.json()["id"]
    response = client.put(f"/orders/{order_id}", json={"description": "Updated"})
    assert response.status_code == 200
    assert response.json()["description"] == "Updated"


def test_delete_order():
    create_resp = client.post("/orders/", json={"customer_name": "Eve"})
    order_id = create_resp.json()["id"]
    assert client.delete(f"/orders/{order_id}").status_code == 204
    assert client.get(f"/orders/{order_id}").status_code == 404


def test_get_pending_orders():
    client.post("/orders/", json={"customer_name": "Frank", "status": "pending"})
    client.post("/orders/", json={"customer_name": "Grace", "status": "completed"})
    response = client.get("/orders/staff/pending")
    assert response.status_code == 200
    assert all(o["status"] == "pending" for o in response.json())


def test_update_order_status():
    create_resp = client.post(
        "/orders/", json={"customer_name": "Henry", "status": "pending"}
    )
    order_id = create_resp.json()["id"]
    response = client.patch(f"/orders/staff/{order_id}/status/in-progress")
    assert response.status_code == 200
    assert response.json()["status"] == "in-progress"


def test_cancel_pending_order():
    create_resp = client.post(
        "/orders/", json={"customer_name": "Leo", "status": "pending"}
    )
    order_id = create_resp.json()["id"]
    response = client.patch(f"/orders/customer/{order_id}/cancel")
    assert response.status_code == 200
    assert response.json()["message"] == "Order successfully cancelled."


def test_cancel_non_pending_order_fails():
    create_resp = client.post(
        "/orders/", json={"customer_name": "Mia", "status": "completed"}
    )
    order_id = create_resp.json()["id"]
    response = client.patch(f"/orders/customer/{order_id}/cancel")
    assert response.status_code == 400
