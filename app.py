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
    .emergency-btn { 
        display: block; width: 100%; padding: 15px; background: #dc2626; color: white; 
        text-align: center; border-radius: 5px; text-decoration: none; font-weight: bold; margin-bottom: 10px;
    }
    [data-testid="stSidebar"], header, footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (INTACTO, COMO TE GUSTA) ---
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
    st.markdown('<div class="header-col">📡 TRANSMISIÓN DE EMERGENCIA</div>', unsafe_allow_html=True)
    
    # SOLUCIÓN DE VIDEO: Usamos la señal de RTVE Noticias (Muy estable)
    # He añadido un botón de respaldo por si el navegador bloquea el embebido.
    st.markdown('<a href="https://www.rtve.es/noticias/directo/canal-24-horas/" target="_blank" class="emergency-btn">🔴 ABRIR SEÑAL TV EN VIVO (OPCIÓN RESPALDO)</a>', unsafe_allow_html=True)
    
    components.iframe("https://www.youtube.com/embed/8I_v6K8M-68?autoplay=1&mute=1", height=400)
    
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
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (VÍA WEB)</div>', unsafe_allow_html=True)
    
    # SOLUCIÓN DE X: Al ver que el feed se queda en negro, 
    # la mejor opción es un enlace de "Visualización Rápida" que carga instantáneamente.
    st.markdown("""
        <div class="card" style="border-left: 4px solid #1d9bf0; text-align: center; padding: 40px 10px;">
            <h3 style="color:#1d9bf0;">SEÑAL DE X ACTIVA</h3>
            <p>Debido a restricciones de seguridad de la plataforma, haz clic abajo para ver los reportes en tiempo real.</p>
            <a href="https://twitter.com/search?q=venezuela&f=live" target="_blank" class="emergency-btn" style="background:#1d9bf0;">
                VER ÚLTIMOS TWEETS (VENEZUELA)
            </a>
            <hr style="border: 0.5px solid #1f2937; margin: 20px 0;">
            <a href="https://twitter.com/AlertaNews24" target="_blank" class="emergency-btn" style="background:#000; border: 1px solid #1d9bf0;">
                CANAL ALERTA NEWS 24
            </a>
        </div>
    """, unsafe_allow_html=True)
