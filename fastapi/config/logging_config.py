# Configuración para los logs


import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Configura el sistema de logging con rotación de archivos"""

    # Crear directorio
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configuración del logger principal
    logger = logging.getLogger("biblioteca")
    logger.setLevel(logging.INFO)

    # Evitar duplicados
    if logger.handlers:
        return logger

    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para archivo (con rotación)
    file_handler = RotatingFileHandler(
        f"{log_dir}/biblioteca.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formato para consola
    console_formatter = logging.Formatter(
        '%(levelname)s - %(funcName)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Añadir handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Logger global
logger = setup_logging()