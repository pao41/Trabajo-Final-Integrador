from datetime import timedelta

from app.core.clock import today_ar
from tests.test_inscripciones import TIEMPO, inscribir, nuevo_alumno, nuevo_plan


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
