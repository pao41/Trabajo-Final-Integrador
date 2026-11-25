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
