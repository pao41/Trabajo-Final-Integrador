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

### Primer administrador

La base de datos nueva no contiene usuarios y el sistema no ofrece registro público, por lo que el primer administrador se crea desde una computadora conectada a la base de producción. En PowerShell, dentro de la carpeta `backend` y con el entorno virtual activo:

```powershell
$env:DATABASE_URL="cadena-de-supabase"
python -m app.db.seed
```

El comando solicita el nombre de usuario y la contraseña del administrador.

### Datos de demostración (opcional)

El archivo `database/datos_demo.sql` carga alumnos, planes y rutinas de ejemplo y se ejecuta desde el editor SQL de Supabase. Incluye un usuario y un código de acceso conocidos, por lo que no debe cargarse en una base con datos reales.

## 5. Frontend (Vercel)

1. Crear un proyecto desde el mismo repositorio, con `frontend` como Root Directory. Vercel detecta Vite: el comando de compilación es `npm run build` y la carpeta de salida es `dist`.
2. Definir la variable de entorno `VITE_API_URL` con el valor `/api`.
3. En el archivo `frontend/vercel.json`, reemplazar el marcador `URL-DEL-BACKEND` por la URL del servicio publicado en Render.
4. Copiar la URL final de Vercel en la variable `FRONTEND_ORIGIN` del backend en Render, que vuelve a publicar el servicio.

El archivo `frontend/vercel.json` define dos reglas: la primera reenvía al backend las solicitudes que comienzan con `/api`, y la segunda devuelve `index.html` para el resto de las rutas, de modo que las pantallas de la aplicación también abren al recargar la página. Con esta configuración el navegador se comunica siempre con el dominio del frontend y la cookie de sesión pertenece al mismo sitio, condición necesaria para su atributo `SameSite=Lax`.