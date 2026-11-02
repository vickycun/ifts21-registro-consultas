from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from src.db.conexion import get_connection

router = APIRouter(prefix="/api/consultas", tags=["Consultas"])

class NuevaConsulta(BaseModel):
    usuario_id: int = Field(gt=0)
    descripcion: str = Field(min_length=5, max_length=2000)

class CambioEstado(BaseModel):
    estado: Literal["pendiente", "resuelta"]

@router.get("")
def listar_consultas(usuario_id: int | None = None):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = """SELECT c.id, c.usuario_id, u.nombre, u.apellido,
                            c.descripcion, c.estado, c.fecha
                     FROM consultas c JOIN usuarios u ON u.id = c.usuario_id"""
            if usuario_id is not None:
                sql += " WHERE c.usuario_id = %s"
                cursor.execute(sql + " ORDER BY c.fecha DESC, c.id DESC", (usuario_id,))
            else:
                cursor.execute(sql + " ORDER BY c.fecha DESC, c.id DESC")
            return cursor.fetchall()
    finally:
        conexion.close()

@router.post("", status_code=201)
def crear_consulta(datos: NuevaConsulta):
    descripcion = datos.descripcion.strip()
    if len(descripcion) < 5:
        raise HTTPException(status_code=422, detail="La descripción debe tener al menos 5 caracteres")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (datos.usuario_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Alumno no encontrado")
            cursor.execute("INSERT INTO consultas (usuario_id, descripcion) VALUES (%s, %s)", (datos.usuario_id, descripcion))
            nuevo_id = cursor.lastrowid
        conexion.commit()
        return {"id": nuevo_id, "detalle": "Consulta registrada"}
    finally:
        conexion.close()

@router.patch("/{id}")
def actualizar_estado(id: int, datos: CambioEstado):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE consultas SET estado = %s WHERE id = %s", (datos.estado, id))
            if cursor.rowcount == 0:
                # MySQL puede reportar cero filas si el valor ya era el mismo.
                cursor.execute("SELECT id FROM consultas WHERE id = %s", (id,))
                if cursor.fetchone() is None:
                    raise HTTPException(status_code=404, detail="Consulta no encontrada")
        conexion.commit()
        return {"id": id, "estado": datos.estado}
    finally:
        conexion.close()
