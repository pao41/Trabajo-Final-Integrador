Sistema de Gestión para Gimnasios

Trabajo Final Integrador — Tecnicatura Universitaria en Programación 

Integrantes: 

## Descripción del proyecto

Plataforma de gestión para gimnasios chicos (boxes, estudios funcionales, gimnasios de barrio) que centraliza el registro de alumnos, planes y pagos, el control de asistencia diaria, y brinda un dashboard con indicadores de facturación y ocupación.

## Problemática

Los gimnasios chicos gestionan alumnos, pagos y asistencia en planillas de papel, Excel suelto o de memoria del encargado, sin sistema centralizado. Esto genera:

Falta de visibilidad sobre la facturación real del mes.
Alumnos con cuota vencida que no son detectados a tiempo.
Ausencia de datos sobre días/horarios de mayor concurrencia para planificar mejor.
Solución propuesta

Un sistema web que centraliza alumnos, planes, inscripciones, pagos y asistencia, generando automáticamente:

Facturación total y por método de pago.
Estado de cada alumno (activo / por vencer / vencido).
Registro histórico de asistencia diaria.

## Alcance (MVP)
Categoría	Funcionalidades
MVP	Registro de alumnos · Catálogo de planes · Inscripciones con estado (activo / por vencer / vencido) · Registro de pagos con método de pago · Check-in manual de asistencia · Dashboard de facturación total y por método · Listado de alumnos por estado

Nice to have	Notificaciones automáticas por email de vencimiento · Check-in por código QR · Gráfico de horas pico / días de mayor asistencia · Envío masivo de avisos y promociones

Fuera de alcance	Notificaciones por WhatsApp · Cobro integrado con pasarela de pago · App móvil nativa · Pagos parciales / prorrateo · Reembolsos · Biometría · Permisos diferenciados por rol

## Tecnologías utilizadas
Frontend	React
Backend	Node.js + Express
Base de datos	PostgreSQL
Despliegue 
Control de versiones	Git + GitHub

