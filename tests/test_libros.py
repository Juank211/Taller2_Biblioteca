def test_listar_libros_publico(client):
    response = client.get("/api/v1/libros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_libro_admin(client, token_usuario_admin):
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json={
            "titulo": "Libro de Prueba",
            "autor": "Autor de Prueba",
            "isbn": "1234567890",
            "copias_disponibles": 5,
            "estado": "Disponible"
        }
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Libro de Prueba"

def test_crear_libro_usuario_estandar(client, token_usuario_estandar):
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"},
        json={
            "titulo": "Libro de Prueba",
            "autor": "Autor de Prueba",
            "isbn": "1234567890",
            "copias_disponibles": 5,
            "estado": "Disponible"
        }
    )
    assert response.status_code == 403

def test_actualizar_libro_admin(client, token_usuario_admin, db_session):
    # Crear un libro primero
    libro = {
        "titulo": "Libro Original",
        "autor": "Autor Original",
        "isbn": "0987654321",
        "copias_disponibles": 3,
        "estado": "Disponible"
    }
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json=libro
    )
    assert response.status_code == 201
    libro_id = response.json()["id"]

    # Actualizar el libro
    response = client.put(
        f"/api/v1/libros/{libro_id}",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json={"titulo": "Libro Actualizado"}
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Libro Actualizado"

def test_actualizar_libro_usuario_estandar(client, token_usuario_estandar, db_session):
    # Crear un libro primero
    libro = {
        "titulo": "Libro Original",
        "autor": "Autor Original",
        "isbn": "0987654321",
        "copias_disponibles": 3,
        "estado": "Disponible"
    }
    response = client.post(
        "/api/v1/libros",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
        json=libro
    )
    assert response.status_code == 201
    libro_id = response.json()["id"]

    # Intentar actualizar el libro como usuario estándar
    response = client.put(
        f"/api/v1/libros/{libro_id}",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"},
        json={"titulo": "Libro Actualizado"}
    )
    assert response.status_code == 403
