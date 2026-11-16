from datetime import timedelta
from decimal import Decimal

from app.core.clock import today_ar
from tests.test_inscripciones import inscribir, nuevo_alumno
from tests.test_planes import sesion_de_entrenador


def obtener(admin):
    respuesta = admin.get("/dashboard")
    assert respuesta.status_code == 200
    return respuesta.json()


def por_metodo(datos):
    return {m["metodo_pago"]: Decimal(m["total"]) for m in datos["facturacion_por_metodo"]}


def inscripto(admin, dni, plan_id, dias_atras=0):
    """Crea un alumno con ese DNI, lo inscribe en el plan y devuelve la inscripción."""
    alumno_id = nuevo_alumno(admin, dni)
    return inscribir(admin, alumno_id, plan_id, dias_atras).json()


def mes_pasado():
    """El último día del mes anterior."""
    return today_ar().replace(day=1) - timedelta(days=1)


def test_sin_sesion_no_se_ve_el_dashboard(client):
    assert client.get("/dashboard").status_code == 401


def test_el_entrenador_no_ve_el_dashboard(crear_usuario, crear_entrenador, iniciar_sesion):
    entrenador = sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion)

    assert entrenador.get("/dashboard").status_code == 403


def test_sin_datos_todo_vale_cero(admin):
    datos = obtener(admin)

    assert Decimal(datos["facturacion_total"]) == 0
    assert list(por_metodo(datos).values()) == [0, 0, 0, 0]
    assert datos["alumnos_activos"] == 0
    assert datos["alumnos_por_vencer"] == 0
    assert datos["alumnos_vencidos"] == 0
    assert datos["alumnos_nuevos_mes"] == 0
    assert [s["total"] for s in datos["asistencias_por_semana"]] == [0, 0, 0, 0]
    assert Decimal(datos["ingresos_proyectados"]) == 0
