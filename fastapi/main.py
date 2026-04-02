# Crear la función registrar libro
# A la hora de configurar el sql para que se guarde en la base de datos, hemos tenido que hacer uso de la IA
# porque no controlamos SQL

from data.database import SessionLocal, engine, Base
from data.models import Libro
from fastapi.errores import CampoFaltanteError, IdNoNumericoError #

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