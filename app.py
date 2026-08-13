import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components
import math

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
IMAGEN_FLORES = Path("flores.png") 

def get_image_base64(path):
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return None

flores_base64 = get_image_base64(IMAGEN_FLORES)

# ──────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500;600&display=swap');

.stApp {{
    background-color: #FAF8F5 !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

.invitation-card, .dress-card {{
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 35px 20px 25px 20px;
    margin: 25px auto;
    box-shadow: 0 8px 25px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    text-align: center;
    position: relative;
}}

/* Flores decorativas en las tarjetas */
{f'''
.invitation-card::before, .dress-card::before {{
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
.invitation-card::after, .dress-card::after {{
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

.title-elegant {{
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1rem !important;
    color: #4A5A48 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.5rem !important;
    color: #4A5A48 !important;
    margin-bottom: 15px;
}}

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

.welcome-envelope {{
    background-color: #FAF8F5;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.03);
    margin: 50px auto;
}}

div.stButton > button:first-child {{
    background-color: #6B7A68 !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
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

    # --- ITINERARIO ---
    st.markdown("""
    <div class="invitation-card">
        <div class="title-elegant">ITINERARIO DE ACTIVIDADES</div>
        <div class="timeline-item">⛪ 16:00 hrs — Ceremonia Religiosa</div>
        <div class="timeline-item">🥂 17:30 hrs — Bienvenida y Felicitaciones</div>
        <div class="timeline-item">🍽️ 19:00 hrs — Cena de Gala</div>
        <div class="timeline-item">💃 20:30 hrs — Fiesta y Baile</div>
    </div>
    """, unsafe_allow_html=True)

    # --- CÓDIGO DE VESTIMENTA (CORREGIDO) ---
    st.markdown("""
    <div class="dress-card">
        <div class="title-elegant">👗 CÓDIGO DE VESTIMENTA</div>
        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.1rem; color: #2D3748; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">FORMAL / ELEGANTE</div>
        <div style="font-family: 'Montserrat', sans-serif; color: #2D3748; font-size: 0.9rem; margin-bottom: 15px;">Por favor, reservar el color blanco para la novia y el verde oliva para el cortejo.</div>
        
        <div style="border-top: 1px solid #E2E8F0; margin: 15px 0;"></div>
        
        <div style="font-family: 'Montserrat', sans-serif; font-size: 0.9rem; color: #4A5568; font-weight: 500;">
            🔞 Evento de Adultos (Sin Niños)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- ORGANIZACIÓN DEL SALÓN Y MESAS (REINSERTADO) ---
    st.markdown("""
    <div class="invitation-card" id="mesas">
        <div class="title-elegant">🍽️ ORGANIZACIÓN DEL SALÓN</div>
        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.88rem; color: #6B7A68 !important; margin-top: 5px;">
            Consulta la mesa asignada para tu lugar en la recepción
        </p>
    </div>
    """, unsafe_allow_html=True)

    df_invitados = cargar_respuestas()
    
    # Buscador de mesa por nombre
    busqueda_nombre = st.text_input("🔍 Ingresa tu nombre para buscar tu mesa:", placeholder="Ej: María López")
    
    if busqueda_nombre.strip():
        coincidencias = df_invitados[df_invitados["Nombre"].str.lower().str.contains(busqueda_nombre.strip().lower(), na=False)]
        if not coincidencias.empty:
            for idx, row in coincidencias.iterrows():
                mesa = row.get("Mesa", "Mesa 1")
                st.success(f"📍 **{row['Nombre']}**, estás en la **{mesa}**.")
        else:
            st.info("No se encontró tu nombre en la lista confirmada o aún no tienes mesa asignada.")

    # Visualización gráfica interactiva del mapa de salón (Estilo Bodas.net)
    st.write("")
    if st.checkbox("🗺️ Ver Mapa Completo del Salón", value=True):
        confirmados = df_invitados[df_invitados["Asiste"] == "Sí"] if not df_invitados.empty else pd.DataFrame()
        
        mesas_dict = {}
        # Inicializar mesas base
        for i in range(1, 7):
            mesas_dict[f"Mesa {i}"] = []
        mesas_dict["Mesa Presidencial"] = ["Carlos (Novio)", "Eunice (Novia)"]

        if not confirmados.empty:
            for _, row in confirmados.iterrows():
                m = row.get("Mesa", "Mesa 1")
                if m not in mesas_dict:
                    mesas_dict[m] = []
                mesas_dict[m].append(row["Nombre"])

        # HTML/CSS del Mapa Interactivo
        html_mesas = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            .salon-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 15px;
                background-color: #F7F5F0;
                border-radius: 15px;
                border: 1px solid #E2E8F0;
            }
            .table-card {
                background: white;
                border-radius: 50%;
                width: 180px;
                height: 180px;
                margin: 0 auto;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.06);
                border: 2px solid #A3B18A;
            }
            .table-center { text-align: center; z-index: 2; }
            .table-title { font-family: 'Cinzel', serif; font-weight: bold; font-size: 12px; color: #4A5A48; }
            .table-count { font-family: 'Montserrat', sans-serif; font-size: 10px; color: #718096; }
            .guest-avatar {
                position: absolute;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: #6B7A68;
                color: white;
                font-size: 9px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.15);
                overflow: hidden;
                text-align: center;
                font-family: 'Montserrat', sans-serif;
            }
        </style>
        </head>
        <body>
        <div class="salon-grid">
        """

        for mesa_nombre, personas in mesas_dict.items():
            html_mesas += f"""
            <div class="table-card">
                <div class="table-center">
                    <div class="table-title">{mesa_nombre}</div>
                    <div class="table-count">{len(personas)} Personas</div>
                </div>
            """
            num_p = len(personas)
            radius = 70 
            for idx, p in enumerate(personas):
                angle = (2 * math.pi / max(num_p, 1)) * idx
                x = 75 + radius * math.cos(angle)
                y = 75 + radius * math.sin(angle)
                iniciales = "".join([w[0].upper() for w in p.split()[:2]])
                html_mesas += f"""
                <div class="guest-avatar" style="left: {x}px; top: {y}px;" title="{p}">
                    {iniciales}
                </div>
                """
            html_mesas += "</div>"

        html_mesas += "</div></body></html>"
        components.html(html_mesas, height=500, scrolling=True)

    # --- CONFIRMACIÓN ---
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
        if not nombre.strip():
            st.error("Por favor, ingresa tu nombre.")
        else:
            df_resp = cargar_respuestas()
            if any(nombre.strip().lower() == str(n).strip().lower() for n in df_resp["Nombre"].tolist()):
                st.warning(f"El nombre {nombre.strip()} ya ha sido registrado.")
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
                    st.markdown(f"""
                    <div class="green-card" style="padding: 20px; border-radius: 12px; margin-top: 15px;">
                        <div class="title-elegant" style="color: #FFFFFF !important; font-size: 0.9rem;">TU SUGERENCIA DE REGALO</div>
                        <p style="font-family: 'Montserrat', sans-serif; font-size: 1.5rem; color: #FFFFFF !important; font-weight: 600; margin: 10px 0;">{regalo}</p>
                        <p style="font-family: 'Montserrat', sans-serif; font-size: 0.85rem; color: #E2E8F0 !important;">Código de confirmación: {codigo}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # --- PANEL ADMIN Y GESTOR DE MESAS ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Gestor de Mesas e Invitados)"):
        df_ver = cargar_respuestas()
        if not df_ver.empty:
            st.write("### Asignación Rápida de Mesas")
            invitados_lista = df_ver[df_ver["Asiste"] == "Sí"]["Nombre"].tolist()
            
            if invitados_lista:
                col1, col2 = st.columns(2)
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

            st.write("### Lista General")
            st.dataframe(df_ver, use_container_width=True)
        else:
            st.caption("Aún no hay respuestas.")
