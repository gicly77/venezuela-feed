import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. Configuración de página limpia
st.set_page_config(page_title="WAR ROOM", layout="wide")

# 2. Hora Madrid (Sin errores)
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 3. Estilo Visual (Noticias en columna única)
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; padding:15px; 
        margin-bottom:10px; border-left: 4px solid #ffcc00; 
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:bold; font-size:1.1rem; }
</style>
""", unsafe_allow_html=True)

# Refresco de 60 segundos
st_autorefresh(interval=60 * 1000, key="warroom_refresh")

# 4. Estructura de Pantalla: Noticias Izquierda | Intelligence X Derecha
col_news, col_x = st.columns([1.5, 1])

with col_news:
    st.markdown(f"## 🛡️ RADAR MADRID: {hora_madrid}")
    
    # Carga de noticias RSS
    try:
        url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
        feed = feedparser.parse(url_rss)
        for e in feed.entries[:15]:
            st.markdown(f"""
            <div class="news-card">
                <div style="font-size:0.7rem; color:#888;">{e.source.get('title')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("Reconectando radar...")

with col_x:
    st.markdown("### 🐦 INTELLIGENCE X")
    # Widget de X con Script de carga forzada
    st.components.v1.html(
        """
        <div id="container" style="background-color:black; height:800px; overflow-y:auto; border: 1px solid #1d9bf0; border-radius:10px;">
            <a class="twitter-timeline" 
               data-theme="dark" 
               data-chrome="noheader nofooter transparent"
               href="https://twitter.com/AlertaNews24">
               Cargando inteligencia en tiempo real...
            </a>
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        <script>
            // Forzar recarga del widget si X lo bloquea inicialmente
            if (window.twttr) {
                twttr.widgets.load(document.getElementById('container'));
            }
        </script>
        """,
        height=850,
    )
