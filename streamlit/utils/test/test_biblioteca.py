import pytest
from fastapi.errores import CampoFaltanteError, IdNoNumericoError
from fastapi.main import registrar_libro

def test_registrar_libro_exitoso():
    """
    Test para ver que funcione la función resgitrar_libro.
    """

    id_test = 10
    titulo_test = "The Hobbit"
    autor_test = "J.R.R. Tolkien"
    genero_test = "Fantasía"

    resultado = registrar_libro(id_test, titulo_test, autor_test, genero_test, disponible=True)

    assert resultado["id"] == id_test
    assert resultado["titulo"] == titulo_test
    assert resultado["autor"] == autor_test
    assert resultado["disponible"] is True

def test_registrar_libro_incompleto():
    """
    Test para verificar que se lanza la excepción si faltan campos.
    """
    id_test = 11
    titulo_vacio = ""
    autor_test = "J.K. Rowling"
    genero_test = "Fantasía"

    with pytest.raises(CampoFaltanteError):
        registrar_libro(id_test, titulo_vacio, autor_test, genero_test)

def test_registrar_libro_id_no_numerico():
    """Test para validar que el ID debe ser un número."""
    with pytest.raises(IdNoNumericoError):
        registrar_libro("diez", "Título", "Autor", "Género")