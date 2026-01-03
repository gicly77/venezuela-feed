import streamlit as st
import feedparser
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { background:#10141b; border:1px solid #1f2937; border-radius:8px; padding:15px; margin-bottom:12px; border-left: 5px solid #ffcc00; position: relative; }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:700; font-size:1.1rem; display: block; margin-right: 60px; }
    .time-badge { 
        position: absolute; top: 15px; right: 15px;
        font-size:0.7rem; background:#dc2626; color:white; 
        padding:2px 6px; border-radius:3px; font-weight:bold; 
    }
    .source-tag { font-size:0.7rem; color:#9ca3af; font-weight:900; text-transform: uppercase; margin-bottom: 5px; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; color: #f0f6fc; letter-spacing: 2px;}
</style>
""", unsafe_allow_html=True)

st.title(f"🛡️ VENEZUELA INTELLIGENCE CENTER | {datetime.now().strftime('%H:%M:%S')}")

# Refresco automático cada 60 segundos
st_autorefresh(interval=60 * 1000, key="global_refresh")

# --- 3. MOTOR DE NOTICIAS CON HORA ---
def get_news_with_time():
    url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    items = []
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:12]:
            # Extraer y formatear la hora (formato HH:MM)
            publicado = e.published_parsed
            hora_local = time.strftime('%H:%M', publicado) if publicado else "AHORA"
            
            items.append({
                "source": e.source.get('title', 'NOTICIA'),
                "title": e.title.rsplit(' - ', 1)[0],
                "link": e.link,
                "time": hora_local
            })
    except: pass
    return items

# --- 4. INTERFAZ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown('<div class="header-col">📡 RADAR DE NOTICIAS CRÍTICAS</div>', unsafe_allow_html=True)
    noticias = get_news_with_time()
    
    if noticias:
        for n in noticias:
            st.markdown(f"""
            <div class="news-card">
                <span class="time-badge">{n['time']}</span>
                <div class="source-tag">{n['source']}</div>
                <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Buscando nuevas actualizaciones...")

with col_right:
    st.markdown('<div class="header-col">🐦 FEED DE INTELIGENCIA X</div>', unsafe_allow_html=True)
    
    # Botón de acceso rápido (siempre funcional)
    st.link_button("🔥 VER TWEETS RECIENTES (VENEZUELA)", 
                   "https://x.com/search?q=venezuela&f=live", use_container_width=True)
    
    st.markdown("---")

    # Widget de X para AlertaNews24 (Integración oficial)
    components.html(
        """
        <div id="twitter-container">
            <a class="twitter-timeline" data-lang="es" data-height="800" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw">
                Cargando inteligencia de X...
            </a> 
        </div>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """,
        height=800,
    )
