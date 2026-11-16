from fastapi.testclient import TestClient

from app.main import app

NUEVA = {
    "nombre_gimnasio": "Gimnasio Central",
    "dias_aviso_vencimiento": 10,
    "metodos_pago_habilitados": ["efectivo", "transferencia"],
}


def test_sin_sesion_no_se_ve_la_configuracion(client):
    assert client.get("/configuracion").status_code == 401


def test_el_entrenador_no_puede_ver_la_configuracion(
    crear_usuario, crear_entrenador, iniciar_sesion
):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")

    assert entrenador.get("/configuracion").status_code == 403


def test_la_primera_vez_devuelve_valores_por_defecto(admin):
    datos = admin.get("/configuracion").json()

    assert datos["dias_aviso_vencimiento"] == 7
    assert datos["metodos_pago_habilitados"] == ["efectivo", "transferencia", "debito", "credito"]
