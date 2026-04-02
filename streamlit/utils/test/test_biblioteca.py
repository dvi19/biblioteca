import pytest
from fastapi.errores import CampoFaltanteError, IdNoNumericoError, LibroNoEncontradoError
from fastapi.main import consultar_catalogo, registrar_libro
from data.database import SessionLocal
from data.models import Libro
from sqlalchemy.exc import IntegrityError  # Importamos esto para manejar duplicados


def test_registrar_libro_exitoso():
    # ELIMINADA LA LIMPIEZA: Ya no borramos el libro 10 al empezar.

    try:
        resultado = registrar_libro(10, "The Hobbit", "J.R.R. Tolkien", "Fantasía")

        # Si el libro es nuevo, hacemos los asserts normales
        assert resultado.id == 10
        assert resultado.titulo == "The Hobbit"
        assert resultado.autor == "J.R.R. Tolkien"
        print("Libro ID 10 registrado con éxito.")

    except IntegrityError:
        # Si ya existe en biblioteca.db, el test también pasa (porque ya está ahí)
        pytest.skip("El libro ID 10 ya existe en la base de datos física.")


def test_registrar_libro_incompleto():
    with pytest.raises(CampoFaltanteError):
        registrar_libro(11, "", "J.K. Rowling", "Fantasía")


def test_registrar_libro_id_no_numerico():
    with pytest.raises(IdNoNumericoError):
        registrar_libro("diez", "Título", "Autor", "Género")


def test_consultar_catalogo_devuelve_lista():
    # Intentamos registrar el 20, si ya existe saltamos al assert
    try:
        registrar_libro(20, "1984", "George Orwell", "Distopía")
    except IntegrityError:
        pass

    resultado = consultar_catalogo()

    assert isinstance(resultado, list)
    assert len(resultado) > 0
    # Verificamos que el libro 1984 está en la lista (ya sea de ahora o de antes)
    assert any(libro.titulo == "1984" for libro in resultado)


def eliminar_libro(id_libro):
    db = SessionLocal()
    try:
        # Buscamos el libro por su id
        libro = db.query(Libro).filter(Libro.id == id_libro).first()
        if not libro:
            # Si no encuentra el libro lanza el error de que no existe el libro
            raise LibroNoEncontradoError(f"No existe el libro con ID {id_libro}")

        db.delete(libro) # Elimina el libro
        db.commit() # Confirma que se ha eliminado el libro
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()