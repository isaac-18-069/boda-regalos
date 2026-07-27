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
    page_title="Nuestra Boda 💍", 
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
# ESTILOS VISUALES (Verde Claro, Blanco y Elegante)
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Fuentes y Títulos */
    h1, h2, h3, p, label, .stMarkdown {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #1c3b2b !important; /* Verde bosque oscuro */
    }
    
    /* Contenedores elegantes tipo tarjeta */
    .boda-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2ebe4;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* Badge de Regalos disponibles */
    .regalos-badge {
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* Tarjeta de resultado final */
    .regalo-resultado {
        background: linear-gradient(135deg, #F1F8E9, #E8F5E9);
        border: 2px solid #81C784;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Botones primarios y de formulario */
    div.stButton > button:first-child {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 30px !important;
        font-size: 1.1em !important;
        font-family: 'Georgia', serif !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Entradas de texto */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #C8E6C9;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ESTADO DE SESIÓN — persiste entre recargas
# ──────────────────────────────────────────────
if "confirmado" not in st.session_state:
    st.session_state.confirmado = False
    st.session_state.nombre = ""
    st.session_state.regalo = ""
    st.session_state.codigo = ""
    st.session_state.asiste = ""

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES DE LÓGICA
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
# CABECERA Y FOTO DE LA INVITACIÓN
# ──────────────────────────────────────────────
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>¡Nos Casamos!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #558B2F;'>Queremos compartir este día tan especial contigo</p>", unsafe_allow_html=True)

# Cargar imagen si existe
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
                🎁 Quedan {disponibles} opciones de regalos en nuestra lista
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Todos los regalos de la lista inicial ya han sido asignados.")

    st.write("Ingresa tu nombre y confirma si nos acompañarás. El sistema te asignará una opción al azar de nuestra lista para no repetir detalles.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── FORMULARIO ──
    with st.form("boda_form"):
        nombre = st.text_input(
            "Tu Nombre Completo:",
            placeholder="Ej: María García López"
        )
        asiste = st.radio(
            "¿Nos acompañarás en nuestro gran día?",
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
# MOSTRAR RESULTADO (Persiste tras recargar)
# ──────────────────────────────────────────────
if st.session_state.confirmado:
    if st.session_state.asiste == "Sí":
        st.balloons()
        
        st.markdown(f"""
        <div class="boda-card">
            <h2 style="color: #2E7D32;">✨ ¡Confirmado, {st.session_state.nombre}! ✨</h2>
            <p>Es un honor para nosotros contar con tu presencia en este gran día.</p>
            
            <div class="regalo-resultado">
                <h3 style="margin-bottom: 5px;">🎁 Tu regalo asignado es:</h3>
                <h1 style="font-size: 2.2em; margin: 10px 0; color: #1B5E20;">
                    {st.session_state.regalo}
                </h1>
                <p style="font-size: 0.9em; opacity: 0.8;">
                    <em>Tu presencia es nuestro mejor regalo. Este detalle fue asignado al azar por el sistema para construir nuestro hogar sin repetir obsequios.</em>
                </p>
            </div>
            
            <p style="font-size: 0.85em; color: #666;">
                🔑 Código de confirmación: <strong>{st.session_state.codigo}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="boda-card">
            <h2>Gracias por avisarnos, {st.session_state.nombre}</h2>
            <p>Lamentamos mucho que no puedas acompañarnos. ¡Te mandamos un fuerte abrazo!</p>
            <p style="font-size: 0.85em; color: #666;">
                🔑 Código de registro: <strong>{st.session_state.codigo}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Botón auxiliar para resetear en pruebas
    if st.button("🔄 Registrar a otra persona"):
        for key in ["confirmado", "nombre", "regalo", "codigo", "asiste"]:
            st.session_state[key] = "" if key != "confirmado" else False
        st.rerun()

# ──────────────────────────────────────────────
# SECCIÓN ADMIN (Oculta en Expander)
# ──────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📊 Ver lista de invitados (Panel Admin)", expanded=False):
    df_resp = cargar_respuestas()
    if not df_resp.empty:
        st.dataframe(df_resp, use_container_width=True, hide_index=True)
        st.download_button(
            label="📥 Descargar respuestas en Excel/CSV",
            data=df_resp.to_csv(index=False).encode("utf-8"),
            file_name="respuestas_boda.csv",
            mime="text/csv"
        )
    else:
        st.caption("Aún no se han recibido confirmaciones.")
