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

# Initialize Session State para controlar la apertura del sobre
if "invitacion_abierta" not in st.session_state:
    st.session_state["invitacion_abierta"] = False

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS EN GITHUB / LOCAL
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

# SVG limpios de flores vectoriales (para evitar marcos/círculos recortados)
FLOWER_TOP_SVG = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 60'><path fill='%23C58B95' d='M100 35c-15 0-25-10-25-20s10-15 25-15 25 5 25 15-10 20-25 20z'/><path fill='%23E1B3BD' d='M80 30c-10 0-18-8-18-15s8-12 18-12 18 5 18 12-8 15-18 15z'/><path fill='%23E1B3BD' d='M120 30c-10 0-18-8-18-15s8-12 18-12 18 5 18 12-8 15-18 15z'/><path fill='%237D8D78' d='M60 30c-15 5-25 0-30-10 10 0 20 5 30 10z'/><path fill='%237D8D78' d='M140 30c15 5 25 0 30-10-10 0-20 5-30 10z'/></svg>"

# ──────────────────────────────────────────────
# ESTILOS CSS CORREGIDOS
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

/* TARJETAS CON ESPACIO CORRECTO PARA LAS FLORES */
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

/* FLORES SUPERIORES CENTRADAS Y LIMPIAS */
.invitation-card::before {{
    content: "";
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    width: 180px;
    height: 45px;
    background-image: url("{FLOWER_TOP_SVG}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.9;
    pointer-events: none;
    z-index: 1;
}}

/* FLORES INFERIORES CENTRADAS Y LIMPIAS */
.invitation-card::after {{
    content: "";
    position: absolute;
    bottom: 5px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 180px;
    height: 45px;
    background-image: url("{FLOWER_TOP_SVG}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.9;
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
.timeline-item:last-child {{
    border-bottom: none;
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
div.stButton > button:first-child:hover {{
    background-color: #556353 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.welcome-envelope {{
    background-color: #5B6B58;
    width: 260px;
    height: 170px;
    margin: 15px auto 15px auto;
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

    # 2. VERSÍCULO BÍBLICO DE AMOR
    st.markdown("""
    <div class="invitation-card verse-card">
        <p class="verse-text">
            «El amor es paciente, es bondadoso. Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta. El amor nunca deja de ser.»
        </p>
        <span class="verse-ref">1 CORINTIOS 13:4, 7-8</span>
    </div>
    """, unsafe_allow_html=True)

    # 3. FOTO INTERACTIVA CON MARCO Y FLORES LIMPIAS EN LAS ESQUINAS
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
                position: relative;
                overflow: visible;
            }}
            .instructions {{
                font-size: 13px;
                color: #6B7A68;
                margin-bottom: 25px;
                font-weight: 600;
                position: relative;
                z-index: 5;
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
                z-index: 2;
            }}

            /* FLORES EN ESQUINA SUPERIOR IZQUIERDA */
            .floral-corner-left {{
                position: absolute;
                top: -20px;
                left: -20px;
                width: 110px;
                height: 110px;
                background-image: url("{FLOWER_TOP_SVG}");
                background-size: contain;
                background-repeat: no-repeat;
                transform: rotate(-30deg);
                z-index: 4;
                pointer-events: none;
            }}

            /* FLORES EN ESQUINA INFERIOR DERECHA */
            .floral-corner-right {{
                position: absolute;
                bottom: -20px;
                right: -20px;
                width: 110px;
                height: 110px;
                background-image: url("{FLOWER_TOP_SVG}");
                background-size: contain;
                background-repeat: no-repeat;
                transform: rotate(150deg);
                z-index: 4;
                pointer-events: none;
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
                position: relative;
                z-index: 3;
            }}
            .tile {{
                width: 100%;
                height: 100%;
                background-image: url('{img_b64}');
                background-size: 300px 300px;
                cursor: pointer;
                transition: transform 0.2s, border 0.2s;
                border: 1px solid rgba(255,255,255,0.4);
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
                position: relative;
                z-index: 5;
            }}
            .success-msg {{
                display: none;
                color: #4A5A48;
                font-weight: bold;
                margin-top: 12px;
                font-size: 14px;
                position: relative;
                z-index: 5;
            }}
        </style>
        </head>
        <body>
        <div class="card-container">
            <div class="instructions">🧩 Haz clic en dos piezas para intercambiarlas y armar la foto</div>
            
            <div class="puzzle-outer-wrapper">
                <div class="floral-corner-left"></div>
                <div class="floral-corner-right"></div>
                <div class="frame-wrapper">
                    <div id="puzzle-board"></div>
                </div>
            </div>

            <button class="btn-resolve" onclick="autoSolve()">✨ Armar automáticamente</button>
            <div id="success" class="success-msg">🎉 ¡Nuestra foto está lista! ❤️</div>
        </div>

        <script>
            const board = document.getElementById('puzzle-board');
            const successMsg = document.getElementById('success');
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
                    [array[i], array[j]] = [array[j], array[i]];
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
                    tile.dataset.index = index;
                    tile.addEventListener('click', () => onTileClick(tile, index));
                    board.appendChild(tile);
                }});
                checkWin();
            }}

            function onTileClick(tile, index) {{
                if (selectedTile === null) {{
                    selectedTile = index;
                    board.children[index].classList.add('selected');
                }} else {{
                    let prevIndex = selectedTile;
                    let temp = currentPositions[prevIndex];
                    currentPositions[prevIndex] = currentPositions[index];
                    currentPositions[index] = temp;

                    selectedTile = null;
                    renderBoard();
                }}
            }}

            function checkWin() {{
                let isWin = currentPositions.every((val, i) => val === correctPositions[i]);
                if (isWin) {{
                    successMsg.style.display = 'block';
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
        components.html(puzzle_html, height=530)

    # 4. MÚSICA DE FONDO (YOUTUBE)
    st.markdown("""
    <div class="invitation-card" style="padding: 50px 25px 20px 25px;">
        <p style="font-size: 0.95rem; color: #4A5A48 !important; font-weight: 600; margin-bottom: 10px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)

    st.video("https://youtu.be/js2MkCAmTJY")

    # 5. PADRES Y PADRINOS
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel" style="margin-bottom: 15px;">Con la bendición de Dios y nuestros padres</div>
        <div style="display: flex; justify-content: space-around; font-size: 0.9rem; margin-top: 10px;">
            <div>
                <strong>Padres del Novio</strong><br>Carlos M & Diana ❤️
            </div>
            <div>
                <strong>Padres de la Novia</strong><br>Emilio M & Pricila C ❤️
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. DÍA Y CALENDARIO
    st.markdown("""
    <div class="green-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.9rem;">EL GRAN DÍA</div>
        <h2 style="font-size: 2.2rem; margin: 10px 0; color: #FFFFFF !important;">SÁBADO 18 DE JUNIO</h2>
        <p style="font-size: 0.95rem; opacity: 0.9; color: #FFFFFF !important;">2027 • 16:00 HRS</p>
    </div>
    """, unsafe_allow_html=True)

    # 7. UBICACIÓN Y CEREMONIA
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel">⛪ Ceremonia</div>
        <p style="margin-top: 8px; font-weight: 600; font-size: 1rem;"></p>
        <p style="font-size: 0.9rem; color: #4A5568 !important;">16:00 HRS</p>
        <a href="https://maps.google.com" target="_blank" style="text-decoration: none;">
            <div style="background-color: #E2E8F0; color: #2D3748 !important; padding: 8px 15px; border-radius: 15px; display: inline-block; font-size: 0.85rem; margin-top: 5px; font-weight: 500; position:relative; z-index:2;">
                📍 Ver ubicación en GPS
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 8. ITINERARIO
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel" style="margin-bottom: 15px;">Itinerario de Actividades</div>
        <div class="timeline-item">⛪ 16:00 hrs — Ceremonia</div>
        <div class="timeline-item">🥂 20:00 hrs — Bienvenida y Felicitaciones A Los Recién Casados</div>
        <div class="timeline-item">🍽️ 20:30 hrs — Cena de Gala</div>
        <div class="timeline-item" style="border-bottom:none;">💃 21:30 hrs — Fiesta y Baile</div>
    </div>
    """, unsafe_allow_html=True)

    # 9. DRESS CODE & NOTAS
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel">👗 Código de Vestimenta</div>
        <p style="font-size: 1.1rem; font-weight: 600; color: #4A5A48 !important; margin-top: 8px;">FORMAL / ELEGANTE</p>
        <p style="font-size: 0.85rem; color: #4A5568 !important;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #E2E8F0;">
        <p style="font-size: 0.9rem; font-weight: 600;">🔞 Evento de Adultos (Sin Niños)</p>
    </div>
    """, unsafe_allow_html=True)

    # 10. SECCIÓN DE CONFIRMACIÓN Y REGALOS
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div class="subtitle-cinzel">CONFIRMAR ASISTENCIA</div>
        <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 8px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
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
                    <div class="confirmation-envelope-card">
                        <div style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%);">
                            <div class="seal-initials" style="width: 45px; height: 45px; font-size: 13px;">✉️</div>
                        </div>
                        <h3 style="font-family: 'Great Vibes', cursive !important; font-size: 2.3rem; margin-top: 15px; color: #F3E5AB !important;">
                            ¡Gracias por confirmar! 💖
                        </h3>
                        <p style="font-size: 1.1rem; line-height: 1.6; font-weight: 500; margin: 15px 0; color: #FFFFFF !important;">
                            Te esperamos con ansias para celebrar este hermoso día con nosotros ✨🥂🎉💒
                        </p>
                        <hr style="border: 0; border-top: 1px dashed rgba(255,255,255,0.4); margin: 20px 0;">
                        <p style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: #F3E5AB !important;">
                            🎁 Sugerencia de Regalo Asignada:
                        </p>
                        <h2 style="font-size: 1.8rem; margin: 8px 0; font-family: 'Cinzel', serif !important; color: #FFFFFF !important;">
                            {regalo}
                        </h2>
                        <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 12px; color: #FFFFFF !important;">
                            Código de Confirmación: <strong>{codigo}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Lamentamos que no puedas acompañarnos, ¡agradecemos mucho tu respuesta!")

    # ADMIN PANEL
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Ver invitados)"):
        df_ver = cargar_respuestas()
        if not df_ver.empty:
            st.dataframe(df_ver, use_container_width=True)
        else:
            st.caption("Aún no hay respuestas.")
