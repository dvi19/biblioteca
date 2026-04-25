import streamlit as st
import requests

st.set_page_config(page_title="Añadir Libro", page_icon="➕")

st.markdown("# ➕ Añadir Nuevo Libro")
st.write("Formulario para registrar un libro en el catálogo.")

API_URL = "http://fastapi:8000"

with st.form("add_book_form"):
    st.subheader("Datos del Libro")

    libro_id = st.number_input("ID del Libro", min_value=1, step=1, help="ID único para el libro")
    titulo = st.text_input("Título *", placeholder="Ej: Don Quijote de la Mancha")
    autor = st.text_input("Autor *", placeholder="Ej: Miguel de Cervantes")
    genero = st.selectbox(
        "Género *",
        ["Clásico", "Distopía", "Técnico", "Realismo mágico", "Ciencia ficción", "Fantasía", "Terror", "Romance",
         "Histórico"]
    )
    disponible = st.checkbox("Disponible", value=True, help="Marca si el libro está disponible para préstamo")

    st.markdown("---")
    submitted = st.form_submit_button("📚 Registrar Libro", use_container_width=True)

    if submitted:
        # Validación
        if not titulo or titulo.strip() == "":
            st.error("⚠️ El título es obligatorio.")
        elif not autor or autor.strip() == "":
            st.error("⚠️ El autor es obligatorio.")
        else:
            st.info(f"Registrando libro '{titulo}'...")

            try:
                payload = {
                    "id": int(libro_id),
                    "titulo": titulo.strip(),
                    "autor": autor.strip(),
                    "genero": genero,
                    "disponible": disponible
                }

                response = requests.post(f"{API_URL}/libros/", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {data['message']}")

                    # Mostrar resumen
                    st.json(data['libro'])

                    st.balloons()
                else:
                    st.error(f"❌ Error al registrar libro: {response.status_code}")
                    try:
                        st.json(response.json())
                    except:
                        st.text(response.text)

            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")

st.markdown("---")
st.info("💡 **Tip**: Después de añadir un libro, puedes verlo en 'List Books' o 'Calendario' → Tab 'Catálogo'")