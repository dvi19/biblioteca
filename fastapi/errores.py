class CampoFaltanteError(Exception):
    """
    Se lanza Excepción cuando falta un campo obligatorio.
    """
    pass

class IdNoNumericoError(Exception):
    """Excepción para IDs que no son enteros."""
    pass