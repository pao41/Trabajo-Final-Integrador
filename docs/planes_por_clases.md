# Gestión de Planes por Cantidad de Clases — Sistema de Gestión para Gimnasios

Este documento completa la definición de los planes de tipo `clases` (RF03, RF20), indicando cómo se gestionan, cómo se descuentan las clases usadas, qué ocurre cuando se agotan y cómo se controla su vigencia.

## Tipos de plan

| Aspecto | Plan por tiempo (`tiempo`) | Plan por clases (`clases`) |
|---|---|---|
| Ejemplo | Mensual libre | Pack de 10 clases |
| Datos del plan | `duracion_dias`, `precio` | `duracion_dias` (vigencia), `precio`, `cantidad_clases` |
| Saldo en la inscripción | No aplica (`clases_restantes` es NULL) | `clases_restantes` (se inicializa con `cantidad_clases`) |
| Qué consume el ingreso | Nada: el alumno entra mientras esté vigente | Una (1) clase por cada ingreso registrado |
| Cuándo pasa a `vencido` | Al vencer la fecha | Al vencer la fecha **o** al llegar el saldo a cero, lo que ocurra primero |
