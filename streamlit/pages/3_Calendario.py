import streamlit as st
import requests
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendario Biblioteca", layout="wide")

# CAMBIO CRUCIAL PARA DOCKER:
API_URL = "http://fastapi:8000"

st.title("📅 HISTORIAL DE PRÉSTAMOS")

tab1, tab2 = st.tabs(["📚 Catálogo", "📆 Mi Calendario"])

with tab1:
    if st.button("Actualizar Catálogo"):
        try:
            # Tu endpoint en server.py es /libros/
            res = requests.get(f"{API_URL}/libros/")
            if res.status_code == 200:
                # Ajustamos para leer la lista de libros correctamente
                libros = res.json()
                st.table(libros)
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    usuario = st.text_input("Usuario:")
    if usuario:
        try:
            res = requests.get(f"{API_URL}/calendario/{usuario}")
            if res.status_code == 200:
                # El backend devuelve un objeto ListadoCalendario con el campo 'eventos'
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
                calendar(events=eventos, options=calendar_options)
        except Exception as e:
            st.error(f"Error de conexión: {e}")