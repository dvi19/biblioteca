import streamlit as st
import requests
import pandas as pd
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendario Biblioteca", layout="wide")

API_URL = "http://fastapi:8000"

st.title("📅 HISTORIAL DE PRÉSTAMOS")

tab1, tab2, tab3 = st.tabs(["📚 Catálogo", "📆 Mi Calendario", "📋 Historial Completo"])

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
    usuario = st.text_input("Usuario:", key="calendario_usuario")
    if usuario:
        try:
            res = requests.get(f"{API_URL}/calendario/{usuario}")
            if res.status_code == 200:
                eventos = res.json().get("eventos", [])

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
            res = requests.get(f"{API_URL}/prestamos/historial/{usuario_historial}")

            if res.status_code == 200:
                prestamos = res.json().get("prestamos", [])

                if prestamos:
                    df = pd.DataFrame(prestamos)


                    # Aplicar estilos condicionales
                    def colorear_estado(row):
                        if row['Estado'] == '🔴 Activo':
                            return ['background-color: #ffe6e6'] * len(row)
                        else:
                            return ['background-color: #e6ffe6'] * len(row)


                    # Mostrar tabla con estilo
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
                else:
                    st.info(f"ℹ️ El usuario '{usuario_historial}' no tiene historial de préstamos.")

            elif res.status_code == 404:
                st.warning(f"⚠️ El usuario '{usuario_historial}' no tiene historial de préstamos.")
            else:
                st.error(f"❌ Error al obtener historial: {res.status_code}")

        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")