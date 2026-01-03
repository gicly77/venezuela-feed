import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de página profesional
st.set_page_config(page_title="MONITOR ESTRATÉGICO VZLA", layout="wide", page_icon="🚨")

# CSS para un diseño limpio y profesional (Estilo Dark Mode Elegante)
st.markdown("""
    <style>
    .stApp { background-color: #111111; color: #f0f2f6; }
    .noticia-card { 
        background-color: #1e1e1e; 
        padding: 20px; 
        border-radius: 8px; 
        border-left: 5px solid #ff4b4b; 
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .fuente-tag { color: #ff4b4b; font-weight: bold; font-size: 0.85em; }
    .titulo-noticia { color: #ffffff; font-size: 1.25em; font-weight: 600; margin: 10px 0; }
    .timestamp { color: #999999; font-size: 0.8em; }
    .link-noticia { color: #4da3ff; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 Monitor de Crisis: Venezuela - Global")
st.markdown("---")

# Lista de fuentes RSS internacionales
RSS_SOURCES = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters": "https://www.reutersagency.com/feed/",
    "CNN": "http://rss.cnn.com/rss/edition_world.rss",
    "ABC": "https://www.abc.es/rss/2.0/internacional/",
    "Infobae": "https://www.infobae.com/feeds/rss/",
    "Efecto Cocuyo": "https://efectococuyo.com/feed/"
}

# Layout de dos columnas
col_prensa, col_x = st.columns([2, 1])

with col_x:
    st.subheader("⚡ Reportes de X (Segundos)")
    # Widget de X optimizado para cargar correctamente
    twitter_html = """
    <div style="background-color: white; border-radius: 10px; padding: 5px;">
        <a class="twitter-timeline" data-height="1000" data-theme="light" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">Tweets</a> 
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>
    """
    components.html(twitter_html, height=1000, scrolling=True)

with col_prensa:
    st.subheader("📡 Cables de Agencia (RSS Global)")
    feed_display = st.empty()

def obtener_datos():
    noticias = []
    # Palabras clave para filtrar el ruido global
    keywords = ['venezuela', 'maduro', 'trump', 'caracas', 'usa', 'libertad', 'biden']
    
    for nombre, url in RSS_SOURCES.items():
        try:
            f = feedparser.parse(url)
            for entry in f.entries:
                texto = (entry.title + entry.get('summary', '')).lower()
                if any(k in texto for k in keywords):
                    noticias.append({
                        'titulo': entry.title,
                        'link': entry.link,
                        'fuente': nombre,
                        'fecha': entry.get('published', 'Reciente')
                    })
        except:
            continue
    return noticias

# Bucle de actualización cada 30 segundos
while True:
    datos = obtener_datos()
    with feed_display.container():
        if not datos:
            st.info("Sincronizando con satélites de noticias...")
        else:
            for n in datos[:20]:
                st.markdown(f"""
                <div class="noticia-card">
                    <span class="fuente-tag">{n['fuente']}</span>
                    <div class="titulo-noticia">{n['titulo']}</div>
                    <span class="timestamp">🕒 {n['fecha']}</span><br><br>
                    <a class="link-noticia" href="{n['link']}" target="_blank">ABRIR REPORTE →</a>
                </div>
                """, unsafe_allow_html=True)
    
    time.sleep(30)
