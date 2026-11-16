from app.core.uow import UnitOfWork
from app.modules.configuracion.model import Configuracion, ConfiguracionDatos


class ConfiguracionService:
    """Datos generales del gimnasio y parámetros que usa el sistema."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def obtener(self) -> Configuracion:
        """Devuelve la configuración; la primera vez la crea con valores por defecto."""
        configuracion = self.uow.configuracion.get_actual()
        if not configuracion:
            configuracion = Configuracion(
                nombre_gimnasio="Mi gimnasio",
                metodos_pago_habilitados=["efectivo", "transferencia", "debito", "credito"],
            )
            self.uow.configuracion.add(configuracion)
        return configuracion

    def guardar(self, datos: ConfiguracionDatos) -> Configuracion:
        configuracion = self.obtener()
        configuracion.nombre_gimnasio = datos.nombre_gimnasio.strip()
        configuracion.dias_aviso_vencimiento = datos.dias_aviso_vencimiento
        configuracion.metodos_pago_habilitados = list(datos.metodos_pago_habilitados)
        return self.uow.configuracion.update(configuracion)
