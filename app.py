import streamlit as st
import feedparser
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL: COLUMNA ÚNICA + X FLOTANTE ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    
    /* NOTICIAS EN COLUMNA ÚNICA */
    .main-news-container { max-width: 900px; margin: 0 auto; padding-top: 20px; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; border-radius:8px; 
        padding:20px; margin-bottom:15px; border-left: 6px solid #ffcc00; 
        position: relative; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:700; font-size:1.3rem; display: block; margin-top: 5px;}
    .time-badge { 
        position: absolute; top: 20px; right: 20px; 
        font-size:0.8rem; background:#dc2626; color:white; 
        padding:3px 8px; border-radius:4px; font-weight:bold; 
    }
    .source-tag { font-size:0.8rem; color:#9ca3af; font-weight:900; text-transform: uppercase; }

    /* VENTANA DE X EN LA ESQUINA SUPERIOR DERECHA */
    .x-monitor {
        position: fixed; top: 20px; right: 20px;
        width: 320px; z-index: 999;
        background: #1d9bf0; color: white;
        padding: 15px; border-radius: 12px;
        box-shadow: 0 10px 30px rgba(29, 155, 240, 0.4);
        border: 2px solid #ffffff33;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DEL ROTADOR DE X (CAMBIA CADA 10 SEGUNDOS) ---
# Definimos las búsquedas tácticas
fuentes_x = [
    {"label": "🔍 VENEZUELA: EN VIVO", "url": "https://x.com/search?q=venezuela&f=live"},
    {"label": "🚨 ALERTA NEWS 24", "url": "https://x.com/AlertaNews24"},
    {"label": "📍 CARACAS: REPORTES", "url": "https://x.com/search?q=caracas&f=live"},
    {"label": "🎥 VIDEOS RECIENTES", "url": "https://x.com/search?q=venezuela%20filter%3Avideos&f=live"}
]

# Inicializar el índice en la sesión
if 'x_index' not in st.session_state:
    st.session_state.x_index = 0

# Forzar refresco cada 10 segundos
st_autorefresh(interval=10 * 1000, key="x_rotator")

# Cambiar al siguiente link
st.session_state.x_index = (st.session_state.x_index + 1) % len(fuentes_x)
current_x = fuentes_x[st.session_state.x_index]

# --- 4. RENDERIZADO DE LA VENTANA DE X (FLOTANTE) ---
st.markdown(f"""
    <div class="x-monitor">
        <div style="font-size:0.7rem; font-weight:bold; opacity:0.8; margin-bottom:5px;">ACTUALIZANDO MONITOR...</div>
        <div style="font-size:1.1rem; font-weight:900; margin-bottom:10px;">🐦 INTELIGENCIA X</div>
        <a href="{current_x['url']}" target="_blank" style="
            display: block; background: white; color: #1d9bf0; 
            padding: 10px; border-radius: 6px; text-decoration: none; 
            font-weight: 800; font-size: 0.9rem;">
            {current_x['label']}
        </a>
        <div style="font-size:0.6rem; margin-top:8px;">Haga clic para abrir señal actual</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. NOTICIAS EN COLUMNA CENTRAL ÚNICA ---
st.markdown('<div class="main-news-container">', unsafe_allow_html=True)
st.markdown(f'<h2 style="text-align:center; color:#f0f6fc; margin-bottom:30px;">🛡️ RADAR VENEZUELA | {datetime.now().strftime("%H:%M:%S")}</h2>', unsafe_allow_html=True)

# Botón de YouTube fuera de la columna para que no estorbe
st.link_button("🔴 ABRIR MONITOR YOUTUBE (VIVO)", "https://www.youtube.com/results?search_query=venezuela+en+vivo&sp=EgJAAQ%253D%253D", use_container_width=True)

def get_news():
    url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            publicado = e.published_parsed
            hora = time.strftime('%H:%M', publicado) if publicado else "AHORA"
            st.markdown(f"""
            <div class="news-card">
                <span class="time-badge">{hora}</span>
                <div class="source-tag">{e.source.get('title', 'NOTICIA')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("Error conectando con el radar de noticias.")

get_news()
st.markdown('</div>', unsafe_allow_html=True)
