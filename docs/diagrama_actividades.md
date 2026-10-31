# Diagramas de Actividades — Sistema de Gestión para Gimnasios

## 1. Control de vencimiento de inscripción

```mermaid
flowchart TD
    Start([Inicio]) --> A[Alumno se inscribe en un plan]
    A --> B[Sistema calcula la fecha de vencimiento e inicializa el saldo si el plan es por clases]
    B --> C{Vigencia vencida o saldo de clases agotado?}
    C -->|Si| F[Estado: vencido]
    C -->|No| C2{Faltan menos dias que el aviso configurado? RN09}
    C2 -->|Si| E[Estado: por_vencer]
    C2 -->|No| D[Estado: activo]
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
    E --> F[Entrenador revisa la sugerencia]
    F --> G{Aprueba?}
    G -->|Si| H[Estado: aprobada - visible para el alumno]
    G -->|No| I[Estado: rechazada - no visible]
    D --> End([Fin])
    H --> End
    I --> End
```

## 3. Registro de ingreso con plan por clases

```mermaid
flowchart TD
    Start([Inicio]) --> A[Personal busca al alumno y registra el ingreso]
    A --> B{Hay un ingreso en las ultimas 2 horas? RN12}
    B -->|Si| C[Se rechaza: check-in duplicado]
    B -->|No| D{Inscripcion vigente?}
    D -->|No| E[Se rechaza: corresponde renovar]
    D -->|Si| F{Plan por clases?}
    F -->|No| G[Se registra la asistencia]
    F -->|Si| H{Saldo mayor a 0?}
    H -->|No| E
    H -->|Si| I[Se registra la asistencia y se descuenta una clase en una sola operacion]
    G --> End([Fin])
    I --> End
    C --> End
    E --> End
```