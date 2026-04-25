class CampoFaltanteError(Exception):
    """
    Se lanza Excepción cuando falta un campo obligatorio.
    """
    pass

class EmailDuplicadoError(Exception):
    """Excepción cuando se intenta registrar un email que ya existe."""
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

class HistorialVacioError(Exception):
    """Excepción cuando un usuario existe pero no tiene préstamos registrados."""
    pass

class FormatoFechaError(Exception):
    """Excepción cuando la fecha no cumple el formato AAAA-MM-DD."""
    pass

class LibroDuplicadoError(Exception):
    """Excepción cuando se intenta registrar un libro con un ID que ya existe."""
    pass

