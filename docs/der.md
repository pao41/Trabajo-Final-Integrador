**Diagrama Entidad-Relación — Sistema de Gestión para Gimnasios**

Diagrama construido con sintaxis Mermaid.

```mermaid
erDiagram
    ALUMNOS --o| FICHA_SALUD : tiene
    ALUMNOS --|{ INSCRIPCIONES : posee
    PLANES --|{ INSCRIPCIONES : define
    INSCRIPCIONES --|{ PAGOS : genera
    ALUMNOS --|{ ASISTENCIAS : registra
    ALUMNOS --|{ RUTINAS_ASIGNADAS : recibe
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