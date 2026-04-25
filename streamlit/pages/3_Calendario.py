import streamlit as st
import requests
import pandas as pd
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendario Biblioteca", layout="wide")

API_URL = "http://fastapi:8000"

st.title("📅 HISTORIAL DE PRÉSTAMOS")

tab1, tab2 = st.tabs(["📚 Catálogo", "📆 Mi Calendario"])

with tab1:
    st.subheader("Libros disponibles")
    if st.button("Actualizar Catálogo"):
        try:
            res = requests.get(f"{API_URL}/libros/")
            if res.status_code == 200:
                datos = res.json()

                # Extraemos la lista de libros
                lista = datos.get("libros", [])

                if lista:
                    # Creamos el DataFrame directamente
                    df = pd.DataFrame(lista)

                    # Renombramos columnas
                    df = df.rename(columns={
                        'id': 'ID',
                        'titulo': 'TÍTULO',
                        'autor': 'AUTOR',
                        'genero': 'GÉNERO',
                        'disponible': 'DISPONIBLE'
                    })

                    # Mostramos la tabla
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning("No hay libros en el catálogo.")
            else:
                st.error("Error al obtener datos")
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("Mi Calendario")
    usuario = st.text_input("Usuario:")
    if usuario:
        try:
            res = requests.get(f"{API_URL}/calendario/{usuario}")
            if res.status_code == 200:
                eventos = res.json().get("eventos", [])
                calendar_options = {
                    "initialView": "dayGridMonth",
                    "headerToolbar": {
                        "left": "prev,next today",
                        "center": "title",
                        "right": "dayGridMonth,dayGridWeek,dayGridDay"
                    },
                    "locale": "es"
                }
                st.markdown("<style>.fc-media-screen { height: 700px !important; }</style>", unsafe_allow_html=True)
                calendar(events=eventos, options=calendar_options)
        except Exception as e:
            st.error(f"Error en calendario: {e}")