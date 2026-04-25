import pytest
from errores import (
    CampoFaltanteError,
    IdNoNumericoError,
    LibroYaDisponibleError,
    EmailDuplicadoError,
    LibroDuplicadoError
)
from main import (
    consultar_catalogo,
    registrar_libro,
    eliminar_libro,
    actualizar_disponibilidad,
    devolver_libro,
    buscar_libro,
    registrar_prestamo,
    consultar_historial,
    registrar_usuario,
    consultar_usuarios
)
from data.database import SessionLocal
from data.models import Libro, Usuario
from sqlalchemy.exc import IntegrityError


def test_registrar_libro_exitoso():
    """HU-02: Registrar un libro con datos válidos"""
    # Limpieza previa
    db = SessionLocal()
    db.query(Libro).filter_by(id=10).delete()
    db.commit()
    db.close()

    resultado = registrar_libro(10, "The Hobbit", "J.R.R. Tolkien", "Fantasía")

    assert resultado.id == 10
    assert resultado.titulo == "The Hobbit"
    assert resultado.autor == "J.R.R. Tolkien"


def test_registrar_libro_incompleto():
    """HU-02: Error si falta un campo obligatorio"""
    with pytest.raises(CampoFaltanteError):
        registrar_libro(11, "", "J.K. Rowling", "Fantasía")


def test_registrar_libro_id_no_numerico():
    """HU-02: Error si el ID no es numérico"""
    with pytest.raises(IdNoNumericoError):
        registrar_libro("diez", "Título", "Autor", "Género")


def test_registrar_libro_id_duplicado():
    """HU-02: Error si se intenta registrar un ID que ya existe"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=15).delete()
    db.commit()
    db.close()

    # Registramos el libro por primera vez
    registrar_libro(15, "Libro Original", "Autor A", "Género A")

    # Intentamos registrar otro libro con el mismo ID
    with pytest.raises(LibroDuplicadoError):
        registrar_libro(15, "Libro Duplicado", "Autor B", "Género B")


def test_consultar_catalogo_devuelve_lista():
    """HU-01: El catálogo devuelve una lista de libros"""
    # Aseguramos que hay al menos un libro
    db = SessionLocal()
    db.query(Libro).filter_by(id=20).delete()
    db.commit()
    db.close()

    registrar_libro(20, "1984", "George Orwell", "Distopía")

    resultado = consultar_catalogo()

    assert isinstance(resultado, list)
    assert len(resultado) > 0
    assert any(libro.titulo == "1984" for libro in resultado)


def test_registrar_usuario_exitoso():
    """HU-03: Registrar un usuario con nombre y email válidos"""
    db = SessionLocal()
    db.query(Usuario).filter_by(email="test@email.com").delete()
    db.commit()
    db.close()

    resultado = registrar_usuario("Juan Pérez", "test@email.com")

    assert resultado.nombre == "Juan Pérez"
    assert resultado.email == "test@email.com"


def test_registrar_usuario_email_duplicado():
    """HU-03: Error si el email ya existe"""
    db = SessionLocal()
    db.query(Usuario).filter_by(email="duplicado@email.com").delete()
    db.commit()
    db.close()

    # Primer registro
    registrar_usuario("Usuario 1", "duplicado@email.com")

    # Intento de duplicado
    with pytest.raises(EmailDuplicadoError):
        registrar_usuario("Usuario 2", "duplicado@email.com")


def test_registrar_usuario_campos_vacios():
    """HU-03: Error si falta nombre o email"""
    with pytest.raises(CampoFaltanteError):
        registrar_usuario("", "email@test.com")

    with pytest.raises(CampoFaltanteError):
        registrar_usuario("Nombre", "")


def test_consultar_usuarios():
    """HU-03: Listar todos los usuarios registrados"""
    db = SessionLocal()
    db.query(Usuario).filter_by(email="listar@test.com").delete()
    db.commit()
    db.close()

    registrar_usuario("Usuario Test", "listar@test.com")

    usuarios = consultar_usuarios()

    assert isinstance(usuarios, list)
    assert len(usuarios) > 0
    assert any(u.email == "listar@test.com" for u in usuarios)


def test_eliminar_libro_exitoso():
    """HU-03: Verificar que un libro se borra correctamente"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=50).delete()
    db.commit()
    db.close()

    registrar_libro(50, "Libro a Borrar", "Autor X", "Género Y")

    fue_borrado = eliminar_libro(50)

    assert fue_borrado is True
    catalogo = consultar_catalogo()
    assert not any(libro.id == 50 for libro in catalogo)


