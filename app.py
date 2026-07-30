import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Carlos & Eunice 💍", 
    page_icon="🌿", 
    layout="centered"
)

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")

def get_image_base64(path):
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return None

img_b64 = get_image_base64(IMAGEN_HEADER)

# ──────────────────────────────────────────────
# ESTILOS CSS ESTILO CANVA / VERDE OLIVA (LEGIBILIDAD MEJORADA)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500;600&display=swap');

/* Fondo general suave */
.stApp {
    background-color: #FAF8F5 !important;
}

/* Ocultar elementos sobrantes de Streamlit */
#MainMenu, footer, header {visibility: hidden;}

/* Forzar color oscuro legible en TODOS los textos */
p, span, label, div, h1, h2, h3, h4, h5, h6 {
    color: #2D3748 !important;
}

/* Tipografía general */
html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif !important;
}

/* Contenedores tipo tarjeta */
.invitation-card {
    background-color: #FFFFFF !important;
    border-radius: 16px;
    padding: 30px 20px;
    margin: 25px auto;
    box-shadow: 0 8px 25px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    text-align: center;
    position: relative;
}

.green-card {
    background-color: #6B7A68 !important;
    border-radius: 16px;
    padding: 30px 20px;
    margin: 25px auto;
    text-align: center;
}
.green-card * {
    color: #FFFFFF !important;
}

/* Títulos elegantes */
.title-names {
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.5rem !important;
    color: #4A5A48 !important;
    margin-bottom: 0px;
    line-height: 1.2;
}

.subtitle-cinzel {
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1rem !important;
    color: #4A5A48 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
}

/* Agenda / Itinerario */
.timeline-item {
    padding: 12px 0;
    border-bottom: 1px dashed #CBD5E0;
    font-size: 1rem !important;
    color: #2D3748 !important;
    font-weight: 500 !important;
}
.timeline-item:last-child {
    border-bottom: none;
}

/* Estilos de Formulario (Labels, Inputs y Radio) */
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] input {
    color: #1A202C !important;
    background-color: #FFFFFF !important;
}

