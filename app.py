import streamlit as st
import pandas as pd
import random
import os
import uuid
from pathlib import Path
from PIL import Image

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
IMAGEN_HEADER = Path("boda_header.jpg")

# ──────────────────────────────────────────────
# ESTILOS VISUALES (Inspirado en la invitación elegida)
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts para la tipografía cursiva elegante */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* Fondo general cálido */
    .stApp {
        background-color: #FAF9F6;
    }
    
    /* Tipografía general */
    h1, h2, h3, p, label, .stMarkdown {
        font-family: 'Montserrat', sans-serif !important;
        color: #2D3748 !important;
    }
    
    /* Encabezado Invitación */
    .boda-subtitulo {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 4px;
        font-size: 1.1rem;
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
        font-size: 1.2rem;
        color: #4A5568;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 25px;
        font-weight: 600;
    }
    
    /* Contenedores tipo tarjeta */
    .boda-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* Badge de Regalos disponibles */
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
    
    /* Tarjeta de resultado del regalo */
    .regalo-resultado {
        background: linear-gradient(135deg, #F7FAFC, #EDF2F7);
        border: 2px dashed #CBD5E0;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Botones principales */
    div.stButton > button:first-child {
        background-color: #4A5568 !important;
        color: #FFFFFF !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 35px !important;
        font-size: 1rem !important;
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2D3748 !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #CBD5E0;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ESTADO DE SESIÓN
# ──────────────────────────────────────────────
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
    """Carga la lista de regalos disponibles con manejo de errores."""
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
    """Carga las respuestas existentes."""
    try:
        if CSV_RESPUESTAS.exists():
            return pd.read_csv(CSV_RESPUESTAS)
        return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo"])
    except Exception as e:
        st.error(f"❌ Error al leer respuestas.csv: {e}")
        return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo"])

def nombre_ya_registrado(nombre: str, df_resp: pd.DataFrame) -> bool:
    """Verifica si un nombre ya fue registrado (insensible a mayúsculas)."""
    return any(
        nombre.strip().lower() == str(n).strip().lower()
        for n in df_resp["Nombre"].tolist()
    )

def asignar_regalo_con_lock(nombre: str) -> str:
    """Asigna un regalo de forma atómica evitando duplicados simultáneos."""
    df = cargar_regalos()
    if df.empty:
        raise ValueError("No quedan regalos disponibles.")

    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

# ──────────────────────────────────────────────
# ENCABEZADO ESTILO INVITACIÓN
# ──────────────────────────────────────────────
st.markdown('<div class="boda-subtitulo">NUESTRA BODA</div>', unsafe_allow_html=True)
st.markdown('<div class="boda-nombres">Carlos & Eunice</div>', unsafe_allow_html=True)
st.markdown('<div class="boda-fecha">18 • 07 • 2027</div>', unsafe_allow_html=True)

# Cargar imagen si existe en la carpeta
if IMAGEN_HEADER.exists():
    try:
        image = Image.open(IMAGEN_HEADER)
        st.image(image, use_container_width=True)
    except Exception:
        pass

# ──────────────────────────────────────────────
# VISTA PRINCIPAL (FORMULARIO)
# ──────────────────────────────────────────────
if not st.session_state.confirmado:
    df_regalos = cargar_regalos()
    disponibles = len(df_regalos)

    st.markdown('<div class="boda-card">', unsafe_allow_html=True)
    if disponibles > 0:
        st.markdown(f"""
            <div class="regalos-badge">
                🎁 Quedan {disponibles} opciones de regalos disponibles
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Todos los regalos de la lista inicial ya han sido asignados.")

    st.write("Por favor ingresa tu nombre completo para confirmar tu asistencia y obtener tu opción de regalo asignada.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── FORMULARIO ──
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

    # ── PROCESAMIENTO ──
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

                        # Guardar respuesta CSV
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

                        # Estado de sesión
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
                    # No asiste
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
# MOSTRAR RESULTADO
# ──────────────────────────────────────────────
if st.session_state.confirmado:
    if st.session_state.asiste == "Sí":
        st.balloons()
        
        st.markdown(f"""
        <div class="boda-card">
            <h2 style="color: #2D3748;">✨ ¡Confirmado, {st.session_state.nombre}! ✨</h2>
            <p>Es un honor para nosotros contar con tu presencia el <strong>18 de Julio de 2027</strong>.</p>
            
            <div class="regalo-resultado">
                <h3 style="margin-bottom: 5px; font-size: 1.1rem; color: #4A5568;">🎁 Tu sugerencia de regalo asignada es:</h3>
                <h1 style="font-size: 2rem; margin: 15px 0; color: #1A202C;">
                    {st.session_state.regalo}
                </h1>
                <p style="font-size: 0.88em; color: #718096; margin-top: 10px;">
                    <em>Este detalle fue asignado al azar para evitar obsequios duplicados. ¡Tu presencia es lo más importante!</em>
                </p>
            </div>
            
            <p style="font-size: 0.85em; color: #A0AEC0;">
                🔑 Código de confirmación: <strong>{st.session_state.codigo}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="boda-card">
            <h2>Gracias por avisarnos, {st.session_state.nombre}</h2>
            <p>Lamentamos que no puedas acompañarnos el 18-07-2027. ¡Te enviamos un gran abrazo!</p>
            <p style="font-size: 0.85em; color: #A0AEC0;">
                🔑 Código de registro: <strong>{st.session_state.codigo}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Botón para resetear en caso de pruebas
    if st.button("🔄 Registrar a otra persona"):
        for key in ["confirmado", "nombre", "regalo", "codigo", "asiste"]:
            st.session_state[key] = "" if key != "confirmado" else False
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
