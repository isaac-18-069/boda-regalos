import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
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

def get_image_base64(path_local):
    if path_local.exists():
        with open(path_local, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return ""

img_b64 = get_image_base64(IMAGEN_HEADER)

SVG_FLORES = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 120'><path fill='%236B7A68' d='M150 70c-20-10-40 0-50 15 15-5 30-2 40 5 5 3 8 7 10 10zM350 70c20-10 40 0 50 15-15-5-30-2-40 5-5 3-8 7-10 10z'/><path fill='%238A9A86' d='M180 50c-15-15-35-10-45 5 12-2 25 3 32 12 4 4 6 9 13-17zM320 50c15-15 35-10 45 5-12-2-25 3-32 12-4 4-6 9-13-17z'/><circle cx='250' cy='50' r='22' fill='%23D4A3A9'/><circle cx='250' cy='50' r='16' fill='%23E8C2C8'/><circle cx='250' cy='50' r='10' fill='%23F4DCDA'/><circle cx='215' cy='60' r='16' fill='%23E8B4B8'/><circle cx='215' cy='60' r='10' fill='%23F4DCDA'/><circle cx='285' cy='60' r='16' fill='%23E8B4B8'/><circle cx='285' cy='60' r='10' fill='%23F4DCDA'/><circle cx='190' cy='72' r='11' fill='%23F3D5D8'/><circle cx='310' cy='72' r='11' fill='%23F3D5D8'/></svg>"

# ──────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

.stApp {{
    background-color: #FAF6F0 !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

p, span, label, div, h1, h2, h3, h4, h5, h6 {{
    color: #2D3748 !important;
}}

html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif !important;
}}

.invitation-card {{
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px;
    padding: 60px 25px;
    margin: 35px auto;
    box-shadow: 0 10px 30px rgba(107, 122, 104, 0.1);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.invitation-card::before {{
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

.invitation-card::after {{
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

.invitation-card * {{
    position: relative;
    z-index: 2;
}}

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

.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #4A5A48 !important;
    margin-bottom: 5px;
    line-height: 1.2;
}}

.subtitle-cinzel {{
    font-family: 'Cinzel', serif !important;
    letter-spacing: 3px;
    font-size: 1.1rem !important;
    color: #4A5A48 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    margin-top: 5px;
}}

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

.timeline-item {{
    padding: 12px 0;
    border-bottom: 1px dashed #CBD5E0;
    font-size: 1rem !important;
    color: #2D3748 !important;
    font-weight: 500 !important;
}}

div[data-baseweb="input"] {{
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
}}

div[data-baseweb="input"] input {{
    color: #1A202C !important;
    background-color: #FFFFFF !important;
}}

.stRadio label {{
    color: #2D3748 !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}}

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

.welcome-envelope {{
    background-color: #5B6B58;
    width: 260px;
    height: 170px;
    margin: 15px auto;
    border-radius: 12px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
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
        df = pd.read_csv(CSV_RESPUESTAS)
        if "Mesa" not in df.columns:
            df["Mesa"] = "Mesa 1"
        return df
    return pd.DataFrame(columns=["Nombre", "Asiste", "Regalo", "Codigo", "Mesa"])

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
    # 1. HEADER
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel">NUESTRA BODA 💍</div>
        <div class="title-names">Carlos & Eunice</div>
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600; margin-top: 5px;">
            18 DE JUNIO DE 2027
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. VERSÍCULO
    st.markdown("""
    <div class="invitation-card verse-card">
        <p class="verse-text">
            «El amor es paciente, es bondadoso. Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta. El amor nunca deja de ser.»
        </p>
        <span class="verse-ref">1 CORINTIOS 13:4, 7-8</span>
    </div>
    """, unsafe_allow_html=True)

    # 3. FOTO / PUZZLE
    if img_b64:
        puzzle_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                background-color: transparent;
                font-family: 'Montserrat', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            .card-container {{
                background-color: #FFFFFF;
                border-radius: 20px;
                padding: 40px 20px 30px 20px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.04);
                border: 1px solid #E8E2D9;
                text-align: center;
                width: 100%;
                max-width: 480px;
            }}
            .instructions {{
                font-size: 13px;
                color: #6B7A68;
                margin-bottom: 25px;
                font-weight: 600;
            }}
            .puzzle-outer-wrapper {{
                position: relative;
                width: 320px;
                height: 320px;
                margin: 0 auto;
            }}
            .frame-wrapper {{
                position: relative;
                width: 310px;
                height: 310px;
                margin: 0 auto;
                padding: 5px;
                background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 50%, #F3E5AB 100%);
                clip-path: polygon(50% 0%, 100% 18%, 100% 82%, 50% 100%, 0% 82%, 0% 18%);
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            #puzzle-board {{
                width: 300px;
                height: 300px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: repeat(3, 1fr);
                gap: 2px;
                background: #FAF6F0;
                clip-path: polygon(50% 0%, 100% 18%, 100% 82%, 50% 100%, 0% 82%, 0% 18%);
            }}
            .tile {{
                width: 100%;
                height: 100%;
                background-image: url('{img_b64}');
                background-size: 300px 300px;
                cursor: pointer;
            }}
            .tile.selected {{
                border: 3px solid #D4AF37;
                transform: scale(0.92);
            }}
            .btn-resolve {{
                margin-top: 25px;
                background-color: #6B7A68;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 20px;
                font-size: 12px;
                cursor: pointer;
                font-weight: 600;
            }}
        </style>
        </head>
        <body>
        <div class="card-container">
            <div class="instructions">🧩 Haz clic en dos piezas para intercambiarlas</div>
            <div class="puzzle-outer-wrapper">
                <div class="frame-wrapper">
                    <div id="puzzle-board"></div>
                </div>
            </div>
            <button class="btn-resolve" onclick="autoSolve()">✨ Armar automáticamente</button>
        </div>
        <script>
            const board = document.getElementById('puzzle-board');
            let tiles = [];
            let selectedTile = null;
            const correctPositions = [
                '0px 0px', '-100px 0px', '-200px 0px',
                '0px -100px', '-100px -100px', '-200px -100px',
                '0px -200px', '-100px -200px', '-200px -200px'
            ];
            let currentPositions = [...correctPositions];
            function shuffle(array) {{
                for (let i = array.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i]], array[j] = [array[j], array[i]];
                }}
            }}
            function initPuzzle() {{
                shuffle(currentPositions);
                renderBoard();
            }}
            function renderBoard() {{
                board.innerHTML = '';
                currentPositions.forEach((pos, index) => {{
                    const tile = document.createElement('div');
                    tile.className = 'tile';
                    tile.style.backgroundPosition = pos;
                    tile.addEventListener('click', () => onTileClick(tile, index));
                    board.appendChild(tile);
                }});
            }}
            function onTileClick(tile, index) {{
                if (selectedTile === null) {{
                    selectedTile = index;
                    board.children[index].classList.add('selected');
                }} else {{
                    let temp = currentPositions[selectedTile];
                    currentPositions[selectedTile] = currentPositions[index];
                    currentPositions[index] = temp;
                    selectedTile = null;
                    renderBoard();
                }}
            }}
            function autoSolve() {{
                currentPositions = [...correctPositions];
                renderBoard();
            }}
            initPuzzle();
        </script>
        </body>
        </html>
        """
        components.html(puzzle_html, height=500)

    # 4. MÚSICA
    st.markdown("""
    <div class="invitation-card" style="padding: 50px 25px 20px 25px;">
        <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)
    st.video("https://youtu.be/js2MkCAmTJY")

    # 5. DÍA Y LUGAR
    st.markdown("""
    <div class="green-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.9rem;">EL GRAN DÍA</div>
        <h2 style="font-size: 2.2rem; margin: 10px 0; color: #FFFFFF !important;">SÁBADO 18 DE JUNIO</h2>
        <p style="font-size: 0.95rem; opacity: 0.9; color: #FFFFFF !important;">2027 • 16:00 HRS</p>
    </div>
    """, unsafe_allow_html=True)

    # 6. ORGANIZACIÓN DEL SALÓN Y MESAS (NUEVA SECCIÓN)
    st.markdown("""
    <div class="invitation-card" id="mesas">
        <div class="subtitle-cinzel">🍽️ ORGANIZACIÓN DEL SALÓN</div>
        <p style="font-size: 0.88rem; color: #6B7A68 !important; margin-top: 5px;">
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
            st.info("No se encontró tu nombre en la lista confirmada. Si te acabas de registrar, la asignación se actualizará pronto.")

    # Visualización gráfica interactiva del mapa de salón
    st.write("")
    if st.checkbox("🗺️ Ver Mapa Completo del Salón", value=True):
        # Agrupar invitados por mesa
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

        # Generar HTML del Mapa Interactivo tipo Bodas.net
        html_mesas = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            .salon-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 25px;
                padding: 15px;
                background-color: #F7F5F0;
                border-radius: 15px;
                border: 1px solid #E2E8F0;
            }
            .table-card {
                background: white;
                border-radius: 50%;
                width: 200px;
                height: 200px;
                margin: 0 auto;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                border: 2px solid #A3B18A;
            }
            .table-center {
                text-align: center;
                z-index: 2;
            }
            .table-title {
                font-family: 'Cinzel', serif;
                font-weight: bold;
                font-size: 13px;
                color: #4A5A48;
            }
            .table-count {
                font-size: 10px;
                color: #718096;
            }
            .guest-avatar {
                position: absolute;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background: #6B7A68;
                color: white;
                font-size: 10px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                overflow: hidden;
                text-align: center;
            }
        </style>
        </head>
        <body>
        <div class="salon-grid">
        """

        import math
        for mesa_nombre, personas in mesas_dict.items():
            html_mesas += f"""
            <div class="table-card">
                <div class="table-center">
                    <div class="table-title">{mesa_nombre}</div>
                    <div class="table-count">{len(personas)} Personas</div>
                </div>
            """
            num_p = len(personas)
            radius = 75  # Radio para distribuir alrededor de la mesa circular
            for idx, p in enumerate(personas):
                angle = (2 * math.pi / max(num_p, 1)) * idx
                x = 84 + radius * math.cos(angle)
                y = 84 + radius * math.sin(angle)
                iniciales = "".join([w[0].upper() for w in p.split()[:2]])
                html_mesas += f"""
                <div class="guest-avatar" style="left: {x}px; top: {y}px;" title="{p}">
                    {iniciales}
                </div>
                """
            html_mesas += "</div>"

        html_mesas += "</div></body></html>"
        components.html(html_mesas, height=520, scrolling=True)

    # 7. CONFIRMACIÓN Y REGALOS
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div class="subtitle-cinzel">CONFIRMAR ASISTENCIA</div>
        <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 8px;">Por favor confirma tu presencia para asignarte tu mesa y sugerencia de regalo.</p>
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
                    mesa_asistente = "Mesa 1"  # Mesa inicial por defecto
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
                        <p style="font-size: 1rem; color: #FFFFFF !important;">
                            Te asignamos temporalmente a la <strong>{mesa_asistente}</strong>.
                        </p>
                        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.4); margin: 15px 0;">
                        <p style="font-size: 0.85rem; color: #F3E5AB !important;">🎁 Sugerencia de Regalo:</p>
                        <h3 style="font-size: 1.5rem; color: #FFFFFF !important;">{regalo}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Agradecemos tu respuesta.")

    # 8. PANEL DE ADMINISTRACIÓN Y ASIGNACIÓN DE MESAS
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

            st.write("### Lista de Confirmados")
            st.dataframe(df_ver, use_container_width=True)
        else:
            st.caption("Aún no hay respuestas.")
