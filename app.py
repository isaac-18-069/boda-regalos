import streamlit as st
import pandas as pd
import random
import os
import uuid
from pathlib import Path
import base64

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Carlos & Eunice 💍", 
    page_icon="✨", 
    layout="centered"
)

# ──────────────────────────────────────────────
# RUTA DE ARCHIVOS
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")

def get_image_base64(path):
    if path.exists():
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return None

# ──────────────────────────────────────────────
# ESTILOS VISUALES (Rosas + Tarjeta Elegante)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

.stApp {
    background-color: #FAF9F6;
}

h1, h2, h3, p, label, .stMarkdown {
    font-family: 'Montserrat', sans-serif !important;
    color: #2D3748 !important;
}

/* Sobre Interactivo */
.envelope-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px auto;
}

.envelope {
    position: relative;
    width: 280px;
    height: 180px;
    background: #90A4AE;
    border-radius: 8px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    display: flex;
    justify-content: center;
    align-items: center;
}

.envelope::before {
    content: '';
    position: absolute;
    top: 0;
    width: 0;
    height: 0;
    border-left: 140px solid transparent;
    border-right: 140px solid transparent;
    border-top: 100px solid #78909C;
}

.seal {
    position: absolute;
    width: 50px;
    height: 50px;
    background: radial-gradient(circle, #D4AF37 0%, #AA7C11 100%);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    z-index: 2;
}

/* Tarjeta de Invitación */
.card-invitation {
    position: relative;
    background-color: #FFFFFF;
    padding: 40px 25px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
    border: 1px solid #E2E8F0;
    margin: 20px auto;
    text-align: center;
    overflow: hidden;
}

.flower-top-left {
    position: absolute;
    top: -10px;
    left: -10px;
    width: 110px;
    opacity: 0.85;
    pointer-events: none;
}
.flower-bottom-right {
    position: absolute;
    bottom: -10px;
    right: -10px;
    width: 110px;
    opacity: 0.85;
    transform: rotate(180deg);
    pointer-events: none;
}

.boda-subtitulo {
    font-family: 'Cinzel', serif !important;
    letter-spacing: 4px;
    font-size: 1rem;
    color: #5A6B7C;
    text-align: center;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.boda-nombres {
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #2C3E50 !important;
    text-align: center;
    margin-top: 0px;
    margin-bottom: 0px;
    line-height: 1.2;
}

.boda-fecha {
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1.1rem;
    color: #4A5568;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
    font-weight: 600;
}

.boda-foto-container {
    margin: 20px auto;
    max-width: 85%;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    border: 3px solid #FAF9F6;
}

.boda-foto-container img {
    width: 100%;
    display: block;
}

.regalos-badge {
    background-color: #EBF8FF;
    color: #2B6CB0;
    border: 1px solid #BEE3F8;
    padding: 10px 18px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.95rem;
    display: inline-block;
    margin-bottom: 15px;
}

.regalo-resultado {
    background: linear-gradient(135deg, #F7FAFC, #EDF2F7);
    border: 2px dashed #CBD5E0;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    margin: 20px 0;
}

div.stButton > button:first-child {
    background-color: #4A5568 !important;
    color: #FFFFFF !important;
    border-radius: 30px !important;
    border: none !important;
    padding: 12px 38px !important;
    font-size: 1rem !important;
    font-family: 'Montserrat', sans-serif !important;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    display: block;
    margin: 15px auto;
}
div.stButton > button:first-child:hover {
    background-color: #2D3748 !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

FLOWER_SVG = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 10C30 15 40 35 30 55C20 40 5 30 10 10Z" fill="#A4C3B2" opacity="0.7"/><path d="M15 5C35 20 45 45 25 65C20 45 5 25 15 5Z" fill="#C4D7D1" opacity="0.6"/><circle cx="45" cy="45" r="18" fill="#E8B4B8" opacity="0.85"/><circle cx="42" cy="42" r="12" fill="#D88A92" opacity="0.9"/><circle cx="40" cy="40" r="6" fill="#B55B65"/><circle cx="65" cy="30" r="12" fill="#F4C2C2" opacity="0.8"/><circle cx="63" cy="28" r="8" fill="#E8B4B8"/></svg>"""

# ──────────────────────────────────────────────
# ESTADO DE SESIÓN
# ──────────────────────────────────────────────
if "paso" not in st.session_state:
    st.session_state.paso = 1

if "confirmado" not in st.session_state:
    st.session_state.confirmado = False
    st.session_state.nombre = ""
    st.session_state.regalo = ""
    st.session_state.codigo = ""
    st.session_state.asiste = ""

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────────
def cargar_regalos() -> pd.DataFrame:
    try:
        if not CSV_REGALOS.exists():
            st.error(f"❌ No se encuentra el archivo {CSV_REGALOS.name}.")
            return pd.DataFrame(columns=["Regalo"])
        df = pd.read_csv(CSV_REGALOS)
        if "Regalo" not in df.columns:
            st.error("❌ El CSV debe tener una columna llamada 'Regalo'.")
            return pd.DataFrame(columns=["Regalo"])
        return df
    except Exception as e:
        st.error(f"❌ Error al leer regalos.csv: {e}")
        return pd.DataFrame(columns=["Regalo"])

def cargar_respuestas() -> pd.DataFrame:
    try:
        if CSV_RESPUESTAS.exists():
            return pd.read_csv(CSV_RESPUESTAS)
        return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo"])
    except Exception as e:
        st.error(f"❌ Error al leer respuestas.csv: {e}")
        return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo"])

def nombre_ya_registrado(nombre: str, df_resp: pd.DataFrame) -> bool:
    return any(
        nombre.strip().lower() == str(n).strip().lower()
        for n in df_resp["Nombre"].tolist()
    )

def asignar_regalo_con_lock(nombre: str) -> str:
    df = cargar_regalos()
    if df.empty:
        raise ValueError("No quedan regalos disponibles.")

    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

# ──────────────────────────────────────────────
# PASO 1: SOBRE CERRADO
# ──────────────────────────────────────────────
if st.session_state.paso == 1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="boda-subtitulo">TIENES UNA INVITACIÓN</div>', unsafe_allow_html=True)
    
    st.markdown("""<div class="envelope-wrapper"><div class="envelope"><div class="seal">🌿</div></div></div>""", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096;'>Haz clic abajo para abrir la invitación</p>", unsafe_allow_html=True)
    
    if st.button("Abrir Invitación ✉️"):
        st.session_state.paso = 2
        st.rerun()

# ──────────────────────────────────────────────
# PASO 2: TARJETA CON ROSAS Y FOTO
# ──────────────────────────────────────────────
elif st.session_state.paso == 2:
    img_b64 = get_image_base64(IMAGEN_HEADER)
    img_html = f'<div class="boda-foto-container"><img src="{img_b64}" /></div>' if img_b64 else ""

    card_html = f"""<div class="card-invitation"><div class="flower-top-left">{FLOWER_SVG}</div><div class="flower-bottom-right">{FLOWER_SVG}</div><div class="boda-subtitulo">NUESTRA BODA</div><div class="boda-nombres">Carlos & Eunice</div><div class="boda-fecha">18 • 07 • 2027</div>{img_html}<p style="font-style: italic; color: #4A5568; margin-top: 15px;">Queremos compartir este día tan especial contigo.</p></div>"""

    st.markdown(card_html, unsafe_allow_html=True)

    if st.button("Siguiente ➡️"):
        st.session_state.paso = 3
        st.rerun()

# ──────────────────────────────────────────────
# PASO 3: FORMULARIO Y REGALOS
# ──────────────────────────────────────────────
elif st.session_state.paso == 3:
    if not st.session_state.confirmado:
        st.markdown('<div class="boda-subtitulo">CONFIRMACIÓN & REGALO</div>', unsafe_allow_html=True)
        st.markdown('<div class="boda-nombres" style="font-size: 2.5rem !important;">Carlos & Eunice</div>', unsafe_allow_html=True)
        st.markdown('<div class="boda-fecha" style="font-size: 1rem;">18 • 07 • 2027</div>', unsafe_allow_html=True)

        df_regalos = cargar_regalos()
        disponibles = len(df_regalos)

        st.markdown('<div class="card-invitation" style="padding: 25px;">', unsafe_allow_html=True)
        if disponibles > 0:
            st.markdown(f'<div class="regalos-badge">🎁 Quedan {disponibles} opciones de regalos en nuestra lista</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Todos los regalos de la lista inicial ya han sido asignados.")

        st.write("Por favor ingresa tu nombre completo para confirmar tu asistencia y recibir la opción de regalo asignada.")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.form("boda_form"):
            nombre = st.text_input(
                "Tu Nombre Completo:",
                placeholder="Ej: María García López"
            )
            asiste = st.radio(
                "¿Nos acompañarás en este día tan especial?",
                ["¡Sí, ahí estaré! 🎉", "Lamentablemente no puedo 😢"]
            )
            st.markdown("<br>", unsafe_allow_html=True)
            btn = st.form_submit_button("Confirmar Asistencia")

        if btn:
            if not nombre.strip():
                st.error("📝 Por favor escribe tu nombre.")
            else:
                df_resp_existente = cargar_respuestas()
                if nombre_ya_registrado(nombre, df_resp_existente):
                    st.warning(f"⚠️ El nombre **{nombre.strip()}** ya se encuentra registrado.")
                else:
                    codigo = uuid.uuid4().hex[:8].upper()
                    
                    if asiste == "¡Sí, ahí estaré! 🎉":
                        try:
                            regalo = asignar_regalo_con_lock(nombre.strip())

                            nueva = pd.DataFrame([{
                                "Nombre": nombre.strip(),
                                "Asiste": "Sí",
                                "Regalo": regalo,
                                "Codigo": codigo
                            }])
                            nueva.to_csv(
                                CSV_RESPUESTAS, mode='a',
                                header=not CSV_RESPUESTAS.exists(), index=False
                            )

                            st.session_state.confirmado = True
                            st.session_state.nombre = nombre.strip()
                            st.session_state.regalo = regalo
                            st.session_state.codigo = codigo
                            st.session_state.asiste = "Sí"

                            st.rerun()

                        except ValueError as e:
                            st.error(f"❌ {e}")
                        except Exception as e:
                            st.error(f"❌ Ocurrió un error inesperado: {e}")
                    else:
                        nueva = pd.DataFrame([{
                            "Nombre": nombre.strip(),
                            "Asiste": "No",
                            "Regalo": "N/A",
                            "Codigo": codigo
                        }])
                        nueva.to_csv(
                            CSV_RESPUESTAS, mode='a',
                            header=not CSV_RESPUESTAS.exists(), index=False
                        )

                        st.session_state.confirmado = True
                        st.session_state.nombre = nombre.strip()
                        st.session_state.regalo = "N/A"
                        st.session_state.codigo = codigo
                        st.session_state.asiste = "No"

                        st.rerun()

# ──────────────────────────────────────────────
# RESULTADO FINAL
# ──────────────────────────────────────────────
if st.session_state.confirmado:
    if st.session_state.asiste == "Sí":
        st.balloons()
        
        st.markdown(f"""
        <div class="card-invitation">
            <h2 style="color: #2D3748;">✨ ¡Confirmado, {st.session_state.nombre}! ✨</h2>
            <p>Es un honor para nosotros contar con tu presencia el <strong>18 de Julio de 2027</strong>.</p>
            <div class="regalo-resultado">
                <h3 style="margin-bottom: 5px; font-size: 1.1rem; color: #4A5568;">🎁 Tu sugerencia de regalo asignada es:</h3>
                <h1 style="font-size: 2rem; margin: 15px 0; color: #1A202C;">{st.session_state.regalo}</h1>
                <p style="font-size: 0.88em; color: #718096; margin-top: 10px;"><em>Este detalle fue asignado al azar para evitar obsequios duplicados. ¡Tu presencia es lo más importante!</em></p>
            </div>
            <p style="font-size: 0.85em; color: #A0AEC0;">🔑 Código de confirmación: <strong>{st.session_state.codigo}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="card-invitation">
            <h2>Gracias por avisarnos, {st.session_state.nombre}</h2>
            <p>Lamentamos que no puedas acompañarnos el 18-07-2027. ¡Te enviamos un gran abrazo!</p>
            <p style="font-size: 0.85em; color: #A0AEC0;">🔑 Código de registro: <strong>{st.session_state.codigo}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 Registrar a otra persona"):
        for key in ["confirmado", "nombre", "regalo", "codigo", "asiste"]:
            st.session_state[key] = "" if key != "confirmado" else False
        st.session_state.paso = 1
        st.rerun()

# ──────────────────────────────────────────────
# PANEL ADMIN
# ──────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📊 Ver lista de invitados (Panel Admin)", expanded=False):
    df_resp = cargar_respuestas()
    if not df_resp.empty:
        st.dataframe(df_resp, use_container_width=True, hide_index=True)
        st.download_button(
            label="📥 Descargar respuestas en Excel/CSV",
            data=df_resp.to_csv(index=False).encode("utf-8"),
            file_name="respuestas_boda_carlos_eunice.csv",
            mime="text/csv"
        )
    else:
        st.caption("Aún no se han recibido confirmaciones.")
