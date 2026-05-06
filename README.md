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
- **SRP**: cada router gestiona una única entidad; `main.py` separa lógica de negocio de los endpoints.
- **OCP**: nuevas funcionalidades se añaden creando routers/decoradores sin modificar los existentes.
- **LSP**: los modelos heredan de `Base` de SQLAlchemy y son sustituibles.
- **ISP**: cada router expone solo los endpoints que le corresponden.
- **DIP**: la UI depende de la API (HTTP), no de la BD directamente.

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