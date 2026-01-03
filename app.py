import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de Terminal de Inteligencia
st.set_page_config(page_title="WAR ROOM VZLA", layout="wide", page_icon="🚨")

# CSS para Animación de Alerta Parpadeante y Diseño Profesional
st.markdown("""
    <style>
    @keyframes blink { 0% { background-color: #161b22; } 50% { background-color: #ff0000; } 100% { background-color: #161b22; } }
    .stApp { background-color: #05070a; color: #ffffff; }
    .seccion-header { background-color: #1f2937; color: #ff4b4b; padding: 10px; border-radius: 5px; font-weight: bold; margin: 15px 0; border-bottom: 2px solid #ff4b4b; text-transform: uppercase; letter-spacing: 1px; }
    .noticia-card { background-color: #161b22; padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #30363d; }
    .alerta-maxima { animation: blink 1s infinite; border: 2px solid white !important; }
    .fuente-tag { color: #ff4b4b; font-weight: bold; font-size: 0.75em; border: 1px solid #ff4b4b; padding: 2px 5px; border-radius: 3px; }
    .noticia-titulo { font-size: 1.05em; font-weight: 600; margin-top: 8px; display: block; color: #e1e1e1; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 Monitor de Alerta Temprana: Venezuela-Mundo")
st.caption("Filtro de Inteligencia Activo | Refresco: 10 segundos")

# --- FUENTES RSS OFICIALES Y GLOBALES ---
RSS_MASTER = {
    "🏛️ OFICIAL / GOBIERNO": [
        ("White House (USA)", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("State Dept (USA)", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("Reuters Intl", "https://www.reutersagency.com/feed/"),
        ("UN News (ONU)", "https://news.un.org/feed/subscribe/es/news/region/latin-america-and-the-caribbean/feed/rss.xml")
    ],
    "🇪🇺 EUROPA / ESPAÑA": [
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"),
        ("El Mundo", "https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml"),
        ("BBC World (EN)", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("DW World", "https://rss.dw.com/xml/rss-es-world")
    ],
    "🇻🇪 VENEZUELA / LATAM": [
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("El Tiempo (COL)", "https://www.eltiempo.com/rss/mundo.xml")
    ]
}

col1, col2, col3 = st.columns([1, 1, 1])

def monitor_inteligencia(columna, titulo, fuentes):
    with columna:
        st.markdown(f'<div class="seccion-header">{titulo}</div>', unsafe_allow_html=True)
        # Palabras que activan la alerta visual parpadeante
        palabras_criticas = ['ataque', 'bomba', 'urgente', 'detenido', 'muerto', 'invasion', 'golpe', 'militar', 'explosion']
        keywords_relevancia = ['venezuela', 'maduro', 'trump', 'caracas', 'usa', 'libertad', 'biden', 'sanctions']
        
        for nombre, url in fuentes:
            try:
                feed = feedparser.parse(url)
                count = 0
                for entry in feed.entries:
                    text_content = (entry.title + entry.get('summary', '')).lower()
                    
                    if any(k in text_content for k in keywords_relevancia):
                        es_critica = any(c in text_content for c in palabras_criticas)
                        clase_alerta = "alerta-maxima" if es_critica else ""
                        prefijo = "⚠️ CRÍTICO: " if es_critica else ""
                        
                        st.markdown(f"""
                        <div class="noticia-card {clase_alerta}">
                            <span class="fuente-tag">{nombre}</span>
                            <a class="noticia-titulo" href="{entry.link}" target="_blank">{prefijo}{entry.title}</a>
                            <span style="font-size: 0.7em; color: #888;">🕒 {entry.get('published', 'Ahora')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        count += 1
                    if count >= 6: break
            except:
                continue

# --- SECCIÓN LATERAL DE REDES ---
with st.sidebar:
    st.markdown('<div class="seccion-header">⚡ SEÑAL X (POTUS)</div>', unsafe_allow_html=True)
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">POTUS</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200)

# --- EJECUCIÓN CONTINUA ---
while True:
    monitor_inteligencia(col1, "🏛️ OFICIAL / GOBIERNO", RSS_MASTER["🏛️ OFICIAL / GOBIERNO"])
    monitor_inteligencia(col2, "🇪🇺 EUROPA / ESPAÑA", RSS_MASTER["🇪🇺 EUROPA / ESPAÑA"])
    monitor_inteligencia(col3, "🇻🇪 VENEZUELA / LATAM", RSS_MASTER["🇻🇪 VENEZUELA / LATAM"])
    
    time.sleep(10) # Refresco cada 10 segundos para tiempo real agresivo
    st.rerun() # Reinicia la aplicación para capturar nuevos cables
