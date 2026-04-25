from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from data.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    genero = Column(String)
    disponible = Column(Boolean, default=True)


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    id_libro = Column(Integer, ForeignKey("libros.id"))
    usuario = Column(String)
    fecha_prestamo = Column(String)
    fecha_devolucion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)


    ## libro = Libro (**unlibro)