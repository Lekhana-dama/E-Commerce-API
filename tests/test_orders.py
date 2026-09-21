def test_get_orders_without_authentication(client):
    response = client.get("/orders")

    assert response.status_code == 401

def test_get_orders_authenticated(client):
    user_data = {
        "name": "Order User",
        "email": "orderuser123@example.com",
        "password": "TestPassword123"
    }

    # Register user
    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code in [200, 201]

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Get user's orders
    response = client.get(
        "/orders",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)