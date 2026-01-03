import streamlit as st
import requests
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL BLINDADO ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { background:#10141b; border:1px solid #1f2937; border-radius:8px; padding:15px; margin-bottom:12px; border-left: 5px solid #ffcc00; }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:700; font-size:1.1rem; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; font-weight:bold; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (EL QUE TE FUNCIONA) ---
def fetch_news():
    rss_url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    pool = []
    try:
        f = feedparser.parse(rss_url)
        for e in f.entries[:15]:
            clean_title = e.title.rsplit(' - ', 1)[0]
            pool.append({
                "source": e.source.get('title', 'Noticia'),
                "title": clean_title,
                "link": e.link
            })
    except: pass
    return pool

st_autorefresh(interval=60 * 1000, key="war_room_refresh")

# --- 4. INTERFAZ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑALES DE VIDEO (DIRECTO)</div>', unsafe_allow_html=True)
    st.warning("⚠️ YouTube y TV incrustada están bloqueados por el servidor. Usa estos accesos directos nativos:")
    
    # BOTONES NATIVOS: Streamlit no puede bloquear sus propios botones.
    if st.button("🔴 ABRIR CANAL 24H (RTVE)", use_container_width=True):
        st.markdown('<meta http-equiv="refresh" content="0; url=https://www.rtve.es/noticias/directo/canal-24-horas/">', unsafe_allow_html=True)
    
    if st.button("🔵 ABRIR FRANCE 24 (ESPAÑOL)", use_container_width=True):
        st.markdown('<meta http-equiv="refresh" content="0; url=https://www.france24.com/es/envivo">', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="header-col">📰 RADAR DE ÚLTIMA HORA</div>', unsafe_allow_html=True)
    for n in fetch_news():
        st.markdown(f"""
        <div class="news-card">
            <span class="time-badge">AHORA</span>
            <div style="font-size:0.7rem; color:#9ca3af; font-weight:900;">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (TIEMPO REAL)</div>', unsafe_allow_html=True)
    st.info("💡 Haz clic para ver los reportes actuales sin bloqueos de API:")
    
    # BÚSQUEDAS DE X DIRECTAS
    st.link_button("🔍 VER VENEZUELA (ÚLTIMO MINUTO)", "https://x.com/search?q=venezuela&f=live", use_container_width=True)
    st.link_button("📢 VER ALERTA NEWS 24", "https://x.com/AlertaNews24", use_container_width=True)
    st.link_button("📍 REPORTE CARACAS (EN VIVO)", "https://x.com/search?q=caracas&f=live", use_container_width=True)
    
    st.markdown("""
    <div style="background:#10141b; padding:20px; border-radius:8px; border: 1px solid #1d9bf0; margin-top:20px;">
        <h4 style="color:#1d9bf0; margin-top:0;">GUÍA DE OPERACIÓN</h4>
        <ol style="font-size:0.9rem; color:#9ca3af;">
            <li>Usa los botones rojos para abrir la TV en otra pestaña.</li>
            <li>Usa los botones azules para monitorear X al segundo.</li>
            <li>Mantén esta ventana abierta para el radar de noticias.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
