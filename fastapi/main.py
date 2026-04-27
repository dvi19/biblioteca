# Crear la función registrar libro
# A la hora de configurar el sql para que se guarde en la base de datos, hemos tenido que hacer uso de la IA
# porque no controlamos SQL

from sqlalchemy import or_
from data.database import SessionLocal, engine, Base
from data.models import Libro, Prestamo, Usuario
from datetime import datetime
Base.metadata.create_all(bind=engine) # Esto lo hemos hecho con IA para que se creen todas las tablas que haya en models.py
from errores import (
    CampoFaltanteError,
    EmailDuplicadoError,
    IdNoNumericoError,
    LibroNoEncontradoError,
    LibroYaDisponibleError,
    HistorialVacioError,
    FormatoFechaError,
    LibroDuplicadoError
)

from config.logging_config import logger
from utils.decoradores import log_execution_time, validar_campos, retry
from utils.context_managers import db_session, db_transaction, measure_time

Base.metadata.create_all(bind=engine)



@log_execution_time
@validar_campos('titulo', 'autor', 'genero')
def registrar_libro(id_libro, titulo, autor, genero, disponible=True):
    """Registra un nuevo libro en la base de datos"""
    logger.info(f"Intentando registrar libro ID {id_libro}: '{titulo}'")

    if not isinstance(id_libro, int):
        logger.error(f"ID no numérico recibido: {id_libro}")
        raise IdNoNumericoError("El ID debe ser un número entero.")

    if not titulo or str(titulo).strip() == "" or not autor or not genero:
        logger.warning(f"Intento de registro con campos vacíos - ID: {id_libro}")
        raise CampoFaltanteError("Todos los campos obligatorios deben estar rellenos.")

    db = SessionLocal()
    try:
        # Verificar si el ID ya existe
        libro_existente = db.query(Libro).filter(Libro.id == id_libro).first()
        if libro_existente:
            logger.warning(
                f"Intento de registrar libro duplicado - ID: {id_libro}, existente: '{libro_existente.titulo}'")
            raise LibroDuplicadoError(f"Ya existe un libro con el ID {id_libro}: '{libro_existente.titulo}'")

        nuevo_libro = Libro(id=id_libro, titulo=titulo, autor=autor, genero=genero, disponible=disponible)
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)

        logger.info(f"✅ Libro registrado exitosamente - ID: {id_libro}, Título: '{titulo}'")
        return nuevo_libro
    except Exception as e:
        db.rollback()
        logger.error(f"Error al registrar libro ID {id_libro}: {str(e)}")
        raise e
    finally:
        db.close()


@log_execution_time
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


@log_execution_time
def devolver_libro(id_libro):
    logger.info(f"Intentando devolver libro ID: {id_libro}")

    db = SessionLocal()
    try:
        libro = db.query(Libro).filter(Libro.id == id_libro).first()

        if not libro:
            logger.error(f"Intento de devolución de libro inexistente - ID: {id_libro}")
            raise LibroNoEncontradoError(f"No existe el libro con ID {id_libro}")

        # SI EL LIBRO YA ESTÁ EN LA BIBLIOTECA
        if libro.disponible:
            logger.warning(f"Intento de devolver libro ya disponible - ID: {id_libro}")
            raise LibroYaDisponibleError(f"El libro {id_libro} ya está disponible.")

        # PROCESO DE DEVOLUCIÓN
        libro.disponible = True
        db.commit()
        db.refresh(libro)

        logger.info(f"✅ Libro devuelto exitosamente - ID: {id_libro}, Título: '{libro.titulo}'")
        return libro
    except Exception as e:
        db.rollback()
        logger.error(f"Error al devolver libro ID {id_libro}: {str(e)}")
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



@log_execution_time
@retry(max_intentos=3, delay=1.0)
def registrar_prestamo(id_libro, usuario, fecha_texto):
    """HU-06: Registra un préstamo."""
    logger.info(f"Intentando registrar préstamo - Libro ID: {id_libro}, Usuario: '{usuario}'")

    db = SessionLocal()
    try:
        # Verificar que el libro existe
        libro = db.query(Libro).filter(Libro.id == id_libro).first()
        if not libro:
            logger.error(f"Intento de préstamo de libro inexistente - ID: {id_libro}")
            raise LibroNoEncontradoError(f"No existe el libro con ID {id_libro}")

        # Crear el prestamo
        nuevo_prestamo = Prestamo(
            id_libro=id_libro,
            usuario=usuario,
            fecha_prestamo=fecha_texto,
            activo=True
        )
        db.add(nuevo_prestamo)

        # Marca el libro como NO disponible
        libro.disponible = False

        # Confirmar ANTES de cerar la sesión
        db.commit()
        db.refresh(nuevo_prestamo)

        logger.info(f"✅ Préstamo registrado - Libro: '{libro.titulo}', Usuario: '{usuario}'")
        return nuevo_prestamo

    except Exception as e:
        db.rollback()
        logger.error(f"Error al registrar préstamo - Libro ID: {id_libro}, Usuario: '{usuario}' - {str(e)}")
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


