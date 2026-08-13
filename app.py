import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components
import math

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
SVG_FLORES = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 120'><path fill='%236B7A68' d='M150 70c-20-10-40 0-50 15 15-5 30-2 40 5 5 3 8 7 10 10zM350 70c20-10 40 0 50 15-15-5 30-2 40 5 5 3 8 7 10 10z'/><path fill='%238A9A86' d='M180 50c-15-15-35-10-45 5 12-2 25 3 32 12 4 4 6 9-13-17zM320 50c15-15 35-10 45 5-12-2-25 3-32 12-4 4 6 9-13-17z'/><circle cx='250' cy='50' r='22' fill='%23D4A3A9'/><circle cx='250' cy='50' r='16' fill='%23E8C2C8'/><circle cx='250' cy='50' r='10' fill='%23F4DCDA'/><circle cx='215' cy='60' r='16' fill='%23E8B4B8'/><circle cx='215' cy='60' r='10' fill='%23F4DCDA'/><circle cx='285' cy='60' r='16' fill='%23E8B4B8'/><circle cx='285' cy='60' r='10' fill='%23F4DCDA'/><circle cx='190' cy='72' r='11' fill='%23F3D5D8'/><circle cx='310' cy='72' r='11' fill='%23F3D5D8'/></svg>"

# ──────────────────────────────────────────────
# ESTILOS CSS CORREGIDOS
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

/* Color de texto predeterminado */
p, span, label, div, h1, h2, h3, h4, h5, h6, input, textarea, button {{
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

/* TARJETA DE RESULTADO / SOBRE CONFIRMADO */
.confirmation-envelope-card {{
    background: linear-gradient(135deg, #5B6B58 0%, #4A5A48 100%);
    border-radius: 20px;
    padding: 35px 25px;
    margin: 25px auto;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    border: 2px solid #D4AF37;
    position: relative;
}}
.confirmation-envelope-card * {{
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

/* SUBTÍTULOS CINZEL */
.subtitle-cinzel {{
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1.1rem !important;
    color: #4A5A48 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    margin-top: 5px;
}}

/* Versículo Bíblico */
.verse-card {{
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(244,239,232,0.95) 100%) !important;
    border-left: 4px solid #A3B18A;
    border-right: 4px solid #A3B18A;
}}

.verse-text {{
    font-family: 'Montserrat', sans-serif;
    font-style: italic;
    font-size: 0.98rem;
    color: #4A5A48 !important;
    line-height: 1.7;
    margin: 0;
}}
.verse-ref {{
    font-family: 'Cinzel', serif !important;
    font-size: 0.85rem !important;
    color: #6B7A68 !important;
    font-weight: 600;
    letter-spacing: 2px;
    margin-top: 10px;
    display: block;
}}

/* Elementos del Itinerario */
.timeline-item {{
    padding: 12px 0;
    border-bottom: 1px dashed #CBD5E0;
    font-size: 1rem !important;
    color: #2D3748 !important;
    font-weight: 500 !important;
}}
.timeline-item:last-child {{
    border-bottom: none;
}}

/* SOBRE DE INICIO INTERACTIVO */
.welcome-envelope {{
    background-color: #FAF6F0;
    width: 260px;
    height: 170px;
    margin: 15px auto 15px auto;
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
    transition: all 0.3s ease;
}}
div.stButton > button:first-child * {{
    color: #FFFFFF !important;
}}
div.stButton > button:first-child:hover {{
    background-color: #556353 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES DE DATOS
# ──────────────────────────────────────────────
def cargar_regalos():
    if not CSV_REGALOS.exists():
        return pd.DataFrame(columns=["Regalo"])
    return pd.read_csv(CSV_REGALOS)

def cargar_respuestas():
    if CSV_RESPUESTAS.exists():
        return pd.read_csv(CSV_RESPUESTAS)
    return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo", "Mesa"])

def asignar_regalo(nombre):
    df = cargar_regalos()
    if df.empty:
        return "Detalle de boda a elección personal"
    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

# ──────────────────────────────────────────────
# PASO 1: PANTALLA INICIAL DEL SOBRE
# ──────────────────────────────────────────────
if not st.session_state["invitacion_abierta"]:
    st.markdown("""
    <div class="invitation-card" style="margin-top: 30px;">
        <div class="subtitle-cinzel">NUESTRA BODA</div>
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
        <div class="subtitle-cinzel">NUESTRA BODA 💍</div>
        <div class="title-names">Carlos & Eunice</div>
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600; margin-top: 5px;">
            18 DE JUNIO DE 2027
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 9. FOTO DE LOS NOVIOS (REORGANIZADO: PRIMERO LA FOTO)
    if IMAGEN_HEADER.exists():
        st.markdown(f"""
        <div class="invitation-card">
            <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 15px;">📸 Nuestra Foto</p>
            <img src="{img_b64}" style="width: 100%; max-width: 500px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)

    # 8. MÚSICA DE FONDO (REORGANIZADO: DESPUÉS DE LA FOTO)
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 30px;">
        <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=js2MkCAmTJY")

    # [RESTO DE LOS ELEMENTOS: ALTAR, PADRES, DRESS-CODE, MAPA DEL SALÓN, ETC. SE MANTIENEN IGUAL]
    # [...]
