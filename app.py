import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
from datetime import date, time

# Configuración inicial de la página Streamlit
st.set_page_config(
    page_title="Gestión de Boda - Sistema Completo",
    page_icon="💒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-family: 'Playfair Display', Georgia, serif;
        color: #4A3E3D;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .sub-title {
        color: #8B5E3C;
        font-weight: 600;
    }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PERSISTENCIA Y DATOS INICIALES (Session State)
# -----------------------------------------------------------------------------
if 'datos_boda' not in st.session_state:
    st.session_state.datos_boda = {
        "novia": "María Elena Rodríguez",
        "novio": "Carlos Alberto Mendoza",
        "padre_novia": "Fernando Rodríguez",
        "madre_novia": "Elena Gómez de Rodríguez",
        "padre_novio": "Carlos Mendoza Sr.",
        "madre_novio": "Beatriz Silva de Mendoza",
        "fecha": date(2027, 10, 16),
        "hora": time(17, 0),
        "lugar_ceremonia": "Catedral Metropolitana",
        "lugar_recepcion": "Hacienda Los Olivos",
        "frase": "Unidos por el amor, guiados por nuestras familias."
    }

if 'invitados' not in st.session_state:
    st.session_state.invitados = pd.DataFrame([
        {
            "ID": 1,
            "Nombre Completo": "Roberto Gómez",
            "Acompañantes Permitidos": 2,
            "Acompañantes Confirmados": 2,
            "Estado RSVP": "Confirmado",
            "Mesa": "Mesa 1 - Familia Novia",
            "Dieta/Restricciones": "Ninguna",
            "Telefono": "+593 99 123 4567"
        },
        {
            "ID": 2,
            "Nombre Completo": "Ana Lucía Martínez",
            "Acompañantes Permitidos": 1,
            "Acompañantes Confirmados": 0,
            "Estado RSVP": "Pendiente",
            "Mesa": "Mesa 2 - Amigos Novio",
            "Dieta/Restricciones": "Vegetariano",
            "Telefono": "+593 98 765 4321"
        },
        {
            "ID": 3,
            "Nombre Completo": "Javier Silva",
            "Acompañantes Permitidos": 1,
            "Acompañantes Confirmados": 0,
            "Estado RSVP": "Cancelado",
            "Mesa": "Sin Asignar",
            "Dieta/Restricciones": "Sin gluten",
            "Telefono": "+593 99 888 7777"
        }
    ])

if 'regalos' not in st.session_state:
    st.session_state.regalos = pd.DataFrame([
        {
            "ID": 1,
            "Artículo / Concepto": "Juego de Vajilla de Porcelana (12 pzas)",
            "Categoría": "Hogar & Cocina",
            "Precio Estimado ($)": 250.0,
            "Monto Recaudado ($)": 250.0,
            "Estado": "Comprado / Reservado",
            "Comprador / Contribuyente": "Roberto Gómez"
        },
        {
            "ID": 2,
            "Artículo / Concepto": "Fondo Luna de Miel (Aéreos)",
            "Categoría": "Fondo Luna de Miel",
            "Precio Estimado ($)": 1200.0,
            "Monto Recaudado ($)": 600.0,
            "Estado": "Parcialmente Financiado",
            "Comprador / Contribuyente": "Familia Silva"
        },
        {
            "ID": 3,
            "Artículo / Concepto": "Cafetera Express Automática",
            "Categoría": "Electrodomésticos",
            "Precio Estimado ($)": 180.0,
            "Monto Recaudado ($)": 0.0,
            "Estado": "Disponible",
            "Comprador / Contribuyente": "-"
        }
    ])

# -----------------------------------------------------------------------------
# MENÚ DE NAVEGACIÓN
# -----------------------------------------------------------------------------
st.sidebar.title("💒 Menú Boda")
opcion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📌 Información General & Padres",
        "👥 Gestión de Invitados & Mesas",
        "🎁 Mesa de Regalos",
        "📊 Estadísticas & Métricas",
        "📁 Importar / Exportar Datos"
    ]
)

