import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestión de Usuarios", page_icon="👥")

st.markdown("# 👥 Gestión de Usuarios")
st.write("Registra y consulta usuarios de la biblioteca.")

API_URL = "http://fastapi:8000"


# FUNCIÓN CON CACHÉ
@st.cache_data(ttl=60)  # Cache por 1 minuto
def obtener_usuarios():
    """Obtiene la lista de usuarios con caché"""
    response = requests.get(f"{API_URL}/usuarios/")
    if response.status_code == 200:
        return response.json()
    return {"total": 0, "usuarios": []}


tab1, tab2 = st.tabs(["➕ Registrar Usuario", "📋 Listado de Usuarios"])

# TAB 1: Registrar Usuario
with tab1:
    st.subheader("Registrar Nuevo Usuario")

    with st.form("register_user_form"):
        nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
        email = st.text_input("Email *", placeholder="Ej: juan.perez@email.com")

        submitted = st.form_submit_button("✅ Registrar Usuario", use_container_width=True)

        if submitted:
            # Validación básica
            if not nombre or nombre.strip() == "":
                st.error("⚠️ El nombre es obligatorio.")
            elif not email or email.strip() == "":
                st.error("⚠️ El email es obligatorio.")
            elif "@" not in email:
                st.error("⚠️ El email debe tener un formato válido (contener @).")
            else:
                st.info(f"Registrando usuario '{nombre}'...")

                try:
                    response = requests.post(
                        f"{API_URL}/usuarios/",
                        params={"nombre": nombre.strip(), "email": email.strip()}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ {data['message']}")
                        st.json(data['usuario'])
                        st.balloons()

                        # Limpiar caché para que aparezca en el listado
                        st.cache_data.clear()
                    else:
                        error_detail = response.json().get('detail', 'Error desconocido')
                        st.error(f"❌ {error_detail}")

                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

# TAB 2: Listado de Usuarios
with tab2:
    st.subheader("📋 Usuarios Registrados")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    try:
        data = obtener_usuarios()
        usuarios = data.get("usuarios", [])
        total = data.get("total", 0)

        if usuarios:
            st.info(f"📊 Total de usuarios registrados: **{total}**")

            df = pd.DataFrame(usuarios)
            df = df.rename(columns={
                'id': 'ID',
                'nombre': 'Nombre',
                'email': 'Email'
            })

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.caption("💾 Listado cacheado - actualización cada 1 minuto")
        else:
            st.warning("ℹ️ No hay usuarios registrados todavía.")
    except Exception as e:
        st.error(f"❌ Error al obtener usuarios: {e}")

st.markdown("---")
st.info(
    "💡 **Tip**: Los emails se guardan en minúsculas automáticamente para evitar duplicados. Los datos se cachean para mejorar el rendimiento.")