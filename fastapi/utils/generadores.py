# Generadores

from typing import Generator, List, Dict, Any
from data.database import SessionLocal
from data.models import Libro, Prestamo, Usuario
from config.logging_config import logger


def procesar_libros_en_lotes(batch_size: int = 10) -> Generator[List[Libro], None, None]:
    """Generador que devuelve libros en lotes."""
    db = SessionLocal()
    try:
        offset = 0
        logger.info(f"📦 Iniciando procesamiento en lotes (tamaño: {batch_size})")

        while True:
            lote = db.query(Libro).offset(offset).limit(batch_size).all()

            if not lote:
                logger.info("✅ Procesamiento de lotes completado")
                break

            logger.info(f"📚 Procesando lote {offset // batch_size + 1} ({len(lote)} libros)")
            yield lote
            offset += batch_size
    finally:
        db.close()


def iterar_prestamos_activos() -> Generator[Prestamo, None, None]:
    """Generador que itera sobre préstamos activos uno por uno."""
    db = SessionLocal()
    try:
        logger.info("🔄 Iniciando iteración de préstamos activos")
        prestamos = db.query(Prestamo).filter(Prestamo.activo == True).all()

        for prestamo in prestamos:
            logger.info(f"📖 Procesando préstamo ID: {prestamo.id}")
            yield prestamo

        logger.info(f"✅ Iteración completada ({len(prestamos)} préstamos)")
    finally:
        db.close()


def generar_reporte_paginado(items_por_pagina: int = 5) -> Generator[Dict[str, Any], None, None]:
    """Generador que devuelve páginas de un reporte."""
    db = SessionLocal()
    try:
        total_libros = db.query(Libro).count()
        total_paginas = (total_libros + items_por_pagina - 1) // items_por_pagina

        logger.info(f"📄 Generando reporte paginado ({total_paginas} páginas)")

        for pagina_num in range(1, total_paginas + 1):
            offset = (pagina_num - 1) * items_por_pagina
            libros = db.query(Libro).offset(offset).limit(items_por_pagina).all()

            libros_dict = [
                {
                    'id': libro.id,
                    'titulo': libro.titulo,
                    'autor': libro.autor,
                    'disponible': libro.disponible
                }
                for libro in libros
            ]

            pagina = {
                'numero': pagina_num,
                'total_paginas': total_paginas,
                'items_por_pagina': items_por_pagina,
                'total_items': total_libros,
                'libros': libros_dict
            }

            logger.info(f"📄 Página {pagina_num}/{total_paginas} generada")
            yield pagina
    finally:
        db.close()


def stream_usuarios_con_estadisticas() -> Generator[Dict[str, Any], None, None]:
    """Generador que devuelve usuarios con estadísticas."""
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        logger.info(f"👥 Iniciando stream de {len(usuarios)} usuarios")

        for usuario in usuarios:
            total_prestamos = db.query(Prestamo).filter(Prestamo.usuario == usuario.nombre).count()
            prestamos_activos = db.query(Prestamo).filter(
                Prestamo.usuario == usuario.nombre,
                Prestamo.activo == True
            ).count()

            usuario_data = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'total_prestamos': total_prestamos,
                'prestamos_activos': prestamos_activos,
                'prestamos_devueltos': total_prestamos - prestamos_activos
            }

            logger.info(f"👤 Procesando usuario: {usuario.nombre}")
            yield usuario_data

        logger.info("✅ Stream completado")
    finally:
        db.close()


def generar_secuencia_fibonacci(n: int) -> Generator[int, None, None]:
    """Generador de ejemplo: Fibonacci."""
    logger.info(f"🔢 Generando Fibonacci (n={n})")
    a, b = 0, 1
    count = 0

    while count < n:
        yield a
        a, b = b, a + b
        count += 1

    logger.info("✅ Fibonacci completada")