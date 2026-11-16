from datetime import timedelta

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from tests.test_inscripciones import CLASES, TIEMPO, inscribir, nuevo_alumno, nuevo_plan
from tests.test_planes import sesion_de_entrenador


def nueva_inscripcion(admin, plan=TIEMPO, dias_atras=0):
    """Crea alumno, plan e inscripción y devuelve el id de la inscripción."""
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin, plan)
    return inscribir(admin, alumno_id, plan_id, dias_atras).json()["id"]


def pagar(admin, inscripcion_id, metodo="efectivo", fecha=None):
    datos = {"inscripcion_id": inscripcion_id, "metodo_pago": metodo}
    if fecha:
        datos["fecha_pago"] = fecha.isoformat()
    return admin.post("/pagos", json=datos)


def en_dias(dias):
    return (today_ar() + timedelta(days=dias)).isoformat()


def test_sin_sesion_no_se_pueden_registrar_pagos(client):
    assert (
        client.post("/pagos", json={"inscripcion_id": 1, "metodo_pago": "efectivo"}).status_code
        == 401
    )


def test_el_entrenador_no_registra_pagos(crear_usuario, crear_entrenador, iniciar_sesion):
    entrenador = sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion)

    respuesta = entrenador.post("/pagos", json={"inscripcion_id": 1, "metodo_pago": "efectivo"})

    assert respuesta.status_code == 403


def test_el_pago_toma_el_precio_del_plan(admin):
    inscripcion_id = nueva_inscripcion(admin)

    respuesta = pagar(admin, inscripcion_id, "transferencia")

    assert respuesta.status_code == 201
    pago = respuesta.json()["pago"]
    assert pago["monto"] == "15000.00"
    assert pago["metodo_pago"] == "transferencia"
    assert pago["fecha_pago"] == today_ar().isoformat()
    assert pago["plan_nombre"] == "Mensual libre"


def test_el_primer_pago_el_dia_de_inicio_vence_a_la_duracion_del_plan(admin):
    inscripcion_id = nueva_inscripcion(admin)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["fecha_vencimiento"] == en_dias(30)
    assert inscripcion["estado"] == "activo"


def test_el_primer_pago_cuenta_desde_la_fecha_del_pago(admin):
    inscripcion_id = nueva_inscripcion(admin, dias_atras=5)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["fecha_vencimiento"] == en_dias(30)


def test_pagar_antes_de_vencer_suma_el_periodo(admin):
    inscripcion_id = nueva_inscripcion(admin)
    pagar(admin, inscripcion_id)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["fecha_vencimiento"] == en_dias(60)


def test_pagar_vencida_reactiva_desde_la_fecha_del_pago(admin):
    inscripcion_id = nueva_inscripcion(admin, dias_atras=40)
    pagar(admin, inscripcion_id, fecha=today_ar() - timedelta(days=40))

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["fecha_vencimiento"] == en_dias(30)
    assert inscripcion["estado"] == "activo"


def test_plan_por_clases_suma_el_saldo_al_renovar(admin):
    inscripcion_id = nueva_inscripcion(admin, CLASES)
    pagar(admin, inscripcion_id)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["clases_restantes"] == 20
    assert inscripcion["fecha_vencimiento"] == en_dias(120)


def test_plan_por_clases_vencido_reinicia_el_saldo(admin):
    inscripcion_id = nueva_inscripcion(admin, CLASES, dias_atras=100)
    with UnitOfWork() as uow:
        inscripcion = uow.inscripciones.get_by_id(inscripcion_id)
        inscripcion.clases_restantes = 3
        uow.inscripciones.update(inscripcion)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["clases_restantes"] == 10
    assert inscripcion["fecha_vencimiento"] == en_dias(60)


def test_renovar_con_el_saldo_agotado_y_la_vigencia_vigente(admin):
    inscripcion_id = nueva_inscripcion(admin, CLASES)
    pagar(admin, inscripcion_id)
    with UnitOfWork() as uow:
        inscripcion = uow.inscripciones.get_by_id(inscripcion_id)
        inscripcion.clases_restantes = 0
        uow.inscripciones.update(inscripcion)

    inscripcion = pagar(admin, inscripcion_id).json()["inscripcion"]

    assert inscripcion["clases_restantes"] == 10
    assert inscripcion["fecha_vencimiento"] == en_dias(120)
    assert inscripcion["estado"] == "activo"