@log_execution_time
@validar_campos('nombre', 'email')
def registrar_usuario(nombre, email):
    """HU-03: Registra un nuevo usuario en la base de datos"""
    logger.info(f"Intentando registrar usuario: '{nombre}' ({email})")

    # Validar campos obligatorios
    if not nombre or str(nombre).strip() == "" or not email or str(email).strip() == "":
        logger.warning(f"Intento de registro de usuario con campos vacíos")
        raise CampoFaltanteError("El nombre y el email son obligatorios.")

    db = SessionLocal()
    try:
        # Verificar si el email ya existe
        usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario_existente:
            logger.warning(f"Intento de registro con email duplicado: {email}")
            raise EmailDuplicadoError(f"El email '{email}' ya está registrado.")

        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre.strip(),
            email=email.strip().lower()
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        logger.info(f"✅ Usuario registrado exitosamente: '{nombre}' ({email})")
        return nuevo_usuario

    except Exception as e:
        db.rollback()
        logger.error(f"Error al registrar usuario '{nombre}': {str(e)}")
        raise e
    finally:
        db.close()


def consultar_usuarios():
    """HU-03: Obtiene todos los usuarios registrados"""
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    finally:
        db.close()


def consultar_catalogo_mejorado():
    """
    HU-01 mejorada: Consulta el catálogo usando context manager.
    """
    with measure_time("Consulta de catálogo completo"):
        with db_session() as db:
            libros = db.query(Libro).all()
            logger.info(f"📚 Se encontraron {len(libros)} libros en el catálogo")
            return libros


def registrar_libro_con_transaccion(id_libro, titulo, autor, genero, disponible=True):
    """
    Versión mejorada de registrar_libro usando context manager de transacciones.
    Si algo falla, hace rollback automático.
    """
    logger.info(f"Intentando registrar libro ID {id_libro}: '{titulo}' (con transacción)")

    if not isinstance(id_libro, int):
        logger.error(f"ID no numérico recibido: {id_libro}")
        raise IdNoNumericoError("El ID debe ser un número entero.")

    if not titulo or str(titulo).strip() == "" or not autor or not genero:
        logger.warning(f"Intento de registro con campos vacíos - ID: {id_libro}")
        raise CampoFaltanteError("Todos los campos obligatorios deben estar rellenos.")

    with db_transaction() as db:
        # Verificar si el ID ya existe
        libro_existente = db.query(Libro).filter(Libro.id == id_libro).first()
        if libro_existente:
            logger.warning(f"Intento de registrar libro duplicado - ID: {id_libro}")
            raise LibroDuplicadoError(f"Ya existe un libro con el ID {id_libro}")

        # Crear nuevo libro
        nuevo_libro = Libro(
            id=id_libro,
            titulo=titulo,
            autor=autor,
            genero=genero,
            disponible=disponible
        )
        db.add(nuevo_libro)
        db.flush()
        db.refresh(nuevo_libro)

        # Extraer datos como diccionario antes de cerrar sesión
        resultado = {
            'id': nuevo_libro.id,
            'titulo': nuevo_libro.titulo,
            'autor': nuevo_libro.autor,
            'genero': nuevo_libro.genero,
            'disponible': nuevo_libro.disponible
        }

        logger.info(f"✅ Libro registrado con transacción - ID: {id_libro}")

    # Devolver diccionario en lugar de objeto SQLAlchemy
    return resultado


def obtener_estadisticas_biblioteca():
    """
    Función que demuestra el uso de context managers para estadísticas.
    """
    with measure_time("Cálculo de estadísticas"):
        with db_session() as db:
            total_libros = db.query(Libro).count()
            libros_disponibles = db.query(Libro).filter(Libro.disponible == True).count()
            libros_prestados = total_libros - libros_disponibles
            total_prestamos = db.query(Prestamo).count()
            prestamos_activos = db.query(Prestamo).filter(Prestamo.activo == True).count()

            stats = {
                "total_libros": total_libros,
                "libros_disponibles": libros_disponibles,
                "libros_prestados": libros_prestados,
                "total_prestamos": total_prestamos,
                "prestamos_activos": prestamos_activos
            }

            logger.info(f"📊 Estadísticas calculadas: {stats}")
            return stats