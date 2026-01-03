import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide")

# 2. HORA MADRID
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 3. ESTILO CSS (Noticias en columna central, X a la derecha fija)
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    
    /* Contenedor de noticias */
    .news-card { 
        background:#10141b; border:1px solid #1f2937; padding:15px; 
        margin-bottom:12px; border-left: 5px solid #ffcc00; border-radius: 8px;
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:bold; font-size:1.2rem; display:block;}
    .source-info { color: #888; font-size: 0.8rem; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;}
</style>
""", unsafe_allow_html=True)

# Refresco automático cada 60 segundos
st_autorefresh(interval=60 * 1000, key="war_room_ref")

# 4. ESTRUCTURA DE PANTALLA (2 COLUMNAS)
col_noticias, col_intelligence = st.columns([1.8, 1])

with col_noticias:
    st.markdown(f"## 🛡️ RADAR MADRID: {hora_madrid}")
    st.markdown("---")
    
    try:
        url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
        feed = feedparser.parse(url_rss)
        if not feed.entries:
            st.info("Buscando nuevas actualizaciones en el radar...")
        for e in feed.entries[:15]:
            st.markdown(f"""
            <div class="news-card">
                <div class="source-info">{e.source.get('title')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        st.error("Error de conexión con el radar de noticias.")

with col_intelligence:
    st.markdown("### 🐦 INTELLIGENCE X")
    
    # ESTE ES EL WIDGET QUE NO PUEDE RECHAZAR LA CONEXIÓN
    # Usamos el componente HTML de Streamlit para inyectar el script de carga de Twitter
    st.components.v1.html(
        """
        <div id="x-feed" style="height: 850px; overflow-y: auto; background: #000; border-radius: 12px; border: 1px solid #1d9bf0;">
            <a class="twitter-timeline" 
               data-theme="dark" 
               data-chrome="noheader nofooter transparent"
               href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw">
            </a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        """,
        height=850,
    )
