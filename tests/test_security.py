import uuid
from app.models.user import User
from app.core.security import hash_password


def test_admin_can_access_product_endpoint(client, db):
    # 1. Create an admin user directly in the test database
    admin_email = "admin_security@test.com"
    admin_password = "Admin@12345"

    admin = User(
        name="Test Admin",
        email=admin_email,
        password_hash=hash_password(admin_password),
        role="ADMIN",
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    # 2. Login as admin
    login_response = client.post(
        "/auth/login",
        data={
            "username": admin_email,
            "password": admin_password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Verify admin authentication
    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert me_response.status_code == 200


def test_access_protected_endpoint_without_token(client):
    response=client.get("/auth/me")
    assert response.status_code==401

def test_customer_cannot_Create_product(client):
    #register a customer
    email=f"customer_{uuid.uuid4().hex[:8]}@test.com"
    register_response=client.post("/auth/register",
                                  json={
                                      "name":"Test Customer",
                                      "email":email,
                                      "password":"Test@12345"
                                  })
    print("REGISTER STATUS:", register_response.status_code)
    print("REGISTER RESPONSE:", register_response.json())
    assert register_response.status_code in [200, 201]

    # 2. Login as customer
    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Try to create a product as customer
    product_response = client.post(
        "/products",
        json={
            "name": "Unauthorized Product",
            "description": "Security test product",
            "price": 100.0,
            "stock_quantity": 10,
            "category_id": 1,
            "image_url": None
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # 4. Customer should be denied
    assert product_response.status_code == 403

def test_access_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer fake_invalid_token"
        }
    )

    assert response.status_code == 401

import uuid


def test_password_hash_not_exposed(client):
    email = f"safe_{uuid.uuid4().hex[:8]}@test.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Security User",
            "email": email,
            "password": "Safe@12345"
        }
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert "password" not in data
    assert "password_hash" not in data