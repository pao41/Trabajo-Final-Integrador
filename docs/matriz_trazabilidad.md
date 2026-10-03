# Matriz de Trazabilidad RF — RN — Módulo

| RF | Reglas de negocio relacionadas | Módulo |
|---|---|---|
| RF01 | RN13, RN14 | 1. Módulo de Alumnos |
| RF02 | RN26 | 1. Módulo de Alumnos |
| RF03 | — | 2. Módulo de Planes e Inscripciones |
| RF04 | RN02 | 2. Módulo de Planes e Inscripciones |
| RF05 | RN01, RN09 | 2. Módulo de Planes e Inscripciones |
| RF06 | RN02, RN03, RN04, RN05, RN06, RN07, RN08, RN27 | 3. Módulo de Pagos |
| RF07 | RN10, RN11, RN12 | 4. Módulo de Asistencia |
| RF08 | — | 5. Módulo de Dashboard Administrativo |
| RF09 | RN01 | 1. Módulo de Alumnos / 5. Módulo de Dashboard Administrativo |
| RF10 | RN16, RN17, RN25 | 6. Módulo de Panel del Alumno |
| RF11 | RN18, RN19, RN24 | 7. Módulo de Rutinas |
| RF12 | RN18, RN20, RN22 | 8. Módulo de Asistente de IA |
| RF13 | RN21, RN23, RN24 | 7. Módulo de Rutinas / 8. Módulo de Asistente de IA |
| RF14 | RN14, RN28 | 3. Módulo de Pagos |
| RF15 | RN16 | 1. Módulo de Alumnos |
| RF16 | RN09 | 9. Módulo de Configuración |
| RF17 | RN24 | 10. Módulo de Gestión de Entrenadores |
| RF18 | RN24, RN28 | 10. Módulo de Gestión de Entrenadores |
| RF19 | RN25 | 1. Módulo de Alumnos / 6. Módulo de Panel del Alumno |

## Requerimientos No Funcionales — relación con el diseño

| RNF | Dónde se refleja |
|---|---|
| RNF01 (Usabilidad) | Diseño de interfaz simple en Frontend (arquitectura.md) |
| RNF02 (Rendimiento) | Índices definidos en schema.sql (idx_inscripciones_alumno, idx_pagos_inscripcion, idx_asistencias_alumno_fecha) |
| RNF03 (Portabilidad) | Frontend React responsive, sin instalación |
| RNF04 (Disponibilidad) | Despliegue en servicios cloud (ver arquitectura.md) |
| RNF05 (Mantenibilidad) | Arquitectura en capas (arquitectura.md) |
| RNF06 (Escalabilidad) | Modelo relacional normalizado en schema.sql |
| RNF07 (Seguridad de acceso) | RN16, acceso por código sin contraseña |
| RNF08 (Consistencia de datos) | Claves foráneas y restricciones CHECK en schema.sql |