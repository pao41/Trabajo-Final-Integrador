from datetime import timedelta

from app.core.clock import today_ar
from app.core.uow import UnitOfWork

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


def test_un_plan_por_clases_arranca_con_su_saldo(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin, CLASES)

    datos = inscribir(admin, alumno_id, plan_id).json()

    assert datos["clases_restantes"] == 10
    assert datos["fecha_vencimiento"] == (today_ar() + timedelta(days=60)).isoformat()


def test_el_alumno_y_el_plan_tienen_que_existir(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)

    assert inscribir(admin, 999, plan_id).status_code == 404
    assert inscribir(admin, alumno_id, 999).status_code == 404


def test_no_se_inscribe_a_un_alumno_dado_de_baja(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    admin.patch(f"/alumnos/{alumno_id}/desactivar")

    assert inscribir(admin, alumno_id, plan_id).status_code == 409


def test_con_una_inscripcion_vigente_no_se_puede_crear_otra(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscribir(admin, alumno_id, plan_id)

    assert inscribir(admin, alumno_id, plan_id).status_code == 409


def test_vencida_la_inscripcion_se_puede_inscribir_de_nuevo(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscribir(admin, alumno_id, plan_id, dias_atras=40)

    assert inscribir(admin, alumno_id, plan_id).status_code == 201


def test_faltando_menos_de_7_dias_queda_por_vencer(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)

    datos = inscribir(admin, alumno_id, plan_id, dias_atras=25).json()

    assert datos["estado"] == "por_vencer"


def test_pasado_el_vencimiento_queda_vencida(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)

    datos = inscribir(admin, alumno_id, plan_id, dias_atras=40).json()

    assert datos["estado"] == "vencido"


def test_el_dia_del_vencimiento_ya_esta_vencida(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)

    datos = inscribir(admin, alumno_id, plan_id, dias_atras=30).json()

    assert datos["estado"] == "vencido"


def test_el_aviso_usa_los_dias_de_la_configuracion(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    config = admin.get("/configuracion").json()
    admin.put("/configuracion", json={**config, "dias_aviso_vencimiento": 3})

    # Faltan 5 días: con aviso de 3 todavía está activa (RN09)
    datos = inscribir(admin, alumno_id, plan_id, dias_atras=25).json()

    assert datos["estado"] == "activo"


def test_un_plan_por_clases_sin_saldo_esta_vencido(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin, CLASES)
    inscripcion_id = inscribir(admin, alumno_id, plan_id).json()["id"]
    uow = UnitOfWork()
    with uow:
        inscripcion = uow.inscripciones.get_by_id(inscripcion_id)
        inscripcion.clases_restantes = 0
        uow.inscripciones.update(inscripcion)

    lista = admin.get("/inscripciones", params={"alumno_id": alumno_id}).json()

    # El saldo en cero vence la inscripción aunque la fecha siga vigente (RN31)
    assert lista[0]["estado"] == "vencido"


def test_al_consultar_se_actualiza_el_estado_guardado(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscripcion_id = inscribir(admin, alumno_id, plan_id, dias_atras=40).json()["id"]
    uow = UnitOfWork()
    with uow:
        inscripcion = uow.inscripciones.get_by_id(inscripcion_id)
        inscripcion.estado = "activo"
        uow.inscripciones.update(inscripcion)

    admin.get("/inscripciones")

    with uow:
        assert uow.inscripciones.get_by_id(inscripcion_id).estado == "vencido"


def test_se_listan_las_inscripciones_de_un_alumno_con_la_mas_nueva_primero(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscribir(admin, alumno_id, plan_id, dias_atras=60)
    inscribir(admin, alumno_id, plan_id)
    otro_id = nuevo_alumno(admin, dni="30111333")
    inscribir(admin, otro_id, plan_id)

    lista = admin.get("/inscripciones", params={"alumno_id": alumno_id}).json()

    assert len(lista) == 2
    assert lista[0]["fecha_inicio"] > lista[1]["fecha_inicio"]
    assert len(admin.get("/inscripciones").json()) == 3


def test_el_historial_se_conserva_al_dar_de_baja_al_alumno(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscribir(admin, alumno_id, plan_id)
    admin.patch(f"/alumnos/{alumno_id}/desactivar")

    lista = admin.get("/inscripciones", params={"alumno_id": alumno_id}).json()

    assert len(lista) == 1


def test_no_se_cambia_el_tipo_de_un_plan_con_inscripciones(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    inscribir(admin, alumno_id, plan_id)
    como_clases = {**CLASES, "nombre": TIEMPO["nombre"]}

    respuesta = admin.put(f"/planes/{plan_id}", json=como_clases)

    assert respuesta.status_code == 409


def test_editar_el_precio_no_cambia_las_inscripciones_hechas(admin):
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin)
    antes = inscribir(admin, alumno_id, plan_id).json()
    admin.put(f"/planes/{plan_id}", json={**TIEMPO, "duracion_dias": 90})

    despues = admin.get("/inscripciones", params={"alumno_id": alumno_id}).json()[0]

    assert despues["fecha_vencimiento"] == antes["fecha_vencimiento"]
