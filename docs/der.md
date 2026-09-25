# Diagrama Entidad-Relación — Sistema de Gestión para Gimnasios

Diagrama construido con sintaxis Mermaid.

```mermaid
erDiagram
    ALUMNOS ||--o| FICHA_SALUD : tiene
    ALUMNOS ||--|{ INSCRIPCIONES : posee
    PLANES ||--|{ INSCRIPCIONES : define
    INSCRIPCIONES ||--|{ PAGOS : genera
    ALUMNOS ||--|{ ASISTENCIAS : registra
    ALUMNOS ||--|{ RUTINAS_ASIGNADAS : recibe
    RUTINAS ||--|{ RUTINAS_ASIGNADAS : sugiere

    ALUMNOS {
        int id PK
        string nombre
        string dni
        string contacto
        string codigo_acceso
        boolean activo
        date fecha_alta
    }
    FICHA_SALUD {
        int id PK
        int alumno_id FK
        boolean problemas_cardiacos
        string lesiones
        string observaciones
        date fecha_registro
    }
    PLANES {
        int id PK
        string nombre
        int duracion_dias
        decimal precio
        string tipo
    }
    INSCRIPCIONES {
        int id PK
        int alumno_id FK
        int plan_id FK
        date fecha_inicio
        date fecha_vencimiento
        string estado
    }
    PAGOS {
        int id PK
        int inscripcion_id FK
        date fecha_pago
        decimal monto
        string metodo_pago
    }
    ASISTENCIAS {
        int id PK
        int alumno_id FK
        date fecha
        time hora
    }
    RUTINAS {
        int id PK
        string nombre
        string tipo
        string contraindicaciones
        string descripcion
    }
    RUTINAS_ASIGNADAS {
        int id PK
        int alumno_id FK
        int rutina_id FK
        string estado
        int entrenador_id
        date fecha_validacion
    }
    CONFIGURACION {
        int id PK
        string nombre_gimnasio
        int dias_aviso_vencimiento
        string metodos_pago_habilitados
    }
```

## Entidades y relaciones

- **alumnos** — entidad central del sistema. Un alumno tiene una ficha_salud, puede tener varias inscripciones a lo largo del tiempo, varios registros de asistencias, y varias rutinas_asignadas.
- **ficha_salud** — relación 1 a 1 con alumnos. Guarda los datos de salud declarados, usados para filtrar rutinas seguras.
- **planes** — catálogo de planes disponibles (mensual, trimestral, por clases, etc.), independiente de los alumnos.
- **inscripciones** — relaciona un alumno con un plan en un período determinado, con su fecha de vencimiento y estado.
- **pagos** — cada pago pertenece a una inscripción; un alumno puede tener muchos pagos a lo largo del tiempo (historial completo, ver RF14).
- **asistencias** — un registro por cada check-in de un alumno.
- **rutinas** — banco de rutinas predefinidas, cargadas por el entrenador, con sus contraindicaciones.
- **rutinas_asignadas** — relaciona una rutina con un alumno, con su estado de aprobación (pendiente / aprobada / rechazada).
- **configuracion** — tabla de parámetros generales del sistema, sin relación directa con las demás entidades.

## Cardinalidades principales

| Relación | Cardinalidad |
|---|---|
| alumnos → ficha_salud | 1 a 1 |
| alumnos → inscripciones | 1 a muchos |
| planes → inscripciones | 1 a muchos |
| inscripciones → pagos | 1 a muchos |
| alumnos → asistencias | 1 a muchos |
| alumnos → rutinas_asignadas | 1 a muchos |
| rutinas → rutinas_asignadas | 1 a muchos |
