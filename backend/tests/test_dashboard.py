from decimal import Decimal

from app.core.clock import today_ar
from tests.test_inscripciones import CLASES, inscribir, nuevo_alumno, nuevo_plan
from tests.test_pagos import pagar
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


def test_la_facturacion_suma_los_pagos_del_mes_por_metodo(admin):
    mensual, pack = nuevo_plan(admin), nuevo_plan(admin, CLASES)
    for dni, plan_id, metodo in [
        ("30111222", mensual, "efectivo"),
        ("30222333", pack, "transferencia"),
        ("30333444", mensual, "efectivo"),
    ]:
        pagar(admin, inscripto(admin, dni, plan_id)["id"], metodo)

    datos = obtener(admin)

    assert Decimal(datos["facturacion_total"]) == 42000
    assert por_metodo(datos) == {
        "efectivo": 30000,
        "transferencia": 12000,
        "debito": 0,
        "credito": 0,
    }