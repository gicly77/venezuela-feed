import streamlit as st
import requests
import feedparser
import time
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:8px; padding:15px; margin-bottom:12px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; letter-spacing: 1px; }
    
    /* BOTONES DE ACCIÓN DIRECTA */
    .action-button {
        display: flex; align-items: center; justify-content: center;
        width: 100%; padding: 18px; margin-bottom: 12px;
        border-radius: 8px; text-decoration: none !important;
        font-weight: 800; font-size: 1.1rem; transition: 0.3s;
        border: none; cursor: pointer;
    }
    .btn-video { background: #dc2626; color: white !important; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3); }
    .btn-video:hover { background: #ff0000; transform: scale(1.02); }
    .btn-x { background: #1d9bf0; color: white !important; box-shadow: 0 4px 15px rgba(29, 155, 240, 0.3); }
    .btn-x:hover { background: #00acee; transform: scale(1.02); }
    
    [data-testid="stSidebar"], header, footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (MANTENIDO) ---
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
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL DE VIDEO (CONTROL DE MONITOR)</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card" style="text-align: center; padding: 30px;">
            <p style="margin-bottom: 20px; font-size: 1.1rem;">Selecciona una fuente de video para abrir el monitor en vivo:</p>
            <a href="https://www.youtube.com/embed/8I_v6K8M-68?autoplay=1" target="_blank" class="action-button btn-video">
                📺 ABRIR MONITOR 1: RTVE 24H (VIVO)
            </a>
            <a href="https://www.france24.com/es/envivo" target="_blank" class="action-button btn-video" style="background: #2c3e50;">
                📺 ABRIR MONITOR 2: FRANCE24 (ES)
            </a>
            <a href="https://www.dw.com/es/tv/s-100452" target="_blank" class="action-button btn-video" style="background: #005191;">
                📺 ABRIR MONITOR 3: DW NOTICIAS
            </a>
            <p style="font-size: 0.8rem; color: #9ca3af; margin-top: 15px;">Nota: El video se abrirá en una nueva pestaña para evitar bloqueos del servidor.</p>
        </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div class="header-col">🐦 PANEL DE INTELIGENCIA X</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card" style="border-left: 4px solid #1d9bf0;">
            <h4 style="color:#1d9bf0; margin-top:0;">MONITOREO DE TENDENCIAS</h4>
            <p style="font-size:0.9rem; color:#9ca3af;">Acceso directo a las fuentes de información más rápidas:</p>
            
            <a href="https://x.com/search?q=venezuela&f=live" target="_blank" class="action-button btn-x">
                🔍 VENEZUELA: ÚLTIMO MINUTO
            </a>
            
            <a href="https://x.com/search?q=caracas&f=live" target="_blank" class="action-button btn-x" style="background: #15202b;">
                📍 REPORTE CARACAS (VIVO)
            </a>
            
            <a href="https://x.com/AlertaNews24" target="_blank" class="action-button btn-x" style="background: #000; border: 1px solid #1d9bf0;">
                📢 CANAL: ALERTA NEWS 24
            </a>
            
            <div style="margin-top:20px; padding:12px; background:#0a0d14; border-radius:8px; font-size:0.85rem; border: 1px dashed #1f2937;">
                <strong>ESTRATEGIA RECOMENDADA:</strong><br>
                1. Abre el monitor de video.<br>
                2. Lanza la búsqueda de X en vivo.<br>
                3. Usa esta ventana para seguir el flujo de noticias minuto a minuto.
            </div>
        </div>
    """, unsafe_allow_html=True)
