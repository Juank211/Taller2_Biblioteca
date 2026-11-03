from datetime import datetime, timedelta

def test_solicitar_prestamo(client, token_usuario_estandar, db_session):
    # Crear un libro con copias disponibles
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json={
            "titulo": "Libro para Prestar",
            "autor": "Autor de Prueba",
            "isbn": "1234567890",
            "copias_disponibles": 2,
            "estado": "Disponible"
        }
    )
    assert response.status_code == 201
    libro_id = response.json()["id"]

    # Solicitar préstamo
    response = client.post(
        "/api/v1/prestamos",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"},
        json={"libro_id": libro_id, "estado": "Prestado"}
    )
    assert response.status_code == 201
    assert response.json()["libro_id"] == libro_id
    assert response.json()["estado"] == "Prestado"

def test_solicitar_prestamo_sin_copias(client, token_usuario_estandar, db_session):
    # Crear un libro sin copias disponibles
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json={
            "titulo": "Libro sin Copias",
            "autor": "Autor de Prueba",
            "isbn": "0987654321",
            "copias_disponibles": 0,
            "estado": "No Disponible"
        }
    )
    assert response.status_code == 201
    libro_id = response.json()["id"]

    # Intentar solicitar préstamo
    response = client.post(
        "/api/v1/prestamos",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"},
        json={"libro_id": libro_id, "estado": "Prestado"}
    )
    assert response.status_code == 400
    assert "No hay copias disponibles" in response.json()["detail"]

def test_devolver_prestamo(client, token_usuario_estandar, db_session):
    # Crear un libro y un préstamo
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json={
            "titulo": "Libro para Devolver",
            "autor": "Autor de Prueba",
            "isbn": "9876543210",
            "copias_disponibles": 1,
            "estado": "Disponible"
        }
    )
    assert response.status_code == 201
    libro_id = response.json()["id"]

    # Solicitar préstamo
    response = client.post(
        "/api/v1/prestamos",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"},
        json={"libro_id": libro_id, "estado": "Prestado"}
    )
    assert response.status_code == 201
    prestamo_id = response.json()["id"]

    # Devolver préstamo
    response = client.put(
        f"/api/v1/prestamos/{prestamo_id}/devolver",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"}
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "Devolvido"
