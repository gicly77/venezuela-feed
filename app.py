import streamlit as st
import requests
import feedparser
import time
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL (MANTENIDO) ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:12px; margin-bottom:10px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; }
    .live-button {
        display: inline-block; width: 100%; padding: 20px; background: #dc2626; color: white !important;
        text-align: center; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1.2rem;
        border: 2px solid #ff0000; transition: 0.3s; margin-bottom: 15px;
    }
    .live-button:hover { background: #ff0000; box-shadow: 0px 0px 15px #ff0000; }
    .x-button { background: #1d9bf0; border: 2px solid #1d9bf0; }
    .x-button:hover { background: #0076bf; box-shadow: 0px 0px 15px #1d9bf0; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (INTACTO) ---
def fetch_realtime_news():
    rss_url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    pool = []
    try:
        f = feedparser.parse(rss_url)
        for e in f.entries[:15]:
            clean_title = e.title.rsplit(' - ', 1)[0]
            source_name = e.source.get('title', 'Noticia')
            pool.append({
                "source": source_name, "title": clean_title, "link": e.link, "time": "AHORA"
            })
    except: pass
    return pool

st_autorefresh(interval=60 * 1000, key="war_room_refresh")

# --- 4. INTERFAZ ---
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL DE VIDEO (DIRECTO)</div>', unsafe_allow_html=True)
    
    # SOLUCIÓN VIDEO: Dado que los embebidos fallan, usamos una señal M3U8 de respaldo
    # que se abre en una ventana optimizada o el botón de acceso directo.
    st.markdown('<a href="https://vaughn.live/embed/video/noticias24h?viewers=true&autoplay=true" target="_blank" class="live-button">🔴 VER CANAL NOTICIAS 24H (VIVO)</a>', unsafe_allow_html=True)
    
    # Intentamos un último reproductor alternativo de una fuente que no es YouTube
    components.html("""
        <iframe src="https://player.twitch.tv/?channel=rtve&parent=share.streamlit.io&muted=true" 
        height="360" width="100%" allowfullscreen></iframe>
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
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (MÉTODO SEGURO)</div>', unsafe_allow_html=True)
    
    # SOLUCIÓN X: Para evitar el cuadro en negro, creamos un Panel de Control de X
    # que te lleva a las búsquedas en vivo y cuentas clave al instante.
    st.markdown("""
        <div class="card" style="border-left: 4px solid #1d9bf0; padding: 20px;">
            <p style="color:#9ca3af; font-size:0.9rem;">⚠️ Las restricciones de X bloquean el feed incrustado. Usa estos accesos directos de inteligencia:</p>
            
            <a href="https://x.com/search?q=venezuela&f=live" target="_blank" class="live-button x-button">
                🔍 BUSCAR VENEZUELA (EN VIVO)
            </a>
            
            <a href="https://x.com/AlertaNews24" target="_blank" class="live-button x-button" style="background: #000;">
                📢 ALERTA NEWS 24 (OFICIAL)
            </a>

            <div style="margin-top:20px; padding:10px; background:#0a0d14; border-radius:5px; font-size:0.85rem;">
                <strong>TIP DE OPERACIONES:</strong> Mantén X abierto en una pestaña lateral y las noticias aquí para monitoreo total.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Intentamos una última carga ligera de un post individual para ver si el navegador permite al menos uno
    components.html("""
        <blockquote class="twitter-tweet" data-theme="dark"><a href="https://twitter.com/AlertaNews24/status/1817758371302834641"></a></blockquote>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """, height=400)
