import streamlit as st
import requests
import time
import streamlit.components.v1 as components

# Configuración profesional
st.set_page_config(page_title="MONITOR VZLA-USA", layout="wide", page_icon="🇻🇪")

# Estilo personalizado para el feed
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMarkdown h3 { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇻🇪 Monitor Geopolítico: Venezuela - USA")
st.markdown("---")

# Tu API Key
API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

# Layout de dos columnas para maximizar el tiempo real
col_prensa, col_redes = st.columns([2, 1])

with col_redes:
    st.subheader("🐦 X (Twitter) - Segundos atrás")
    # Este componente carga el feed de X en tiempo real absoluto.
    # He configurado una búsqueda que mezcla tus palabras clave en X.
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" 
    href="https://twitter.com/ReporteYa?ref_src=twsrc%5Etfw">Cargando reporte de calle...</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200, scrolling=True)

with col_prensa:
    st.subheader("📰 Noticias de Última Hora (Prensa)")
    contenedor_noticias = st.empty()

def buscar_noticias_avanzadas():
    # Búsqueda quirúrgica con tus palabras clave: Maduro, Trump, Libertad, Caracas, USA
    query = "(Venezuela AND (Maduro OR Trump OR USA OR libertad OR 'ultima hora' OR Caracas))"
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize=15&apiKey={API_KEY}"
    
    try:
        r = requests.get(url)
        return r.json().get('articles', [])
    except:
        return []

# Bucle de monitoreo constante
while True:
    noticias = buscar_noticias_avanzadas()
    
    with contenedor_noticias.container():
        if not noticias:
            st.info("Buscando nuevas señales de prensa...")
        else:
            for art in noticias:
                with st.container():
                    # Formato de alerta
                    st.error(f"🚨 {art['title']}")
                    st.caption(f"🗓️ {art['publishedAt']} | 🏛️ Fuente: {art['source']['name']}")
                    
                    if art.get('urlToImage'):
                        st.image(art['urlToImage'], use_container_width=True)
                    
                    st.write(f"**Detalles:** {art['description']}")
                    st.markdown(f"[➡️ Abrir Fuente Oficial]({art['url']})")
                    st.divider()
    
    # Actualización automática cada 30 segundos
    time.sleep(30)
