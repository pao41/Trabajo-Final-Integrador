from datetime import timedelta

from app.core.clock import now_ar, today_ar
from app.core.uow import UnitOfWork
from app.modules.asistencias.model import Asistencia
from tests.test_inscripciones import CLASES, TIEMPO, inscribir, nuevo_alumno, nuevo_plan
from tests.test_planes import sesion_de_entrenador


def alumno_inscripto(admin, plan=TIEMPO, dias_atras=0):
    """Crea alumno, plan e inscripción y devuelve (alumno_id, inscripcion_id)."""
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin, plan)
    return alumno_id, inscribir(admin, alumno_id, plan_id, dias_atras).json()["id"]


def ingresar(admin, alumno_id):
    return admin.post("/asistencias", json={"alumno_id": alumno_id})


def ingreso_hace(alumno_id, inscripcion_id, horas):
    """Deja guardado un ingreso anterior, de hace tantas horas."""
    antes = now_ar().replace(tzinfo=None) - timedelta(hours=horas)
    with UnitOfWork() as uow:
        uow.asistencias.add(
            Asistencia(
                alumno_id=alumno_id,
                inscripcion_id=inscripcion_id,
                fecha=antes.date(),
                hora=antes.time(),
            )
        )


def fijar_saldo(inscripcion_id, saldo):
    with UnitOfWork() as uow:
        inscripcion = uow.inscripciones.get_by_id(inscripcion_id)
        inscripcion.clases_restantes = saldo
        uow.inscripciones.update(inscripcion)


def test_sin_sesion_no_se_registran_ingresos(client):
    assert client.post("/asistencias", json={"alumno_id": 1}).status_code == 401


def test_el_entrenador_no_registra_ingresos(crear_usuario, crear_entrenador, iniciar_sesion):
    entrenador = sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion)

    assert entrenador.post("/asistencias", json={"alumno_id": 1}).status_code == 403


def test_el_ingreso_queda_asociado_a_la_inscripcion(admin):
    alumno_id, inscripcion_id = alumno_inscripto(admin)

    respuesta = ingresar(admin, alumno_id)

    assert respuesta.status_code == 201
    ingreso = respuesta.json()["asistencia"]
    assert ingreso["inscripcion_id"] == inscripcion_id
    assert ingreso["fecha"] == today_ar().isoformat()
    assert ingreso["plan_nombre"] == "Mensual libre"
    assert respuesta.json()["inscripcion"]["clases_restantes"] is None


def test_el_ingreso_descuenta_una_clase(admin):
    alumno_id, _ = alumno_inscripto(admin, CLASES)

    respuesta = ingresar(admin, alumno_id)

    assert respuesta.json()["inscripcion"]["clases_restantes"] == 9


def test_la_ultima_clase_deja_la_inscripcion_vencida(admin):
    alumno_id, inscripcion_id = alumno_inscripto(admin, CLASES)
    fijar_saldo(inscripcion_id, 1)

    inscripcion = ingresar(admin, alumno_id).json()["inscripcion"]

    assert inscripcion["clases_restantes"] == 0
    assert inscripcion["estado"] == "vencido"


def test_con_el_saldo_en_cero_se_rechaza_el_ingreso(admin):
    alumno_id, inscripcion_id = alumno_inscripto(admin, CLASES)
    fijar_saldo(inscripcion_id, 0)

    respuesta = ingresar(admin, alumno_id)

    assert respuesta.status_code == 409
    assert "corresponde renovar" in respuesta.json()["detail"]
