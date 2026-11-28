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


def test_el_entrenador_edita_y_la_rutina_conserva_a_quien_la_cargo(
    crear_usuario, crear_entrenador, iniciar_sesion
):
    autora, autora_id = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    otro, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion, "pedro")
    rutina_id = autora.post("/rutinas", json=NUEVA).json()["id"]

    editada = otro.put(f"/rutinas/{rutina_id}", json={**NUEVA, "nombre": "Movilidad de cuello"})

    assert editada.status_code == 200
    assert editada.json()["nombre"] == "Movilidad de cuello"
    assert editada.json()["entrenador_id"] == autora_id
    assert otro.put("/rutinas/999", json=NUEVA).status_code == 404


def test_solo_se_permiten_los_tres_tipos_de_rutina(crear_usuario, crear_entrenador, iniciar_sesion):
    sesion, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)

    fuerza = sesion.post("/rutinas", json={**NUEVA, "tipo": "fuerza"})

    assert fuerza.status_code == 422


def test_no_se_repite_el_nombre_de_una_rutina(crear_usuario, crear_entrenador, iniciar_sesion):
    sesion, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    primera = sesion.post("/rutinas", json=NUEVA).json()["id"]
    otra = sesion.post("/rutinas", json={**NUEVA, "nombre": "Estiramiento"}).json()["id"]

    assert sesion.post("/rutinas", json=NUEVA).status_code == 409
    repetida = {**NUEVA, "nombre": " MOVILIDAD de hombros"}
    assert sesion.post("/rutinas", json=repetida).status_code == 409
    assert sesion.put(f"/rutinas/{otra}", json=NUEVA).status_code == 409
    # Editar conservando el propio nombre sí se puede
    assert sesion.put(f"/rutinas/{primera}", json=NUEVA).status_code == 200


def test_el_entrenador_elimina_una_rutina_que_nunca_se_sugirio(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    sesion, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    rutina_id = sesion.post("/rutinas", json=NUEVA).json()["id"]

    assert admin.delete(f"/rutinas/{rutina_id}").status_code == 403
    assert sesion.delete(f"/rutinas/{rutina_id}").status_code == 204
    assert sesion.get("/rutinas").json() == []
    assert sesion.delete(f"/rutinas/{rutina_id}").status_code == 404
