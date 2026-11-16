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


def test_el_precio_y_la_duracion_tienen_que_ser_positivos(admin):
    assert admin.post("/planes", json={**TIEMPO, "precio": "0"}).status_code == 422
    assert admin.post("/planes", json={**TIEMPO, "duracion_dias": 0}).status_code == 422


def test_un_nombre_repetido_da_409(admin):
    admin.post("/planes", json=TIEMPO)

    respuesta = admin.post("/planes", json=TIEMPO)

    assert respuesta.status_code == 409


def test_se_listan_los_planes_por_nombre(admin):
    admin.post("/planes", json=TIEMPO)
    admin.post("/planes", json=CLASES)

    nombres = [p["nombre"] for p in admin.get("/planes").json()]

    assert nombres == ["Mensual libre", "Pack 10 clases"]


def test_se_edita_un_plan(admin):
    plan_id = admin.post("/planes", json=TIEMPO).json()["id"]

    respuesta = admin.put(f"/planes/{plan_id}", json={**TIEMPO, "precio": "18000"})

    assert respuesta.status_code == 200
    assert respuesta.json()["precio"] == "18000.00"


def test_editar_un_plan_inexistente_da_404(admin):
    assert admin.put("/planes/999", json=TIEMPO).status_code == 404


def test_al_editar_no_se_puede_repetir_el_nombre_de_otro_plan(admin):
    admin.post("/planes", json=TIEMPO)
    otro_id = admin.post("/planes", json=CLASES).json()["id"]

    respuesta = admin.put(f"/planes/{otro_id}", json={**CLASES, "nombre": TIEMPO["nombre"]})

    assert respuesta.status_code == 409


def test_se_puede_guardar_un_plan_con_su_mismo_nombre(admin):
    plan_id = admin.post("/planes", json=TIEMPO).json()["id"]

    assert admin.put(f"/planes/{plan_id}", json=TIEMPO).status_code == 200
