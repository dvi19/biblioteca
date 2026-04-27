# Decoradores personalizados para el proyecto

import time
import functools
from typing import Callable, Any
from config.logging_config import logger


def log_execution_time(func: Callable) -> Callable:
    """
    Decorador que mide y registra el tiempo de ejecución de una función.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        logger.info(f"⏱️  Iniciando ejecución de '{func.__name__}'")

        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"✅ '{func.__name__}' completada en {elapsed_time:.4f} segundos")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"❌ '{func.__name__}' falló después de {elapsed_time:.4f} segundos: {str(e)}")
            raise

    return wrapper


def validar_campos(*campos_requeridos):
    """
    Decorador que valida que ciertos campos no estén vacíos.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener los argumentos de la función
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validar cada campo requerido
            for campo in campos_requeridos:
                valor = bound_args.arguments.get(campo)

                if valor is None or (isinstance(valor, str) and valor.strip() == ""):
                    error_msg = f"El campo '{campo}' es obligatorio y no puede estar vacío"
                    logger.warning(f"⚠️  Validación fallida en '{func.__name__}': {error_msg}")
                    raise ValueError(error_msg)

            logger.info(f"✅ Validación de campos exitosa para '{func.__name__}'")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(max_intentos: int = 3, delay: float = 1.0):
    """
    Decorador que reintenta ejecutar una función si falla.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            intentos = 0

            while intentos < max_intentos:
                try:
                    if intentos > 0:
                        logger.warning(f"🔄 Reintentando '{func.__name__}' (intento {intentos + 1}/{max_intentos})")

                    result = func(*args, **kwargs)

                    if intentos > 0:
                        logger.info(f"✅ '{func.__name__}' exitosa después de {intentos + 1} intentos")

                    return result

                except Exception as e:
                    intentos += 1

                    if intentos >= max_intentos:
                        logger.error(f"❌ '{func.__name__}' falló después de {max_intentos} intentos: {str(e)}")
                        raise

                    logger.warning(f"⚠️  '{func.__name__}' falló (intento {intentos}/{max_intentos}): {str(e)}")
                    time.sleep(delay)

        return wrapper

    return decorator


def cache_result(ttl_seconds: int = 300):
    """
    Decorador simple de caché para funciones.
    Guarda el resultado en memoria por un tiempo determinado.
    """
    cache = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Crear una clave única basada en argumentos
            cache_key = str(args) + str(kwargs)
            current_time = time.time()

            # Si está en caché y no expiró, devolver resultado cacheado
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl_seconds:
                    logger.info(f"📦 Resultado de '{func.__name__}' obtenido de caché")
                    return result

            # Si no está en caché o expiró, ejecutar función
            logger.info(f"🔄 Ejecutando '{func.__name__}' y guardando en caché")
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)

            return result

        return wrapper

    return decorator