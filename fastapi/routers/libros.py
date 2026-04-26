
# Router para endpoints relacionados con LIBROS

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from data.database import SessionLocal
from data.models import Libro as LibroDB


# Esquema para Libro
class LibroSchema(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool


class ListadoLibros(BaseModel):
    libros: List[LibroSchema] = []


# Crear el router
router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)


@router.get("/", response_model=ListadoLibros)
def listar_libros():
    """HU-01: Lee el catálogo desde la base de datos"""
    db = SessionLocal()
    try:
        libros = db.query(LibroDB).all()

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


@router.get("/buscar")
def buscar_libros(termino: str):
    """HU-07: Busca libros por título o autor"""
    from main import buscar_libro

    try:
        libros = buscar_libro(termino)

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

        return {
            "resultados": len(libros_dict),
            "libros": libros_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def crear_libro(libro: LibroSchema):
    """HU-02: Registra un nuevo libro en el catálogo"""
    from main import registrar_libro

    try:
        nuevo_libro = registrar_libro(
            id_libro=libro.id,
            titulo=libro.titulo,
            autor=libro.autor,
            genero=libro.genero,
            disponible=libro.disponible
        )
        return {
            "message": "Libro registrado correctamente",
            "libro": {
                "id": nuevo_libro.id,
                "titulo": nuevo_libro.titulo,
                "autor": nuevo_libro.autor,
                "genero": nuevo_libro.genero,
                "disponible": nuevo_libro.disponible
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{libro_id}/devolver")
async def devolver_libro_endpoint(libro_id: int):
    """HU-05: Marca un libro como devuelto (disponible)"""
    from main import devolver_libro

    try:
        libro = devolver_libro(libro_id)
        return {
            "message": f"Libro '{libro.titulo}' devuelto correctamente",
            "libro": {
                "id": libro.id,
                "titulo": libro.titulo,
                "disponible": libro.disponible
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))