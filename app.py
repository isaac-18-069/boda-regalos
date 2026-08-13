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

# Initialize Session State para controlar la apertura del sobre
if "invitacion_abierta" not in st.session_state:
    st.session_state["invitacion_abierta"] = False

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")

# Ruta opcional para la imagen decorativa de flores (PNG transparente)
# Si no la tienes, el código funcionará igual, solo que sin las flores.
IMAGEN_FLORES = Path("flores.png") 

def get_image_base64(path):
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            # Asumimos PNG para soporte de transparencia
            return f"data:image/png;base64,{encoded}"
    return None

flores_base64 = get_image_base64(IMAGEN_FLORES)

# ──────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500;600&display=swap');

/* Color de fondo de la página */
.stApp {{
    background-color: #FAF8F5 !important;
}}

/* Ocultar elementos predeterminados de Streamlit */
#MainMenu, footer, header {{visibility: hidden;}}

/* Estilo para las tarjetas de información (bordes redondeados, sombra, fondo blanco) */
.invitation-card {{
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 30px 20px 20px 20px;
    margin: 25px auto;
    box-shadow: 0 8px 25px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    text-align: center;
    position: relative;
}}

/* Flores decorativas en las tarjetas (opcional) */
{f'''
.invitation-card::before {{
    content: "";
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 35px;
    background-image: url("{flores_base64}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.8;
}}
.invitation-card::after {{
    content: "";
    position: absolute;
    bottom: 5px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 100px;
    height: 35px;
    background-image: url("{flores_base64}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.8;
}}
''' if flores_base64 else ""}

/* Títulos principales (tipo Cinzel, elegantes) */
.title-elegant {{
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1rem !important;
    color: #4A5A48 !important; /* Verde oliva oscuro */
    font-weight: 600 !important;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

/* Títulos de nombres (tipo Great Vibes, caligrafía) */
.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.5rem !important;
    color: #4A5A48 !important;
    margin-bottom: 15px;
}}

/* Estilo para los ítems del itinerario */
.timeline-item {{
    padding: 10px 0;
    border-bottom: 1px dashed #CBD5E0;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.95rem !important;
    color: #2D3748 !important;
    font-weight: 500 !important;
}}
.timeline-item:last-child {{
    border-bottom: none;
}}

/* Estilo para los ítems del código de vestimenta */
.dresscode-item {{
    font-family: 'Montserrat', sans-serif;
    color: #2D3748 !important;
    margin-top: 10px;
    font-size: 0.9rem !important;
}}

/* SOBRE DE INICIO */
.welcome-envelope {{
    background-color: #FAF8F5;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.03);
    margin: 50px auto;
}}

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
# PASO 1: PANTALLA INICIAL DEL SOBRE
# ──────────────────────────────────────────────
if not st.session_state["invitacion_abierta"]:
    st.markdown("""
    <div class="welcome-envelope">
        <div class="title-elegant" style="font-size: 0.8rem; letter-spacing: 2px;">NUESTRA BODA</div>
        <div style="font-family: 'Cinzel', serif; font-size: 2rem; color: #AA7C11; margin: 20px 0;">💍</div>
        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.95rem; color: #4A5568;">Has recibido una invitación</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✉️ Click para abrir la invitación"):
        st.session_state["invitacion_abierta"] = True
        st.rerun()

# ──────────────────────────────────────────────
# PASO 2: CONTENIDO DE LA INVITACIÓN
# ──────────────────────────────────────────────
else:
    # --- HEADER ---
    st.markdown("""
    <div class="invitation-card">
        <div class="title-elegant" style="font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 5px;">NUESTRA BODA</div>
        <div class="title-names">Carlos & Eunice</div>
        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.9rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; font-weight: 500;">
            Te invitamos a celebrar con nosotros
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN 1: ITINERARIO DE ACTIVIDADES ---
    st.markdown("""
    <div class="invitation-card">
        <div class="title-elegant">ITINERARIO DE ACTIVIDADES</div>
        <div class="timeline-item">⛪ 16:00 hrs — Ceremonia Religiosa</div>
        <div class="timeline-item">🥂 17:30 hrs — Bienvenida y Felicitaciones</div>
        <div class="timeline-item">🍽️ 19:00 hrs — Cena de Gala</div>
        <div class="timeline-item">💃 20:30 hrs — Fiesta y Baile</div>
    </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN 2: CÓDIGO DE VESTIMENTA ---
    st.markdown("""
    <div class="invitation-cardDressCode">
        <div class="title-elegant">👗 CÓDIGO DE VESTIMENTA</div>
        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.1rem; color: #2D3748; font-weight: 600; text-transform: uppercase;">FORMAL / ELEGANTE</div>
        <div class="dresscode-item">Por favor, reservar el color blanco para la novia y el verde oliva para el cortejo.</div>
        
        <div style="border-top: 1px solid #E2E8F0; margin: 20px 0;"></div>
        
        <div style="font-family: 'Montserrat', sans-serif; font-size: 0.9rem; color: #4A5568; font-weight: 500;">
            🔞 Evento de Adultos (Sin Niños)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- CONFIRMACIÓN DE ASISTENCIA Y REGALOS ---
    st.markdown("""
    <div class="invitation-card">
        <div class="title-elegant">CONFIRMAR ASISTENCIA</div>
        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.9rem; color: #4A5568;">Por favor confirma tu presencia y recibe tu sugerencia de regalo.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_invitacion"):
        nombre = st.text_input("Nombre y Apellido:", placeholder="Ej: María López")
        asistencia = st.radio("¿Nos acompañarás?", ["¡Sí, allí estaré! 🎉", "Lo siento, no podré asistir 😢"])
        submit = st.form_submit_button("Enviar Confirmación ✉️")

    if submit:
        if not nombre:
            st.error("Por favor, ingresa tu nombre.")
        else:
            df_resp = cargar_respuestas()
            if nombre in df_resp["Nombre"].tolist():
                st.warning(f"El nombre {nombre} ya ha sido registrado.")
            else:
                codigo = uuid.uuid4().hex[:8].upper()
                if asistencia == "¡Sí, allí estaré! 🎉":
                    regalo = asignar_regalo(nombre)
                    asiste_val = "Sí"
                else:
                    regalo = "N/A"
                    asiste_val = "No"

                nueva_fila = pd.DataFrame([{
                    "Nombre": nombre,
                    "Asiste": asiste_val,
                    "Regalo": regalo,
                    "Codigo": codigo
                }])
                nueva_fila.to_csv(CSV_RESPUESTAS, mode='a', header=not CSV_RESPUESTAS.exists(), index=False)

                st.success("¡Respuesta guardada con éxito!")
                if asiste_val == "Sí":
                    st.markdown(f"""
                    <div class="green-card" style="padding: 20px; border-radius: 12px; margin-top: 15px;">
                        <div class="title-elegant" style="color: #FFFFFF !important; font-size: 0.9rem;">TU SUGERENCIA DE REGALO</div>
                        <p style="font-family: 'Montserrat', sans-serif; font-size: 1.5rem; color: #FFFFFF !important; font-weight: 600; margin: 10px 0;">{regalo}</p>
                        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.85rem; color: #E2E8F0 !important;">Código de confirmación: {codigo}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # --- PANEL ADMIN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Ver invitados)"):
        df_ver = cargar_respuestas()
        if not df_ver.empty:
            st.write("Lista de confirmaciones:")
            st.dataframe(df_ver)
        else:
            st.caption("Aún no hay respuestas.")
