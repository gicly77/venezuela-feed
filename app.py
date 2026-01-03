import streamlit as st
import requests
import time
import streamlit.components.v1 as components

# Configuración de Centro de Mando
st.set_page_config(page_title="GLOBAL MONITOR VZLA", layout="wide", page_icon="🌎")

# Estética de Terminal de Inteligencia
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stMarkdown h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌎 Monitor Global de Crisis: Venezuela-Mundo")
st.write("Fuentes: White House, POTUS, Prensa España, Colombia, Argentina, USA y Vzla.")

API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

# --- PANEL DUAL: PRENSA Y REDES ---
col_prensa, col_x = st.columns([1, 1])

with col_x:
    st.subheader("⚡ SEÑAL X (TIEMPO REAL ABSOLUTO)")
    # El feed de POTUS y agencias internacionales es el único que te dará el "segundo a segundo"
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">Real-time Global Feed</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200, scrolling=True)

with col_prensa:
    st.subheader("📰 REDACCIÓN GLOBAL (PRENSA FLASH)")
    feed_prensa = st.empty()

def buscar_noticias_globales():
    # Búsqueda ampliada a todos los países y términos clave que pediste
    query = "(Venezuela AND (Maduro OR Trump OR libertad OR 'ultima hora' OR 'Casa Blanca' OR POTUS OR Caracas OR 'Donald Trump'))"
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize=30&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        return r.json().get('articles', [])
    except:
        return []

# Bucle de vigilancia agresiva
while True:
    noticias = buscar_noticias_globales()
    with feed_prensa.container():
        for art in noticias:
            with st.container():
                st.markdown(f"### 🔴 {art['title']}")
                st.caption(f"🌎 {art['source']['name']} | 🕒 {art['publishedAt']}")
                if art.get('urlToImage'):
                    st.image(art['urlToImage'], use_container_width=True)
                st.write(f"**DESPACHO:** {art['description']}")
                st.markdown(f"[🔗 ACCEDER A LA FUENTE]({art['url']})")
                st.divider()
    
    # Actualización cada 20 segundos para la prensa
    time.sleep(20)
