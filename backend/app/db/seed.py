from getpass import getpass

from fastapi import HTTPException
from pydantic import ValidationError

from app.core.uow import UnitOfWork
from app.modules.usuarios.model import UsuarioCreate
from app.modules.usuarios.service import UsuarioService


def main():
    """Crea el primer usuario administrador (no hay registro público)."""
    nombre = input("Nombre de usuario del administrador: ")
    password = getpass("Contraseña (mínimo 8 caracteres): ")
    try:
        datos = UsuarioCreate(nombre_usuario=nombre, password=password)
        uow = UnitOfWork()
        with uow:
            usuario = UsuarioService(uow).crear(datos)
    except ValidationError:
        print("Datos inválidos: usuario de 3 caracteres o más y contraseña de 8 a 72.")
    except HTTPException as error:
        print("No se pudo crear:", error.detail)
    else:
        print(f"Administrador '{usuario.nombre_usuario}' creado.")


if __name__ == "__main__":
    main()
