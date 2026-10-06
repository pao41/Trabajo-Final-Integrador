# Diagramas de Actividades — Sistema de Gestión para Gimnasios

## 1. Control de vencimiento de inscripción

```mermaid
flowchart TD
    Start([Inicio]) --> A[Alumno se inscribe en un plan]
    A --> B[Sistema calcula fecha de vencimiento]
    B --> C{Cuantos dias faltan?}