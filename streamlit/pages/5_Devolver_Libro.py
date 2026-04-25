import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Devolver Libro", page_icon="📥")

st.markdown("# 📥 Devolver Libro")
st.write("Marca un libro prestado como devuelto para que quede disponible nuevamente.")

API_URL = "http://fastapi:8000"

# Primero mostramos los libros NO disponibles
st.subheader("📕 Libros actualmente prestados")

try:
    response = requests.get(f"{API_URL}/libros/")
    if response.status_code == 200:
        libros = response.json().get("libros", [])
        libros_prestados = [libro for libro in libros if not libro['disponible']]

        if libros_prestados:
            df = pd.DataFrame(libros_prestados)
            df = df.rename(columns={
                'id': 'ID',
                'titulo': 'Título',
                'autor': 'Autor',
                'genero': 'Género'
            })
            st.dataframe(df[['ID', 'Título', 'Autor', 'Género']], use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No hay libros prestados en este momento. ¡Todos están disponibles!")
except Exception as e:
    st.warning(f"⚠️ No se pudo cargar el catálogo: {e}")

st.markdown("---")

# Formulario de devolución
with st.form("return_book_form"):
    st.subheader("Registrar Devolución")

    libro_id = st.number_input(
        "ID del Libro a Devolver",
        min_value=1,
        step=1,
        help="Introduce el ID del libro que se está devolviendo"
    )

    submitted = st.form_submit_button("✅ Registrar Devolución", use_container_width=True)

    if submitted:
        st.info(f"Procesando devolución del libro {libro_id}...")

        try:
            response = requests.put(f"{API_URL}/libros/{libro_id}/devolver")

            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ {data['message']}")
                st.json(data['libro'])
                st.balloons()

                st.info("🔄 Recarga la página para ver el libro actualizado en la lista de prestados.")

            elif response.status_code == 400:
                error_detail = response.json().get('detail', 'Error desconocido')
                st.error(f"❌ {error_detail}")
            else:
                st.error(f"❌ Error: {response.status_code}")
                try:
                    st.json(response.json())
                except:
                    st.text(response.text)

        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

st.markdown("---")
st.info("💡 **Tip**: Después de devolver un libro, aparecerá como disponible en el catálogo.")