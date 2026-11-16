from fastapi.testclient import TestClient

from app.main import app

TIEMPO = {"nombre": "Mensual libre", "duracion_dias": 30, "precio": "15000.00", "tipo": "tiempo"}
CLASES = {
    "nombre": "Pack 10 clases",
    "duracion_dias": 60,
    "precio": "12000.50",
    "tipo": "clases",
    "cantidad_clases": 10,
}


def sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")
    return entrenador


def test_sin_sesion_no_se_ven_los_planes(client):
    assert client.get("/planes").status_code == 401


def test_el_entrenador_no_puede_gestionar_planes(crear_usuario, crear_entrenador, iniciar_sesion):
    entrenador = sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion)

    assert entrenador.get("/planes").status_code == 403
    assert entrenador.post("/planes", json=TIEMPO).status_code == 403


def test_se_crea_un_plan_por_tiempo(admin):
    respuesta = admin.post("/planes", json=TIEMPO)

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["nombre"] == "Mensual libre"
    assert datos["precio"] == "15000.00"
    assert datos["cantidad_clases"] is None


def test_se_crea_un_plan_por_clases(admin):
    respuesta = admin.post("/planes", json=CLASES)

    assert respuesta.status_code == 201
    assert respuesta.json()["cantidad_clases"] == 10


def test_un_plan_por_clases_necesita_su_cantidad_de_clases(admin):
    sin_cantidad = {**CLASES, "cantidad_clases": None}

    assert admin.post("/planes", json=sin_cantidad).status_code == 422


def test_un_plan_por_tiempo_no_lleva_cantidad_de_clases(admin):
    con_cantidad = {**TIEMPO, "cantidad_clases": 10}

    assert admin.post("/planes", json=con_cantidad).status_code == 422
