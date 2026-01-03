import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN E HORA MADRID
st.set_page_config(page_title="WAR ROOM: MONITOREO X", layout="wide")
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 2. ESTILO TÁCTICO (Optimizado para visibilidad)
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; padding:15px; 
        margin-bottom:10px; border-left: 5px solid #ffcc00; border-radius: 5px;
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:bold; font-size:1.1rem; }
    .x-container { border: 2px solid #1d9bf0; border-radius: 12px; background: #000; padding: 5px; }
</style>
""", unsafe_allow_html=True)

# Refresco automático cada 60 segundos para evitar bloqueos por spam de peticiones
st_autorefresh(interval=60 * 1000, key="war_room_ref")

# 3. ESTRUCTURA DE COLUMNAS
col_noticias, col_x = st.columns([2, 1])

with col_noticias:
    st.markdown(f"## 🛡️ RADAR CRÍTICO | {hora_madrid}")
    try:
        url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
        feed = feedparser.parse(url_rss)
        for e in feed.entries[:12]:
            st.markdown(f"""
            <div class="news-card">
                <div style="font-size:0.7rem; color:#888;">{e.source.get('title')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("Error en feed RSS.")

with col_x:
    st.markdown("### 🐦 INTELIGENCIA X")
    
    # METODO OFICIAL OPTIMIZADO: Evita el error "Nada que ver aquí" inyectando el widget 
    # mediante un componente HTML con el script de carga forzada.
    st.components.v1.html(
        """
        <div class="x-container" style="height: 85vh; overflow-y: auto;">
            <a class="twitter-timeline" 
               data-theme="dark" 
               data-chrome="noheader nofooter transparent noborders"
               href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw">
               Cargando flujo de datos X...
            </a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        
        <script>
            // Script de respaldo para forzar la inicialización del widget si el async falla
            window.twttr = (function(d, s, id) {
              var js, fjs = d.getElementsByTagName(s)[0], t = window.twttr || {};
              if (d.getElementById(id)) return t;
              js = d.createElement(s); js.id = id;
              js.src = "https://platform.twitter.com/widgets.js";
              fjs.parentNode.insertBefore(js, fjs);
              t._e = []; t.ready = function(f) { t._e.push(f); };
              return t;
            }(document, "script", "twitter-wjs"));
        </script>
        """,
        height=900,
    )
