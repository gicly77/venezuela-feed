import streamlit as st
import feedparser
import time
from datetime import datetime, timezone
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PANTALLA COMPLETA
st.set_page_config(page_title="MONITOR TIEMPO REAL", layout="wide", page_icon="📡")

# 2. CSS: MODO "SALA DE GUERRA" (SIN SCROLL Y ADAPTATIVO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; overflow: hidden; }
    
    /* Barra de progreso de 20 segundos */
    .loading-bar-bg { position: fixed; top: 0; left: 0; width: 100%; height: 5px; background: #161b22; z-index: 9999; }
    .loading-bar-fill { height: 100%; background: linear-gradient(90deg, #58a6ff, #f85149); width: 0%; animation: progress 20s linear infinite; }
    @keyframes progress { from { width: 0%; } to { width: 100%; } }

    /* Tarjetas Optimizadas */
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 0.8rem; margin-bottom: 0.6rem; }
    .card-potus { border: 2px solid #58a6ff; animation: pulse 2s infinite; }
    .card-video { border-left: 5px solid #a371f7; }
    
    @keyframes pulse { 0%, 100% { border-color: #58a6ff; box-shadow: 0 0 5px #58a6ff; } 50% { border-color: #f0f6fc; box-shadow: 0 0 15px #58a6ff; } }

    .tag { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; font-weight: 700; }
    .title { font-size: 0.95rem; color: #f0f6fc; text-decoration: none; font-weight: 600; display: block; line-height: 1.2; margin: 4px 0; }
    .time-badge { font-size: 0.6rem; color: #ffffff; background: #238636; padding: 1px 6px; border-radius: 10px; }

    /* Contenedores con scroll interno oculto para estética de monitor */
    .scroll-area { height: 85vh; overflow-y: auto; scrollbar-width: none; }
    .scroll-area::-webkit-scrollbar { display: none; }

    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    <div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
    """, unsafe_allow_html=True)

# 3. FUENTES DE DATOS
SOURCES = {
    "INTEL": [
        ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("AP News", "https://apnews.com/hub/venezuela.rss")
    ],
    "LOCAL_VIDEO": [
        ("📹 YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
        ("📹 YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/")
    ]
}

def render_feed(feeds):
    vzla_keys = ['venezuela', 'maduro', 'caracas', 'miraflores', 'padrino', 'delcy', 'cabello', 'corina', 'edmundo']
    pool = []
    for name, url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                text = (e.title + e.get('summary', '')).lower()
                if any(k in text for k in vzla_keys):
                    pub_time = e.get('published_parsed', time.gmtime())
                    pool.append({
                        "source": name, "title": e.title, "link": e.link,
                        "sort_key": pub_time, "is_video": "📹" in name,
                        "is_potus": "🏛️" in name,
                        "time_str": time.strftime('%H:%M', pub_time)
                    })
        except: continue
    pool.sort(key=lambda x: x['sort_key'], reverse=True)
    
    st.markdown('<div class="scroll-area">', unsafe_allow_html=True)
    for n in pool[:20]:
        c_class = "card"
        if n['is_potus']: c_class += " card-potus"
        elif n['is_video']: c_class += " card-video"
        st.markdown(f"""<div class="{c_class}">
            <span class="tag">{n['source']}</span>
            <a class="title" href="{n['link']}" target="_blank">{n['title']}</a>
            <span class="time-badge">{n['time_str']}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. DASHBOARD DE DOS COLUMNAS (NOTICIAS VS TWITTER)
col_news, col_twitter = st.columns([1, 1])

with col_news:
    st.markdown('<p style="color:#8b949e; font-weight:bold; letter-spacing:2px;">📡 SEÑAL NOTICIAS & VIDEO</p>', unsafe_allow_html=True)
    # Combinamos todas las fuentes en una sola columna para maximizar visibilidad
    all_feeds = SOURCES["INTEL"] + SOURCES["LOCAL_VIDEO"]
    render_feed(all_feeds)

with col_twitter:
    st.markdown('<p style="color:#58a6ff; font-weight:bold; letter-spacing:2px;">🐦 SEÑAL X (AUTOREFRESH)</p>', unsafe_allow_html=True)
    # El widget se recrea desde cero cada 20 segundos, forzando la carga de tweets nuevos
    components.html(f"""
        <div id="twitter-container">
            <a class="twitter-timeline" 
               data-theme="dark" 
               data-chrome="noheader nofooter noborders transparent" 
               href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw"
               data-height="1000">
            </a>
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        <script>
            // Forzar recarga del widget si es necesario
            if (window.twttr) {{ window.twttr.widgets.load(); }}
        </script>
    """, height=1200)

# 5. EL RELOJ DE 20 SEGUNDOS
time.sleep(20)
st.rerun()
