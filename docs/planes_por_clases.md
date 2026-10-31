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

## Datos involucrados

| Tabla | Columna | Función |
|---|---|---|
| `planes` | `cantidad_clases` | Clases que incluye el plan (solo para tipo `clases`) |
| `planes` | `duracion_dias` | Vigencia máxima del plan, también para los de clases |
| `inscripciones` | `clases_restantes` | Saldo actual de clases del alumno |
| `inscripciones` | `fecha_vencimiento` | Fin de la vigencia (RN02) |
| `asistencias` | `inscripcion_id` | Inscripción contra la que se registró el ingreso, para poder reconstruir el consumo |

## Reglas aplicadas

- **RN29:** un plan por clases define `cantidad_clases` y vigencia; uno por tiempo no define cantidad de clases.
- **RN30:** al inscribir, el saldo arranca en `cantidad_clases`; cada ingreso descuenta una clase, en la misma operación que registra la asistencia.
- **RN31:** la inscripción pasa a `vencido` cuando el saldo llega a cero o vence la vigencia. Las clases no usadas al vencer la vigencia se pierden.
- **RN32:** con saldo cero no se registra el ingreso y se avisa al personal que corresponde renovar. Al renovar con un nuevo pago se aplica RN03 (si la vigencia todavía no venció) o RN04 (si ya venció), tomando como criterio la **fecha de vencimiento** y no el estado.
