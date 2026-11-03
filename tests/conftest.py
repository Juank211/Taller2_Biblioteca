import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.main import app
from app.models import Usuario, Libro, Prestamo
from app.services.auth_service import obtener_password_hash

# Configuración de la base de datos de pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia get_db
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

# Crear las tablas antes de ejecutar las pruebas
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture para el cliente de pruebas
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# Fixture para crear un usuario estándar
@pytest.fixture
def usuario_estandar(db_session):
    hashed_password = obtener_password_hash("password123")
    usuario = Usuario(
        nombre="Usuario Estándar",
        email="usuario@test.com",
        password_hash=hashed_password,
        rol="usuario",
        activo=True
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario

# Fixture para crear un usuario administrador
@pytest.fixture
def usuario_admin(db_session):
    hashed_password = obtener_password_hash("admin123")
    usuario = Usuario(
        nombre="Usuario Admin",
        email="admin@test.com",
        password_hash=hashed_password,
        rol="admin",
        activo=True
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario

# Fixture para generar un token Bearer
@pytest.fixture
def token_usuario_estandar(client, usuario_estandar):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": usuario_estandar.email, "password": "password123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def token_usuario_admin(client, usuario_admin):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": usuario_admin.email, "password": "admin123"}
    )
    return response.json()["access_token"]

# Fixture para la sesión de base de datos
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Fixture para crear un libro
@pytest.fixture
def libro(db_session):
    libro = Libro(
        titulo="Libro de Prueba",
        autor="Autor de Prueba",
        isbn="1234567890",
        copias_disponibles=2,
        estado="Disponible"
    )
    db_session.add(libro)
    db_session.commit()
    db_session.refresh(libro)
    return libro

# Fixture para crear un préstamo
@pytest.fixture
def prestamo(db_session, usuario_estandar, libro):
    prestamo = Prestamo(
        usuario_id=usuario_estandar.id,
        libro_id=libro.id,
        estado="Prestado"
    )
    db_session.add(prestamo)
    db_session.commit()
    db_session.refresh(prestamo)
    return prestamo
