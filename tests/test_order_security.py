def test_cancel_order_without_authentication(client):
    response = client.put("/orders/1/cancel")

    assert response.status_code == 401
def test_cancel_nonexistent_order(client):
    user_data = {
        "name": "Cancel User",
        "email": "canceluser123@example.com",
        "password": "TestPassword123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code in [200, 201]

    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/orders/999999/cancel",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [400, 404]
def test_customer_cannot_update_order_status(client):
    user_data = {
        "name": "Status User",
        "email": "statususer123@example.com",
        "password": "TestPassword123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code in [200, 201]

    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/orders/999999/status?status=SHIPPED",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

