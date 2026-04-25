from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

# Importaciones de tu base de datos
from data.database import SessionLocal, engine, Base
from data.models import Libro as LibroDB, Prestamo as PrestamoDB

# AUTO-SEED: Crear tablas y poblar la BD con datos del CSV al inicio
Base.metadata.create_all(bind=engine)


def seed_database_if_empty():
    """Inserta libros del CSV si la BD está vacía"""
    db = SessionLocal()
    try:
        count = db.query(LibroDB).count()
        if count == 0:
            csv_path = './books.csv'
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, sep=';')
                for _, row in df.iterrows():
                    libro = LibroDB(
                        id=int(row['id']),
                        titulo=str(row['titulo']),
                        autor=str(row['autor']),
                        genero=str(row['genero']),
                        disponible=bool(row['disponible'])
                    )
                    db.add(libro)
                db.commit()
                print(f"✅ Base de datos inicializada con {len(df)} libros")
            else:
                print("⚠️ Archivo books.csv no encontrado")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al inicializar BD: {e}")
    finally:
        db.close()


# Ejecutar seed al inicio
seed_database_if_empty()


# Configuración de Pydantic
class BaseModelConfig(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# --- ESQUEMAS PARA EL CATÁLOGO ---
class LibroSchema(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool


class ListadoLibros(BaseModel):
    libros: List[LibroSchema] = []


# --- ESQUEMAS PARA EL CALENDARIO ---
class EventoCalendario(BaseModel):
    title: str
    start: str
    end: str
    backgroundColor: str
    borderColor: str
    allDay: bool = True


class ListadoCalendario(BaseModel):
    eventos: List[EventoCalendario] = []


# --- ESQUEMA PARA CREAR PRÉSTAMO ---
class PrestamoCreate(BaseModel):
    id_libro: int
    usuario: str
    fecha_prestamo: str


# --- INICIALIZACIÓN DE LA APP ---
app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="1.0.0",
)


# --- RUTAS ---

@app.get("/libros/", response_model=ListadoLibros)
def retrieve_data():
    """Lee el catálogo desde la base de datos (ya no desde CSV)"""
    db = SessionLocal()
    try:
        libros = db.query(LibroDB).all()

        # Convertir a diccionarios
        libros_dict = [
            {
                "id": libro.id,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "genero": libro.genero,
                "disponible": libro.disponible
            }
            for libro in libros
        ]

        return ListadoLibros(libros=libros_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/calendario/{usuario}", response_model=ListadoCalendario)
def get_calendario_usuario(usuario: str):
    """Obtiene los préstamos de la DB y los formatea para el calendario de Streamlit"""
    db = SessionLocal()
    try:
        # Buscamos préstamos en la DB para ese usuario
        prestamos = db.query(PrestamoDB).filter(PrestamoDB.usuario == usuario).all()

        eventos_formateados = []
        for p in prestamos:
            # Buscamos el título del libro usando el ID del préstamo
            libro = db.query(LibroDB).filter(LibroDB.id == p.id_libro).first()
            titulo_mostrar = libro.titulo if libro else f"Libro ID: {p.id_libro}"

            # Lógica de colores HU-08: Rojo (Prestado/Activo) | Verde (Devuelto)
            color = "#ff4b4b" if p.activo else "#28a745"

            eventos_formateados.append(
                EventoCalendario(
                    title=f"📚 {titulo_mostrar}",
                    start=str(p.fecha_prestamo),
                    end=str(p.fecha_devolucion) if p.fecha_devolucion else str(p.fecha_prestamo),
                    backgroundColor=color,
                    borderColor=color,
                    allDay=True
                )
            )

        return ListadoCalendario(eventos=eventos_formateados)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/prestamos/")
async def create_loan(prestamo: PrestamoCreate):
    """Registra un préstamo en la base de datos"""
    from main import registrar_prestamo

    try:
        nuevo_prestamo = registrar_prestamo(
            id_libro=prestamo.id_libro,
            usuario=prestamo.usuario,
            fecha_texto=prestamo.fecha_prestamo
        )
        return {
            "message": "Préstamo registrado correctamente",
            "prestamo_id": nuevo_prestamo.id,
            "libro_id": nuevo_prestamo.id_libro,
            "usuario": nuevo_prestamo.usuario,
            "fecha": nuevo_prestamo.fecha_prestamo
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))