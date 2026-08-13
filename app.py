import streamlit as st
import pandas as pd
import random
from pathlib import Path
import base64
import uuid
import streamlit.components.v1 as components
import io

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
# RUTAS DE ARCHIVOS LOCALES
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")
IMAGEN_HEADER = Path("WhatsApp Image 2026-07-27 at 15.26.46.jpeg")
IMAGEN_FLORES = Path("Este artículo no está disponible - Etsy.jpg")

def get_image_base64(path_local):
    if path_local.exists():
        with open(path_local, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = path_local.suffix.replace('.', '').lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
            return f"data:{mime};base64,{encoded}"
    return ""

img_b64 = get_image_base64(IMAGEN_HEADER)
flores_b64 = get_image_base64(IMAGEN_FLORES)

# ──────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500;600&display=swap');

.stApp {{
    background-color: #FAF6F0 !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

p, span, div, h1, h2, h3, h4, h5, h6 {{
    color: #4A5A48 !important;
}}

input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{
    color: #4A5A48 !important;
    font-weight: 600 !important;
}}

html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif !important;
}}

/* TARJETA PRINCIPAL CON FLORES Y DISEÑO ELEGANTE */
.invitation-card, .dress-card {{
    background-color: #FFFFFF !important;
    border-radius: 25px;
    padding: 70px 25px 50px 25px;
    margin: 10px auto;
    box-shadow: 0 15px 35px rgba(107, 122, 104, 0.12);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.invitation-card::before, .dress-card::before {{
    content: "";
    position: absolute;
    top: 0px;
    left: 50%;
    transform: translateX(-50%);
    width: 320px;
    height: 80px;
    background-image: url('{flores_b64}');
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card::after, .dress-card::after {{
    content: "";
    position: absolute;
    bottom: 0px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 320px;
    height: 80px;
    background-image: url('{flores_b64}');
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.card-content {{
    position: relative;
    z-index: 2;
}}

.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #4A5A48 !important;
    margin-bottom: 0px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
}}

.welcome-envelope {{
    background: linear-gradient(145deg, #FAF6F0 0%, #F5EFE6 100%);
    width: 200px;
    height: 125px;
    margin: 15px auto;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border: 1px solid #E8E2D9;
}}

.seal-initials {{
    width: 60px;
    height: 60px;
    background: radial-gradient(circle, #D4AF37 0%, #AA7C11 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-family: 'Cinzel', serif !important;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(170, 124, 17, 0.3);
}}

/* BOTÓN DORADO/VERDE ELEGANTE */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
    color: #FFFFFF !important;
    border-radius: 30px !important;
    border: none !important;
    padding: 12px 30px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    width: 100%;
    max-width: 280px;
    margin: 10px auto 0 auto;
    display: block;
    box-shadow: 0 6px 18px rgba(170, 124, 17, 0.25);
    transition: all 0.3s ease;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(170, 124, 17, 0.35);
}}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FUNCIONES DE DATOS
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

def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Invitados')
    return output.getvalue()

def obtener_apellido(nombre_completo):
    partes = nombre_completo.strip().split()
    return partes[-1] if len(partes) > 1 else partes[0]

def reorganizar_mesas_alfabetico(df):
    if df.empty:
        return df
    
    asistentes = df[df["Asiste"] == "Sí"].copy()
    if asistentes.empty:
        return df

    asistentes["Apellido_Tmp"] = asistentes["Nombre"].apply(obtener_apellido)
    asistentes = asistentes.sort_values(by="Apellido_Tmp", key=lambda col: col.str.lower()).reset_index(drop=True)
    
    mesas_disponibles = ["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5", "Mesa 6"]
    
    for i, idx in enumerate(asistentes.index):
        mesa_num = mesas_disponibles[i % len(mesas_disponibles)]
        df.loc[df["Nombre"] == asistentes.loc[idx, "Nombre"], "Mesa"] = mesa_num

    return df

# ──────────────────────────────────────────────
# PANTALLA INICIAL (PORTADA CORREGIDA)
# ──────────────────────────────────────────────
if not st.session_state["invitacion_abierta"]:
    portada_html = """
    <div class="invitation-card">
        <div class="card-content">
            <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 0.9rem; text-transform: uppercase; color: #6B7A68; font-weight: 600;">
                ✨ ¡Nuestra Boda! ✨
            </div>
            <div class="title-names">Carlos & Eunice</div>
            <p style="font-size: 1.1rem; margin: 2px 0 10px 0;">💖 🕊️ 💖</p>
            <div class="welcome-envelope">
                <div class="seal-initials">C & E</div>
            </div>
            <p style="font-size: 0.95rem; color: #6B7A68; margin-top: 10px; font-weight: 600;">
                Has recibido una invitación muy especial
            </p>
            <p style="font-size: 0.85rem; color: #8A9A88; font-style: italic;">
                Haz clic en el botón para abrir tu sobre
            </p>
        </div>
    </div>
    """
    st.markdown(portada_html, unsafe_allow_html=True)
    
    if st.button("✉️ Abrir Invitación ✨"):
        st.session_state["invitacion_abierta"] = True
        st.rerun()

# ──────────────────────────────────────────────
# CONTENIDO INTERNO DE LA INVITACIÓN
# ──────────────────────────────────────────────
else:
    # 1. NOMBRES Y FECHA
    st.markdown("""
    <div class="invitation-card">
        <div class="card-content">
            <div style="font-size: 1.2rem;">🌸 💖 🌸</div>
            <div class="title-names">Carlos & Eunice</div>
            <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; color: #6B7A68; font-weight: 600; font-size: 1rem; margin-top: 10px;">
                18 DE JUNIO DE 2027
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. FOTO DE LOS NOVIOS
    if IMAGEN_HEADER.exists():
        st.markdown(f"""
        <div class="invitation-card">
            <div class="card-content">
                <img src="{img_b64}" style="width: 100%; max-width: 480px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. MÚSICA
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 20px;">
        <div class="card-content">
            <p style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0px;">🎵 Escucha nuestra canción de amor 💕</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=js2MkCAmTJY")

    # 4. PADRES DE LOS NOVIOS
    st.markdown("""
    <div class="invitation-card">
        <div class="card-content">
            <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">
                Con la bendición de Dios y nuestros padres
            </div>
            <div style="display: flex; justify-content: space-around; font-size: 0.88rem; margin-top: 18px;">
                <div><strong>Padres del Novio</strong><br>Carlos M & Diana ❤️</div>
                <div><strong>Padres de la Novia</strong><br>Emilio M & Pricila C ❤️</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. DRESS CODE
    st.markdown("""
    <div class="dress-card">
        <div class="card-content">
            <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">
                👗 Código de Vestimenta
            </div>
            <p style="font-size: 1rem; font-weight: 600; margin-top: 8px;">FORMAL / ELEGANTE</p>
            <p style="font-size: 0.82rem;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
            <hr style="margin: 12px 0; border: none; border-top: 1px solid #E8E2D9;">
            <p style="font-size: 0.88rem; font-weight: 600;">🔞 Evento de Adultos (Sin Niños)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. FORMULARIO DE CONFIRMACIÓN
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div class="card-content">
            <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 0.95rem; font-weight: 600; text-transform: uppercase;">
                💌 Confirmar Asistencia
            </div>
            <p style="font-size: 0.85rem; margin-top: 8px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
        </div>
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
                    mesa_asistente = "Mesa 1"
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
                df_actualizado = reorganizar_mesas_alfabetico(df_actualizado)
                guardar_respuestas(df_actualizado)

                st.success("¡Respuesta guardada con éxito!")
                st.balloons()

    # 7. PANEL ADMIN INTERACTIVO
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Gestor de Mesas e Invitados)"):
        df_ver = cargar_respuestas()
        
        st.write("### 🗺️ Distribución Interactiva del Salón (A-Z por Apellido)")
        
        mesas_dict = {f"Mesa {i}": [] for i in range(1, 7)}
        if not df_ver.empty:
            for _, row in df_ver[df_ver["Asiste"] == "Sí"].iterrows():
                m_nombre = str(row["Mesa"]).split(" ")[0] + " " + str(row["Mesa"]).split(" ")[1] if "Mesa" in str(row["Mesa"]) else "Mesa 1"
                if m_nombre in mesas_dict:
                    mesas_dict[m_nombre].append(row["Nombre"])

        def generar_html_m(m_key):
            lista = mesas_dict.get(m_key, [])
            if not lista:
                return "<em style='color:#A0AEC0; font-size:10px;'>Vacía</em>"
            items = "".join([f"<li style='font-size:10px; line-height:1.2; text-align:left;'>{n}</li>" for n in lista])
            return f"<ul style='margin:2px 0 0 0; padding-left:14px;'>{items}</ul>"

        salon_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&family=Cinzel:wght@600&display=swap');
            body {{ font-family: 'Montserrat', sans-serif; background: transparent; margin:0; padding:10px; }}
            .salon-container {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
            .separated-section {{
                width: 100%; display: flex; justify-content: space-around;
                padding: 15px; border: 2px dashed #D4AF37; border-radius: 15px; background: rgba(255, 255, 255, 0.85);
            }}
            .square-table {{
                width: 130px; min-height: 110px; background: #FFFFFF;
                border: 2px solid #D4AF37; border-radius: 8px;
                display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
                box-shadow: 0 4px 10px rgba(0,0,0,0.06); padding: 8px; overflow-y: auto;
            }}
            .round-section {{
                display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 10px;
            }}
            .round-table {{
                width: 130px; height: 130px; border-radius: 50%; background: #FFFFFF;
                border: 2px solid #A3B18A; display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.06); padding: 10px; overflow: hidden;
            }}
            .table-title {{ font-family: 'Cinzel', serif; font-size: 11px; font-weight: bold; color: #4A5A48; border-bottom: 1px solid #E2E8F0; width: 100%; text-align: center; padding-bottom: 2px; }}
            .badge {{ font-size: 9px; color: #6B7A68; font-weight: 600; }}
            .guest-list {{ max-height: 70px; overflow-y: auto; width: 100%; color: #4A5A48; }}
        </style>
        </head>
        <body>
            <div class="salon-container">
                <div class="separated-section">
                    <div class="square-table">
                        <div class="table-title">Mesa 1</div>
                        <div class="badge">🔲 Cuadrada</div>
                        <div class="guest-list">{generar_html_m('Mesa 1')}</div>
                    </div>
                    <div class="square-table">
                        <div class="table-title">Mesa 2</div>
                        <div class="badge">🔲 Cuadrada</div>
                        <div class="guest-list">{generar_html_m('Mesa 2')}</div>
                    </div>
                </div>

                <div class="round-section">
                    <div class="round-table">
                        <div class="table-title">Mesa 3</div>
                        <div class="badge">⚪ Redonda</div>
                        <div class="guest-list">{generar_html_m('Mesa 3')}</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 4</div>
                        <div class="badge">⚪ Redonda</div>
                        <div class="guest-list">{generar_html_m('Mesa 4')}</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 5</div>
                        <div class="badge">⚪ Redonda</div>
                        <div class="guest-list">{generar_html_m('Mesa 5')}</div>
                    </div>
                    <div class="round-table">
                        <div class="table-title">Mesa 6</div>
                        <div class="badge">⚪ Redonda</div>
                        <div class="guest-list">{generar_html_m('Mesa 6')}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        components.html(salon_html, height=480)

        if not df_ver.empty:
            st.write("### Reorganizar Manualmente o Reordenar")
            if st.button("🔄 Reordenar Lista Completa por Apellidos (A-Z)"):
                df_ver = reorganizar_mesas_alfabetico(df_ver)
                guardar_respuestas(df_ver)
                st.success("¡Lista y mesas reorganizadas de la A a la Z!")
                st.rerun()

            st.write("### Lista General de Confirmados")
            st.dataframe(df_ver, use_container_width=True)
            
            excel_data = convertir_excel(df_ver)
            st.download_button(
                label="📥 Descargar Lista Completa (Excel)",
                data=excel_data,
                file_name="lista_invitados_boda.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.caption("Aún no hay respuestas registradas.")
