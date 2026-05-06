"""
Tests unitarios con Mocks — aíslan la lógica de negocio de la base de datos.
Cumple con el requisito XP de "usando Mocks para aislar dependencias".
"""
import pytest
from unittest.mock import MagicMock, patch
from errores import (
    CampoFaltanteError,
    IdNoNumericoError,
    LibroNoEncontradoError,
    LibroDuplicadoError,
    LibroYaDisponibleError,
    EmailDuplicadoError,
)


@patch("main.SessionLocal")
def test_registrar_libro_exitoso_mock(mock_session_local):
    """Registrar libro con BD mockeada (no toca SQLite)"""
    from main import registrar_libro

    # Configurar el mock de la sesión
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No existe ID duplicado

    resultado = registrar_libro(999, "Libro Mock", "Autor Mock", "Género Mock")

    # Verificamos que se llamó add y commit
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


@patch("main.SessionLocal")
def test_registrar_libro_duplicado_mock(mock_session_local):
    """Registrar libro con ID duplicado (BD mockeada devuelve un libro existente)"""
    from main import registrar_libro

    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    libro_existente = MagicMock()
    libro_existente.titulo = "Existente"
    mock_db.query.return_value.filter.return_value.first.return_value = libro_existente

    with pytest.raises(LibroDuplicadoError):
        registrar_libro(999, "Otro libro", "Otro autor", "Otro género")


def test_registrar_libro_id_no_numerico_mock():
    """No se necesita mock de BD: la validación es previa"""
    from main import registrar_libro
    with pytest.raises(IdNoNumericoError):
        registrar_libro("abc", "Título", "Autor", "Género")


def test_registrar_libro_campos_vacios_mock():
    """No se necesita mock de BD: la validación es previa"""
    from main import registrar_libro
    with pytest.raises(CampoFaltanteError):
        registrar_libro(998, "", "Autor", "Género")


@patch("main.SessionLocal")
def test_eliminar_libro_no_existe_mock(mock_session_local):
    """Eliminar un libro inexistente devuelve False"""
    from main import eliminar_libro

    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = None

    resultado = eliminar_libro(99999)

    assert resultado is False
    mock_db.delete.assert_not_called()


@patch("main.SessionLocal")
def test_actualizar_disponibilidad_libro_no_existe_mock(mock_session_local):
    """Actualizar disponibilidad de un libro inexistente lanza LibroNoEncontradoError"""
    from main import actualizar_disponibilidad

    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(LibroNoEncontradoError):
        actualizar_disponibilidad(99999, False)


@patch("main.SessionLocal")
def test_devolver_libro_ya_disponible_mock(mock_session_local):
    """Devolver un libro que ya está disponible lanza LibroYaDisponibleError"""
    from main import devolver_libro

    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    libro_mock = MagicMock()
    libro_mock.disponible = True
    mock_db.query.return_value.filter.return_value.first.return_value = libro_mock

    with pytest.raises(LibroYaDisponibleError):
        devolver_libro(50)


@patch("main.SessionLocal")
def test_registrar_usuario_email_duplicado_mock(mock_session_local):
    """Registrar usuario con email ya existente lanza EmailDuplicadoError"""
    from main import registrar_usuario

    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    usuario_existente = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = usuario_existente

    with pytest.raises(EmailDuplicadoError):
        registrar_usuario("Test User", "ya@existe.com")