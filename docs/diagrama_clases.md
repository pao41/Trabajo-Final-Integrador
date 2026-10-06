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