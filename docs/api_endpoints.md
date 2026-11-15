Este documento describe los endpoints de la API REST del sistema, organizados por módulo. Los nombres de los recursos se definen en español y en plural (por ejemplo, /alumnos o /inscripciones), y los datos se intercambian en formato JSON. La documentación interactiva de la API se genera automáticamente y puede consultarse en /docs mientras el backend está en ejecución.

El acceso a cada endpoint depende del perfil del usuario, conforme a la matriz de permisos de [`seguridad_y_permisos.md`](./seguridad_y_permisos.md). La sesión del personal se mantiene mediante una cookie HttpOnly, por lo que no es necesario enviar credenciales en cada petición.

La columna "Estado" indica si el endpoint ya se encuentra disponible o si se incorporará junto con su módulo en las próximas etapas.