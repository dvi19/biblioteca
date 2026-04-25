import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Esto detecta la ruta automáticamente.
basedir = os.path.abspath(os.path.dirname(__file__))

# Esto genera la URL final usando la ruta detectada
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(basedir, 'biblioteca.db')

# Creamos el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Configuramos la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para que nuestros modelos hereden de ella
Base = declarative_base()