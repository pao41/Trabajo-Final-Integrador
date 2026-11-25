from tests.test_alumnos import alta


def cargar(entrenador, nombre, contraindicaciones=None, tipo="calentamiento"):
    """Carga una rutina en el banco por la API."""
    datos = {"nombre": nombre, "tipo": tipo, "contraindicaciones": contraindicaciones}
    return entrenador.post("/rutinas", json=datos).json()["id"]


def alumno_con_ficha(admin, **ficha):
    """Da de alta un alumno y le carga su ficha de salud."""
    alumno = alta(admin).json()
    admin.put(f"/alumnos/{alumno['id']}/ficha-salud", json=ficha)
    return alumno