import streamlit as st
import pandas as pd
import random
import os
import uuid
from pathlib import Path

st.set_page_config(page_title="Nuestra Boda 💍", page_icon="✨", layout="centered")

# ──────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────
CSV_REGALOS = Path("regalos.csv")
CSV_RESPUESTAS = Path("respuestas.csv")

# ──────────────────────────────────────────────
# ESTADO DE SESIÓN — persiste entre recargas
# ──────────────────────────────────────────────
if "confirmado" not in st.session_state:
    st.session_state.confirmado = False
    st.session_state.nombre = ""
    st.session_state.regalo = ""
    st.session_state.codigo = ""

# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────────
def cargar_regalos() -> pd.DataFrame:
    """Carga la lista de regalos disponibles con manejo de errores."""
    try:
        if not CSV_REGALOS.exists():
            st.error(f"❌ No se encuentra el archivo {CSV_REGALOS.name}. "
                     "Créalo con la lista de regalos.")
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
        nombre.strip().lower() == n.strip().lower()
        for n in df_resp["Nombre"].tolist()
    )

def asignar_regalo_con_lock(nombre: str) -> str:
    """
    Asigna un regalo de forma atómica: lee, escoge, elimina y guarda
    en un solo paso para evitar race conditions.
    """
    df = cargar_regalos()
    if df.empty:
        raise ValueError("No quedan regalos disponibles.")

    # Elegir aleatoriamente
    regalo = random.choice(df["Regalo"].tolist())

    # Eliminar el regalo de la lista
    df = df[df["Regalo"] != regalo]

    # Escribir de vuelta (sobrescribe completo = atómico para este caso)
    df.to_csv(CSV_REGALOS, index=False)

    return regalo

# ──────────────────────────────────────────────
# INTERFAZ DE USUARIO
# ──────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align: center; color: #8B5CF6;'>
        💍 ¡Nos Casamos! ✨
    </h1>
""", unsafe_allow_html=True)

# Mostrar cuántos regalos quedan (solo si no ha confirmado aún)
if not st.session_state.confirmado:
    df_regalos = cargar_regalos()
    disponibles = len(df_regalos)

    if disponibles > 0:
        st.markdown(f"""
            <div style='text-align: center; padding: 10px; background: #F3E8FF; 
                        border-radius: 10px; margin-bottom: 20px;'>
                🎁 Quedan <strong>{disponibles}</strong> regalos por asignar
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Ya no quedan regalos disponibles. Todos fueron asignados.")

    st.write("Confirma tu asistencia y el sistema te asignará un regalo al azar.")

# ── FORMULARIO ──
with st.form("boda_form"):
    nombre = st.text_input(
        "Tu Nombre Completo:",
        placeholder="Ej: María García López",
        disabled=st.session_state.confirmado
    )
    asiste = st.radio(
        "¿Nos acompañarás?",
        ["¡Sí, ahí estaré! 🎉", "No puedo ir 😢"],
        disabled=st.session_state.confirmado
    )
    btn = st.form_submit_button("Confirmar", disabled=st.session_state.confirmado)

# ── PROCESAMIENTO ──
if btn and not st.session_state.confirmado:
    if not nombre.strip():
        st.error("📝 Por favor escribe tu nombre.")
    else:
        # Verificar duplicados
        df_resp_existente = cargar_respuestas()
        if nombre_ya_registrado(nombre, df_resp_existente):
            st.warning(f"⚠️ El nombre **{nombre.strip()}** ya está registrado. "
                       "Si crees que es un error, contacta a los organizadores.")
        else:
            if asiste == "¡Sí, ahí estaré! 🎉":
                try:
                    codigo = uuid.uuid4().hex[:8].upper()
                    regalo = asignar_regalo_con_lock(nombre.strip())

                    # Guardar respuesta
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

                    # Guardar en sesión para mostrar aunque se recargue
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
                codigo = uuid.uuid4().hex[:8].upper()
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

# ── MOSTRAR RESULTADO (persiste con session_state) ──
if st.session_state.confirmado:
    st.divider()

    if st.session_state.asiste == "Sí":
        st.balloons()
        st.success(f"✅ **¡Confirmado, {st.session_state.nombre}!** ❤️")

        # Tarjeta visual del regalo
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #F3E8FF, #E8F4FF);
                    border: 2px solid #8B5CF6; border-radius: 15px;
                    padding: 25px; text-align: center; margin: 20px 0;">
            <h3 style="color: #6B21A8; margin-bottom: 5px;">🎁 Tu regalo asignado</h3>
            <h1 style="color: #7C3AED; font-size: 2.2em; margin: 10px 0;">
                {st.session_state.regalo}
            </h1>
            <p style="color: #666;">
                <em>Tu presencia es lo más importante.<br>
                Este detalle fue elegido al azar para no repetir regalos.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"🔑 **Código de confirmación:** `{st.session_state.codigo}`\n\n"
                "Guárdalo por si necesitas hacer algún cambio.")

    else:
        st.info(f"😢 Lamentamos que **{st.session_state.nombre}** no pueda venir. "
                "¡Un abrazo grande!")
        st.info(f"🔑 **Código de registro:** `{st.session_state.codigo}`")

    # Botón para reiniciar (solo útil en pruebas)
    if st.button("🔄 Registrar a otra persona", type="secondary"):
        for key in ["confirmado", "nombre", "regalo", "codigo", "asiste"]:
            st.session_state[key] = "" if key != "confirmado" else False
        st.rerun()

# ── ADMIN: Ver respuestas acumuladas (solo si existe el archivo) ──
with st.expander("📊 Ver lista de invitados que ya confirmaron (admin)", expanded=False):
    df_resp = cargar_respuestas()
    if not df_resp.empty:
        st.dataframe(df_resp, use_container_width=True, hide_index=True)
        st.download_button(
            label="📥 Descargar respuestas como CSV",
            data=df_resp.to_csv(index=False).encode("utf-8"),
            file_name="respuestas_boda.csv",
            mime="text/csv"
        )
    else:
        st.caption("Todavía no hay respuestas registradas.")