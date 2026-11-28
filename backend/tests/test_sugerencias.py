from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.uow import UnitOfWork
from app.main import app
from app.modules.sugerencias import ia
from tests.test_alumnos import alta
from tests.test_panel_alumno import entrar
from tests.test_rutinas import entrenador_con_sesion


def cargar(entrenador, nombre, contraindicaciones=None, tipo="calentamiento"):
    """Carga una rutina en el banco por la API."""
    datos = {"nombre": nombre, "tipo": tipo, "contraindicaciones": contraindicaciones}
    return entrenador.post("/rutinas", json=datos).json()["id"]


def alumno_con_ficha(admin, **ficha):
    """Da de alta un alumno y le carga su ficha de salud."""
    alumno = alta(admin).json()
    admin.put(f"/alumnos/{alumno['id']}/ficha-salud", json=ficha)
    return alumno


def test_el_asistente_sugiere_solo_rutinas_compatibles_con_la_ficha(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Caminata suave", "Problemas cardíacos")
    cargar(entrenador, "Sentadillas asistidas", "Lesión de rodilla")
    cargar(entrenador, "Respiración profunda")
    alumno = alumno_con_ficha(admin, problemas_cardiacos=True, lesiones="Dolor de rodilla")
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])

    respuesta = cliente.post("/sugerencias")
    pendientes = entrenador.get("/sugerencias", params={"estado": "pendiente"}).json()

    assert respuesta.status_code == 201
    assert [s["rutina_nombre"] for s in pendientes] == ["Respiración profunda"]
    assert pendientes[0]["alumno_nombre"] == "Ana Pérez"


def test_no_se_sugiere_sin_ficha_sin_rutinas_compatibles_ni_con_otra_pendiente(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    sin_ficha = alta(admin, nombre="Luis Gómez", dni="30111333").json()
    sesion_sin_ficha, _ = entrar(sin_ficha["dni"], sin_ficha["codigo_acceso"])
    alumno = alumno_con_ficha(admin, problemas_cardiacos=False)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])

    assert sesion_sin_ficha.post("/sugerencias").status_code == 409
    # Con ficha pero con el banco vacío
    assert cliente.post("/sugerencias").status_code == 409
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    assert cliente.post("/sugerencias").status_code == 201
    # Mientras haya una pendiente no se pide otra
    assert cliente.post("/sugerencias").status_code == 409


def test_la_rutina_llega_al_alumno_solo_si_el_entrenador_la_aprueba(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, entrenador_id = entrenador_con_sesion(
        crear_usuario, crear_entrenador, iniciar_sesion
    )
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin, problemas_cardiacos=False)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")
    sugerencia_id = entrenador.get("/sugerencias").json()[0]["id"]

    assert cliente.get("/panel-alumno/rutinas").json()["rutinas"] == []
    aprobada = entrenador.patch(f"/sugerencias/{sugerencia_id}/aprobar")
    rutinas = cliente.get("/panel-alumno/rutinas").json()

    assert aprobada.json()["estado"] == "aprobada"
    assert [r["nombre"] for r in rutinas["rutinas"]] == ["Respiración profunda"]
    assert "no reemplazan la supervisión presencial" in rutinas["aviso"]
    # La aprobación queda a nombre del entrenador, con su fecha (RF18)
    with UnitOfWork() as uow:
        guardada = uow.sugerencias.get_by_id(sugerencia_id)
        assert guardada.entrenador_id == entrenador_id
        assert guardada.fecha_validacion is not None


