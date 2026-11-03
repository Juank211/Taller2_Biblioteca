def test_consultar_multas(client, token_usuario_estandar, db_session):
    # Consultar multas (debería estar vacío inicialmente)
    response = client.get(
        "/api/v1/multas",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

def test_pagar_multa(client, token_usuario_estandar, db_session):
    # Primero, crear una multa manualmente en la base de datos
    from app.models import Multa
    multa = Multa(
        usuario_id=1,  # ID del usuario estándar
        prestamo_id=1,  # ID de un préstamo (simulado)
        monto=10.0,
        pagado=False
    )
    db_session.add(multa)
    db_session.commit()

    # Pagar la multa
    response = client.post(
        "/api/v1/multas/1/pagar",
        headers={"Authorization": f"Bearer {token_usuario_estandar}"}
    )
    assert response.status_code == 200
    assert response.json()["pagado"] is True
    assert response.json()["monto"] == 10.0
