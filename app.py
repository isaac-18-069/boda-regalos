import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components
import math
import io # Necesario para la descarga de Excel

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA Y TEMA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Carlos & Eunice 💍", 
    page_icon="🌿", 
    layout="centered"
)

# Control de estado de la sesión para el sobre
if "invitacion_abierta" not in st.session_state:
    st.session_state["invitacion_abierta"] = False

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS LOCALES
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")

def get_image_base64(path_local):
    if path_local.exists():
        with open(path_local, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return ""

img_b64 = get_image_base64(IMAGEN_HEADER)

# Ilustración floral SVG pura
SVG_FLORES = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 120'><path fill='%236B7A68' d='M150 70c-20-10-40 0-50 15 15-5 30-2 40 5 5 3 8 7 10 10zM350 70c20-10 40 0 50 15-15-5 30-2 40 5 5 3 8 7 10 10z'/><path fill='%238A9A86' d='M180 50c-15-15-35-10-45 5 12-2 25 3 32 12 4 4 6 9 13-17zM320 50c15-15 35-10 45 5-12-2-25 3-32 12-4 4 6 9-13-17z'/><circle cx='250' cy='50' r='22' fill='%23D4A3A9'/><circle cx='250' cy='50' r='16' fill='%23E8C2C8'/><circle cx='250' cy='50' r='10' fill='%23F4DCDA'/><circle cx='215' cy='60' r='16' fill='%23E8B4B8'/><circle cx='215' cy='60' r='10' fill='%23F4DCDA'/><circle cx='285' cy='60' r='16' fill='%23E8B4B8'/><circle cx='285' cy='60' r='10' fill='%23F4DCDA'/><circle cx='190' cy='72' r='11' fill='%23F3D5D8'/><circle cx='310' cy='72' r='11' fill='%23F3D5D8'/></svg>"

# ──────────────────────────────────────────────
# ESTILOS CSS CORREGIDOS (FLORES Y COLOR AL ESCRIBIR)
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* Color de fondo de la aplicación */
.stApp {{
    background-color: #FAF6F0 !important;
}}

/* Ocultar elementos predeterminados de Streamlit */
#MainMenu, footer, header {{visibility: hidden;}}

/* Color de texto predeterminado para p y span */
p, span, div, h1, h2, h3, h4, h5, h6 {{
    color: #4A5A48 !important;
}}

/* CAMBIO SOLICITADO: Color de texto claro al escribir en inputs y textareas */
input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{
    color: #A3B18A !important; /* Verde Oliva Claro */
}}

/* Asegurar que las etiquetas (labels) de inputs se mantengan oscuras */
[data-baseweb="input"] label, [data-baseweb="select"] label, [data-baseweb="radio"] label {{
    color: #4A5A48 !important;
}}

html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif !important;
}}

/* TARJETAS PRINCIPALES */
.invitation-card, .dress-card {{
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px;
    padding: 70px 25px 70px 25px;
    margin: 35px auto;
    box-shadow: 0 10px 30px rgba(107, 122, 104, 0.1);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

/* RAMO FLORAL SUPERIOR CENTRADO */
.invitation-card::before, .dress-card::before {{
    content: "";
    position: absolute;
    top: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 250px;
    height: 60px;
    background-image: url("{SVG_FLORES}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    opacity: 0.95;
    pointer-events: none;
    z-index: 1;
}}

/* RAMO FLORAL INFERIOR CENTRADO */
.invitation-card::after, .dress-card::after {{
    content: "";
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 250px;
    height: 60px;
    background-image: url("{SVG_FLORES}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    opacity: 0.95;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card *, .dress-card * {{
    position: relative;
    z-index: 2;
}}

/* TARJETAS CON FONDO VERDE OLIVA */
.green-card {{
    background-color: #6B7A68 !important;
    border-radius: 20px;
    padding: 35px 25px;
    margin: 25px auto;
    text-align: center;
    box-shadow: 0 10px 25px rgba(107, 122, 104, 0.2);
}}
.green-card * {{
    color: #FFFFFF !important;
}}

/* TÍTULOS DE NOMBRES PRINCIPALES */
.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #4A5A48 !important;
    margin-bottom: 5px;
    line-height: 1.2;
}}

/* SOBRE DE INICIO INTERACTIVO */
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
    z-index: 2;
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
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    border: 2px solid #F3E5AB;
}}

