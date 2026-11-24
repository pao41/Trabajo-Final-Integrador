from fastapi.testclient import TestClient

from app.main import app

NUEVA = {
    "nombre": "Movilidad de hombros",
    "tipo": "movilidad",
    "contraindicaciones": "Lesión de hombro",
    "descripcion": "Círculos suaves con los brazos, 2 series de 10.",
}


def entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion, nombre="laura"):
    """Crea un usuario entrenador y devuelve un cliente con su sesión iniciada."""
    entrenador_id = crear_entrenador()
    crear_usuario(nombre, rol="entrenador", entrenador_id=entrenador_id)
    sesion = TestClient(app)
    iniciar_sesion(sesion, nombre)
    return sesion, entrenador_id


def test_el_entrenador_carga_una_rutina_a_su_nombre(
    crear_usuario, crear_entrenador, iniciar_sesion
):
    sesion, entrenador_id = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)

    respuesta = sesion.post("/rutinas", json=NUEVA)

    assert respuesta.status_code == 201
    assert respuesta.json()["entrenador_id"] == entrenador_id
    assert sesion.get("/rutinas").json()[0]["nombre"] == "Movilidad de hombros"


def test_el_administrador_consulta_pero_no_carga_ni_edita(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    sesion, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    rutina_id = sesion.post("/rutinas", json=NUEVA).json()["id"]

    assert len(admin.get("/rutinas").json()) == 1
    assert admin.post("/rutinas", json=NUEVA).status_code == 403
    assert admin.put(f"/rutinas/{rutina_id}", json=NUEVA).status_code == 403


def test_sin_sesion_no_se_ven_las_rutinas(client):
    assert client.get("/rutinas").status_code == 401