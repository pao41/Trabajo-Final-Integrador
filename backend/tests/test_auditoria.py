import logging

import pytest


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


