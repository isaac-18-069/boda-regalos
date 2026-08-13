import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import io
import streamlit.components.v1 as components

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Carlos & Eunice 😍💍", 
    page_icon="🌿", 
    layout="centered"
)

# Initialize Session State
if "invitacion_abierta" not in st.session_state:
    st.session_state["invitacion_abierta"] = False

# ──────────────────────────────────────────────
# ARCHIVOS Y RUTAS
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")

IMAGEN_FLORES_LOCAL = Path("Cet article n'est pas disponible - Etsy.jpg")
URL_FLORES_GITHUB = "https://raw.githubusercontent.com/isaac-18-069/boda-regalos/main/Cet%20article%20n'est%20pas%20disponible%20-%20Etsy.jpg"

def get_image_base64_or_url(path_local, url_github):
    if path_local.exists():
        with open(path_local, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return url_github

img_b64 = get_image_base64_or_url(IMAGEN_HEADER, "")
flores_src = get_image_base64_or_url(IMAGEN_FLORES_LOCAL, URL_FLORES_GITHUB)

# ──────────────────────────────────────────────
# ESTILOS CSS INCLUYENDO PLANO DE MESAS
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
    margin: 25px auto;
    box-shadow: 0 10px 30px rgba(107, 122, 104, 0.1);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.invitation-card::before {{
    content: ""; position: absolute; top: -10px; left: 50%;
    transform: translateX(-50%); width: 250px; height: 75px;
    background-image: url('{flores_src}'); background-size: 100% auto;
    background-position: top center; background-repeat: no-repeat;
    opacity: 0.95; pointer-events: none; z-index: 1;
}}

.invitation-card::after {{
    content: ""; position: absolute; bottom: -10px; left: 50%;
    transform: translateX(-50%) rotate(180deg); width: 250px; height: 75px;
    background-image: url('{flores_src}'); background-size: 100% auto;
    background-position: top center; background-repeat: no-repeat;
    opacity: 0.95; pointer-events: none; z-index: 1;
}}

.invitation-card * {{ position: relative; z-index: 2; }}

.green-card {{
    background-color: #6B7A68 !important; border-radius: 20px;
    padding: 35px 25px; margin: 25px auto; text-align: center;
    box-shadow: 0 10px 25px rgba(107, 122, 104, 0.2);
}}
.green-card * {{ color: #FFFFFF !important; }}

.confirmation-envelope-card {{
    background: linear-gradient(135deg, #5B6B58 0%, #4A5A48 100%);
    border-radius: 20px; padding: 35px 25px; margin: 25px auto;
    text-align: center; box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    border: 2px solid #D4AF37; position: relative;
}}
.confirmation-envelope-card * {{ color: #FFFFFF !important; }}

.title-names {{
    font-family: 'Great Vibes', cursive !important; font-size: 3.8rem !important;
    color: #4A5A48 !important; margin-bottom: 5px; line-height: 1.2;
}}

.subtitle-cinzel {{
    font-family: 'Cinzel', serif !important; letter-spacing: 3px;
    font-size: 1.1rem !important; color: #4A5A48 !important;
    font-weight: 600 !important; text-transform: uppercase; margin-top: 5px;
}}

/* --- PLANO DEL SALÓN Y MESAS REDONDAS --- */
.hall-layout {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 25px;
    padding: 20px 10px; background: #FAF6F0; border: 2px dashed #CBD5E0;
    border-radius: 15px; margin-top: 15px;
}}

.table-container {{
    position: relative; width: 130px; height: 130px;
    display: flex; align-items: center; justify-content: center;
}}

.table-circle {{
    width: 65px; height: 65px; border-radius: 50%; background: #ffffff;
    border: 2px solid #6B7A68; display: flex; flex-direction: column;
    align-items: center; justify-content: center; font-weight: bold;
    font-size: 0.75rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); z-index: 2;
}}

.seat {{
    position: absolute; width: 22px; height: 22px; border-radius: 50%;
    background: #CBD5E0; border: 2px solid #fff; display: flex;
    align-items: center; justify-content: center; font-size: 0.6rem;
    font-weight: bold; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}}
.seat.confirmed {{ background: #25D366; color: white; }}

.s1 {{ top: 0; left: 54px; }}
.s2 {{ top: 12px; right: 12px; }}
.s3 {{ top: 54px; right: 0; }}
.s4 {{ bottom: 12px; right: 12px; }}
.s5 {{ bottom: 0; left: 54px; }}
.s6 {{ bottom: 12px; left: 12px; }}
.s7 {{ top: 54px; left: 0; }}
.s8 {{ top: 12px; left: 12px; }}

.timeline-item {{ padding: 12px 0; border-bottom: 1px dashed #CBD5E0; font-size: 1rem !important; font-weight: 500 !important; }}
.timeline-item:last-child {{ border-bottom: none; }}

div.stButton > button:first-child {{
    background-color: #6B7A68 !important; color: #FFFFFF !important;
    border-radius: 25px !important; border: none !important;
    padding: 14px 35px !important; font-size: 1.1rem !important;
    font-weight: 600 !important; width: 100%; transition: all 0.3s ease;
}}
div.stButton > button:first-child * {{ color: #FFFFFF !important; }}

.welcome-envelope {{
    background-color: #5B6B58; width: 260px; height: 170px; margin: 15px auto;
    border-radius: 12px; position: relative; display: flex; align-items: center;
    justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2); z-index: 2;
}}

.seal-initials {{
    width: 65px; height: 65px; background: radial-gradient(circle, #D4AF37 0%, #AA7C11 100%);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    color: white !important; font-family: 'Cinzel', serif !important; font-size: 18px;
    font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px solid #F3E5AB;
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
    return pd.DataFrame(columns=["Nombre", "Asiste", "Mesa", "Personas", "Regalo", "Codigo"])

def asignar_regalo(nombre):
    df = cargar_regalos()
    if df.empty:
        return "Detalle de boda a elección personal"
    regalo = random.choice(df["Regalo"].tolist())
    df = df[df["Regalo"] != regalo]
    df.to_csv(CSV_REGALOS, index=False)
    return regalo

def convertir_df_a_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Invitados Confirmados')
    return output.getvalue()

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
        <div class="subtitle-cinzel">NUESTRA BODA 🥰💍</div>
        <div class="title-names">Carlos & Eunice 💏💖</div>
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

    # 3. ROMPECABEZAS FOTO
    if img_b64:
        puzzle_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background-color: transparent; font-family: 'Montserrat', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
            .card-container {{ background-color: #FFFFFF; border-radius: 20px; padding: 40px 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.04); border: 1px solid #E8E2D9; text-align: center; width: 100%; max-width: 450px; position: relative; overflow: hidden; }}
            .instructions {{ font-size: 13px; color: #6B7A68; margin-bottom: 12px; font-weight: 600; z-index: 2; }}
            #puzzle-board {{ width: 300px; height: 300px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); gap: 2px; background: #E2E8F0; border-radius: 14px; overflow: hidden; border: 2px solid #6B7A68; z-index: 2; }}
            .tile {{ width: 100%; height: 100%; background-image: url('{img_b64}'); background-size: 300px 300px; cursor: pointer; transition: transform 0.2s; border: 1px solid rgba(255,255,255,0.4); }}
            .tile.selected {{ border: 3px solid #D4AF37; transform: scale(0.95); }}
            .btn-resolve {{ margin-top: 14px; background-color: #6B7A68; color: white; border: none; padding: 8px 20px; border-radius: 20px; font-size: 12px; cursor: pointer; font-weight: 600; }}
            .success-msg {{ display: none; color: #4A5A48; font-weight: bold; margin-top: 10px; font-size: 14px; }}
        </style>
        </head>
        <body>
        <div class="card-container">
            <div class="instructions">🧩 haz clic en dos piezas para intercambiarlas y armar la foto</div>
            <div id="puzzle-board"></div>
            <button class="btn-resolve" onclick="autoSolve()">✨ Armar automáticamente</button>
            <div id="success" class="success-msg">🎉 ¡Nuestra foto está lista! ❤️</div>
        </div>
        <script>
            const board = document.getElementById('puzzle-board');
            const successMsg = document.getElementById('success');
            let selectedTile = null;
            const correctPositions = ['0px 0px', '-100px 0px', '-200px 0px', '0px -100px', '-100px -100px', '-200px -100px', '0px -200px', '-100px -200px', '-200px -200px'];
            let currentPositions = [...correctPositions];
            function shuffle(array) {{ for (let i = array.length - 1; i > 0; i--) {{ const j = Math.floor(Math.random() * (i + 1)); [array[i], array[j]] = [array[j], array[i]]; }} }}
            function initPuzzle() {{ shuffle(currentPositions); renderBoard(); }}
            function renderBoard() {{
                board.innerHTML = '';
                currentPositions.forEach((pos, index) => {{
                    const tile = document.createElement('div');
                    tile.className = 'tile';
                    tile.style.backgroundPosition = pos;
                    tile.addEventListener('click', () => onTileClick(index));
                    board.appendChild(tile);
                }});
                checkWin();
            }}
            function onTileClick(index) {{
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
            function checkWin() {{
                if (currentPositions.every((val, i) => val === correctPositions[i])) {{
                    successMsg.style.display = 'block';
                    board.style.border = '3px solid #28a745';
                }}
            }}
            function autoSolve() {{ currentPositions = [...correctPositions]; renderBoard(); }}
            initPuzzle();
        </script>
        </body>
        </html>
        """
        components.html(puzzle_html, height=480)

    # 4. MÚSICA DE FONDO
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 30px;">
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

    # 6. PLANO DEL SALÓN Y MESAS (ORGANIZACIÓN VISUAL ESTILO CROQUIS)
    st.markdown("""
    <div class="invitation-card">
        <div class="subtitle-cinzel">🪑 Organización del Salón</div>
        <p style="font-size: 0.85rem; color: #666 !important; margin-top: 5px;">Distribución circular de mesas para nuestros invitados</p>
        <div class="hall-layout">
            <div class="table-container">
                <div class="table-circle">Mesa 1</div>
                <div class="seat s1 confirmed">✓</div><div class="seat s2 confirmed">✓</div>
                <div class="seat s3">3</div><div class="seat s4">4</div>
                <div class="seat s5">5</div><div class="seat s6">6</div>
                <div class="seat s7">7</div><div class="seat s8">8</div>
            </div>
            <div class="table-container">
                <div class="table-circle">Mesa 2</div>
                <div class="seat s1 confirmed">✓</div><div class="seat s2">2</div>
                <div class="seat s3">3</div><div class="seat s4">4</div>
                <div class="seat s5">5</div><div class="seat s6">6</div>
                <div class="seat s7">7</div><div class="seat s8">8</div>
            </div>
            <div class="table-container">
                <div class="table-circle">Mesa 3</div>
                <div class="seat s1">1</div><div class="seat s2">2</div>
                <div class="seat s3">3</div><div class="seat s4">4</div>
                <div class="seat s5">5</div><div class="seat s6">6</div>
                <div class="seat s7">7</div><div class="seat s8">8</div>
            </div>
            <div class="table-container">
                <div class="table-circle">Mesa 4</div>
                <div class="seat s1">1</div><div class="seat s2">2</div>
                <div class="seat s3">3</div><div class="seat s4">4</div>
                <div class="seat s5">5</div><div class="seat s6">6</div>
                <div class="seat s7">7</div><div class="seat s8">8</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7. CONFIRMACIÓN & REGALOS
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div class="subtitle-cinzel">CONFIRMAR ASISTENCIA</div>
        <p style="font-size: 0.9rem; color: #4A5568 !important; margin-top: 8px;">Por favor confirma tu presencia y selecciona tu mesa asignada.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_invitacion"):
        nombre = st.text_input("Nombre y Apellido:", placeholder="Ej: Carlos & Eunice")
        mesa_seleccionada = st.selectbox("Selecciona tu Mesa Asignada:", ["Mesa 1 (Familia)", "Mesa 2 (Amigos)", "Mesa 3 (Cortejo)", "Mesa 4 (Especiales)"])
        personas = st.number_input("Número de Personas:", min_value=1, max_value=5, value=1)
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
                    "Mesa": mesa_seleccionada,
                    "Personas": personas,
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
                        <p style="font-size: 0.95rem; color: #F3E5AB !important;">
                            🪑 Mesa: <strong>{mesa_seleccionada}</strong> | 👥 Lugares: <strong>{personas}</strong>
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

    # 8. ADMIN PANEL & DESCARGA DE EXCEL
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Ver e Imprimir Lista en Excel)"):
        df_ver = cargar_respuestas()
        if not df_ver.empty:
            # Filtrar solo confirmados
            df_confirmados = df_ver[df_ver["Asiste"] == "Sí"]
            st.subheader("Lista de Confirmados")
            st.dataframe(df_confirmados, use_container_width=True)
            
            # Botón de Descarga directa a Excel (.xlsx)
            excel_bytes = convertir_df_a_excel(df_confirmados)
            st.download_button(
                label="📥 Descargar Lista de Confirmados en Excel (.xlsx)",
                data=excel_bytes,
                file_name="Invitados_Confirmados_Boda.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.caption("Aún no hay respuestas.")
