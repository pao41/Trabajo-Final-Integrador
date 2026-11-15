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