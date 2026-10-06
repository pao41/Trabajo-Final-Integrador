# Casos de Uso — Sistema de Gestión para Gimnasios

## Actores

- **Administrador/Staff** — personal del gimnasio, opera el Panel Administrador (RN15: sin distinción de roles).
- **Alumno** — consulta el Panel del Alumno.
- **Entrenador** — carga rutinas y aprueba sugerencias del Asistente de IA.

## Diagrama de Casos de Uso

```mermaid
flowchart LR
    subgraph Actores
        A[Administrador / Staff]
        AL[Alumno]
        E[Entrenador]
    end
    A --> UC1([Gestionar Alumnos])
    A --> UC2([Gestionar Planes e Inscripciones])
    A --> UC3([Registrar Pagos])
    A --> UC4([Registrar Asistencia])
    A --> UC5([Ver Dashboard])
    A --> UC6([Configurar Sistema])
    A --> UC7([Gestionar Entrenadores])
    AL --> UC8([Consultar Panel del Alumno])
    AL --> UC9([Solicitar Sugerencia de Rutina])
    E --> UC10([Cargar Rutinas])
    E --> UC11([Aprobar o Rechazar Rutinas Sugeridas])
```

## Listado de Casos de Uso

| ID | Nombre | Actor | RF relacionado |
|---|---|---|---|
| UC01 | Gestionar Alumnos | Administrador | RF01, RF02, RF09, RF15 |
| UC02 | Gestionar Planes e Inscripciones | Administrador | RF03, RF04, RF05 |
| UC03 | Registrar Pagos | Administrador | RF06, RF14 |
| UC04 | Registrar Asistencia | Administrador | RF07 |
| UC05 | Ver Dashboard | Administrador | RF08 |