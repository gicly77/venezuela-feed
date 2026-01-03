import streamlit as st
import feedparser
import time
from datetime import datetime, timezone
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PANTALLA PRO
st.set_page_config(page_title="MONITOR ESTRATÉGICO", layout="wide", page_icon="📡")

# 2. CSS: SIN TEXTOS DE RELLENO Y DISEÑO MÓVIL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Barra de carga discreta (sin texto) */
    .loading-bar-bg { position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: #161b22; z-index: 9999; }
    .loading-bar-fill { height: 100%; background: #58a6ff; width: 0%; animation: progress 30s linear infinite; }
    @keyframes progress { from { width: 0%; } to { width: 100%; } }

    /* Tarjetas de Noticias Limpias */
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 0.9rem; margin-bottom: 0.8rem; }
    .card-potus { border: 2px solid #58a6ff; box-shadow: 0 0 12px rgba(88, 166, 255, 0.2); }
    .card-video { border-left: 4px solid #a371f7; }
    
    .tag { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; display: block; }
    .title { font-size: 1rem; color: #f0f6fc; text-decoration: none; font-weight: 600; display: block; line-height: 1.3; }
    .time-badge { font-size: 0.6rem; color: #ffffff; background: #238636; padding: 1px 6px; border-radius: 4px; font-weight: 600; }
    
    .header-col { font-size: 0.85rem; color: #8b949e; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px; font-weight: 600; }

    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    <div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
    """, unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px;">Monitor de Eventos</h1>', unsafe_allow_html=True)

# 3. FUENTES DE DATOS (VERIFICADAS 100%)
SOURCES = {
    "INTEL": [
        ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("AP News", "https://apnews.com/hub/venezuela.rss"),
        ("El Mundo", "https://www.elmundo.es/rss/internacional.xml")
    ],
    "LOCAL_Y_VIDEO": [
        ("📹 YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
        ("📹 YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/")
    ]
}

# 4. FUNCIÓN DE RENDERIZADO
def render_news():
    vzla_keys = ['venezuela', 'maduro', 'caracas', 'miraflores', 'padrino', 'delcy', 'cabello', 'corina', 'edmundo', 'ataque', 'captura']
    pool = []
    all_sources = SOURCES["INTEL"] + SOURCES["LOCAL_Y_VIDEO"]
    
    for name, url in all_sources:
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
    
    for n in pool[:25]:
        c_class = "card"
        if n['is_potus']: c_class += " card-potus"
        elif n['is_video']: c_class += " card-video"
        
        st.markdown(f"""
        <div class="{c_class}">
            <span class="tag">{n['source']}</span>
            <a class="title" href="{n['link']}" target="_blank">{n['title']}</a>
            <div style="margin-top:6px;"><span class="time-badge">{n['time_str']}</span></div>
        </div>
        """, unsafe_allow_html=True)

# 5. LAYOUT DE COLUMNAS
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown('<div class="header-col">📡 SEÑAL NOTICIAS & VIDEO</div>', unsafe_allow_html=True)
    render_news()

with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X</div>', unsafe_allow_html=True)
    components.html("""
        <a class="twitter-timeline" 
           data-theme="dark" 
           data-chrome="noheader nofooter noborders transparent" 
           href="https://twitter.com/POTUS"
           data-height="1000">
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """, height=1200, scrolling=True)

# 6. ACTUALIZACIÓN SILENCIOSA CADA 30 SEGUNDOS
time.sleep(30)
st.rerun()
