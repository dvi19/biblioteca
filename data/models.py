from sqlalchemy import Column, Integer, String, Boolean
from data.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    genero = Column(String)
    disponible = Column(Boolean, default=True)