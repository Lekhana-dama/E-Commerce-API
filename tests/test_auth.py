def test_register_user(client):
    response=client.post("/auth/register",
                         json={
                                "name":"Test User",
                                "email":"testuser123@example.com",
                                "password":"TestPassword123"
                                })
    assert response.status_code in [200,201]
    data=response.json()
    assert data["email"]=="testuser123@example.com"
    assert data["name"]=="Test User"

def test_register_duplicate_user(client):
    user_data={
        "name":"Duplicate user",
        "email":"testuser123@example.com",
        "password":"TestPassword123"
    }
    fisrt_response=client.post("/auth/register",json=user_data)
    second_response=client.post("/auth/register",json=user_data)
    assert second_response.status_code in [400,409]

def test_login_user(client):
    #Register user first
    user_data={
        "name":"Login user",
        "email":"loginuser@example.com",
        "password":"TestPassword123"
    }
    register_response=client.post("/auth/register",json=user_data)
    assert register_response.status_code in [200,201]

    #login using from data
    login_response=client.post("/auth/login",data={
        "username":"loginuser@example.com",
        "password":"TestPassword123"
    })
    assert login_response.status_code==200
    data=login_response.json()

    assert "access_token" in data
    assert data["token_type"]=="bearer"

def test_login_wrong_password(client):
    response=client.post("/auth/login",data={
        "username":"loginuser@example.com",
        "password":"wrongpasswordd"

    })
    assert response.status_code==401
    