# -----------------------------------------------------------------------------
# SECCIÓN 1: INFORMACIÓN GENERAL Y PADRES DE LOS NOVIOS
# -----------------------------------------------------------------------------
if opcion == "📌 Información General & Padres":
    st.markdown("<div class='main-header'><h1>💍 Detalles del Evento y Padres de los Novios</h1></div>", unsafe_allow_html=True)
    
    with st.form("form_info_boda"):
        st.subheader("💑 Datos de los Novios")
        col1, col2 = st.columns(2)
        with col1:
            novia = st.text_input("Nombre de la Novia", value=st.session_state.datos_boda["novia"])
        with col2:
            novio = st.text_input("Nombre del Novio", value=st.session_state.datos_boda["novio"])
            
        st.markdown("---")
        st.subheader("👨‍👩‍👧‍👦 Padres de los Novios")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("<h4 class='sub-title'>Padres de la Novia</h4>", unsafe_allow_html=True)
            padre_novia = st.text_input("Padre de la Novia", value=st.session_state.datos_boda["padre_novia"])
            madre_novia = st.text_input("Madre de la Novia", value=st.session_state.datos_boda["madre_novia"])
            
        with col_p2:
            st.markdown("<h4 class='sub-title'>Padres del Novio</h4>", unsafe_allow_html=True)
            padre_novio = st.text_input("Padre del Novio", value=st.session_state.datos_boda["padre_novio"])
            madre_novio = st.text_input("Madre del Novio", value=st.session_state.datos_boda["madre_novio"])
            
        st.markdown("---")
        st.subheader("📅 Logística del Evento")
        col3, col4 = st.columns(2)
        with col3:
            fecha = st.date_input("Fecha de la Boda", value=st.session_state.datos_boda["fecha"])
            lugar_ceremonia = st.text_input("Lugar de la Ceremonia", value=st.session_state.datos_boda["lugar_ceremonia"])
        with col4:
            hora = st.time_input("Hora del Evento", value=st.session_state.datos_boda["hora"])
            lugar_recepcion = st.text_input("Lugar de la Recepción", value=st.session_state.datos_boda["lugar_recepcion"])
            
        frase = st.text_area("Frase o Lema de la Invitación", value=st.session_state.datos_boda["frase"])
        
        guardar_info = st.form_submit_button("💾 Guardar Cambios")
        if guardar_info:
            st.session_state.datos_boda.update({
                "novia": novia, "novio": novio,
                "padre_novia": padre_novia, "madre_novia": madre_novia,
                "padre_novio": padre_novio, "madre_novio": madre_novio,
                "fecha": fecha, "hora": hora,
                "lugar_ceremonia": lugar_ceremonia, "lugar_recepcion": lugar_recepcion,
                "frase": frase
            })
            st.success("¡Información actualizada con éxito!")

    # Vista previa de la tarjeta
    st.markdown("### 💌 Vista Previa de la Tarjeta Digital")
    st.info(f"""
    **{st.session_state.datos_boda['novia']} & {st.session_state.datos_boda['novio']}**
    
    *Con la bendición de nuestros padres:*
    * **Padres de la Novia:** {st.session_state.datos_boda['padre_novia']} y {st.session_state.datos_boda['madre_novia']}
    * **Padres del Novio:** {st.session_state.datos_boda['padre_novio']} y {st.session_state.datos_boda['madre_novio']}
    
    📅 **Fecha:** {st.session_state.datos_boda['fecha'].strftime('%d de %B de %Y')} | ⏰ **Hora:** {st.session_state.datos_boda['hora'].strftime('%H:%M')}
    💒 **Ceremonia:** {st.session_state.datos_boda['lugar_ceremonia']}
    🥂 **Recepción:** {st.session_state.datos_boda['lugar_recepcion']}
    
    > *"{st.session_state.datos_boda['frase']}"*
    """)

