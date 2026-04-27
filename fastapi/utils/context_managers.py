
# Context Managers personalizados para el proyecto

from contextlib import contextmanager
from typing import Generator
import time
from data.database import SessionLocal
from config.logging_config import logger


@contextmanager
def db_session() -> Generator:
    """
    Context manager para gestionar sesiones de base de datos.
    Cierra automáticamente la sesión al finalizar.
    """
    session = SessionLocal()
    try:
        logger.info("📂 Sesión de BD abierta")
        yield session
        logger.info("✅ Sesión de BD cerrada correctamente")
    except Exception as e:
        logger.error(f"❌ Error en sesión de BD: {str(e)}")
        raise
    finally:
        session.close()


@contextmanager
def db_transaction() -> Generator:
    """
    Context manager para transacciones de base de datos.
    Hace commit automático si todo va bien, rollback si falla.
    """
    session = SessionLocal()
    try:
        logger.info("🔄 Transacción iniciada")
        yield session
        session.commit()
        logger.info("✅ Transacción completada (commit)")
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Transacción revertida (rollback): {str(e)}")
        raise
    finally:
        session.close()


@contextmanager
def measure_time(operation_name: str) -> Generator:
    """
    Context manager para medir el tiempo de ejecución de un bloque de código.
    """
    start_time = time.time()
    logger.info(f"⏱️  Iniciando: {operation_name}")

    try:
        yield
        elapsed = time.time() - start_time
        logger.info(f"✅ {operation_name} completado en {elapsed:.4f} segundos")
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ {operation_name} falló después de {elapsed:.4f} segundos: {str(e)}")
        raise


@contextmanager
def temporary_data_modification(session, model_instance, **kwargs):
    """
    Context manager para modificaciones temporales de datos.
    Restaura los valores originales al salir del contexto.
    """
    # Guardar valores originales
    original_values = {}
    for key in kwargs:
        if hasattr(model_instance, key):
            original_values[key] = getattr(model_instance, key)

    try:
        # Aplicar cambios temporales
        for key, value in kwargs.items():
            if hasattr(model_instance, key):
                setattr(model_instance, key, value)
        logger.info(f"🔄 Modificación temporal aplicada: {kwargs}")
        yield model_instance
    finally:
        # Restaurar valores originales
        for key, value in original_values.items():
            setattr(model_instance, key, value)
        logger.info(f"↩️  Valores restaurados: {original_values}")