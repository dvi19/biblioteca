
# Servidor principal de FastAPI - Gestor de Bibliotecas
# Arquitectura con APIRouter para separar responsabilidades (SOLID)

from fastapi import FastAPI
import pandas as pd
import os
from data.database import SessionLocal, engine, Base
from data.models import Libro as LibroDB

# Importar los routers
from routers import libros, usuarios, prestamos

# Crear tablas y poblar la BD con datos del CSV al inicio
Base.metadata.create_all(bind=engine)


def seed_database_if_empty():
    """Inserta libros del CSV si la BD está vacía"""
    db = SessionLocal()
    try:
        count = db.query(LibroDB).count()
        if count == 0:
            csv_path = './books.csv'
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, sep=';')
                for _, row in df.iterrows():
                    libro = LibroDB(
                        id=int(row['id']),
                        titulo=str(row['titulo']),
                        autor=str(row['autor']),
                        genero=str(row['genero']),
                        disponible=bool(row['disponible'])
                    )
                    db.add(libro)
                db.commit()
                print(f"✅ Base de datos inicializada con {len(df)} libros")
            else:
                print("⚠️ Archivo books.csv no encontrado")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al inicializar BD: {e}")
    finally:
        db.close()


# Ejecutar seed al inicio
seed_database_if_empty()


# Iniciación de al app
app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas con arquitectura modular (APIRouter)",
    version="2.0.0",
)


# routers
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)



@app.get("/")
def health_check():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "status": "online",
        "message": "API Gestor de Bibliotecas funcionando correctamente",
        "version": "2.0.0",
        "routers": ["libros", "usuarios", "prestamos"]
    }