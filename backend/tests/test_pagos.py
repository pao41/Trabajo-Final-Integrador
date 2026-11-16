from datetime import timedelta

from app.core.clock import today_ar
from tests.test_inscripciones import TIEMPO, inscribir, nuevo_alumno, nuevo_plan
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