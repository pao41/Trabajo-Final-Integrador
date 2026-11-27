# Despliegue

## 1. Objetivo y arquitectura

Este documento describe el procedimiento para publicar el Sistema de Gestión para Gimnasios en internet. El despliegue se compone de tres servicios independientes, todos con plan gratuito:

| Servicio | Componente | Función |
|---|---|---|
| Supabase | Base de datos | Aloja la base de datos PostgreSQL. |
| Render | Backend | Ejecuta la API desarrollada con FastAPI. |
| Vercel | Frontend | Publica la aplicación web desarrollada con React. |

El orden de publicación es el de este documento, dado que cada paso requiere un dato obtenido en el anterior.

## 2. Requisitos previos

* Repositorio del proyecto alojado en GitHub, con acceso habilitado para los tres servicios.
* Cuenta en cada uno de los servicios: Supabase, Render y Vercel.
* Clave de la API de Gemini obtenida en Google AI Studio (opcional). Sin ella el sistema funciona con normalidad, pero el asistente no redacta la explicación de las sugerencias.
* Computadora con el proyecto instalado según el README, necesaria para crear el primer administrador.

## 3. Base de datos (Supabase)

1. Crear un proyecto nuevo y registrar la contraseña de la base de datos definida durante su creación.
2. Abrir el editor SQL (SQL Editor) y ejecutar el contenido completo del archivo `database/schema.sql`, que crea las tablas del sistema.
3. En la opción Connect, copiar la cadena de conexión del Session pooler y reemplazar `[YOUR-PASSWORD]` por la contraseña registrada. El texto resultante es el valor de la variable `DATABASE_URL`.

Se utiliza el Session pooler porque la conexión directa de Supabase emplea únicamente IPv6, mientras que Render requiere IPv4.

## 4. Backend (Render)

Se crea un Web Service conectado al repositorio, con la siguiente configuración:

| Parámetro | Valor |
|---|---|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Se definen las siguientes variables de entorno:

| Variable | Valor |
|---|---|
| `PYTHON_VERSION` | `3.13.5` |
| `DATABASE_URL` | Cadena de conexión de Supabase obtenida en la sección 3. |
| `SECRET_KEY` | Clave de firma de las sesiones, de 32 caracteres o más. Puede generarse con `python -c "import secrets; print(secrets.token_urlsafe(48))"`. |
| `COOKIE_SECURE` | `true`. La cookie de sesión se transmite solo por HTTPS. |
| `FRONTEND_ORIGIN` | URL del frontend en Vercel, disponible al finalizar la sección 5. |
| `GEMINI_API_KEY` | Clave de Google AI Studio (opcional). |
| `GEMINI_MODEL` | `gemini-3.5-flash` |