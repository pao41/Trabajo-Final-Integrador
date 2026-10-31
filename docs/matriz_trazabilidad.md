# Matriz de Trazabilidad — Requerimientos, Reglas, Casos de Uso, Criterios y Pruebas

## 1. Requerimientos funcionales, reglas de negocio y módulos

| RF | Reglas de negocio relacionadas | Módulo |
|---|---|---|
| RF01 | RN13, RN14, RN37 | 1. Módulo de Alumnos |
| RF02 | RN26, RN39 | 1. Módulo de Alumnos |
| RF03 | RN29, RN36 | 2. Módulo de Planes e Inscripciones |
| RF04 | RN02, RN30 | 2. Módulo de Planes e Inscripciones |
| RF05 | RN01, RN09, RN31 | 2. Módulo de Planes e Inscripciones |
| RF06 | RN02, RN03, RN04, RN05, RN06, RN07, RN08, RN27, RN32 | 3. Módulo de Pagos |
| RF07 | RN10, RN11, RN12, RN30 | 4. Módulo de Asistencia |
| RF08 | RN36 | 5. Módulo de Dashboard Administrativo |
| RF09 | RN01 | 1. Módulo de Alumnos / 5. Módulo de Dashboard Administrativo |
| RF10 | RN16, RN17, RN38, RN39 | 6. Módulo de Panel del Alumno |
| RF11 | RN18, RN19, RN24, RN35 | 7. Módulo de Rutinas |
| RF12 | RN18, RN20, RN22 | 8. Módulo de Asistente de IA |
| RF13 | RN21, RN23, RN24 | 7. Módulo de Rutinas / 8. Módulo de Asistente de IA |
| RF14 | RN14, RN28 | 3. Módulo de Pagos |
| RF15 | RN16, RN37 | 1. Módulo de Alumnos |
| RF16 | RN09, RN36 | 9. Módulo de Configuración |
| RF17 | RN24, RN36 | 10. Módulo de Gestión de Entrenadores |
| RF18 | RN24, RN28, RN35 | 10. Módulo de Gestión de Entrenadores |
| RF19 | RN25 | 1. Módulo de Alumnos / 6. Módulo de Panel del Alumno |
| RF20 | RN29, RN30, RN31, RN32 | 4. Módulo de Asistencia / 2. Módulo de Planes e Inscripciones |
| RF21 | RN33, RN38 | 11. Módulo de Usuarios y Seguridad |
| RF22 | RN15, RN34, RN36 | 11. Módulo de Usuarios y Seguridad |
| RF23 | RN33, RN34, RN35, RN36 | 11. Módulo de Usuarios y Seguridad |

## 2. Cadena completa: requerimiento → caso de uso → criterio de aceptación → caso de prueba

Cada requerimiento se rastrea hasta su verificación: el caso de uso está en `casos_de_uso.md`, el criterio en `criterios_aceptacion.md` (el criterio de RF01 se llama CA-RF01, y así con los demás) y los casos de prueba en `casos_prueba.md`.

| RF | Caso de uso | Criterio de aceptación | Casos de prueba |
|---|---|---|---|
| RF01 | UC01 | CA-RF01 | CP01, CP02 |
| RF02 | UC01 | CA-RF02 | CP13 |
| RF03 | UC02 | CA-RF03 | CP14 |
| RF04 | UC02 | CA-RF04 | CP03 |
| RF05 | UC02 | CA-RF05 | CP11 |
| RF06 | UC03 | CA-RF06 | CP03, CP04, CP23, CP31 |
| RF07 | UC04 | CA-RF07 | CP06, CP21 |
| RF08 | UC05 | CA-RF08 | CP05 |
| RF09 | UC01 | CA-RF09 | CP15 |
| RF10 | UC08 | CA-RF10 | CP16, CP17, CP18 |
| RF11 | UC10 | CA-RF11 | CP19 |
| RF12 | UC09 | CA-RF12 | CP07 |
| RF13 | UC11 | CA-RF13 | CP08, CP32 |
| RF14 | UC03 | CA-RF14 | CP09, CP30 |
| RF15 | UC01 | CA-RF15 | CP10 |
| RF16 | UC06 | CA-RF16 | CP11 |
| RF17 | UC07 | CA-RF17 | CP12 |
| RF18 | UC10, UC11 | CA-RF18 | CP12, CP32 |
| RF19 | UC01, UC08 | CA-RF19 | CP20 |
| RF20 | UC04 | CA-RF20 | CP21, CP22, CP23, CP24 |
| RF21 | UC13 | CA-RF21 | CP25 |
| RF22 | UC13 | CA-RF22 | CP26, CP27 |
| RF23 | UC12 | CA-RF23 | CP28, CP29 |

## 3. Requerimientos No Funcionales — relación con el diseño

| RNF | Dónde se refleja |
|---|---|
| RNF01 (Usabilidad) | Diseño de interfaz simple en Frontend (arquitectura.md) |
| RNF02 (Rendimiento) | Índices definidos en schema.sql (idx_inscripciones_alumno, idx_pagos_inscripcion, idx_asistencias_alumno_fecha, idx_asistencias_inscripcion) |
| RNF03 (Portabilidad) | Frontend React responsive, sin instalación |
| RNF04 (Disponibilidad) | Despliegue en servicios cloud (ver arquitectura.md) |
| RNF05 (Mantenibilidad) | Arquitectura en capas (arquitectura.md) |
| RNF06 (Escalabilidad) | Modelo relacional normalizado en schema.sql |
| RNF07 (Seguridad de acceso) | RN16, RN33, RN37, RN38 — ver seguridad_y_permisos.md |
| RNF08 (Consistencia de datos) | Claves foráneas y restricciones CHECK en schema.sql — ver integridad_datos.md |
| RNF09 (Protección de datos personales y de salud) | RN34, RN39 — ver seguridad_y_permisos.md |
| RNF10 (Auditoría) | RN28, RN40 — ver contingencia_auditoria_recuperacion.md |
| RNF11 (Recuperación) | RN42 — ver contingencia_auditoria_recuperacion.md |
| RNF12 (Continuidad operativa) | RN41 — ver contingencia_auditoria_recuperacion.md |