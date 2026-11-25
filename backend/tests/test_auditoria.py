import logging

import pytest

from tests.test_panel_alumno import entrar
from tests.test_rutinas import entrenador_con_sesion
from tests.test_sugerencias import alumno_con_ficha, cargar


@pytest.fixture
def lineas(caplog):
    """Devuelve una función que entrega las líneas del registro de auditoría."""
    caplog.set_level(logging.INFO, logger="auditoria")
    return lambda: [r.getMessage() for r in caplog.records if r.name == "auditoria"]


def crear_alumno(admin):
    datos = {"nombre": "Ana Pérez", "dni": "30111222", "contacto": "387-4000000"}
    return admin.post("/alumnos", json=datos).json()["id"]


def test_dar_de_baja_a_un_alumno_queda_registrado(admin, lineas):
    alumno_id = crear_alumno(admin)

    admin.patch(f"/alumnos/{alumno_id}/desactivar")

    campos = lineas()[-1].split(" | ")
    assert campos[1:] == ["admin", "dar de baja", f"alumno {alumno_id}", "éxito"]
    # El primer campo es la fecha y hora
    assert len(campos[0]) == 19


def test_una_accion_rechazada_se_registra_como_rechazo(admin, lineas):
    respuesta = admin.patch("/alumnos/999/desactivar")

    assert respuesta.status_code == 404
    assert lineas()[-1].endswith("| admin | dar de baja | alumno 999 | rechazo")


def test_regenerar_el_codigo_no_guarda_el_codigo_en_el_registro(admin, lineas):
    alumno_id = crear_alumno(admin)

    codigo = admin.post(f"/alumnos/{alumno_id}/codigo-acceso").json()["codigo_acceso"]

    assert lineas()[-1].endswith(f"| admin | regenerar código | alumno {alumno_id} | éxito")
    assert codigo not in " ".join(lineas())


def test_gestionar_usuarios_se_registra_sin_la_contrasena(admin, lineas):
    nuevo = {"nombre_usuario": "marta", "password": "clave-marta-123"}

    creado = admin.post("/usuarios", json=nuevo).json()
    admin.put(f"/usuarios/{creado['id']}/password", json={"nueva_password": "otra-clave-456"})
    admin.patch(f"/usuarios/{creado['id']}/desactivar")

    texto = "\n".join(lineas())
    assert "| admin | crear usuario | usuario marta | éxito" in texto
    assert f"| admin | restablecer contraseña | usuario {creado['id']} | éxito" in texto
    assert f"| admin | desactivar usuario | usuario {creado['id']} | éxito" in texto
    assert "clave-marta-123" not in texto
    assert "otra-clave-456" not in texto


PLAN = {"nombre": "Mensual libre", "duracion_dias": 30, "precio": "15000.00", "tipo": "tiempo"}
CONFIG = {
    "nombre_gimnasio": "Gimnasio Central",
    "dias_aviso_vencimiento": 5,
    "metodos_pago_habilitados": ["efectivo"],
}


def test_los_cambios_de_planes_y_de_configuracion_se_registran(admin, lineas):
    plan_id = admin.post("/planes", json=PLAN).json()["id"]
    admin.put(f"/planes/{plan_id}", json={**PLAN, "precio": "16000.00"})
    admin.put("/configuracion", json=CONFIG)

    texto = "\n".join(lineas())
    assert "| admin | crear plan | plan Mensual libre | éxito" in texto
    assert f"| admin | editar plan | plan {plan_id} | éxito" in texto
    assert "| admin | cambiar configuración | configuración | éxito" in texto


def test_una_accion_sin_permiso_no_llega_a_registrarse(
    client, crear_usuario, crear_entrenador, iniciar_sesion, lineas
):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    iniciar_sesion(client, "laura")

    assert client.patch("/alumnos/1/desactivar").status_code == 403
    assert lineas() == []


def test_gestionar_entrenadores_se_registra(admin, lineas):
    entrenador_id = admin.post("/entrenadores", json={"nombre": "Laura Gómez"}).json()["id"]

    admin.put(f"/entrenadores/{entrenador_id}", json={"nombre": "Laura Gómez Díaz"})

    acciones = [linea.split(" | ")[2:] for linea in lineas()]
    assert acciones == [
        ["crear entrenador", "entrenador Laura Gómez", "éxito"],
        ["editar entrenador", f"entrenador {entrenador_id}", "éxito"],
    ]


def test_aprobar_y_rechazar_sugerencias_se_registra(
    admin, crear_usuario, crear_entrenador, iniciar_sesion, lineas
):
    entrenador, _ = entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion)
    cargar(entrenador, "Respiración profunda")
    cargar(entrenador, "Giros de cadera", tipo="movilidad")
    alumno = alumno_con_ficha(admin)
    cliente, _ = entrar(alumno["dni"], alumno["codigo_acceso"])
    cliente.post("/sugerencias")
    entrenador.patch("/sugerencias/1/aprobar")
    cliente.post("/sugerencias")
    entrenador.patch("/sugerencias/2/rechazar")

    acciones = [linea.split(" | ")[1:] for linea in lineas() if "sugerencia" in linea]
    assert acciones == [
        ["laura", "aprobar sugerencia", "sugerencia 1", "éxito"],
        ["laura", "rechazar sugerencia", "sugerencia 2", "éxito"],
    ]