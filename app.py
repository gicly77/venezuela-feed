import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de Terminal Profesional
st.set_page_config(page_title="MONITOR ESTRATÉGICO VZLA", layout="wide", page_icon="🇻🇪")

# CSS para un diseño sobrio y profesional
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .seccion-header { background-color: #1f2937; color: #ffffff; padding: 10px; border-radius: 5px; font-weight: bold; margin: 15px 0; border-left: 5px solid #ff4b4b; text-transform: uppercase; }
    .noticia-card { background-color: #161b22; padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #30363d; }
    .noticia-importante { border: 1px solid #ff4b4b; background-color: #1c1314; }
    .fuente-tag { color: #ff4b4b; font-weight: bold; font-size: 0.75em; text-transform: uppercase; }
    .noticia-titulo { font-size: 1.05em; font-weight: 600; margin-top: 8px; display: block; color: #e1e1e1; text-decoration: none; }
    .noticia-titulo:hover { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇻🇪 Monitor de Inteligencia: Solo Venezuela")
st.caption("Filtro Estricto Activo | Refresco: 10 segundos")

# --- FUENTES RSS ---
RSS_MASTER = {
    "🏛️ OFICIAL / GOBIERNO": [
        ("White House", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("State Dept", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("ONU News", "https://news.un.org/feed/subscribe/es/news/region/latin-america-and-the-caribbean/feed/rss.xml"),
        ("OEA", "https://www.oas.org/es/centro_noticias/rss.asp")
    ],
    "🌍 PRENSA INTERNACIONAL": [
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"),
        ("El Mundo", "https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml"),
        ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Reuters", "https://www.reutersagency.com/feed/")
    ],
    "🇻🇪 PRENSA NACIONAL": [
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("NTN24", "https://www.ntn24.com/rss.xml")
    ]
}

col1, col2, col3 = st.columns([1, 1, 1])

def monitor_estricto(columna, titulo, fuentes):
    with columna:
        st.markdown(f'<div class="seccion-header">{titulo}</div>', unsafe_allow_html=True)
        
        # Palabras clave obligatorias (si no están, la noticia no sale)
        filtro_venezuela = ['venezuela', 'caracas', 'maduro', 'chavismo', 'padrino lópez', 'miraflores']
        # Palabras de alto impacto para destacar
        palabras_alerta = ['gobierno', 'trump', 'cambio de gobierno', 'guerra', 'ejército', 'ejercito', 'golpe de estado', 'sanciones', 'ataque', 'captura']
        
        encontrado = False
        for nombre, url in fuentes:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:15]:
                    texto = (entry.title + entry.get('summary', '')).lower()
                    
                    # CONDICIÓN ESTRICTA: Debe mencionar a Venezuela o Maduro
                    if any(v in texto for v in filtro_venezuela):
                        encontrado = True
                        # Si además tiene palabras de alerta, le ponemos un borde especial
                        es_alerta = any(a in texto for a in palabras_alerta)
                        clase_css = "noticia-card noticia-importante" if es_alerta else "noticia-card"
                        
                        st.markdown(f"""
                        <div class="{clase_css}">
                            <span class="fuente-tag">{nombre}</span>
                            <a class="noticia-titulo" href="{entry.link}" target="_blank">{entry.title}</a>
                            <span style="font-size: 0.7em; color: #888;">🕒 {entry.get('published', 'Reciente')}</span>
                        </div>
                        """, unsafe_allow_html=True)
            except:
                continue
        
        if not encontrado:
            st.caption("Sin noticias recientes de Venezuela en este sector.")

# --- EJECUCIÓN ---
monitor_estricto(col1, "🏛️ OFICIAL / GOBIERNO", RSS_MASTER["🏛️ OFICIAL / GOBIERNO"])
monitor_estricto(col2, "🌍 PRENSA INTERNACIONAL", RSS_MASTER["🌍 PRENSA INTERNACIONAL"])
monitor_estricto(col3, "🇻🇪 PRENSA NACIONAL", RSS_MASTER["🇻🇪 PRENSA NACIONAL"])

# Sidebar para X (Twitter)
with st.sidebar:
    st.markdown('<div class="seccion-header">⚡ SEÑAL X (POTUS)</div>', unsafe_allow_html=True)
    twitter_html = """
    <a class="twitter-timeline" data-height="1000" data-theme="dark" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">POTUS</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1000)

time.sleep(10)
st.rerun()
