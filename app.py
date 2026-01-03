import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de Centro de Inteligencia
st.set_page_config(page_title="GLOBAL VZLA MONITOR", layout="wide", page_icon="🌎")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; }
    .noticia-card { border-left: 4px solid #ff4b4b; padding: 15px; margin-bottom: 20px; background: #111; }
    .fuente-tag { color: #ff4b4b; font-weight: bold; text-transform: uppercase; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌎 Monitor Global de Crisis: Venezuela-Mundo")
st.write("Señal combinada: Redacciones Globales (RSS) + Redes Sociales (X)")

# --- LISTA DE FUENTES RSS (HABLA HISPANA E INGLESA) ---
RSS_FEEDS = {
    "El País (ES)": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "ABC (ES)": "https://www.abc.es/rss/2.0/internacional/latinoamerica/",
    "BBC World (UK)": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters (INT)": "https://www.reutersagency.com/feed/",
    "CNN (USA)": "http://rss.cnn.com/rss/edition_world.rss",
    "Infobae (ARG)": "https://www.infobae.com/feeds/rss/",
    "El Tiempo (COL)": "https://www.eltiempo.com/rss/mundo.xml"
}

col_prensa, col_x = st.columns([2, 1])

with col_x:
    st.subheader("⚡ SEÑAL X (TIEMPO REAL)")
    # Feed de POTUS para reportes de la Casa Blanca al segundo
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">Tweets</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200, scrolling=True)

with col_prensa:
    st.subheader("📡 CABLES DE AGENCIA (RSS GLOBAL)")
    feed_display = st.empty()

def obtener_noticias_globales():
    noticias = []
    # Palabras clave exhaustivas
    keywords = ['venezuela', 'maduro', 'trump', 'caracas', 'usa', 'libertad', 'white house', 'biden']
    
    for nombre, url in RSS_FEEDS.items():
        try:
            f = feedparser.parse(url)
            for entry in f.entries:
                texto_total = (entry.title + entry.get('summary', '')).lower()
                if any(k in texto_total for k in keywords):
                    noticias.append({
                        'titulo': entry.title,
                        'link': entry.link,
                        'fuente': nombre,
                        'fecha': entry.get('published', 'Reciente')
                    })
        except:
            continue
    return noticias

# Bucle de monitoreo
while True:
    lista_noticias = obtener_noticias_globales()
    with feed_display.container():
        if not lista_noticias:
            st.info("Escaneando frecuencias internacionales...")
        else:
            for n in lista_noticias[:25]: # Mostramos las 25 más frescas de todas las fuentes
                st.markdown(f"""
                <div class="noticia-card">
                    <span class="fuente-tag">{n['fuente']} | {n['fecha']}</span>
                    <h3>{n['titulo']}</h3>
                    <a href="{n['link']}" target="_blank" style="color: #4da3ff;">Abrir despacho oficial →</a>
                </div>
                """, unsafe_allow_html=True)
    
    time.sleep(15) # Refresco cada 15 segundos
