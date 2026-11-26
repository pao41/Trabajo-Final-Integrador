"""Configuración de las pruebas: usan una base propia (gimnasio_test), nunca la de desarrollo."""

import os
from pathlib import Path

import psycopg
import pytest
from dotenv import dotenv_values
from sqlalchemy.engine import make_url

BACKEND = Path(__file__).resolve().parents[1]
ESQUEMA = BACKEND.parent / "database" / "schema.sql"


def calcular_url_de_pruebas() -> str:
    # Toma la base del .env y le agrega el sufijo _test
    url = make_url(dotenv_values(BACKEND / ".env")["DATABASE_URL"])
    if not url.database.endswith("_test"):
        url = url.set(database=url.database + "_test")
    return url.render_as_string(hide_password=False)


URL_PRUEBAS = calcular_url_de_pruebas()
# Se configura antes de importar la aplicación, para que use la base de pruebas
os.environ["DATABASE_URL"] = URL_PRUEBAS


@pytest.fixture(scope="session", autouse=True)
def base_de_pruebas():
    """Crea las tablas desde schema.sql una sola vez por corrida de pruebas."""
    try:
        conexion = psycopg.connect(URL_PRUEBAS, autocommit=True)
    except psycopg.OperationalError:
        pytest.exit("No existe la base de pruebas. Creala con: CREATE DATABASE gimnasio_test;", 2)
    with conexion:
        conexion.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conexion.execute(ESQUEMA.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def tablas_vacias(base_de_pruebas):
    """Cada prueba empieza con todas las tablas vacías."""
    consulta = "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
    with psycopg.connect(URL_PRUEBAS, autocommit=True) as conexion:
        tablas = [fila[0] for fila in conexion.execute(consulta)]
        conexion.execute("TRUNCATE " + ", ".join(tablas) + " RESTART IDENTITY CASCADE")


@pytest.fixture(autouse=True)
def sin_bloqueos():
    """Cada prueba empieza sin intentos fallidos ni bloqueos."""
    from app.core.bloqueo import control_de_intentos

    control_de_intentos.reiniciar()


@pytest.fixture(autouse=True)
def sin_ia(monkeypatch):
    """Las pruebas no consultan a Gemini aunque el .env tenga una clave."""
    from app.core.config import settings

    monkeypatch.setattr(settings, "gemini_api_key", "")


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


@pytest.fixture
def crear_usuario():
    """Devuelve una función que crea un usuario directo en la base y entrega su id."""

    def crear(nombre, password="clave-segura-123", rol="administrador", entrenador_id=None):
        from app.core.security import hash_password
        from app.core.uow import UnitOfWork
        from app.modules.usuarios.model import Usuario

        uow = UnitOfWork()
        with uow:
            usuario = Usuario(
                nombre_usuario=nombre,
                password_hash=hash_password(password),
                rol=rol,
                entrenador_id=entrenador_id,
            )
            uow.usuarios.add(usuario)
            return usuario.id

    return crear


@pytest.fixture
def crear_entrenador():
    """Devuelve una función que crea un entrenador directo en la base y entrega su id."""

    def crear(nombre="Laura Gómez"):
        with psycopg.connect(URL_PRUEBAS, autocommit=True) as conexion:
            fila = conexion.execute(
                "INSERT INTO entrenadores (nombre) VALUES (%s) RETURNING id", (nombre,)
            ).fetchone()
            return fila[0]

    return crear


@pytest.fixture
def iniciar_sesion():
    """Devuelve una función que inicia sesión con un cliente."""

    def iniciar(client, nombre, password="clave-segura-123"):
        return client.post("/auth/token", data={"username": nombre, "password": password})

    return iniciar


@pytest.fixture
def admin(client, crear_usuario, iniciar_sesion):
    """Un administrador con la sesión ya iniciada en el cliente."""
    crear_usuario("admin")
    assert iniciar_sesion(client, "admin").status_code == 200
    return client
