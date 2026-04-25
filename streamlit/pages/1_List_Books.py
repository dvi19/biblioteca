import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")

st.markdown("# 📖 Catálogo de Libros")
st.write("Listado de libros disponibles en la biblioteca.")

API_URL = "http://fastapi:8000"

# HU-07: Campo de búsqueda
st.subheader("🔍 Buscar Libros")
termino_busqueda = st.text_input(
    "Buscar por título o autor",
    placeholder="Ej: Orwell, 1984, Python...",
    help="Busca libros por título o autor. No distingue mayúsculas/minúsculas."
)

# Botón para mostrar todos los libros
col1, col2 = st.columns([1, 4])
with col1:
    mostrar_todos = st.button("📚 Mostrar Todos", use_container_width=True)

st.markdown("---")

try:
    # Si hay término de búsqueda, usar endpoint de búsqueda
    if termino_busqueda and termino_busqueda.strip() != "":
        response = requests.get(f"{API_URL}/libros/buscar", params={"termino": termino_busqueda})
        titulo_tabla = f"Resultados de búsqueda: '{termino_busqueda}'"
    else:
        # Si no hay búsqueda o se presionó "Mostrar Todos", mostrar todos
        response = requests.get(f"{API_URL}/libros/")
        titulo_tabla = "Todos los libros"

    if response.status_code == 200:
        data = response.json()
        libros = data.get("libros", [])

        if libros:
            st.subheader(titulo_tabla)

            # Mostrar número de resultados si es búsqueda
            if termino_busqueda and termino_busqueda.strip() != "":
                num_resultados = data.get("resultados", len(libros))
                st.info(f"📊 Se encontraron **{num_resultados}** libro(s)")

            # Crear DataFrame
            df = pd.DataFrame(libros)

            # Renombrar columnas
            df = df.rename(columns={
                'id': 'ID',
                'titulo': 'Título',
                'autor': 'Autor',
                'genero': 'Género',
                'disponible': 'Disponible'
            })

            # Mostrar tabla
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Disponible": st.column_config.CheckboxColumn(
                        "Disponible",
                        help="Indica si el libro está disponible para préstamo",
                    )
                }
            )
        else:
            # Criterio de aceptación: mensaje claro si no hay resultados
            if termino_busqueda and termino_busqueda.strip() != "":
                st.warning(f"🔍 No se encontraron libros que coincidan con '{termino_busqueda}'")
                st.info(
                    "💡 **Sugerencias:**\n- Verifica la ortografía\n- Intenta con palabras más cortas\n- Busca por autor en lugar de título (o viceversa)")
            else:
                st.warning("📚 No hay libros disponibles en el catálogo.")
    else:
        st.error(f"Error al obtener libros: {response.status_code}")

except Exception as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.info("Asegúrate de que el contenedor 'fastapi' está corriendo.")

st.markdown("---")
st.caption(
    "💡 **Tip**: La búsqueda no distingue entre mayúsculas y minúsculas. Puedes buscar 'orwell' y encontrará 'George Orwell'.")
