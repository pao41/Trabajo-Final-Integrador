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
## 2. Aprobación de rutina sugerida por el Asistente de IA

```mermaid
flowchart TD
    Start([Inicio]) --> A[Alumno solicita sugerencia de rutina]
    A --> B[Sistema filtra banco de rutinas segun ficha de salud]
    B --> C{Existe rutina compatible?}
    C -->|No| D[Sistema informa que no hay sugerencias disponibles]
    C -->|Si| E[Se crea rutina_asignada en estado pendiente]