# -----------------------------------------------------------------------------
# SECCIÓN 2: GESTIÓN DE INVITADOS & MESAS
# -----------------------------------------------------------------------------
elif opcion == "👥 Gestión de Invitados & Mesas":
    st.markdown("<div class='main-header'><h1>👥 Gestión de Invitados, RSVP y Mesas</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Lista & Edición Directa", "➕ Registrar Nuevo Invitado"])
    
    with tab1:
        st.subheader("Lista Completa de Invitados")
        edited_df = st.data_editor(
            st.session_state.invitados,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Estado RSVP": st.column_config.SelectboxColumn(
                    "Estado RSVP",
                    options=["Confirmado", "Pendiente", "Cancelado"],
                    required=True
                )
            },
            key="editor_invitados"
        )
        st.session_state.invitados = edited_df

    with tab2:
        st.subheader("Añadir Invitado")
        with st.form("form_add_invitado"):
            nombre = st.text_input("Nombre Completo")
            col_a, col_b = st.columns(2)
            with col_a:
                permitidos = st.number_input("Acompañantes Permitidos", min_value=0, max_value=10, value=1)
                estado = st.selectbox("Estado RSVP Inicial", ["Pendiente", "Confirmado", "Cancelado"])
            with col_b:
                confirmados = st.number_input("Acompañantes Confirmados", min_value=0, max_value=10, value=0)
                mesa = st.text_input("Mesa / Asiento", value="Mesa 1")
            
            dieta = st.text_input("Restricciones Alimentarias", value="Ninguna")
            telefono = st.text_input("Teléfono de Contacto")
            
            btn_add = st.form_submit_button("Añadir Invitado")
            if btn_add and nombre:
                new_id = len(st.session_state.invitados) + 1
                nueva_fila = {
                    "ID": new_id,
                    "Nombre Completo": nombre,
                    "Acompañantes Permitidos": permitidos,
                    "Acompañantes Confirmados": confirmados,
                    "Estado RSVP": estado,
                    "Mesa": mesa,
                    "Dieta/Restricciones": dieta,
                    "Telefono": telefono
                }
                st.session_state.invitados = pd.concat([st.session_state.invitados, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success(f"Invitado {nombre} registrado correctamente.")
                st.rerun()

# -----------------------------------------------------------------------------
# SECCIÓN 3: MESA DE REGALOS
# -----------------------------------------------------------------------------
elif opcion == "🎁 Mesa de Regalos":
    st.markdown("<div class='main-header'><h1>🎁 Gestión de Mesa de Regalos</h1></div>", unsafe_allow_html=True)
    
    t_reg1, t_reg2 = st.tabs(["🎁 Lista de Regalos & Aportes", "➕ Registrar Nuevo Regalo / Opción"])
    
    with t_reg1:
        st.subheader("Estado de la Mesa de Regalos")
        edited_reg = st.data_editor(
            st.session_state.regalos,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Estado": st.column_config.SelectboxColumn(
                    "Estado",
                    options=["Disponible", "Parcialmente Financiado", "Comprado / Reservado"],
                    required=True
                )
            },
            key="editor_regalos"
        )
        st.session_state.regalos = edited_reg

    with t_reg2:
        st.subheader("Añadir Nuevo Artículo / Fondo")
        with st.form("form_add_regalo"):
            articulo = st.text_input("Artículo o Concepto (ej. Licuadora, Fondo Viaje)")
            categoria = st.selectbox("Categoría", ["Hogar & Cocina", "Electrodomésticos", "Fondo Luna de Miel", "Experiencias", "Otro"])
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                precio = st.number_input("Precio / Meta Estimada ($)", min_value=0.0, value=100.0)
            with col_r2:
                recaudado = st.number_input("Monto Recaudado Inicial ($)", min_value=0.0, value=0.0)
            
            estado_r = st.selectbox("Estado", ["Disponible", "Parcialmente Financiado", "Comprado / Reservado"])
            comprador = st.text_input("Nombre de quien regala / aporta", value="-")
            
            btn_add_r = st.form_submit_button("Añadir a la Mesa de Regalos")
            if btn_add_r and articulo:
                new_r_id = len(st.session_state.regalos) + 1
                nueva_r = {
                    "ID": new_r_id,
                    "Artículo / Concepto": articulo,
                    "Categoría": categoria,
                    "Precio Estimado ($)": precio,
                    "Monto Recaudado ($)": recaudado,
                    "Estado": estado_r,
                    "Comprador / Contribuyente": comprador
                }
                st.session_state.regalos = pd.concat([st.session_state.regalos, pd.DataFrame([nueva_r])], ignore_index=True)
                st.success(f"Regalo '{articulo}' añadido con éxito.")
                st.rerun()