/* BOTÓN DE CONFIRMACIÓN PRINCIPAL */
div.stButton > button:first-child {{
    background-color: #6B7A68 !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 14px 35px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
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
    processed_data = output.getvalue()
    return processed_data

# ──────────────────────────────────────────────
# PASO 1: PANTALLA INICIAL DEL SOBRE
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
# PASO 2: CONTENIDO DE LA INVITACIÓN
# ──────────────────────────────────────────────
else:
    # 1. HEADER CON NOMBRES
    st.markdown("""
    <div class="invitation-card">
        <div class="title-names">Carlos & Eunice</div>
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600; margin-top: 5px;">
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

    # 3. MÚSICA DE FONDO
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 30px;">
        <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=js2MkCAmTJY")

    # 4. VERSÍCULO BÍBLICO DE AMOR
    st.markdown("""
    <div class="invitation-card verse-card">
        <p class="verse-text">
            «El amor es paciente, es bondadoso. Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta. El amor nunca deja de ser.»
        </p>
        <span class="verse-ref">1 CORINTIOS 13:4, 7-8</span>
    </div>
    """, unsafe_allow_html=True)

    # 5. PADRES DE LOS NOVIOS
    st.markdown("""
    <div class="invitation-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; color: #4A5A48; font-weight: 600; text-transform: uppercase;">
            Con la bendición de nuestros padres
        </div>
        <div style="display: flex; justify-content: space-around; font-size: 0.9rem; margin-top: 20px;">
            <div>
                <strong>Padres del Novio</strong><br>Carlos M & Diana ❤️
            </div>
            <div>
                <strong>Padres de la Novia</strong><br>Emilio M & Pricila C ❤️
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. ITINERARIO DE ACTIVIDADES
    st.markdown("""
    <div class="invitation-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; color: #4A5A48; font-weight: 600; text-transform: uppercase;">
            Itinerario de Actividades
        </div>
        <div class="timeline-item">⛪ 16:00 hrs — Ceremonia</div>
        <div class="timeline-item">🥂 20:00 hrs — Bienvenida y Felicitaciones</div>
        <div class="timeline-item">🍽️ 20:30 hrs — Cena de Gala</div>
        <div class="timeline-item" style="border-bottom:none;">💃 21:30 hrs — Fiesta y Baile</div>
    </div>
    """, unsafe_allow_html=True)

    # 7. DÍA Y CALENDARIO
    st.markdown("""
    <div class="green-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.9rem;">EL GRAN DÍA</div>
        <h2 style="font-size: 2.2rem; margin: 10px 0; color: #FFFFFF !important;">SÁBADO 18 DE JUNIO</h2>
        <p style="font-size: 0.95rem; opacity: 0.9; color: #FFFFFF !important;">2027 • 16:00 HRS</p>
    </div>
    """, unsafe_allow_html=True)

    # 8. UBICACIÓN Y CEREMONIA
    st.markdown("""
    <div class="invitation-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; color: #4A5A48; font-weight: 600; text-transform: uppercase;">
            Ceremonia
        </div>
        <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 10px;">Lugar de la Ceremonia</p>
        <p style="font-size: 0.85rem; color: #4A5568 !important;">16:00 HRS</p>
        <a href="https://maps.google.com" target="_blank" style="text-decoration: none;">
            <div style="background-color: #E2E8F0; color: #2D3748 !important; padding: 8px 15px; border-radius: 15px; display: inline-block; font-size: 0.85rem; margin-top: 10px; font-weight: 500;">
                📍 Ver ubicación en GPS
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 9. CÓDIGO DE VESTIMENTA (DRESS CODE)
    st.markdown("""
    <div class="dress-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; color: #4A5A48; font-weight: 600; text-transform: uppercase;">
            👗 Código de Vestimenta
        </div>
        <p style="font-size: 1.1rem; font-weight: 600; color: #4A5A48 !important; margin-top: 10px;">FORMAL / ELEGANTE</p>
        <p style="font-size: 0.85rem; color: #4A5568 !important;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;">
        <p style="font-size: 0.9rem; font-weight: 600;">Eventos de Adultos (Sin Niños)</p>
    </div>
    """, unsafe_allow_html=True)

    # 10. SECCIÓN DE CONFIRMACIÓN Y REGALOS
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 1.1rem; color: #4A5A48; font-weight: 600; text-transform: uppercase;">
            Confirmar Asistencia
        </div>
        <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 10px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
    </div>
    """, unsafe_allow_html=True)

    # FORMULARIO DE CONFIRMACIÓN (CORREGIDO COLOR AL ESCRIBIR)
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
                    mesa_asistente = "Mesa 1" # Por defecto
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
                if asiste_val == "Sí":
                    st.balloons()
                    st.markdown(f"""
                    <div class="confirmation-envelope-card">
                        <h3 style="font-family: 'Great Vibes', cursive !important; font-size: 2.3rem; color: #F3E5AB !important;">
                            ¡Gracias por confirmar! 💖
                        </h3>
                        <p style="font-size: 1.1rem; line-height: 1.6; font-weight: 500; margin: 15px 0;">
                            Te esperamos con ansias para celebrar este hermoso día con nosotros ✨🥂🎉💒
                        </p>
                        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.4); margin: 20px 0;">
                        <p style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: #F3E5AB !important;">
                            🎁 Sugerencia de Regalo Asignada:
                        </p>
                        <h2 style="font-size: 1.8rem; margin: 8px 0; font-family: 'Cinzel', serif !important;">
                            {regalo}
                        </h2>
                        <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 12px;">
                            Código de Confirmación: <strong>{codigo}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Lamentamos que no puedas acompañarnos, ¡agradecemos mucho tu respuesta!")

    # 11. PANEL DE ADMINISTRACIÓN Y ASIGNACIÓN DE MESAS
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Gestor de Mesas e Invitados)"):
        df_ver = cargar_respuestas()
        if not df_ver.empty:
            st.write("### Asignación Rápida de Mesas")
            invitados_lista = df_ver[df_ver["Asiste"] == "Sí"]["Nombre"].tolist()
            
            if invitados_lista:
                col1, col2 =
                st.columns(2)
                with col1:
                    invitado_sel = st.selectbox("Selecciona Invitado:", invitados_lista)
                with col2:
                    opciones_mesas = [f"Mesa {i}" for i in range(1, 11)] + ["Mesa Presidencial"]
                    nueva_mesa = st.selectbox("Asignar Mesa:", opciones_mesas)
                
                if st.button("Guardar Mesa Asignada"):
                    df_ver.loc[df_ver["Nombre"] == invitado_sel, "Mesa"] = nueva_mesa
                    guardar_respuestas(df_ver)
                    st.success(f"¡{invitado_sel} reasignado a {nueva_mesa}!")
                    st.rerun()

            st.write("### Lista General de Confirmados")
            st.dataframe(df_ver, use_container_width=True)
            
            # Botón para descargar Excel
            excel_data = convertir_excel(df_ver)
            st.download_button(
                label="📥 Descargar Lista Completa (Excel)",
                data=excel_data,
                file_name="lista_invitados_confirmados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.caption("Aún no hay respuestas.")
