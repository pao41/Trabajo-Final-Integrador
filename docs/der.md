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
