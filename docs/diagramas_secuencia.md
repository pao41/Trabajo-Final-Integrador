# Diagramas de Secuencia — Sistema de Gestión para Gimnasios

## 1. Registrar pago y renovar inscripción (RF06)

```mermaid
sequenceDiagram
    actor Staff
    participant Frontend
    participant Backend
    participant DB as Base de Datos

    Staff->>Frontend: Ingresa pago (alumno, monto, metodo)
    Frontend->>Backend: POST /pagos
    Backend->>DB: Verificar inscripcion existente
    DB-->>Backend: Inscripcion encontrada
    Backend->>DB: Insertar pago
    Backend->>DB: Actualizar fecha_vencimiento (RN02, RN03, RN04)
    DB-->>Backend: OK
    Backend-->>Frontend: Pago registrado, nuevo estado
    Frontend-->>Staff: Confirmacion
```

## 2. Alumno solicita sugerencia de rutina y entrenador la aprueba (RF12, RF13)

```mermaid
sequenceDiagram
    actor Alumno
    participant Frontend
    participant Backend
    participant DB as Base de Datos
    actor Entrenador

    Alumno->>Frontend: Solicita sugerencia de rutina
    Frontend->>Backend: GET /rutinas/sugerencia
    Backend->>DB: Consultar ficha_salud del alumno
    DB-->>Backend: Ficha de salud
    Backend->>DB: Filtrar rutinas compatibles (RN18, RN20)
    DB-->>Backend: Rutina candidata
    Backend->>DB: Crear rutina_asignada (estado=pendiente)
    DB-->>Backend: OK
    Backend-->>Frontend: Sugerencia pendiente de aprobacion
    Entrenador->>Frontend: Revisa sugerencias pendientes
    Entrenador->>Backend: PATCH /rutinas-asignadas/id (aprobar)
    Backend->>DB: Actualizar estado=aprobada, entrenador_id, fecha_validacion
    DB-->>Backend: OK
    Backend-->>Frontend: Rutina aprobada visible para el alumno
```
## 3. Check-in de asistencia con validación de duplicado (RF07, RN12)

```mermaid
sequenceDiagram
    actor Staff
    participant Frontend
    participant Backend
    participant DB as Base de Datos

    Staff->>Frontend: Busca alumno y registra ingreso
    Frontend->>Backend: POST /asistencias
    Backend->>DB: Verificar ultimo check-in del alumno
    DB-->>Backend: Ultima asistencia (hora)
    alt Dentro de ventana de 2 horas
        Backend-->>Frontend: Rechazado - check-in duplicado
    else Fuera de la ventana
        Backend->>DB: Insertar asistencia
        DB-->>Backend: OK
        Backend-->>Frontend: Check-in registrado
    end
```