def test_una_rutina_rechazada_no_llega_al_alumno_ni_se_vuelve_a_sugerir(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")
    sugerencia_id = entrenador.get("/sugerencias").json()[0]["id"]

    rechazada = entrenador.patch(f"/sugerencias/{sugerencia_id}/rechazar")
    cliente.post("/sugerencias")
    nueva = entrenador.get("/sugerencias", params={"estado": "pendiente"}).json()

    assert rechazada.json()["estado"] == "rechazada"
    assert cliente.get("/panel-alumno/rutinas").json()["rutinas"] == []
    assert [s["rutina_nombre"] for s in nueva] == ["Giros de cadera"]


def test_las_sugerencias_las_resuelve_solo_el_entrenador_y_una_sola_vez(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")
    sin_sesion = TestClient(app)

    assert len(admin.get("/sugerencias").json()) == 1
    assert admin.patch("/sugerencias/1/aprobar").status_code == 403
    assert sin_sesion.get("/sugerencias").status_code == 401
    assert entrenador.patch("/sugerencias/999/aprobar").status_code == 404
    assert entrenador.patch("/sugerencias/1/aprobar").status_code == 200
    assert entrenador.patch("/sugerencias/1/rechazar").status_code == 409


def test_el_alumno_puede_pedir_un_tipo_de_rutina(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])

    sin_rutinas = cliente.post("/sugerencias", json={"tipo": "vuelta_a_la_calma"})
    movilidad = cliente.post("/sugerencias", json={"tipo": "movilidad", "animo": "cansado"})
    pendientes = entrenador.get("/sugerencias", params={"estado": "pendiente"}).json()

    assert sin_rutinas.status_code == 409
    assert movilidad.status_code == 201
    assert [s["rutina_nombre"] for s in pendientes] == ["Giros de cadera"]


def test_la_ia_elige_la_rutina_y_explica_el_motivo(
    admin, crear_usuario, crear_entrenador, iniciar_sesion, monkeypatch
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    monkeypatch.setattr(settings, "gemini_api_key", "clave")
    monkeypatch.setattr(ia, "consultar", lambda texto: "2\nEs suave para un día de poca energía.")

    respuesta = cliente.post("/sugerencias", json={"animo": "cansado"})
    pendientes = entrenador.get("/sugerencias", params={"estado": "pendiente"}).json()

    assert respuesta.json()["explicacion"] == "Es suave para un día de poca energía."
    assert [s["rutina_nombre"] for s in pendientes] == ["Giros de cadera"]


def test_si_la_ia_falla_el_asistente_sugiere_la_primera_rutina_compatible(
    admin, crear_usuario, crear_entrenador, iniciar_sesion, monkeypatch
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])

    def sin_conexion(texto):
        raise OSError("sin conexión")

    monkeypatch.setattr(settings, "gemini_api_key", "clave")
    monkeypatch.setattr(ia, "consultar", sin_conexion)

    respuesta = cliente.post("/sugerencias", json={"animo": "con_molestia"})
    pendientes = entrenador.get("/sugerencias", params={"estado": "pendiente"}).json()

    assert respuesta.status_code == 201
    assert respuesta.json()["explicacion"] is None
    assert [s["rutina_nombre"] for s in pendientes] == ["Respiración profunda"]


def test_el_listado_de_alumnos_cuenta_las_rutinas_aprobadas(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    alumno = alumno_con_ficha(admin, problemas_cardiacos=False)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")

    antes = admin.get("/alumnos").json()[0]["rutinas_aprobadas"]
    sugerencia_id = entrenador.get("/sugerencias").json()[0]["id"]
    entrenador.patch(f"/sugerencias/{sugerencia_id}/aprobar")
    despues = admin.get("/alumnos").json()[0]["rutinas_aprobadas"]

    assert (antes, despues) == (0, 1)


def test_no_se_elimina_una_rutina_que_ya_se_sugirio(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    rutina_id = cargar(entrenador, "Respiración profunda")
    alumno = alumno_con_ficha(admin, problemas_cardiacos=False)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")

    respuesta = entrenador.delete(f"/rutinas/{rutina_id}")

    assert respuesta.status_code == 409
    assert [r["nombre"] for r in entrenador.get("/rutinas").json()] == ["Respiración profunda"]
