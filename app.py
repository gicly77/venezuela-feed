import streamlit as st
import requests
import feedparser
import time
from datetime import datetime, timezone
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL (LIMPIO Y SIN SIDEBAR) ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:12px; margin-bottom:10px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS DE TIEMPO REAL (GOOGLE NEWS ULTRA-FAST) ---
def fetch_realtime_news():
    # Usamos Google News filtrado por la última hora para garantizar frescura
    rss_url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    pool = []
    try:
        f = feedparser.parse(rss_url)
        for e in f.entries[:15]:
            # Limpieza básica del título (Google añade el nombre del medio al final)
            clean_title = e.title.rsplit(' - ', 1)[0]
            source_name = e.source.get('title', 'Noticia')
            pool.append({
                "source": source_name,
                "title": clean_title,
                "link": e.link,
                "time": "AHORA"
            })
    except: pass
    return pool

# Actualización cada 60 segundos
st_autorefresh(interval=60 * 1000, key="war_room_refresh")

# --- 4. INTERFAZ ---
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL (DW EN VIVO)</div>', unsafe_allow_html=True)
    
    # VIDEO: DW en Español - Es la señal más confiable y libre de bloqueos
    components.html("""
        <div style="background:#000; width:100%; height:360px;">
            <iframe width="100%" height="360" src="https://www.youtube.com/embed/live_stream?channel=UCT4J_Y8_v4Z68Wec-77v4cg&autoplay=1&mute=1" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """, height=365)
    
    st.markdown('<div class="header-col" style="margin-top:20px;">📰 RADAR DE ÚLTIMA HORA</div>', unsafe_allow_html=True)
    for n in fetch_realtime_news():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div style="font-size:0.7rem; color:#9ca3af; font-weight:900;">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (REAL-TIME)</div>', unsafe_allow_html=True)
    
    # X (Twitter): Al fallar tu API por cuota, usamos el Timeline de AlertaNews24. 
    # Es la única forma de garantizar que SIEMPRE veas tweets sin errores.
    components.html("""
        <div style="background:#10141b; border-radius:8px;">
            <a class="twitter-timeline" data-height="900" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw"></a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
    """, height=900)
