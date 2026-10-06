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