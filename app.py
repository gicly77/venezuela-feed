import streamlit as st
import requests
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="CENTRO DE MANDO VZLA", layout="wide", page_icon="🌎")

# Interfaz de Monitor de Inteligencia
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; }
    .stMarkdown h3 { color: #ffffff; border-left: 5px solid #ff4b4b; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌎 Monitor Global de Crisis: Venezuela-Mundo")
st.write("Fuentes: White House, POTUS, Prensa España, Colombia, Argentina, USA y Vzla.")

API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

# --- ESTRUCTURA DE PANTALLA ---
col_prensa, col_x = st.columns([1, 1])

with col_x:
    st.subheader("⚡ SEÑAL X (TIEMPO REAL ABSOLUTO)")
    # Widget que conecta con una lista de noticias globales (puedes crear una lista propia en X y poner el link aquí)
    # Por ahora, usamos un perfil de noticias flash que centraliza fuentes oficiales.
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" href="https://twitter.com/POTUS?ref_src=twsrc%5Etfw">Real-time POTUS & Global Feed</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200, scrolling=True)

with col_prensa:
    st.subheader("📰 REDACCIÓN GLOBAL (PRENSA FLASH)")
    feed_prensa = st.empty()

def buscar_noticias_globales():
    # Buscador exhaustivo: Maduro, Trump, Libertad, Caracas + Países clave
    # Ordenado por "publishedAt" para asegurar que lo último subido aparezca primero
    query = "(Venezuela AND (Maduro OR Trump OR libertad OR 'ultima hora' OR 'Casa Blanca' OR POTUS OR 'White House' OR 'Caracas'))"
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize=30&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        return r.json().get('articles', [])
    except:
        return []

# Bucle de vigilancia constante
while True:
    noticias = buscar_noticias_globales()
    
    with feed_prensa.container():
        if not noticias:
            st.warning("Escaneando frecuencias de noticias globales...")
        else:
            for art in noticias:
                with st.container():
                    # Formato de Alerta Roja para noticias de hace pocos minutos
                    st.markdown(f"### 🔴 {art['title']}")
                    st.caption(f"🌎 ORIGEN: {art['source']['name']} | 🕒 HORA: {art['publishedAt']}")
                    
                    if art.get('urlToImage'):
                        st.image(art['urlToImage'], use_container_width=True)
                    
                    st.write(f"**DESPACHO:** {art['description']}")
                    st.markdown(f"[🔗 ACCEDER A LA FUENTE]({art['url']})")
                    st.markdown("---")
    
    # Refresco ultra-rápido de la prensa
    time.sleep(20)
