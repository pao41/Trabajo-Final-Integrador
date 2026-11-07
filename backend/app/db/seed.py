from getpass import getpass

from fastapi import HTTPException
from pydantic import ValidationError

from app.core.uow import UnitOfWork
from app.modules.usuarios.model import UsuarioCreate
from app.modules.usuarios.service import UsuarioService
