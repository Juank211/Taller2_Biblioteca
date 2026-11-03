def test_login_success(client, usuario_estandar):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": usuario_estandar.email, "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure(client, usuario_estandar):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": usuario_estandar.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_logout(client, token_usuario_estandar):
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Sesión cerrada exitosamente"}
