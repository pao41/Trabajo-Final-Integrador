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


def test_sin_sesion_no_se_puede_inscribir(client):
    assert client.post("/inscripciones", json={"alumno_id": 1, "plan_id": 1}).status_code == 401


def test_la_inscripcion_calcula_el_vencimiento(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)

    respuesta = inscribir(admin, alumno_id, plan_id)

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["fecha_vencimiento"] == (today_ar() + timedelta(days=30)).isoformat()
    assert datos["plan_nombre"] == "Mensual libre"
    assert datos["clases_restantes"] is None
    assert datos["estado"] == "activo"


def test_sin_fecha_de_inicio_se_toma_la_de_hoy(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    datos = {"alumno_id": alumno_id, "plan_id": plan_id}

    respuesta = admin.post("/inscripciones", json=datos)

    assert respuesta.json()["fecha_inicio"] == today_ar().isoformat()
