# Gestor de Bibliotecas 📚

Sistema completo de gestión de bibliotecas (catálogo, usuarios y préstamos) desarrollado como práctica final de Programación II. Backend en **FastAPI + SQLAlchemy**, frontend en **Streamlit**, todo orquestado con **Docker Compose**.

## Equipo
- Pablo Gómez
- Daniel Gradillas
- Jorge García
- Álvaro Gutiérrez
- Daniel Vaquerizo

## Tecnologías
- Python 3.10+
- FastAPI con APIRouter (libros, usuarios, préstamos)
- SQLAlchemy 2.x sobre SQLite
- Streamlit (multipágina)
- Pytest + pytest-cov
- Docker / Docker Compose

## Cómo ejecutar

### Con Docker (recomendado)
```bash
docker compose up --build
```
- API: http://localhost:8000 (docs en `/docs`)
- UI: http://localhost:8501

### En local (sin Docker)
```bash
# Backend
cd fastapi
pip install -r requirements.txt
uvicorn server:app --reload

# Frontend (en otra terminal)
cd streamlit
pip install -r requirements.txt
streamlit run Library_App.py
```

### Tests
```bash
cd fastapi
pytest --cov=. --cov-report=term-missing
```

## Arquitectura
- `fastapi/` — API REST con routers separados (`routers/libros.py`, `usuarios.py`, `prestamos.py`)
- `fastapi/data/` — Modelos SQLAlchemy y configuración de la BD
- `fastapi/utils/` — Decoradores, context managers y generadores
- `fastapi/config/` — Configuración de logging
- `streamlit/` — UI multipágina que consume la API

## Cumplimiento de SOLID

### SRP — Single Responsibility Principle
Cada módulo tiene una única responsabilidad:
- `data/models.py`: define los modelos de datos (Libro, Usuario, Prestamo).
- `data/database.py`: gestiona exclusivamente la conexión y sesiones de SQLAlchemy.
- `errores.py`: agrupa todas las excepciones personalizadas del dominio.
- `routers/libros.py`, `routers/usuarios.py`, `routers/prestamos.py`: cada router gestiona endpoints de una sola entidad.
- `config/logging_config.py`: aísla la configuración del sistema de logs.

### OCP — Open/Closed Principle
La arquitectura permite añadir funcionalidad **sin modificar** el código existente:
- Para añadir una nueva entidad (ej. "Categorías"), basta con crear un nuevo router e incluirlo en `server.py` con `app.include_router(...)`. No se modifica ningún router previo.
- Los decoradores (`@log_execution_time`, `@validar_campos`, `@retry`) extienden el comportamiento de las funciones sin alterarlas.

### LSP — Liskov Substitution Principle
Todos los modelos heredan de `Base` (`declarative_base()` de SQLAlchemy) y son sustituibles entre sí cuando la operación es genérica (`db.query(Modelo).all()` funciona igual para `Libro`, `Usuario` o `Prestamo`).

### ISP — Interface Segregation Principle
La API expone interfaces específicas por entidad: el cliente de libros solo conoce `/libros/...`, el de préstamos solo `/prestamos/...`. Ningún consumidor depende de endpoints que no usa.

### DIP — Dependency Inversion Principle
La capa de presentación (Streamlit) **no depende** directamente de SQLAlchemy ni de los modelos. Se comunica con la API REST mediante HTTP (módulo `requests`), de forma que la implementación concreta de la persistencia podría sustituirse (por ejemplo, cambiar SQLite por PostgreSQL) sin tocar la UI.

## Características técnicas implementadas
- Excepciones personalizadas (`errores.py`)
- Logging multinivel (`config/logging_config.py`)
- Decoradores propios (`@log_execution_time`, `@validar_campos`, `@retry`)
- Properties en los modelos (`estado_legible`, `dias_transcurridos`, etc.)
- Context managers (`db_session`, `db_transaction`, `measure_time`)
- Generadores (`utils/generadores.py`)
- Tests con Pytest

## Metodología
Trabajo en 3 sprints siguiendo XP: pair programming (commits con `co-authored-by`), TDD y refactoring continuo. Stand-ups recogidos en `DAILYS.md`.