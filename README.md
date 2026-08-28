# Trabajo Final Integrador — Tecnicatura Universitaria en Programación

## Sistema de Gestión para Gimnasios

**Integrantes:**
* Arjona, Martin
* Arjona, Paola

**Grupo:** 105
**Tutor:** Herrera, Gerardo Adrian
---

### Descripción del proyecto

El **Sistema de Gestión para Gimnasios** es una plataforma web integral concebida para profesionalizar, optimizar y automatizar las operaciones diarias en establecimientos deportivos de escala pequeña y mediana. El proyecto nace para solucionar la brecha digital existente en centros de entrenamiento que aún dependen de métodos analógicos o herramientas desvinculadas entre sí.

El ecosistema centraliza tres pilares fundamentales de la gestión operativa y comercial:

1. **Gestión Administrativa y Financiera:** Permite el control de alumnos, vencimientos de membresías y registro de cobranzas. Cuenta con un dashboard analítico con indicadores en tiempo real que visibiliza la facturación mensual y el desglose según el método de pago utilizado.
2. **Seguimiento Operativo y de Asistencia:** Incluye un panel interactivo con un módulo tipo *checklist* diario que agiliza el control de acceso de los socios, permitiendo detectar de forma inmediata a usuarios con cuotas vencidas o por vencer.
3. **Módulo Técnico Deportivo e Inteligencia Artificial:** Incorpora una sección para la consulta de rutinas físicas personalizadas y un asistente basado en Inteligencia Artificial. Este módulo actúa como una guía de apoyo para la generación de rutinas básicas de calentamiento, movilidad articular y vuelta a la calma, diseñado estrictamente como una herramienta complementaria para el alumno que no sustituye el criterio, la supervisión ni la labor del entrenador presencial.

En conjunto, la solución combina una interfaz ágil en el frontend con una arquitectura de servicios robusta en el backend, garantizando la trazabilidad de la información, la fidelización de los socios y la toma de decisiones basada en datos para los administradores.

---

### Problemática

Los gimnasios chicos y medianos suelen gestionar sus operaciones principales (socios, cobros y asistencia) mediante planillas de papel, libros contables físicos u hojas de cálculo desvinculadas. Esta falta de centralización operativa genera:
* **Falta de visibilidad financiera:** Dificultad para conocer la facturación real del mes, métodos de pago más utilizados y proyecciones de ingresos.
* **Morosidad no detectada:** Socios con cuotas vencidas que continúan ingresando a las instalaciones por falta de un control automático en la recepción.
* **Ineficiencia en la planificación:** Ausencia de registros sobre días y horarios de mayor concurrencia para la organización de clases o turnos de entrenadores.
* **Seguimiento informal del entrenamiento:** Ausencia de un espacio digital centralizado para la consulta de rutinas de ejercicios y la guía física inicial del alumno.

---

### Solución propuesta

Un sistema web centralizado que conecta la administración del gimnasio con el seguimiento continuo de los alumnos, generando automáticamente:
* Reportes de facturación total detallados por método de pago.
* Monitoreo en tiempo real del estado de cada alumno (*activo / por vencer / vencido*).
* Checklist diario de asistencia y registro histórico de concurrencia.
* Panel interactivo de alumnos con gestión y visualización de rutinas.
* Módulo de Inteligencia Artificial para la asistencia en ejercicios básicos de entrada en calor y movilidad.

---

### Alcance (MVP)

#### Funcionalidades del MVP:
* **Panel de Alumnos:** Vista centralizada para la administración de perfiles, datos de contacto e historial de estados (*activo / por vencer / vencido*).
* **Catálogo de planes e inscripciones:** Configuración de ofertas de membresías y cálculo automático de vencimientos.
* **Registro de pagos:** Alta de cobranzas con especificación del método de pago (efectivo, transferencia, tarjeta).
* **Checklist de asistencia:** Módulo rápido de registro manual para la marcación diaria de presencia de los alumnos.
* **Opciones de Rutinas:** Sección orientada a la visualización, selección y consulta de rutinas de entrenamiento físico.
* **Asistente de IA:** Generación guiada de ejercicios básicos de calentamiento, movilidad articular y estiramiento (orientado a acompañar al alumno sin reemplazar la labor del entrenador).
* **Dashboard administrativo:** Métricas visuales de facturación total, ingresos por canal de cobro y distribución de alumnos según estado de cuota.

#### Nice to have (Futuras mejoras):
* Notificaciones automáticas por email sobre vencimientos de cuota.
* Check-in de asistencia por código QR.
* Gráficos analíticos de horas pico y distribución semestral de concurrencia.
* Módulo de envío masivo de avisos, eventos y promociones.

#### Fuera de alcance:
* Notificaciones directas mediante integración con WhatsApp.
* Integración con pasarelas de pago online.
* Aplicación móvil nativa (iOS / Android).
* Gestión automatizada de devoluciones y reembolsos.
* Control de acceso físico mediante hardware biométrico.

---

### Tecnologías utilizadas

* **Frontend:** React
* **Backend:** Node.js + Express
* **Base de datos:** PostgreSQL
* **Control de versiones:** Git + GitHub
