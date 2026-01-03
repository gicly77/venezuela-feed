import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN E HORA MADRID
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide")

madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 2. ESTILO CSS SEGURO (Sin recuadros flotantes que tapen contenido)
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; padding:15px; 
        margin-bottom:10px; border-left: 4px solid #ffcc00; border-radius: 5px;
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:bold; font-size:1.1rem; }
    .time-tag { color: #ff4b4b; font-weight: bold; font-size: 0.8rem; float: right; }
</style>
""", unsafe_allow_html=True)

# Refresco automático cada 60 segundos
st_autorefresh(interval=60 * 1000, key="refresh_global")

# 3. ESTRUCTURA DE COLUMNAS (NOTICIAS IZQUIERDA | X DERECHA)
col_noticias, col_x = st.columns([1.8, 1])

with col_noticias:
    st.markdown(f"## 🛡️ RADAR VENEZUELA | MADRID: {hora_madrid}")
    
    # Botón de YouTube fuera de marcos para evitar bloqueos
    st.link_button("🔴 ABRIR MONITOR YOUTUBE (VIVO)", 
                   "https://www.youtube.com/results?search_query=venezuela+en+vivo&sp=EgJAAQ%253D%253D", 
                   use_container_width=True)
    
    st.markdown("---")
    
    # Carga de noticias
    try:
        url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
        feed = feedparser.parse(url_rss)
        if not feed.entries:
            st.warning("Buscando nuevas actualizaciones...")
        for e in feed.entries[:15]:
            st.markdown(f"""
            <div class="news-card">
                <span class="time-tag">ACTUALIZADO</span>
                <div style="font-size:0.75rem; color:#888; margin-bottom:5px;">{e.source.get('title')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except Exception as err:
        st.error("Reconectando con el servidor de noticias...")

with col_x:
    st.markdown("### 🐦 INTELIGENCIA X")
    st.info("Si el feed de abajo aparece vacío, haz clic en el botón azul de emergencia.")
    
    # Botón de respaldo por si el navegador bloquea el iframe de X
    st.link_button("📂 ABRIR X EN PESTAÑA LATERAL", "https://x.com/search?q=venezuela&f=live", use_container_width=True)
    
    # Widget de X integrado con altura fija
    st.components.v1.html(
        """
        <div style="background-color: black; height: 800px; overflow: hidden; border-radius: 10px; border: 1px solid #1d9bf0;">
            <a class="twitter-timeline" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw"></a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        """,
        height=800,
    )
