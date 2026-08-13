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
# RUTAS DE ARCHIVOS
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

/* TARJETA PRINCIPAL Y BORDES CON FLORES */
.invitation-card, .dress-card {{
    background-color: #FFFFFF !important;
    border-radius: 20px;
    padding: 80px 25px 80px 25px;
    margin: 20px auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    border: 1px solid #E8E2D9;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.invitation-card::before, .dress-card::before {{
    content: "";
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 290px;
    height: 75px;
    background-image: url("{flores_b64}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card::after, .dress-card::after {{
    content: "";
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
    width: 290px;
    height: 75px;
    background-image: url("{flores_b64}");
    background-size: contain;
    background-position: center top;
    background-repeat: no-repeat;
    pointer-events: none;
    z-index: 1;
}}

.invitation-card *, .dress-card * {{
    position: relative;
    z-index: 2;
}}

.title-names {{
    font-family: 'Great Vibes', cursive !important;
    font-size: 3.8rem !important;
    color: #4A5A48 !important;
    margin-bottom: 5px;
}}

.welcome-envelope {{
    background-color: #FAF6F0;
    width: 220px;
    height: 140px;
    margin: 20px auto;
    border-radius: 12px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
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
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}}

/* BOTÓN ELEGANTE */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #6B7A68 0%, #4A5A48 100%) !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 12px 30px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    letter-spacing: 1px;
    width: 100%;
    box-shadow: 0 4px 12px rgba(74, 90, 72, 0.2);
    margin-top: 10px;
}}
div.stButton > button:first-child:hover {{
    background: linear-gradient(135deg, #586655 0%, #394637 100%) !important;
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

def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Invitados')
    return output.getvalue()

def obtener_apellido(nombre_completo):
    partes = nombre_completo.strip().split()
    return partes[-1] if len(partes) > 1 else partes[0]

def reorganizar_mesas_alfabetico(df):
    """Ordena los asistentes por apellido y asigna mesas del 1 al 6 dinámicamente."""
    if df.empty:
        return df
    
    asistentes = df[df["Asiste"] == "Sí"].copy()
    if asistentes.empty:
        return df

    # Ordenar A-Z por apellido
    asistentes["Apellido_Tmp"] = asistentes["Nombre"].apply(obtener_apellido)
    asistentes = asistentes.sort_values(by="Apellido_Tmp", key=lambda col: col.str.lower()).reset_index(drop=True)
    
    mesas_disponibles = ["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5", "Mesa 6"]
    
    for i, idx in enumerate(asistentes.index):
        mesa_num = mesas_disponibles[i % len(mesas_disponibles)]
        df.loc[df["Nombre"] == asistentes.loc[idx, "Nombre"], "Mesa"] = mesa_num

    return df

# ──────────────────────────────────────────────
# PANTALLA INICIAL (PORTADA)
# ──────────────────────────────────────────────
if not st.session_state["invitacion_abierta"]:
    st.markdown("""
    <div class="invitation-card" style="margin-top: 20px;">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 3px; font-size: 0.9rem; text-transform: uppercase; color: #6B7A68 !important;">
            Nuestra Boda
        </div>
        <div class="title-names">Carlos & Eunice</div>
        <div class="welcome-envelope">
            <div class="seal-initials">C & E</div>
        </div>
        <p style="font-size: 0.95rem; color: #6B7A68 !important; margin-top: 15px; font-weight: 500;">
            Has recibido una invitación especial
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✉️ Abrir Invitación"):
        st.session_state["invitacion_abierta"] = True
        st.rerun()

# ──────────────────────────────────────────────
# CONTENIDO INTERNO DE LA INVITACIÓN
# ──────────────────────────────────────────────
else:
    # 1. NOMBRES Y FECHA
    st.markdown("""
    <div class="invitation-card">
        <div class="title-names">Carlos & Eunice</div>
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; color: #6B7A68 !important; font-weight: 600; font-size: 1.1rem; margin-top: 10px;">
            18 DE JUNIO DE 2027
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. FOTO DE LOS NOVIOS
    if IMAGEN_HEADER.exists():
        st.markdown(f"""
        <div class="invitation-card">
            <img src="{img_b64}" style="width: 100%; max-width: 500px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        </div>
        """, unsafe_allow_html=True)

    # 3. MÚSICA
    st.markdown("""
    <div class="invitation-card" style="padding-bottom: 25px;">
        <p style="font-size: 0.95rem; font-weight: 600; margin-bottom: 5px;">🎵 Escucha nuestra canción</p>
    </div>
    """, unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=js2MkCAmTJY")

    # 4. PADRES DE LOS NOVIOS
    st.markdown("""
    <div class="invitation-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 1rem; font-weight: 600; text-transform: uppercase;">
            Con la bendición de Dios y nuestros padres
        </div>
        <div style="display: flex; justify-content: space-around; font-size: 0.9rem; margin-top: 20px;">
            <div><strong>Padres del Novio</strong><br>Carlos M & Diana ❤️</div>
            <div><strong>Padres de la Novia</strong><br>Emilio M & Pricila C ❤️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. DRESS CODE
    st.markdown("""
    <div class="dress-card">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 1rem; font-weight: 600; text-transform: uppercase;">
            👗 Código de Vestimenta
        </div>
        <p style="font-size: 1.1rem; font-weight: 600; margin-top: 10px;">FORMAL / ELEGANTE</p>
        <p style="font-size: 0.85rem;">Reservamos el color blanco para la novia y el verde oliva para el cortejo.</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #E8E2D9;">
        <p style="font-size: 0.9rem; font-weight: 600;">🔞 Evento de Adultos (Sin Niños)</p>
    </div>
    """, unsafe_allow_html=True)

    # 6. FORMULARIO DE CONFIRMACIÓN
    st.markdown("""
    <div class="invitation-card" id="confirmacion">
        <div style="font-family: 'Cinzel', serif; letter-spacing: 2px; font-size: 1rem; font-weight: 600; text-transform: uppercase;">
            Confirmar Asistencia
        </div>
        <p style="font-size: 0.88rem; margin-top: 10px;">Por favor confirma tu presencia e ingresa para recibir la sugerencia de regalo asignada.</p>
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
                
                # Reorganizar automáticamente por apellido A-Z
                df_actualizado = reorganizar_mesas_alfabetico(df_actualizado)
                guardar_respuestas(df_actualizado)

                st.success("¡Respuesta guardada con éxito!")
                st.balloons()

    # 7. PANEL ADMIN INTERACTIVO (DISTRIBUCIÓN REAL A-Z)
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📊 Panel Admin (Gestor de Mesas e Invitados)"):
        df_ver = cargar_respuestas()
        
        st.write("### 🗺️ Distribución Interactiva del Salón (A-Z por Apellido)")
        
        # Agrupar nombres por mesa
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
                padding: 15px; border: 2px dashed #D4AF37; border-radius: 15px; background: rgba(255, 255, 255, 0.8);
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
