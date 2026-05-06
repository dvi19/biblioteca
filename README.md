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
- FastAPI con `APIRouter` (libros, usuarios, préstamos)
- SQLAlchemy 2.x sobre SQLite
- Streamlit (multipágina)
- Pytest + pytest-cov + `unittest.mock`
- Docker / Docker Compose
- GitHub Actions (CI/CD)

## Cómo ejecutar

### Con Docker (recomendado)
```bash
docker compose up --build
```
- API: http://localhost:8000 (docs interactivas en `/docs`)
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
biblioteca/
├── fastapi/
│   ├── server.py             # Punto de entrada de la API + montaje de routers
│   ├── main.py               # Lógica de negocio
│   ├── errores.py            # Excepciones personalizadas
│   ├── conftest.py           # Configuración de pytest
│   ├── routers/              # Endpoints separados por entidad
│   │   ├── libros.py
│   │   ├── usuarios.py
│   │   └── prestamos.py
│   ├── data/                 # Modelos SQLAlchemy y conexión BD
│   │   ├── database.py
│   │   └── models.py
│   ├── utils/                # Decoradores, context managers, generadores
│   ├── config/               # Configuración de logging
│   └── test_biblioteca*.py   # Suites de tests (integración + mocks)
├── streamlit/                # Interfaz multipágina
├── .github/workflows/        # CI/CD
├── docker-compose.yml
├── DAILYS.md
└── README.md

## Niveles de evaluación cumplidos

Marcamos a continuación los requisitos cubiertos según el sistema incremental del enunciado.

### ✅ Aprobado — Funcionamiento básico
- Listado de libros, alta de usuarios y gestión de préstamos.
- Commits semánticos en Git.
- Tests unitarios con **Mocks** (`unittest.mock`) para aislar dependencias de la base de datos (`fastapi/test_biblioteca_mocks.py`).
- Código limpio y organizado por responsabilidades.

### ✅ Notable — Robustez y calidad
- **Excepciones personalizadas** tipadas (`errores.py`): `CampoFaltanteError`, `LibroDuplicadoError`, `LibroNoEncontradoError`, `EmailDuplicadoError`, `LibroYaDisponibleError`, `IdNoNumericoError`, `HistorialVacioError`, `FormatoFechaError`.
- **Logging multinivel** (`config/logging_config.py`) con `INFO`, `WARNING`, `ERROR`.
- **APIRouter** para separar endpoints (`routers/libros.py`, `usuarios.py`, `prestamos.py`).
- **Caché en Streamlit** mediante `@st.cache_data` para reducir llamadas a la API.
- **CI/CD con GitHub Actions** que ejecuta los tests en cada push (`.github/workflows/tests.yml`).

### ✅ Sobresaliente — Ingeniería del Software
- **Decoradores propios** (`utils/decoradores.py`):
  - `@log_execution_time`: mide y registra el tiempo de ejecución.
  - `@validar_campos`: valida que los campos obligatorios no estén vacíos.
  - `@retry`: reintentos automáticos ante fallos transitorios.
- **Properties** (`data/models.py`): `estado_legible`, `info_completa`, `dias_transcurridos`, `descripcion_estado`, `email_dominio`, `iniciales`.
- **Context managers** (`utils/context_managers.py`): `db_session`, `db_transaction`, `measure_time`.
- **Generadores** (`utils/generadores.py`) para procesar grandes volúmenes de datos con `yield`.

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

## Suite de tests

El proyecto incluye dos suites complementarias:

- **`test_biblioteca.py`** — Tests de integración contra la BD real (SQLite). Verifican el comportamiento end-to-end de las funciones de negocio.
- **`test_biblioteca_mocks.py`** — Tests unitarios con `unittest.mock` que aíslan la lógica de la base de datos. Mockean `SessionLocal` para validar reglas de negocio sin depender de la persistencia.

Cobertura ejecutable con `pytest --cov=. --cov-report=term-missing`.

## Metodología

Trabajo en **3 sprints** siguiendo eXtreme Programming (XP):
- **Pair programming** evidenciado en commits con `co-authored-by`.
- **TDD**: los tests guiaron el desarrollo de las nuevas funcionalidades.
- **Refactoring continuo**: el esqueleto inicial leía de un CSV en cada petición; refactorizamos para usar SQLAlchemy + APIRouter.
- **Integración Continua**: GitHub Actions ejecuta los tests automáticamente en cada `push` y `pull_request`.
- **Stand-ups diarios** registrados en [`DAILYS.md`](DAILYS.md).