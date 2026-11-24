from app.main import app
from tests.test_alumnos import alta
from tests.test_inscripciones import inscribir, nuevo_plan


def entrar(dni, codigo):
    """Un cliente nuevo, sin la sesión del administrador, que intenta entrar al panel."""
    cliente = TestClient(app)
    respuesta = cliente.post("/panel-alumno/acceso", json={"dni": dni, "codigo": codigo})
    return cliente, respuesta


def test_el_error_es_el_mismo_si_falla_el_dni_o_el_codigo(admin):
    alumno = alta(admin).json()

    _, dni_inexistente = entrar("99999999", alumno["codigo_acceso"])
    _, codigo_incorrecto = entrar(alumno["dni"], "XXXXXXXX")

    assert dni_inexistente.status_code == codigo_incorrecto.status_code == 401
    assert dni_inexistente.json() == codigo_incorrecto.json()


def test_el_alumno_entra_con_dni_y_codigo_y_ve_su_resumen(admin):
    alumno = alta(admin).json()
    inscribir(admin, alumno["id"], nuevo_plan(admin))

    # El código también sirve escrito en minúsculas
    cliente, acceso = entrar(alumno["dni"], alumno["codigo_acceso"].lower())
    resumen = cliente.get("/panel-alumno/resumen")

    assert acceso.status_code == 200
    assert resumen.status_code == 200
    datos = resumen.json()
    assert datos["nombre"] == "Ana Pérez"
    assert datos["inscripcion"]["plan_nombre"] == "Mensual libre"
    assert datos["inscripcion"]["estado"] == "activo"
    assert datos["checklist"] == {"meta": 3, "asistencias": 0, "cumplida": False}
    # Solo cuota y checklist: la ficha de salud no está en el panel
    assert set(datos) == {"nombre", "inscripcion", "checklist"}


def test_un_alumno_dado_de_baja_no_puede_entrar(admin):
    alumno = alta(admin).json()
    admin.patch(f"/alumnos/{alumno['id']}/desactivar")

    _, acceso = entrar(alumno["dni"], alumno["codigo_acceso"])

    assert acceso.status_code == 401
