# Crear la función registrar libro

from fastapi.errores import CampoFaltanteError, IdNoNumericoError
from data.models import Libro
def registrar_libro(id, titulo, autor, genero, disponible: bool = True):
    """
    Crear un nuevo libro (HU-02)
    """
    if type(id) != int:
        raise IdNoNumericoError("El ID de libro tiene que ser un entero")
    if not id or not titulo or not autor or not genero:
        raise CampoFaltanteError("Faltan casos obligatorios")

    nuevo_libro = Libro(id,titulo, autor, genero,disponible)
    return {
        "id": nuevo_libro.id,
        "titulo": nuevo_libro.titulo,
        "autor": nuevo_libro.autor,
        "genero": nuevo_libro.genero,
        "disponible": nuevo_libro.disponible
    }