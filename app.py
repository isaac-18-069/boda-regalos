import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components
import io

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA Y TEMA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Carlos & Eunice 💍", 
    page_icon="🌿", 
    layout="centered"
)

if "invitacion_abierta" not in st.session_state:
    st.session_state["invitacion_abierta"] = False

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS LOCALES
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")
IMAGEN_FLORES = Path("Este artículo no está disponible - Etsy.jpg")

def get_image_base64(path_local):
    if path_local.exists():
        with open(path_local, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = path_local.suffix.replace('.', '').lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
            return f"data:{mime};base64,{encoded}"
    return ""

img_b64 = get_image_base64(IMAGEN_HEADER)
flores_b64 = get_image_base64(IMAGEN_FLORES)

# ──────────────────────────────────────────────
# ESTILOS CSS CON TUS FLORES Y TEXTO CLARO
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

.stApp {{
    background-color: #FAF6F0 !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

p, span, div, h1, h2, h3, h4, h5, h6 {{
    color: #4A5A48 !important;
}}

/* COLOR CLARO AL ESCRIBIR EN LOS CAMPOS */
input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{
    color: #6B7A68 !important;
    font-weight: 600 !important;
}}

html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif !important;
}}

.invitation-card, .dress-card {{
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px;
    padding: 85px 25px 85px 25px;
    margin: 35px auto;
    box-shadow: 0 10px 30px rgba(107, 122, 104, 0.1);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

/* MARGEN CON TU IMAGEN REAL DE FLORES ROSADAS */
.invitation-card::before, .dress-card::before {{
    content: "";
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    width: 320px;
    height: 80px;
    background-image: url("{flores_b64}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card::after, .dress-card::after {{
    content: "";
    position: absolute;
    bottom: 5px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 320px;
    height: 80px;
    background-image: url("{flores_b64}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card *, .dress-card * {{
    position: relative;
    z-index: 2;
}}

.green-card {{
    background-color: #6B7A68 !important;
    border-radius: 20px;
    padding: 35px 25px;
    margin: 25px auto;
    text-align: center;
}}
.green-card * {{
    color: #FFFFFF !important;
}}

.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #4A5A48 !important;
    margin-bottom: 5px;
}}

.welcome-envelope {{
    background-color: #FAF6F0;
    width: 260px;
    height: 170px;
    margin: 15px auto;
    border-radius: 12px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}

.seal-initials {{
    width: 65px;
    height: 65px;
    background: radial-gradient(circle, #D4AF37 0%, #AA7C11 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-family: 'Cinzel', serif !important;
    font-size: 18px;
    font-weight: bold;
}}

div.stButton > button:first-child {{
    background-color: #6B7A68 !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 14px 35px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100%;
}}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES DE DATOS
# ──────────────────────────────────────────────
def cargar_respuestas():
    if CSV_RESPUESTAS.exists():
        df = pd.read_csv(CSV_RESPUESTAS)
        if "Mesa" not in df.columns:
            df["Mesa"] = "Mesa 1"
        return df
    return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo", "Mesa"])

def cargar_regalos():
    if not CSV_REGALOS.exists():
        return pd.DataFrame(columns=["Regalo"])
    return pd.read_csv(CSV_REGALOS)

def asignar_regalo(nombre):
    df = cargar_regalos()
    if df.empty:
        return "Detalle de boda a elección personal"
    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

def guardar_respuestas(df):
    df.to_csv(CSV_RESPUESTAS, index=False)

def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Invitados')
    return output.getvalue()

# ──────────────────────────────────────────────
# PANTALLA INICIAL
# ──────────────────────────────────────────────
if not st.session_state["invitacion_abierta"]:
    st.markdown("""
    <div class="invitation-card" style="margin-top: 30px;">
        <div class="welcome-envelope">
            <div class="seal-initials">C & E</div>
        </div>
        <p style="font-size: 0.9rem; color: #6B7A68 !important; margin-top: 10px; font-weight: 500;">
            Has recibido una invitación especial
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✉️ Click para abrir la invitación"):
        st.session_state["invitacion_abierta"] = True
        st.rerun()

# ──────────────────────────────────────────────
# CONTENIDO DE LA INVITACIÓN
# ──────────────────────────────────────────────
else:
    # 1. NOMBRES
    st.markdown("""
    <div class="invitation-card">
        <div class="title-names">Carlos & Eunice</div>
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600;">
            18 DE JUNIO DE 2027
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. FOTO DE LOS NOVIOS
    if IMAGEN_HEADER.exists():
        st.markdown(f"""
        <div class="invitation-card">
            <img src="{img_b64}" style="width: 100%; max-width: 500px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)

    # 3. MÚSICA
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 30px;">
        <p style="font-size: 0.95rem; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=js2MkCAmTJY")

    # 4. PADRES DE LOS NOVIOS
    st.markdown("""
    <div class="invitation-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; font-weight: 600; text-transform: uppercase;">
            Con la bendición de Dios y nuestros padres
        </div>
        <div style="display: flex; justify-content: space-around; font-size: 0.9rem; margin-top: 20px;">
            <div><strong>Padres del Novio</strong><br>Carlos M & Diana ❤️</div>
            <div><strong>Padres de la Novia</strong><br>Emilio M & Pricila C ❤️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. DRESS CODE
    st.markdown("""
    <div class="dress-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; font-weight: 600; text-transform: uppercase;">
            👗 Código de Vestimenta
        </div>
        <p style="font-size: 1.1rem; font-weight: 600; margin-top: 10px;">FORMAL / ELEGANTE</p>
        <p style="font-size: 0.85rem;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;">
        <p style="font-size: 0.9rem; font-weight: 600;">🔞 Evento de Adultos (Sin Niños)</p>
    </div>
    """, unsafe_allow_html=True)

    # 6. FORMULARIO DE CONFIRMACIÓN
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; font-weight: 600; text-transform: uppercase;">
            Confirmar Asistencia
        </div>
        <p style="font-size: 0.9rem; margin-top: 10px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_invitacion"):
        nombre = st.text_input("Nombre y Apellido:", placeholder="Ej: María López")
        asistencia = st.radio("¿Nos acompañarás?", ["¡Sí, allí estaré! 🎉", "Lo siento, no podré asistir 😢"])
        submit = st.form_submit_button("Enviar Confirmación ✉️")

    if submit:
        if not nombre.strip():
            st.error("Por favor ingresa tu nombre.")
        else:
            df_resp = cargar_respuestas()
            if any(nombre.strip().lower() == str(n).strip().lower() for n in df_resp["Nombre"].tolist()):
                st.warning(f"El nombre {nombre.strip()} ya ha sido registrado previamente.")
            else:
                codigo = uuid.uuid4().hex[:8].upper()
                if asistencia == "¡Sí, allí estaré! 🎉":
                    regalo = asignar_regalo(nombre.strip())
                    asiste_val = "Sí"
                    mesa_asistente = "Mesa 1 (Cuadrada)"
                else:
                    regalo = "N/A"
                    asiste_val = "No"
                    mesa_asistente = "Sin Mesa"

                nueva_fila = pd.DataFrame([{
                    "Nombre": nombre.strip(),
                    "Asiste": asiste_val,
                    "Regalo": regalo,
                    "Codigo": codigo,
                    "Mesa": mesa_asistente
                }])
                df_actualizado = pd.concat([df_resp, nueva_fila], ignore_index=True)
                guardar_respuestas(df_actualizado)

                st.success("¡Respuesta guardada con éxito!")
                st.balloons()

    # 7. PANEL ADMIN (DISTRIBUCIÓN: 2 MESAS CUADRADAS APARTADAS + 4 MESAS REDONDAS)
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Gestor de Mesas e Invitados)"):
        df_ver = cargar_respuestas()
        
        st.write("### 🗺️ Distribución del Salón")
        
        # CROQUIS DEL SALÓN: 2 CUADRADAS APARTADAS + 4 REDONDAS
        salon_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&family=Cinzel:wght@600&display=swap');
            body { font-family: 'Montserrat', sans-serif; background: transparent; margin:0; padding:10px; }
            
            /* CONTENEDOR GENERAL */
            .salon-container { display: flex; flex-direction: column; align-items: center; gap: 20px; }

            /* SECCIÓN ARRIBA: 2 MESAS CUADRADAS SEPARADAS/APARTADAS */
            .separated-section {
                width: 100%; display: flex; justify-content: space-around;
                padding: 15px; border: 2px dashed #D4AF37; border-radius: 15px; background: rgba(255, 255, 255, 0.6);
            }
            .square-table {
                width: 110px; height: 100px; background: #FFFFFF;
                border: 2px solid #D4AF37; border-radius: 8px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.06); text-align: center; padding: 5px;
            }

            /* SECCIÓN ABAJO: 4 MESAS REDONDAS EN CUADRÍCULA */
            .round-section {
                display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px; margin-top: 10px;
            }
            .round-table {
                width: 110px; height: 110px; border-radius: 50%; background: #FFFFFF;
                border: 2px solid #A3B18A; display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.06); padding: 5px;
            }

            .table-title { font-family: 'Cinzel', serif; font-size: 11px; font-weight: bold; color: #4A5A48; }
            .badge { font-size: 9px; color: #6B7A68; margin-top: 3px; font-weight: 600; }
        </style>
        </head>
        <body>
            <div class="salon-container">
                <!-- 2 MESAS CUADRADAS APARTADAS -->
                <div class="separated-section">
                    <div class="square-table">
                        <div class="table-title">Mesa 1</div>
                        <div class="badge">🔲 Cuadrada</div>
                    </div>
                    <div class="square-table">
                        <div class="table-title">Mesa 2</div>
                        <div class="badge">🔲 Cuadrada</div>
                    </div>
                </div>

                <!-- 4 MESAS REDONDAS PRINCIPALES -->
                <div class="round-section">
                    <div class="round-table">
                        <div class="table-title">Mesa 3</div>
                        <div class="badge">⚪ Redonda</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 4</div>
                        <div class="badge">⚪ Redonda</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 5</div>
                        <div class="badge">⚪ Redonda</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 6</div>
                        <div class="badge">⚪ Redonda</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        components.html(salon_html, height=420)

        # SECCIÓN DE ASIGNACIÓN Y LISTADO DE INVITADOS
        if not df_ver.empty:
            st.write("### Asignación de Mesas")
            invitados_lista = df_ver[df_ver["Asiste"] == "Sí"]["Nombre"].tolist()
            
            if invitados_lista:
                col1, col2 = st.columns(2)
                with col1:
                    invitado_sel = st.selectbox("Seleccionar Invitado:", invitados_lista)
                with col2:
                    opciones_mesas = [
                        "Mesa 1 (Cuadrada Apartada)", 
                        "Mesa 2 (Cuadrada Apartada)", 
                        "Mesa 3 (Redonda)", 
                        "Mesa 4 (Redonda)", 
                        "Mesa 5 (Redonda)", 
                        "Mesa 6 (Redonda)"
                    ]
                    nueva_mesa = st.selectbox("Asignar a:", opciones_mesas)
                
                if st.button("Guardar Mesa"):
                    df_ver.loc[df_ver["Nombre"] == invitado_sel, "Mesa"] = nueva_mesa
                    guardar_respuestas(df_ver)
                    st.success(f"¡{invitado_sel} asignado a {nueva_mesa}!")
                    st.rerun()

            st.write("### Lista General de Confirmados")
            st.dataframe(df_ver, use_container_width=True)
            
            excel_data = convertir_excel(df_ver)
            st.download_button(
                label="📥 Descargar Lista Completa (Excel)",
                data=excel_data,
                file_name="lista_invitados_boda.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.caption("Aún no hay respuestas registradas.")
