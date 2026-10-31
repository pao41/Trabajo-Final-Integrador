# Seguridad y Permisos — Sistema de Gestión para Gimnasios

Este documento detalla cómo se protege el acceso al sistema (Panel del Alumno y Panel Administrador), qué perfiles existen y qué puede hacer cada uno. Complementa la sección de Seguridad de [`arquitectura.md`](./arquitectura.md).

## 1. Datos a proteger

| Tipo de dato | Dónde se guarda | Nivel de protección |
|---|---|---|
| Datos personales (nombre, DNI, contacto) | `alumnos` | Acceso solo para personal autenticado |
| Datos de salud declarados | `ficha_salud` | Datos sensibles: acceso restringido por perfil (RN39), nunca visibles en el Panel del Alumno |
| Credenciales de alumnos y personal | `alumnos.codigo_acceso_hash`, `usuarios.password_hash` | Se guardan solo como hash, nunca en texto plano (RN33, RN37) |
| Datos de pago | `pagos` | Solo el método como categoría; no se guardan datos de tarjetas (RN27) |

## 2. Acceso del alumno (Panel del Alumno)

El acceso por DNI solo no es seguro, porque el DNI no es un dato secreto. Por eso el alumno debe ingresar **DNI y código de acceso** (RN16).

| Mecanismo | Qué evita | Regla |
|---|---|---|
| Se exigen DNI **y** código de acceso | Que alguien entre conociendo solo el DNI de otra persona | RN16 |
| El código lo genera el sistema de forma aleatoria (8 caracteres alfanuméricos) y no se deriva del DNI | Códigos fáciles de adivinar | RN37 |
| El código se guarda como hash y se muestra al personal una sola vez, al generarlo o regenerarlo | Que alguien con acceso a la base lea los códigos | RN37 |
| Después de 5 intentos fallidos seguidos se bloquea el acceso durante 15 minutos | Ataques de prueba y error | RN38 |
| El mensaje de error es genérico ("datos incorrectos"), sin indicar si falló el DNI o el código | Descubrir qué DNI están registrados | RN38 |
| Panel de solo lectura que muestra únicamente datos del propio alumno | Que un alumno vea o modifique datos de otros | RN17 |
| La ficha de salud no se muestra en el Panel del Alumno | Exposición de datos sensibles | RN39 |
| Al regenerar el código, el anterior deja de ser válido | Uso de un código perdido o robado | RF15, RN37 |
| La sesión es temporal (token con vencimiento) y todo viaja por HTTPS | Sesiones abiertas indefinidamente e interceptación | RNF09 |