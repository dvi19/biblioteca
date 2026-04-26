from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from data.database import SessionLocal
from data.models import Libro as LibroDB, Prestamo as PrestamoDB

class PrestamoCreate(BaseModel):
    id_libro: int
    usuario: str
    fecha_prestamo: str

class EventoCalendario(BaseModel):
    title: str
    start: str
    end: str
    backgroundColor: str
    borderColor: str
    allDay: bool = True

class ListadoCalendario(BaseModel):
    eventos: List[EventoCalendario] = []

router = APIRouter(tags=["Préstamos"])

@router.post("/prestamos/")
async def create_loan(prestamo: PrestamoCreate):
    from main import registrar_prestamo
    try:
        nuevo_prestamo = registrar_prestamo(id_libro=prestamo.id_libro, usuario=prestamo.usuario, fecha_texto=prestamo.fecha_prestamo)
        return {"message": "Préstamo registrado correctamente", "prestamo_id": nuevo_prestamo.id, "libro_id": nuevo_prestamo.id_libro, "usuario": nuevo_prestamo.usuario, "fecha": nuevo_prestamo.fecha_prestamo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/prestamos/historial/{usuario}")
def get_historial_prestamos(usuario: str):
    from main import consultar_historial
    try:
        prestamos = consultar_historial(usuario)
        prestamos_dict = [{"ID": p.id, "Libro": p.id_libro, "Usuario": p.usuario, "Fecha": p.fecha_prestamo, "Devolucion": p.fecha_devolucion if p.fecha_devolucion else "-", "Estado": "Activo" if p.activo else "Devuelto"} for p in prestamos]
        return {"prestamos": prestamos_dict}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/calendario/{usuario}", response_model=ListadoCalendario)
def get_calendario_usuario(usuario: str):
    db = SessionLocal()
    try:
        prestamos = db.query(PrestamoDB).filter(PrestamoDB.usuario == usuario).all()
        eventos = []
        for p in prestamos:
            libro = db.query(LibroDB).filter(LibroDB.id == p.id_libro).first()
            titulo = libro.titulo if libro else f"Libro {p.id_libro}"
            color = "#ff4b4b" if p.activo else "#28a745"
            eventos.append(EventoCalendario(title=f"📚 {titulo}", start=str(p.fecha_prestamo), end=str(p.fecha_devolucion) if p.fecha_devolucion else str(p.fecha_prestamo), backgroundColor=color, borderColor=color, allDay=True))
        return ListadoCalendario(eventos=eventos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()