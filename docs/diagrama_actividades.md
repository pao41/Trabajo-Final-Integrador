# Diagramas de Actividades — Sistema de Gestión para Gimnasios

## 1. Control de vencimiento de inscripción

```mermaid
flowchart TD
    Start([Inicio]) --> A[Alumno se inscribe en un plan]
    A --> B[Sistema calcula fecha de vencimiento]
    B --> C{Cuantos dias faltan?}
    C -->|Mas de 7 dias| D[Estado: activo]
    C -->|7 dias o menos| E[Estado: por_vencer]
    C -->|Fecha ya paso| F[Estado: vencido]
    D --> G[Alumno puede ingresar al gimnasio]
    E --> G
    F --> H[Acceso restringido hasta renovar pago]
    H --> I[Alumno realiza un pago]
    I --> B
    G --> End([Fin])
```