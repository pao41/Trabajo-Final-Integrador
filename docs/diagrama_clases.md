# Diagrama de Clases — Sistema de Gestión para Gimnasios

```mermaid
classDiagram
    class Alumno {
        +int id
        +string nombre
        +string dni
        +string contacto
        +string codigoAcceso
        +boolean activo
        +date fechaAlta
    }
    class FichaSalud {
        +int id
        +boolean problemasCardiacos
        +string lesiones
        +string observaciones
        +date fechaRegistro
    }
    class Plan {
        +int id
        +string nombre
        +int duracionDias
        +decimal precio
        +string tipo
    }
    class Inscripcion {
        +int id
        +date fechaInicio
        +date fechaVencimiento
        +string estado
    }
    class Pago {
        +int id
        +date fechaPago
        +decimal monto
        +string metodoPago
    }
    class Asistencia {
        +int id
        +date fecha
        +time hora
    }
    class Entrenador {
        +int id
        +string nombre
        +string contacto
        +date fechaAlta
    }
    class Rutina {
        +int id
        +string nombre
        +string tipo
        +string contraindicaciones
        +string descripcion
    }
    class RutinaAsignada {
        +int id
        +string estado
        +date fechaValidacion
    }
    class Configuracion {
        +int id
        +string nombreGimnasio
        +int diasAvisoVencimiento
        +string[] metodosPagoHabilitados
    }
     class MetaAlumno {
        +int id
        +int metaAsistenciasSemanales
        +date fechaActualizacion
    }

    Alumno "1" --> "1" FichaSalud
    Alumno "1" --> "1" MetaAlumno
    Alumno "1" --> "*" Inscripcion
    Plan "1" --> "*" Inscripcion
    Inscripcion "1" --> "*" Pago
    Alumno "1" --> "*" Asistencia
    Alumno "1" --> "*" RutinaAsignada
    Rutina "1" --> "*" RutinaAsignada
    Entrenador "1" --> "*" Rutina
    Entrenador "1" --> "*" RutinaAsignada
```

Este diagrama es la representación orientada a objetos del modelo relacional definido en [`/database/schema.sql`](../database/schema.sql) — cada clase corresponde a una tabla, y cada atributo a una columna. `Configuracion` no participa de ninguna relación, por ser una entidad de parámetros globales del sistema.