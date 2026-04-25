import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Préstamo de Libros", page_icon="✍️")

st.markdown("# Gestionar Préstamo")
st.write("Formulario para realizar un préstamo.")

API_URL = "http://fastapi:8000"

with st.form("loan_form"):
    libro_id = st.number_input("ID del Libro", min_value=1, step=1, value=1)
    usuario = st.text_input("Nombre de Usuario", placeholder="Ej: Juan Pérez")
    fecha_prestamo = st.date_input("Fecha de Préstamo", value=date.today())

    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        if not usuario or usuario.strip() == "":
            st.error("⚠️ Debes introducir un nombre de usuario.")
        else:
            st.info(f"Registrando préstamo del libro {libro_id} para {usuario}...")

            try:
                # Creamos el payload completo
                payload = {
                    "id_libro": int(libro_id),
                    "usuario": usuario.strip(),
                    "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d")
                }

                response = requests.post(f"{API_URL}/prestamos/", json=payload)

                if response.status_code == 200:
                    st.success("✅ Préstamo registrado correctamente.")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error al registrar préstamo: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
