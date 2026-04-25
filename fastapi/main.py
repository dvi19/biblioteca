# Crear la función registrar libro
# A la hora de configurar el sql para que se guarde en la base de datos, hemos tenido que hacer uso de la IA
# porque no controlamos SQL

from sqlalchemy import or_
from data.database import SessionLocal, engine, Base
from data.models import Libro, Prestamo
from datetime import datetime
Base.metadata.create_all(bind=engine) # Esto lo hemos hecho con IA para que se creen todas las tablas que haya en models.py
from errores import (
    CampoFaltanteError,
    IdNoNumericoError,
    LibroNoEncontradoError,
    LibroYaDisponibleError,
    HistorialVacioError,
    FormatoFechaError
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


def registrar_prestamo(id_libro, usuario, fecha_texto):
    """HU-06: Registra un préstamo."""
    db = SessionLocal()
    try:
        # Verificar que el libro existe
        libro = db.query(Libro).filter(Libro.id == id_libro).first()
        if not libro:
            raise LibroNoEncontradoError(f"No existe el libro con ID {id_libro}")

        # Crear el préstamo
        nuevo_prestamo = Prestamo(
            id_libro=id_libro,
            usuario=usuario,
            fecha_prestamo=fecha_texto,
            activo=True
        )
        db.add(nuevo_prestamo)

        # Marcar el libro como NO disponible
        libro.disponible = False

        # Confirmar ANTES de cerrar la sesión
        db.commit()
        db.refresh(nuevo_prestamo)  # Ahora sí podemos hacer refresh

        # Retornar el préstamo (ya está "detached" pero con datos completos)
        return nuevo_prestamo

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def consultar_historial(nombre_usuario):
    db = SessionLocal()
    try:
        historial = db.query(Prestamo).filter(Prestamo.usuario == nombre_usuario).all()

        # Si la lista está vacía, lanzamos el error
        if not historial:
            raise HistorialVacioError(f"El usuario {nombre_usuario} no tiene historial de préstamos.")

        return historial
    finally:
        db.close()


def obtener_eventos_calendario(nombre_usuario):
    """HU-08: Prepara los datos del historial para el calendario."""
    db = SessionLocal()
    try:
        prestamos = db.query(Prestamo).filter(Prestamo.usuario == nombre_usuario).all()
        eventos = []

        for p in prestamos:
            # Buscamos el título del libro para que aparezca en el calendario
            libro = db.query(Libro).filter(Libro.id == p.id_libro).first()
            titulo = libro.titulo if libro else f"Libro {p.id_libro}"

            # Color: Rojo si está activo, Verde si ya se devolvió
            color_evento = "#ff4b4b" if p.activo else "#28a745"

            eventos.append({
                "title": f" {titulo}",
                "start": p.fecha_prestamo,
                "end": p.fecha_devolucion if p.fecha_devolucion else p.fecha_prestamo,
                "backgroundColor": color_evento,
                "display": "block"
            })
        return eventos
    finally:
        db.close()