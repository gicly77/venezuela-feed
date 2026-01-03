import streamlit as st
import feedparser
from datetime import datetime
import time
import pytz 
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. HORA MADRID ---
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# --- 3. ESTILO VISUAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    
    .main-news-container { max-width: 900px; margin: 0 auto; padding-top: 20px; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; border-radius:8px; 
        padding:20px; margin-bottom:15px; border-left: 6px solid #ffcc00; 
        position: relative; 
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:700; font-size:1.3rem; display: block; margin-top: 5px;}
    .time-badge { 
        position: absolute; top: 20px; right: 20px; 
        font-size:0.8rem; background:#dc2626; color:white; 
        padding:3px 8px; border-radius:4px; font-weight:bold; 
    }
    
    /* MONITOR X MEJORADO */
    .x-monitor-fixed {
        position: fixed; top: 10px; right: 10px;
        width: 350px; height: 500px; z-index: 9999;
        background: #000; border: 2px solid #1d9bf0;
        border-radius: 12px; overflow: hidden;
        box-shadow: 0 0 20px rgba(29, 155, 240, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. MONITOR X (INYECCIÓN DIRECTA SIN ROTACIÓN INTERNA) ---
# He quitado la rotación de 10 segundos del script de Python porque eso mataba a X.
# Ahora X se mantiene estable y cargará los tweets de AlertaNews24 y Venezuela en Vivo.
with st.container():
    st.markdown("""
        <div class="x-monitor-fixed">
            <div style="background:#1d9bf0; color:white; padding:5px; text-align:center; font-weight:bold; font-size:0.8rem;">
                🐦 INTELIGENCIA X EN VIVO
            </div>
            <div style="height:465px; overflow-y:auto;">
                <a class="twitter-timeline" data-theme="dark" data-chrome="noheader nofooter" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw"></a>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. CUERPO PRINCIPAL ---
# Refrescamos las noticias cada 60 segundos (no 10, para dejar que X respire)
st_autorefresh(interval=60 * 1000, key="news_update")

st.markdown('<div class="main-news-container">', unsafe_allow_html=True)
st.markdown(f'<h2 style="text-align:center; color:#f0f6fc;">🛡️ RADAR MADRID: {hora_madrid}</h2>', unsafe_allow_html=True)

st.link_button("🔴 ABRIR MONITOR YOUTUBE (DIRECTOS)", "https://www.youtube.com/results?search_query=venezuela+en+vivo&sp=EgJAAQ%253D%253D", use_container_width=True)

def get_news():
    url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            # Ajuste de hora Madrid
            pub_utc = datetime(*e.published_parsed[:6], tzinfo=pytz.utc)
            pub_mad = pub_utc.astimezone(madrid_tz)
            st.markdown(f"""
            <div class="news-card">
                <span class="time-badge">{pub_mad.strftime('%H:%M')}</span>
                <div style="font-size:0.8rem; color:#9ca3af;">{e.source.get('title')}</div>
                <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    except: pass

get_news()
st.markdown('</div>', unsafe_allow_html=True)
            
