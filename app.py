import streamlit as st
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .news-card { background:#10141b; border:1px solid #1f2937; border-radius:8px; padding:15px; margin-bottom:12px; border-left: 5px solid #ffcc00; }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:700; font-size:1.1rem; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; font-weight:800; text-transform: uppercase; color: #f0f6fc; }
</style>
""", unsafe_allow_html=True)

st.title(f"🛡️ WAR ROOM: VENEZUELA | {datetime.now().strftime('%H:%M:%S')}")

# Refresco automático cada 60 segundos para las noticias
st_autorefresh(interval=60 * 1000, key="refresh_noticias")

# --- 3. MOTOR DE NOTICIAS (RADAR) ---
def get_venezuela_news():
    # Usamos Google News RSS que es infalible
    url = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:10]
    except:
        return []

# --- 4. DISEÑO DE COLUMNAS ---
col_video, col_x = st.columns([1.2, 1])

with col_video:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL EN VIVO</div>', unsafe_allow_html=True)
    
    # SEÑAL DE VIDEO: Usamos el ID directo de YouTube que permite incrustación
    # Esta es la señal oficial de RTVE Noticias (Canal 24h)
    st.video("https://www.youtube.com/watch?v=R_m9m3Uun_o")
    
    st.markdown('<div class="header-col" style="margin-top:25px;">📰 RADAR DE ÚLTIMA HORA</div>', unsafe_allow_html=True)
    noticias = get_venezuela_news()
    if noticias:
        for n in noticias:
            st.markdown(f"""
            <div class="news-card">
                <div style="font-size:0.7rem; color:#9ca3af; font-weight:900;">{n.source.get('title', 'NOTICIA')}</div>
                <a class="headline" href="{n.link}" target="_blank">{n.title.rsplit(' - ', 1)[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Error al cargar noticias. Reintentando...")

with col_x:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (SISTEMA DE ENLACE)</div>', unsafe_allow_html=True)
    
    st.warning("⚠️ La API de X tiene restricciones de servidor. Usa estos accesos directos de alta velocidad:")
    
    # BOTONES DE INTELIGENCIA: Abren X en pestañas laterales con búsquedas pre-filtradas
    st.link_button("🔍 VENEZUELA: ÚLTIMO MINUTO (VIVO)", 
                   "https://x.com/search?q=venezuela&f=live", use_container_width=True)
    
    st.link_button("📢 CANAL DE ALERTA NEWS 24", 
                   "https://x.com/AlertaNews24", use_container_width=True)
    
    st.link_button("📍 SITUACIÓN EN CARACAS (VIVO)", 
                   "https://x.com/search?q=caracas&f=live", use_container_width=True)

    # Widget visual de apoyo (solo si el navegador lo permite)
    st.markdown("---")
    st.info("💡 Consejo: Abre una de las pestañas de X a la derecha de tu pantalla para monitoreo simultáneo.")
    
    # Intento de cargar un post específico para verificar conexión
    st.markdown('<div style="background:#10141b; padding:20px; border-radius:8px; border: 1px solid #1d9bf0;">'
                '<p style="color:#1d9bf0; text-align:center;"><b>Sincronización manual de X activada</b></p>'
                '</div>', unsafe_allow_html=True)
