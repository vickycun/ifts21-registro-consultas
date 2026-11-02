# Registro de consultas de alumnos — IFTS 21

Ejemplo didáctico: frontend HTML/CSS/JS → API FastAPI → MySQL.

## Qué hace

Secretaría selecciona un alumno, registra una consulta recibida y luego consulta su historial. Cada consulta empieza `pendiente` y puede marcarse `resuelta` o reabrirse. **No envía mensajes al alumno.**

## Preparación local

1. Abrir `db/schema.sql` en MySQL Workbench y ejecutar el script. **No borra la tabla `contactos` anterior.** Crea la tabla nueva `consultas` y conserva los usuarios existentes. Si en tu base hay otros registros con los IDs 1–6, revisalos antes de ejecutar el INSERT de ejemplo.
2. Copiar `.env.example` a `.env` y completar las credenciales de MySQL.
3. En PowerShell, dentro del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

4. Abrir http://127.0.0.1:8000 y http://127.0.0.1:8000/docs. **No usar Live Server para probar el modo local.**

## API

- `GET /api/usuarios` y `GET /api/usuarios?apellido=López`
- `GET /api/usuarios/2`
- `GET /api/consultas` y `GET /api/consultas?usuario_id=2`
- `POST /api/consultas`: `{ "usuario_id": 2, "descripcion": "Consultó por equivalencias" }`
- `PATCH /api/consultas/1`: `{ "estado": "resuelta" }`

## Publicación

1. Subir el repositorio a GitHub sin `.env` ni `.venv`.
2. Crear MySQL en Railway y ejecutar `db/schema.sql` en esa **nueva** base (no es la base local).
3. Desplegar FastAPI en Railway, configurar `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` con los datos de Railway. Comando de inicio: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Publicar en Netlify con directorio de publicación `public`. En `public/config.js`, configurar `window.API_BASE_URL` con la URL HTTPS del backend Railway (sin barra final) y volver a desplegar.
5. Configurar en Railway `FRONTEND_ORIGIN` con el dominio HTTPS real de Netlify (sin barra final) y reiniciar el backend.

**Importante:** este ejemplo no tiene autenticación. Para una demo pública, usar únicamente datos ficticios; cualquiera con la URL podría consultar y modificar registros. No es adecuado para almacenar consultas reales de alumnos sin autenticación, permisos y protección de datos.