def test_actualizar_disponibilidad_exitoso():
    """HU-04: Cambiar el estado de disponibilidad de un libro"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=30).delete()
    db.commit()
    db.close()

    registrar_libro(30, "El Quijote", "Cervantes", "Clásico", disponible=True)

    resultado = actualizar_disponibilidad(30, False)

    assert resultado.disponible is False
    assert resultado.id == 30


def test_devolver_libro_exitoso():
    """HU-05: Un libro prestado vuelve a estar disponible"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=60).delete()
    db.commit()
    db.close()

    registrar_libro(60, "Libro Prestado", "Autor F", "Ensayo", disponible=False)

    resultado = devolver_libro(60)

    assert resultado.disponible is True
    assert resultado.id == 60


def test_devolver_libro_ya_disponible_error():
    """HU-05: Error si el libro ya está disponible"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=70).delete()
    db.commit()
    db.close()

    registrar_libro(70, "Libro en Estantería", "Autor G", "Poesía", disponible=True)

    with pytest.raises(LibroYaDisponibleError):
        devolver_libro(70)


def test_consultar_historial_prestamo():
    """HU-06: Consultar historial de préstamos de un usuario"""
    registrar_prestamo(id_libro=10, usuario="Guti", fecha_texto="2024-01-15")

    historial = consultar_historial("Guti")

    assert len(historial) > 0
    assert any(p.fecha_prestamo == "2024-01-15" for p in historial)
    assert any(p.usuario == "Guti" for p in historial)


def test_buscar_libro_por_coincidencia():
    """HU-07: Búsqueda case-insensitive por título/autor"""
    db = SessionLocal()
    db.query(Libro).filter_by(id=100).delete()
    db.commit()
    db.close()

    registrar_libro(100, "1984", "George Orwell", "Distopía")

    resultados = buscar_libro("orwell")

    assert len(resultados) > 0
    assert any("Orwell" in libro.autor for libro in resultados)


    def test_obtener_eventos_calendario_activo():
        """HU-08: Eventos activos se muestran en rojo"""
        from main import obtener_eventos_calendario, registrar_prestamo
        from data.database import SessionLocal
        from data.models import Prestamo

        db = SessionLocal()
        db.query(Prestamo).filter_by(usuario="CalendarioTest1").delete()
        db.commit()
        db.close()

        registrar_prestamo(id_libro=1, usuario="CalendarioTest1", fecha_texto="2024-01-20")

        eventos = obtener_eventos_calendario("CalendarioTest1")

        assert len(eventos) > 0
        assert eventos[0]["start"] == "2024-01-20"
        assert eventos[0]["backgroundColor"] == "#ff4b4b"  # Rojo (activo)

    def test_obtener_eventos_calendario_devuelto():
        """HU-08: Eventos devueltos se muestran en verde"""
        from main import obtener_eventos_calendario, registrar_prestamo, devolver_libro
        from data.database import SessionLocal
        from data.models import Prestamo

        db = SessionLocal()
        db.query(Prestamo).filter_by(usuario="CalendarioTest2").delete()
        db.commit()
        db.close()

        # Registramos y devolvemos
        registrar_prestamo(id_libro=1, usuario="CalendarioTest2", fecha_texto="2024-01-20")
        devolver_libro(1)

        eventos = obtener_eventos_calendario("CalendarioTest2")

        # Verificamos que hay eventos devueltos en verde
        eventos_devueltos = [e for e in eventos if e["backgroundColor"] == "#28a745"]
        assert len(eventos_devueltos) > 0

    def test_obtener_eventos_calendario_sin_prestamos():
        """HU-08: Usuario sin préstamos devuelve lista vacía"""
        from main import obtener_eventos_calendario

        eventos = obtener_eventos_calendario("UsuarioSinPrestamos999")

        assert eventos == []