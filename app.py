import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# 1. Configuración de la aplicación
st.set_page_config(page_title="Monitor Directo", layout="wide", page_icon="📡")

# 2. CSS Estilizado (Diseño Moderno y Barra de Progreso)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'JetBrains Mono', monospace; }
    
    /* Barra de Progreso Superior */
    .top-bar { position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: #161b22; z-index: 9999; }
    .progress-fill { height: 100%; background: #58a6ff; width: 0%; animation: load 10s linear infinite; }
    @keyframes load { from { width: 0%; } to { width: 100%; } }

    /* Tarjetas de Noticias */
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; }
    .card:hover { border-color: #58a6ff; }
    .alert-card { border-left: 4px solid #f85149; background: #1c1314; }
    
    .source-tag { font-size: 0.7rem; color: #8b949e; text-transform: uppercase; font-weight: bold; }
    .news-title { font-size: 1rem; color: #58a6ff; text-decoration: none; font-weight: 600; display: block; margin: 5px 0; }
    .news-time { font-size: 0.7rem; color: #484f58; }
    
    .col-header { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 20px; }
    </style>
    <div class="top-bar"><div class="progress-fill"></div></div>
    """, unsafe_allow_html=True)

st.markdown('<h2 style="color:#f0f6fc; margin-top:-20px;">Monitor de Eventos en Directo</h2>', unsafe_allow_html=True)

# 3. Diccionario de Fuentes RSS (URLs verificadas y cerradas)
FEEDS = {
    "OFICIAL": [
        ("White House", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("State Dept", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("UN News", "https://news.un.org/feed/subscribe/es/news/region/latin-america-and-the-caribbean/feed/rss.xml")
    ],
    "GLOBAL": [
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml")
    ],
    "TERRENO": [
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/")
    ]
}

# 4. Lógica de Filtrado Estricto
def display_feed(column, title, sources):
    with column:
        st.markdown(f'<div class="col-header">{title}</div>', unsafe_allow_html=True)
        keywords_vzla = ['venezuela', 'maduro', 'caracas', 'miraflores', 'padrino lópez']
        keywords_alert = ['gobierno', 'trump', 'guerra', 'ejército', 'golpe', 'sanciones', 'ataque']
        
        found = False
        for name, url in sources:
            try:
                f = feedparser.parse(url)
                for entry in f.entries[:10]:
                    txt = (entry.title + entry.get('summary', '')).lower()
                    if any(k in txt for k in keywords_vzla):
                        found = True
                        is_alert = any(a in txt for a in keywords_alert)
                        alert_class = "alert-card" if is_alert else ""
                        st.markdown(f"""
                        <div class="card {alert_class}">
                            <span class="source-tag">{name}</span>
                            <a class="news-title" href="{entry.link}" target="_blank">{entry.title}</a>
                            <span class="news-time">{entry.get('published', 'Reciente')}</span>
                        </div>
                        """, unsafe_allow_html=True)
            except: continue
        if not found: st.caption("Sincronizando...")

# 5. Renderizado de Columnas
c1, c2, c3 = st.columns(3)
display_feed(c1, "🏛️ Oficial", FEEDS["OFICIAL"])
display_feed(c2, "🌍 Global", FEEDS["GLOBAL"])
display_feed(c3, "🇻🇪 Terreno", FEEDS["TERRENO"])

# 6. Sidebar X (Twitter)
with st.sidebar:
    st.markdown('<div class="col-header">⚡ SEÑAL X</div>', unsafe_allow_html=True)
    components.html('<a class="twitter-timeline" data-theme="dark" data-height="800" href="https://twitter.com/POTUS"></a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>', height=800)

# 7. Refresco Automático cada 10s
time.sleep(10)
st.rerun()
