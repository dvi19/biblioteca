class CampoFaltanteError(Exception):
    """
    Se lanza Excepción cuando falta un campo obligatorio.
    """
    pass

class IdNoNumericoError(Exception):
    """Excepción para IDs que no son enteros."""
    pass

class LibroNoEncontradoError(Exception):
    """Excepción cuando el ID no existe en la base de datos."""
    pass

class LibroYaDisponibleError(Exception):
    """Excepción cuando intentas devolver un libro que no estaba prestado."""
    pass