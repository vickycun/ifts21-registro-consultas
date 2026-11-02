from fastapi import APIRouter, HTTPException
from src.db.conexion import get_connection

router = APIRouter(prefix="/api/usuarios", tags=["Alumnos"])

@router.get("")
def listar_usuarios(apellido: str | None = None):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            if apellido:
                cursor.execute("SELECT * FROM usuarios WHERE apellido LIKE %s ORDER BY apellido, nombre", (f"%{apellido}%",))
            else:
                cursor.execute("SELECT * FROM usuarios ORDER BY apellido, nombre")
            return cursor.fetchall()
    finally:
        conexion.close()

@router.get("/{id}")
def ver_usuario(id: int):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            usuario = cursor.fetchone()
    finally:
        conexion.close()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return usuario
