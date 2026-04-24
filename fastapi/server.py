from data.database import SessionLocal
from data.models import Libro, Prestamo
from fastapi import FastAPI, HTTPException
import pandas as pd
from typing import List
from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool

class ListadoLibros(BaseModel):
    libros: List[Libro] = []

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="1.0.0",
)

@app.get("/libros/")
def retrieve_data():
    # EDUCATIONAL INEFFICIENCY: Reading CSV on every request
    # Students should optimize this by using a database or caching
    try:
        todosmisdatos = pd.read_csv('./books.csv', sep=';')
        todosmisdatos = todosmisdatos.fillna(0)
        todosmisdatosdict = todosmisdatos.to_dict(orient='records')
        listado = ListadoLibros()
        listado.libros = todosmisdatosdict
        return listado
    except Exception as e:
        return {"error": str(e)}

@app.post("/prestamos/")
async def create_loan(libro_id: int):
    # This is a stub for students to implement
    return {"message": "Préstamo creado (no realmente)", "libro_id": libro_id}


# --- 1. Primero define cómo es el formato del evento (Esquemas) ---
class EventoCalendario(PydanticBaseModel):
    title: str
    start: str
    end: str
    backgroundColor: str
    borderColor: str
    allDay: bool = True


class ListadoCalendario(PydanticBaseModel):
    eventos: List[EventoCalendario] = []


# --- 2. Luego crea la ruta (Endpoint) al final del archivo ---
@app.get("/calendario/{usuario}", response_model=ListadoCalendario)
def get_calendario_usuario(usuario: str):
    db = SessionLocal()
    try:
        # Buscamos préstamos en la DB para ese usuario
        prestamos = db.query(Prestamo).filter(Prestamo.usuario == usuario).all()

        eventos_formateados = []
        for p in prestamos:
            # Buscamos el título del libro
            libro = db.query(Libro).filter(Libro.id == p.id_libro).first()
            titulo = libro.titulo if libro else f"ID: {p.id_libro}"

            # Color: Rojo si es activo (True), Verde si está devuelto (False)
            color = "#ff4b4b" if p.activo else "#28a745"

            eventos_formateados.append(
                EventoCalendario(
                    title=f"📚 {titulo}",
                    start=p.fecha_prestamo,
                    end=p.fecha_devolucion if p.fecha_devolucion else p.fecha_prestamo,
                    backgroundColor=color,
                    borderColor=color,
                    allDay=True
                )
            )

        # Devolvemos el objeto que espera Streamlit
        return ListadoCalendario(eventos=eventos_formateados)
    finally:
        db.close()