import streamlit as st
import requests
import pandas as pd
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendario Biblioteca", layout="wide")

API_URL = "http://fastapi:8000"

st.title("📅 HISTORIAL DE PRÉSTAMOS")


# FUNCIONES CON CACHÉ
@st.cache_data(ttl=300)  # Cache por 5 minutos
def obtener_catalogo():
    """Obtiene el catálogo de libros con caché"""
    res = requests.get(f"{API_URL}/libros/")
    if res.status_code == 200:
        return res.json().get("libros", [])
    return []


@st.cache_data(ttl=60)  # Cache por 1 minuto
def obtener_eventos_usuario(usuario):
    """Obtiene eventos del calendario de un usuario con caché"""
    res = requests.get(f"{API_URL}/calendario/{usuario}")
    if res.status_code == 200:
        return res.json().get("eventos", [])
    return []


@st.cache_data(ttl=60)  # Cache por 1 minuto
def obtener_historial_usuario(usuario):
    """Obtiene historial de préstamos de un usuario con caché"""
    res = requests.get(f"{API_URL}/prestamos/historial/{usuario}")
    if res.status_code == 200:
        return res.json().get("prestamos", [])
    return []


tab1, tab2, tab3 = st.tabs(["📚 Catálogo", "📆 Mi Calendario", "📋 Historial Completo"])

with tab1:
    st.subheader("Libros disponibles")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Actualizar Catálogo", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    try:
        lista = obtener_catalogo()

        if lista:
            df = pd.DataFrame(lista)
            df = df.rename(columns={
                'id': 'ID',
                'titulo': 'TÍTULO',
                'autor': 'AUTOR',
                'genero': 'GÉNERO',
                'disponible': 'DISPONIBLE'
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption("💾 Datos cacheados - actualización automática cada 5 minutos")
        else:
            st.warning("No hay libros en el catálogo.")
    except Exception as e:
        st.error(f"Error: {e}")

with tab2:
    st.subheader("Mi Calendario")
    usuario = st.text_input("Usuario:", key="calendario_usuario")

    if usuario:
        try:
            eventos = obtener_eventos_usuario(usuario)

            if eventos:
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
                st.caption("💾 Eventos cacheados - actualización cada 1 minuto")
            else:
                st.info(f"El usuario '{usuario}' no tiene préstamos registrados.")
        except Exception as e:
            st.error(f"Error en calendario: {e}")

with tab3:
    st.subheader("📋 Historial Completo de Préstamos")
    st.write("Consulta todos los préstamos (activos y pasados) de un usuario.")

    usuario_historial = st.text_input("Nombre de Usuario:", key="historial_usuario")

    if usuario_historial:
        try:
            prestamos = obtener_historial_usuario(usuario_historial)

            if prestamos:
                df = pd.DataFrame(prestamos)


                # Aplicar estilos condicionales
                def colorear_estado(row):
                    if row['Estado'] == '🔴 Activo':
                        return ['background-color: #ffe6e6'] * len(row)
                    else:
                        return ['background-color: #e6ffe6'] * len(row)


                st.dataframe(
                    df.style.apply(colorear_estado, axis=1),
                    use_container_width=True,
                    hide_index=True
                )

                # Estadísticas
                activos = df[df['Estado'] == '🔴 Activo'].shape[0]
                devueltos = df[df['Estado'] == '✅ Devuelto'].shape[0]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Préstamos", len(prestamos))
                with col2:
                    st.metric("🔴 Activos", activos)
                with col3:
                    st.metric("✅ Devueltos", devueltos)

                st.caption("💾 Historial cacheado - actualización cada 1 minuto")
            else:
                st.info(f"ℹ️ El usuario '{usuario_historial}' no tiene historial de préstamos.")

        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")