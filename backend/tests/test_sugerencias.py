from app.core.uow import UnitOfWork
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
