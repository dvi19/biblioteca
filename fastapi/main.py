# Crear la función registrar libro
# A la hora de configurar el sql para que se guarde en la base de datos, hemos tenido que hacer uso de la IA
# porque no controlamos SQL

from sqlalchemy import or_
from data.database import SessionLocal, engine, Base
from data.models import Libro
from fastapi.errores import (
    CampoFaltanteError,
    IdNoNumericoError,
    LibroNoEncontradoError,
    LibroYaDisponibleError
)

def registrar_libro(id_libro, titulo, autor, genero, disponible=True):
    # 1. Lanzar excepción si el id no es entero
    if not isinstance(id_libro, int):
        raise IdNoNumericoError("El ID debe ser un número entero.")

    # 2. Lanzar la excepción si faltan campos obligatorios
    if not titulo or str(titulo).strip() == "" or not autor or not genero:
        raise CampoFaltanteError("Todos los campos obligatorios deben estar rellenos.")

    db = SessionLocal()
    try:
        nuevo_libro = Libro(id=id_libro, titulo=titulo, autor=autor, genero=genero, disponible=disponible)
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)
        return nuevo_libro
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def consultar_catalogo():
    db = SessionLocal() # abrimos sesión
    try:
        # Hemos necesita de IA para completar este paso
        libros = db.query(Libro).all()
        return libros
    finally:
        db.close() # cerramos la sesión


def eliminar_libro(id_libro):
    db = SessionLocal()
    try:
        # Buscamos el libro por su ID
        libro = db.query(Libro).filter(Libro.id == id_libro).first()

        if libro:
            db.delete(libro)  # Marcamos para borrar
            db.commit()  # Confirmamos el borrado
            return True
        return False  # Si no existía el libro
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def actualizar_disponibilidad(id_libro, nuevo_estado: bool):
    db = SessionLocal()
    try:
        # Buscamos el libro
        libro = db.query(Libro).filter(Libro.id == id_libro).first()

        if not libro:
            raise LibroNoEncontradoError(f"No se encontró el libro {id_libro}")

        # Modificamos el atributo
        libro.disponible = nuevo_estado

        db.commit()  # Guarda el cambio
        db.refresh(libro)  # Actualiza el objeto
        return libro
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def devolver_libro(id_libro):
    db = SessionLocal()
    try:
        libro = db.query(Libro).filter(Libro.id == id_libro).first()

        if not libro:
            raise LibroNoEncontradoError(f"No existe el libro con ID {id_libro}")

        # SI EL LIBRO YA ESTÁ EN LA BIBLIOTECA (disponible = True)
        if libro.disponible:
            raise LibroYaDisponibleError(f"El libro {id_libro} ya está disponible.")

        # PROCESO DE DEVOLUCIÓN
        libro.disponible = True
        db.commit()
        db.refresh(libro)
        return libro
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def buscar_libro(termino: str):
    """HU-07: Filtra libros por título o autor."""
    db = SessionLocal()
    try:
        # byscamos que contenga lo que hemos escrito
        formato_busqueda = f"%{termino}%"

        # Filtramos por lo que hemos puesto en formato_busqueda
        libros = db.query(Libro).filter(
            or_(
                Libro.titulo.ilike(formato_busqueda),
                Libro.autor.ilike(formato_busqueda)
            )
        ).all()

        return libros
    finally:
        db.close()