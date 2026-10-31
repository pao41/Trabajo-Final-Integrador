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
    Backend->>DB: Actualizar fecha_vencimiento y saldo de clases (RN02, RN03, RN04, RN32)
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
## 3. Check-in de asistencia con descuento de clases (RF07, RF20, RN12, RN30, RN32)

```mermaid
sequenceDiagram
    actor Staff
    participant Frontend
    participant Backend
    participant DB as Base de Datos

    Staff->>Frontend: Busca alumno y registra ingreso
    Frontend->>Backend: POST /asistencias
    Backend->>DB: Consultar ultimo check-in e inscripcion vigente
    DB-->>Backend: Ultima asistencia e inscripcion
    alt Dentro de la ventana de 2 horas (RN12)
        Backend-->>Frontend: Rechazado - check-in duplicado
    else Inscripcion vencida o plan por clases con saldo 0 (RN32)
        Backend-->>Frontend: Rechazado - corresponde renovar
    else Ingreso valido
        Backend->>DB: Iniciar transaccion
        Backend->>DB: Insertar asistencia con inscripcion_id
        Backend->>DB: Descontar 1 clase si el plan es por clases (RN30)
        DB-->>Backend: Confirmar transaccion
        Backend-->>Frontend: Check-in registrado con clases restantes
    end
    Frontend-->>Staff: Resultado del ingreso
```
## 4. Acceso del alumno con DNI y código (RF10, RN16, RN17, RN38)

```mermaid
sequenceDiagram
    actor Alumno
    participant Frontend
    participant Backend
    participant DB as Base de Datos

    Alumno->>Frontend: Ingresa DNI y codigo de acceso
    Frontend->>Backend: POST /alumnos/acceso por HTTPS
    Backend->>Backend: Verificar si el acceso esta bloqueado (RN38)
    alt Acceso bloqueado
        Backend-->>Frontend: Rechazado - intente mas tarde
    else Acceso no bloqueado
        Backend->>DB: Buscar alumno por DNI
        DB-->>Backend: Alumno y hash del codigo
        Backend->>Backend: Comparar el codigo ingresado con el hash
        alt Datos correctos
            Backend-->>Frontend: Token de sesion temporal
            Frontend->>Backend: GET /alumnos/panel con token
            Backend->>DB: Consultar solo datos del propio alumno (RN17)
            DB-->>Backend: Cuota, asistencias y rutinas aprobadas
            Backend-->>Frontend: Datos del panel sin ficha de salud (RN39)
        else Datos incorrectos
            Backend->>Backend: Registrar intento fallido (RN38)
            Backend-->>Frontend: Rechazado - datos incorrectos
        end
    end
```
## 5. Inicio de sesión del personal y control por perfil (RF21, RF22, RN33, RN34)

```mermaid
sequenceDiagram
    actor Staff
    participant Frontend
    participant Backend
    participant DB as Base de Datos

    Staff->>Frontend: Ingresa usuario y contrasena
    Frontend->>Backend: POST /login por HTTPS
    Backend->>DB: Buscar usuario activo
    DB-->>Backend: Usuario, perfil y hash de la contrasena
    Backend->>Backend: Comparar la contrasena con el hash (RN33)
    alt Credenciales correctas
        Backend-->>Frontend: Token de sesion temporal con el perfil
        Staff->>Frontend: Ejecuta una funcion
        Frontend->>Backend: Peticion con token
        Backend->>Backend: Verificar que el perfil tenga habilitada la funcion (RN34, RN36)
        alt Perfil habilitado
            Backend->>DB: Ejecutar la operacion
            DB-->>Backend: OK
            Backend-->>Frontend: Resultado
        else Perfil no habilitado
            Backend-->>Frontend: Rechazado - acceso denegado
        end
    else Credenciales incorrectas
        Backend-->>Frontend: Rechazado - datos incorrectos (RN38)
    end
```
