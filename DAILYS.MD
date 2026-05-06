# Stand-ups diarios

Registro de reuniones diarias del equipo siguiendo metodología eXtreme Programming (XP). Cada entrada documenta: asistentes, trabajo realizado, próximos objetivos y bloqueos.

**Equipo:** Pablo Gómez, Daniel Gradillas, Jorge García, Álvaro Gutiérrez, Daniel Vaquerizo.

---

## Sprint 1 — Migración a base de datos y CRUD inicial

### 31/03/2026
- **Asistentes:** Pablo, Jorge, Daniel Gradillas
- **Hecho ayer:** Lectura del enunciado, reparto de historias de usuario y diseño inicial del modelo de datos.
- **Para hoy:** Preparar la función para consultar el listado de libros disponibles y configurar `registrar_libro` para que cada vez que se añada un libro quede registrado en la base de datos.
- **Bloqueos:** Dudas con SQLAlchemy al pasar del CSV original al modelo persistente.

### 02/04/2026
- **Asistentes:** Pablo, Jorge, Álvaro
- **Hecho ayer:** Listado de libros y `registrar_libro` operativos.
- **Para hoy:** Cerrar HU-03 (eliminar libro lanzando excepción si no existe) y HU-04 (cambiar disponibilidad del libro al realizar el préstamo).
- **Bloqueos:** Ninguno.

### 03/04/2026
- **Asistentes:** Pablo, Álvaro, Daniel Vaquerizo, Daniel Gradillas
- **Hecho ayer:** HU-03 y HU-04 cerradas.
- **Para hoy:** Implementar HU-05 (devolver un libro ya prestado), HU-07 (búsqueda de libros por título o autor sin distinguir mayúsculas/minúsculas) y actualizar `requirements.txt`.
- **Bloqueos:** Ninguno.

### 05/04/2026
- **Asistentes:** Pablo, Jorge, Daniel Gradillas
- **Hecho ayer:** HU-05 y HU-07 funcionando.
- **Para hoy:** Cerrar HU-06 (consulta del historial de un usuario) lanzando excepción cuando el historial esté vacío.
- **Bloqueos:** Ninguno.

---

## Sprint 2 — Refactor, robustez e integración con UI

### 17/04/2026
- **Asistentes:** Pablo, Daniel Vaquerizo
- **Hecho ayer:** Pausa por Semana Santa.
- **Para hoy:** Dejar una primera versión funcional con la base de datos completamente mapeada.
- **Bloqueos:** Algunas inconsistencias entre los modelos y los endpoints existentes.

### 24/04/2026
- **Asistentes:** Pablo, Álvaro
- **Hecho ayer:** Versión funcional con BD mapeada.
- **Para hoy:** Finalizar la última historia de usuarios y conseguir que el sistema arranque correctamente en localhost.
- **Bloqueos:** Ninguno.

### 25/04/2026
- **Asistentes:** Pablo, Jorge, Daniel Vaquerizo
- **Hecho ayer:** Sistema arrancando en local.
- **Para hoy:** Sesión intensiva de cierre y testing inicial:
  - Modificación de código para que se vea bien el préstamo de libros, se actualice el catálogo y aparezca el calendario con los libros que ha reservado cada usuario.
  - Modificar HU-02 y HU-05 para que aparezcan correctamente en el localhost.
  - Cerrar HU-07 corrigiendo el error encontrado al buscar libros.
  - Pulir HU-03 y reordenar las páginas de Streamlit para que se vea más profesional.
  - Configurar pytest y medir cobertura: alcanzado un **84%**.
- **Bloqueos:** Ninguno.

### 26/04/2026
- **Asistentes:** Pablo, Daniel Gradillas, Álvaro
- **Hecho ayer:** Tests configurados y cobertura medida.
- **Para hoy:** Refactor de robustez:
  - Crear el sistema de registro de logs.
  - Separar los endpoints en routers (`libros.py`, `usuarios.py`, `prestamos.py`) para mejorar organización y limpieza del código.
  - Implementar la caché en Streamlit para mayor velocidad al recargar la página.
- **Bloqueos:** Ninguno.

### 27/04/2026
- **Asistentes:** Pablo
- **Hecho ayer:** Refactor de routers, logging y caché cerrado.
- **Para hoy:** Atacar las características avanzadas:
  - Completar los diferentes decoradores que se pueden poner.
  - Añadir las properties en los modelos.
  - Completar context managers.
  - Hacer los generadores necesarios.
- **Bloqueos:** Ninguno.

---

## Sprint 3 — Calidad, CI/CD y entrega final

### 06/05/2026
- **Asistentes:** Daniel Gradillas
- **Hecho ayer:** Auditoría del estado del proyecto antes de la entrega.
- **Para hoy:** Cierre completo de la entrega final:
  - Actualización inicial del `README.md` con una explicación global del proyecto.
  - Configurar `conftest.py` en `fastapi/` para resolver los errores de importación al ejecutar pytest.
  - Probar todos los tests y modificar los problemas que hacían que no pasasen (ajuste del decorador `@validar_campos` para que lance `CampoFaltanteError` en lugar de `ValueError`).
  - Eliminar archivos basura y caché del repositorio (`Zone.Identifier`, `__pycache__`, `.pytest_cache`, logs, BD local).
  - Solucionar problemas en `main.py` y la indentación de los tests del calendario, que impedía que se ejecutaran.
  - Corregir el bug de `devolver_libro` para que actualice también el `Prestamo` asociado (`activo = False`, `fecha_devolucion`).
  - Implementar la validación de formato de fecha mediante `FormatoFechaError`, que estaba definido pero sin uso.
  - Crear la carpeta `.github/workflows/` con `tests.yml` para que en cada `git push` se ejecuten los tests automáticamente.
  - Añadir suite de tests con Mocks (`test_biblioteca_mocks.py`) usando `unittest.mock` para aislar la base de datos.
  - Reescribir el `README.md` con la documentación completa de los principios SOLID y los niveles de evaluación cubiertos (Aprobado, Notable, Sobresaliente).
  - Corregir el formato del árbol de arquitectura en el `README.md`.
- **Bloqueos:** Ninguno. Entrega lista, CI en verde.


### 06/05/2026 — Sesión de cierre y limpieza
- **Asistentes:** Álvaro, Daniel Gradillas, Jorge
- **Hecho ayer:** Cierre de la entrega final con CI en verde y 26 tests pasando.
- **Para hoy:** Revisión general y últimos detalles:
  - Eliminar la carpeta `logs/` del repositorio y añadir `logs/` y `*.log` al `.gitignore` para evitar que se vuelvan a colar.
  - Verificación final del estado del proyecto.
- **Bloqueos:** Ninguno. Proyecto cerrado.