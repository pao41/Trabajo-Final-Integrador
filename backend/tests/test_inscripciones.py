from datetime import timedelta

from app.core.clock import today_ar

TIEMPO = {"nombre": "Mensual libre", "duracion_dias": 30, "precio": "15000", "tipo": "tiempo"}
CLASES = {
    "nombre": "Pack 10 clases",
    "duracion_dias": 60,
    "precio": "12000",
    "tipo": "clases",
    "cantidad_clases": 10,
}


def nuevo_alumno(admin, dni="30111222"):
    return admin.post("/alumnos", json={"nombre": "Ana Pérez", "dni": dni}).json()["id"]


def nuevo_plan(admin, plan=TIEMPO):
    return admin.post("/planes", json=plan).json()["id"]


def inscribir(admin, alumno_id, plan_id, dias_atras=0):
    """Inscribe al alumno; con dias_atras simula una inscripción que empezó antes."""
    inicio = (today_ar() - timedelta(days=dias_atras)).isoformat()
    datos = {"alumno_id": alumno_id, "plan_id": plan_id, "fecha_inicio": inicio}
    return admin.post("/inscripciones", json=datos)
