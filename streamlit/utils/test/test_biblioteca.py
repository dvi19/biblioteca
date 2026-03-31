import pytest
from fastapi.errores import CampoFaltanteError, IdNoNumericoError
from fastapi.main import registrar_libro
from data.database import SessionLocal
from data.models import Libro


def test_registrar_libro_exitoso():
    # LIMPIEZA: Borramos el libro 10 por si ya existiese de antes
    db = SessionLocal()
    libro_viejo = db.query(Libro).filter_by(id=10).first()
    if libro_viejo:
        db.delete(libro_viejo)
        db.commit()
    db.close()

    # EL TEST
    resultado = registrar_libro(10, "The Hobbit", "J.R.R. Tolkien", "Fantasía")

    assert resultado.id == 10
    assert resultado.titulo == "The Hobbit"
    assert resultado.autor == "J.R.R. Tolkien"

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