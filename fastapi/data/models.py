from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from data.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    genero = Column(String)
    disponible = Column(Boolean, default=True)

    @property
    def estado_legible(self) -> str:
        """Devuelve el estado del libro en formato legible"""
        return "📗 Disponible" if self.disponible else "📕 Prestado"

    @property
    def info_completa(self) -> str:
        """Devuelve información completa del libro"""
        return f"{self.titulo} - {self.autor} ({self.genero}) - {self.estado_legible}"


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    id_libro = Column(Integer, ForeignKey("libros.id"))
    usuario = Column(String)
    fecha_prestamo = Column(String)
    fecha_devolucion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

    @property
    def esta_activo(self) -> bool:
        """Indica si el préstamo está activo"""
        return self.activo

    @property
    def dias_transcurridos(self) -> int:
        """Calcula los días transcurridos desde el préstamo"""
        from datetime import datetime
        try:
            fecha_inicio = datetime.strptime(self.fecha_prestamo, "%Y-%m-%d")
            fecha_fin = datetime.now() if self.activo else datetime.strptime(self.fecha_devolucion, "%Y-%m-%d")
            return (fecha_fin - fecha_inicio).days
        except:
            return 0

    @property
    def descripcion_estado(self) -> str:
        """Describe el estado del préstamo"""
        if self.activo:
            return f"🔴 Activo ({self.dias_transcurridos} días)"
        else:
            return f"✅ Devuelto (duró {self.dias_transcurridos} días)"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    @property
    def email_dominio(self) -> str:
        """Extrae el dominio del email"""
        try:
            return self.email.split('@')[1] if '@' in self.email else "desconocido"
        except:
            return "desconocido"

    @property
    def nombre_completo_mayusculas(self) -> str:
        """Devuelve el nombre en mayúsculas"""
        return self.nombre.upper()

    @property
    def iniciales(self) -> str:
        """Devuelve las iniciales del nombre"""
        palabras = self.nombre.split()
        return ''.join([p[0].upper() for p in palabras if p])