# Arquitectura del Proyecto — Sistema de Gestión para Gimnasios

## Arquitectura elegida

El sistema sigue una arquitectura **cliente-servidor de tres capas**, con separación clara entre presentación, lógica de negocio y persistencia:

```mermaid
flowchart LR
    A[Frontend<br/>React] -->|HTTP / JSON<br/>API REST| B[Backend<br/>Python + FastAPI]
    B -->|Consultas SQL| C[(Base de datos<br/>PostgreSQL)]
```

- **Capa de presentación (Frontend):** React. Consume la API del backend mediante peticiones HTTP y renderiza el Panel Administrador y el Panel del Alumno.
- **Capa de lógica de negocio (Backend):** Python + FastAPI, expuesto como una API REST. Organizado internamente por capas:
  - **Routers** — definen los endpoints disponibles.
  - **Esquemas** — definen y validan los datos de entrada y de salida de cada endpoint.
  - **Dependencias y middleware** — autenticación de sesiones, control de permisos según el perfil del usuario, límite de intentos fallidos y registro de acciones sensibles.
  - **Servicios** — contienen la lógica de negocio.
  - **Modelos / acceso a datos** — modelos SQLModel que reflejan las tablas y comunicación con PostgreSQL.
- **Capa de persistencia (Base de datos):** PostgreSQL, con el esquema relacional definido en [`/database/schema.sql`](../database/schema.sql).

## Decisiones

- **Separación de responsabilidades:** cada capa puede modificarse o reemplazarse sin afectar directamente a las demás (por ejemplo, cambiar el frontend sin tocar el backend).
- **Mantenibilidad:** organizar el backend en capas (routers/esquemas/servicios) facilita ubicar y corregir código a medida que el sistema crezca.
- **Organización por funcionalidad:** el backend tiene una carpeta por módulo (alumnos, planes, pagos, etc.), cada una con sus modelos, esquemas, servicios y rutas, en lugar de agrupar por tipo de archivo.
- **Despliegue independiente:** cada capa se aloja en un servicio distinto en la nube, lo que permite escalar o actualizar una sin afectar a las otras.

## Tecnologías 

| Capa | Tecnología |
|---|---|
| Frontend | React |
| Backend | Python + FastAPI (API REST) |
| Base de datos | PostgreSQL |
| Control de versiones | Git + GitHub |

## Comunicación entre capas

El frontend se comunica con el backend exclusivamente a través de una API REST. El backend es el único componente con acceso directo a la base de datos — el frontend nunca consulta PostgreSQL de forma directa, lo que mantiene la lógica de negocio y las validaciones centralizadas del lado del servidor.

## Seguridad

El detalle completo está en [`seguridad_y_permisos.md`](./seguridad_y_permisos.md). En resumen:

- **Acceso del alumno:** requiere DNI y código de acceso. El código lo genera el sistema, se guarda como hash y, tras 5 intentos fallidos seguidos, el acceso se bloquea 15 minutos. El Panel del Alumno es de solo lectura y no muestra la ficha de salud.
- **Acceso del personal:** requiere usuario y contraseña (guardada como hash). Cada usuario tiene un perfil (administrador o entrenador) y el backend valida los permisos en cada petición.
- **Datos personales y de salud:** el acceso se limita por perfil, la comunicación usa HTTPS y se toman como marco los principios de la Ley 25.326. No se almacenan datos de tarjetas.
- **Integridad:** las reglas críticas se controlan también en la base de datos (ver [`integridad_datos.md`](./integridad_datos.md)).

## Despliegue

El despliegue de la aplicación —previsto en Vercel (frontend), Render o Railway (backend) y Railway o Supabase (base de datos PostgreSQL)— se definirá de manera definitiva en etapas posteriores, dando cumplimiento al Requerimiento No Funcional RNF04 (Disponibilidad), el cual exige garantizar la accesibilidad continua del sistema mediante servicios de hosting en la nube, sin condicionar la arquitectura a un proveedor tecnológico específico en esta fase.

## Métricas operativas (propuestas)

- Cantidad de alumnos activos / por vencer / vencidos (en tiempo real, vía Dashboard).
- Tiempo de respuesta promedio de los endpoints principales (objetivo: < 2s).
- Tasa de errores de la API.
- Cantidad de sugerencias de IA generadas vs. aprobadas por semana.

## Lineamientos de despliegue

- Variables de entorno (credenciales de base de datos, puertos) gestionadas fuera del código fuente, mediante archivos .env no versionados.
- El backend se despliega como servicio independiente del frontend, permitiendo actualizar uno sin reconstruir el otro.
- La base de datos mantiene backups automáticos provistos por el servicio de hosting elegido.
- Toda la comunicación usa HTTPS, y el backend acepta solo el origen del frontend (CORS).
- Ver el diagrama de despliegue en [`diagrama_despliegue.md`](./diagrama_despliegue.md).

## Auditoría, contingencia y recuperación

El sistema registra las acciones sensibles en el log del backend y conserva el historial de operaciones sin borrado físico. Para continuar operando ante una caída se usa una planilla manual de contingencia, y para recuperar datos se usan copias de respaldo periódicas junto con `database/schema.sql`. El detalle está en [`contingencia_auditoria_recuperacion.md`](./contingencia_auditoria_recuperacion.md).