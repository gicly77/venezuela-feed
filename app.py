import streamlit as st
import streamlit.components.v1 as components
import requests
import feedparser
from datetime import datetime
import pytz

# 1. CONFIGURACIÓN TÁCTICA
st.set_page_config(page_title="VENEZUELA INTELLIGENCE", layout="wide")

# Estilo para que el radar se vea profesional
st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #e1e1e1; }
    .news-card { 
        background: #10141b; border: 1px solid #1f2937; padding: 15px; 
        margin-bottom: 10px; border-left: 5px solid #ffcc00; border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 2. FUNCIÓN DE INSERCIÓN OFICIAL (oEmbed)
def get_x_embed(url):
    try:
        # Solicitamos el HTML oficial a X
        api_url = f"https://publish.twitter.com/oembed?url={url}&theme=dark&omit_script=false"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()["html"]
        return "Error: No se pudo obtener el feed."
    except:
        return "Error de conexión con X."

# 3. INTERFAZ DE COLUMNAS
col_radar, col_x = st.columns([2, 1])

with col_radar:
    st.header("🛡️ RADAR CRÍTICO VENEZUELA")
    # Simulación de carga de noticias (puedes mantener tu código RSS aquí)
    st.markdown('<div class="news-card"><b>TELEMUNDO:</b> Trump dice que EE.UU. dirigirá Venezuela...</div>', unsafe_allow_html=True)

with col_x:
    st.subheader("🐦 INTELIGENCIA X")
    
    # URL de un post reciente de una cuenta de inteligencia (ej. AlertaNews24)
    # Es vital usar una URL de un POST específico para que el widget se active
    target_url = "https://twitter.com/AlertaNews24/status/1875323267591602521" 
    
    html_content = get_x_embed(target_url)
    
    # Renderizado forzado
    components.html(
        f"""
        <div style="display: flex; justify-content: center;">
            {html_content}
        </div>
        """,
        height=800,
        scrolling=True
    )
