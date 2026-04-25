import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestión de Usuarios", page_icon="👥")

st.markdown("# 👥 Gestión de Usuarios")
st.write("Registra y consulta usuarios de la biblioteca.")

API_URL = "http://fastapi:8000"

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
                    else:
                        error_detail = response.json().get('detail', 'Error desconocido')
                        st.error(f"❌ {error_detail}")

                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

# TAB 2: Listado de Usuarios
with tab2:
    st.subheader("📋 Usuarios Registrados")

    if st.button("🔄 Actualizar Listado", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/usuarios/")

            if response.status_code == 200:
                data = response.json()
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
                else:
                    st.warning("ℹ️ No hay usuarios registrados todavía.")
            else:
                st.error(f"❌ Error al obtener usuarios: {response.status_code}")

        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

st.markdown("---")
st.info("💡 **Tip**: Los emails se guardan en minúsculas automáticamente para evitar duplicados.")