.stRadio label {
    color: #2D3748 !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}

/* Botones con estilo oliva */
div.stButton > button:first-child {
    background-color: #6B7A68 !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 12px 35px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    width: 100%;
    transition: all 0.3s ease;
}
div.stButton > button:first-child * {
    color: #FFFFFF !important;
}
div.stButton > button:first-child:hover {
    background-color: #556353 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Sobre animado */
.envelope-box {
    background-color: #5B6B58;
    width: 220px;
    height: 140px;
    margin: 20px auto;
    border-radius: 8px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 15px rgba(0,0,0,0.15);
}
.envelope-seal {
    width: 45px;
    height: 45px;
    background: radial-gradient(circle, #D4AF37 0%, #AA7C11 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-size: 18px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────────
def cargar_regalos():
    if not CSV_REGALOS.exists():
        return pd.DataFrame(columns=["Regalo"])
    return pd.read_csv(CSV_REGALOS)

def cargar_respuestas():
    if CSV_RESPUESTAS.exists():
        return pd.read_csv(CSV_RESPUESTAS)
    return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo"])

def asignar_regalo(nombre):
    df = cargar_regalos()
    if df.empty:
        return "Detalle de boda a elección personal"
    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

# ──────────────────────────────────────────────
# VISTA PRINCIPAL DE LA INVITACIÓN
# ──────────────────────────────────────────────

# HEADER CON NOMBRES
st.markdown("""
<div class="invitation-card">
    <div class="subtitle-cinzel">NUESTRA BODA 😍💍</div>
    <div class="title-names">Carlos & Eunice 😍 </div>
    <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600; margin-top: 5px;">
        18 DE JULIO DE 2027
    </div>
</div>
""", unsafe_allow_html=True)

# FOTO DE LOS NOVIOS
if img_b64:
    st.markdown(f"""
    <div class="invitation-card" style="padding: 10px; overflow: hidden;">
        <img src="{img_b64}" style="width: 100%; border-radius: 12px; display: block;" />
    </div>
    """, unsafe_allow_html=True)

# MÚSICA DE FONDO (ROMÁNTICA DE VIOLÍN)
st.markdown("""
<div class="invitation-card" style="padding-bottom: 10px;">
    <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
</div>
""", unsafe_allow_html=True)

st.video("https://youtu.be/js2MkCAmTJY")

# PADRES Y PADRINOS
st.markdown("""
<div class="invitation-card">
    <div class="subtitle-cinzel" style="margin-bottom: 15px;">Con la bendición de Dios y nuestros padres</div>
    <div style="display: flex; justify-content: space-around; font-size: 0.9rem; margin-top: 10px;">
        <div>
            <strong>Padres del Novio</strong><br>Carlos M & Diana P
        </div>
        <div>
            <strong>Padres de la Novia</strong><br>Emilio M & Pricila C
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# DÍA Y CALENDARIO
st.markdown("""
<div class="green-card">
    <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.9rem;">EL GRAN DÍA</div>
    <h2 style="font-size: 2.2rem; margin: 10px 0; color: #FFFFFF !important;">SÁBADO 18 DE JULIO</h2>
    <p style="font-size: 0.95rem; opacity: 0.9; color: #FFFFFF !important;">2027 • 20:00 HRS</p>
</div>
""", unsafe_allow_html=True)

# UBICACIÓN Y CEREMONIA
st.markdown("""
<div class="invitation-card">
    <div class="subtitle-cinzel">⛪ Boda Civil </div>
    <p style="margin-top: 8px; font-weight: 600; font-size: 1rem;">Registro  civil del Canton Babahoyo </p>
    <p style="font-size: 0.9rem; color: #4A5568 !important;">15:30 HRS</p>
    <a href="https://maps.google.com" target="_blank" style="text-decoration: none;">
        <div style="background-color: #E2E8F0; color: #2D3748 !important; padding: 8px 15px; border-radius: 15px; display: inline-block; font-size: 0.85rem; margin-top: 5px; font-weight: 500;">
            📍 Ver ubicación en GPS
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# ITINERARIO
st.markdown("""
<div class="invitation-card">
    <div class="subtitle-cinzel" style="margin-bottom: 15px;">Itinerario de Actividades</div>
    <div class="timeline-item">⛪ 15:30 hrs — Boda Civil </div>
    <div class="timeline-item">🥂 20:30 hrs — Bienvenida y felicitaciones a los recien casados </div>
    <div class="timeline-item">🍽️ 21:00 hrs — Cena de Gala</div>
    <div class="timeline-item">💃 21:30 hrs — Evento Musical</div>
</div>
""", unsafe_allow_html=True)

# DRESS CODE & NOTAS
st.markdown("""
<div class="invitation-card">
    <div class="subtitle-cinzel">👗 Código de Vestimenta</div>
    <p style="font-size: 1.1rem; font-weight: 600; color: #4A5A48 !important; margin-top: 5px;">FORMAL / ELEGANTE</p>
    <p style="font-size: 0.85rem; color: #4A5568 !important;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
    <hr style="margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;">
    <p style="font-size: 0.9rem; font-weight: 600;">🔞 Evento de Adultos (Sin Niños)</p>
</div>
""", unsafe_allow_html=True)

# SECCIÓN DE CONFIRMACIÓN Y REGALOS
st.markdown("""
<div class="invitation-card" id="confirmacion">
    <div class="envelope-box">
        <div class="envelope-seal">🌿</div>
    </div>
    <div class="subtitle-cinzel">CONFIRMAR ASISTENCIA</div>
    <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 5px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
</div>
""", unsafe_allow_html=True)

# FORMULARIO
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
            else:
                regalo = "N/A"
                asiste_val = "No"

            nueva_fila = pd.DataFrame([{
                "Nombre": nombre.strip(),
                "Asiste": asiste_val,
                "Regalo": regalo,
                "Codigo": codigo
            }])
            nueva_fila.to_csv(CSV_RESPUESTAS, mode='a', header=not CSV_RESPUESTAS.exists(), index=False)

            st.success("¡Respuesta guardada con éxito!")
            if asiste_val == "Sí":
                st.balloons()
                st.markdown(f"""
                <div class="green-card">
                    <h3 style="color:#FFFFFF !important;">🎁 Tu sugerencia de regalo:</h3>
                    <h1 style="font-size: 2rem; color:#FFFFFF !important;">{regalo}</h1>
                    <p style="font-size: 0.85rem; color:#FFFFFF !important;">Código de confirmación: {codigo}</p>
                </div>
                """, unsafe_allow_html=True)

# ADMIN PANEL (EXPANDIBLE)
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📊 Panel Admin (Ver invitados)"):
    df_ver = cargar_respuestas()
    if not df_ver.empty:
        st.dataframe(df_ver, use_container_width=True)
    else:
        st.caption("Aún no hay respuestas.")