# -----------------------------------------------------------------------------
# SECCIÓN 4: ESTADÍSTICAS & MÉTRICAS
# -----------------------------------------------------------------------------
elif opcion == "📊 Estadísticas & Métricas":
    st.markdown("<div class='main-header'><h1>📊 Panel Estadístico & Métricas de la Boda</h1></div>", unsafe_allow_html=True)
    
    df_inv = st.session_state.invitados
    df_reg = st.session_state.regalos
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    total_invitados = len(df_inv)
    confirmados = len(df_inv[df_inv["Estado RSVP"] == "Confirmado"])
    asistentes_totales = df_inv[df_inv["Estado RSVP"] == "Confirmado"]["Acompañantes Confirmados"].sum() + confirmados
    monto_recaudado = df_reg["Monto Recaudado ($)"].sum()
    
    col_m1.metric("Invitaciones Enviadas", total_invitados)
    col_m2.metric("Pases Confirmados", confirmados)
    col_m3.metric("Total Asistentes Estimados", asistentes_totales)
    col_m4.metric("Recaudado Regalos", f"${monto_recaudado:,.2f}")
    
    st.markdown("---")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Estado de Confirmaciones (RSVP)")
        fig_rsvp = px.pie(
            df_inv, 
            names="Estado RSVP", 
            title="Distribución de Respuestas RSVP",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_rsvp, use_container_width=True)

    with col_g2:
        st.subheader("Avance de Regalos por Categoría")
        fig_reg = px.bar(
            df_reg, 
            x="Categoría", 
            y=["Precio Estimado ($)", "Monto Recaudado ($)"],
            barmode="group",
            title="Comparativo Meta vs Recaudado por Categoría",
            color_discrete_sequence=["#D3D3D3", "#2ECC71"]
        )
        st.plotly_chart(fig_reg, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 5: IMPORTAR / EXPORTAR DATOS
# -----------------------------------------------------------------------------
elif opcion == "📁 Importar / Exportar Datos":
    st.markdown("<div class='main-header'><h1>📁 Importación y Exportación de Datos</h1></div>", unsafe_allow_header=True)
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.subheader("📥 Exportar Datos")
        
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            st.session_state.invitados.to_excel(writer, sheet_name='Invitados', index=False)
            st.session_state.regalos.to_excel(writer, sheet_name='Regalos', index=False)
            df_info = pd.DataFrame([st.session_state.datos_boda])
            df_info.to_excel(writer, sheet_name='Informacion_General', index=False)
            
        st.download_button(
            label="📄 Descargar Todo en Excel (.xlsx)",
            data=buffer_excel.getvalue(),
            file_name="boda_datos_completos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        json_data = {
            "datos_boda": {k: str(v) for k, v in st.session_state.datos_boda.items()},
            "invitados": st.session_state.invitados.to_dict(orient="records"),
            "regalos": st.session_state.regalos.to_dict(orient="records")
        }
        st.download_button(
            label="📌 Descargar Copia Backup (.json)",
            data=json.dumps(json_data, indent=4, ensure_ascii=False),
            file_name="boda_backup.json",
            mime="application/json"
        )
        
    with col_exp2:
        st.subheader("📤 Cargar Datos Backup")
        uploaded_file = st.file_uploader("Cargar archivo JSON de respaldo", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.session_state.invitados = pd.DataFrame(data["invitados"])
                st.session_state.regalos = pd.DataFrame(data["regalos"])
                st.success("¡Backup de datos restaurado exitosamente!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar archivo: {e}")
