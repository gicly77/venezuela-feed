import streamlit as st
import requests
import time
import streamlit.components.v1 as components

# Configuración de alto impacto
st.set_page_config(page_title="MONITOR VZLA-USA", layout="wide", page_icon="🇻🇪")

# Encabezado con estilo
st.title("🇻🇪 Monitor Geopolítico: Venezuela - USA")
st.markdown(f"**Actualización en vivo:** Reportes de Caracas, Washington y el mundo.")

# Tu API Key fija
API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

# Layout de dos columnas
col_prensa, col_redes = st.columns([2, 1])

with col_redes:
    st.subheader("🐦 X (Twitter) en Vivo")
    # Feed de X enfocado en noticias de última hora
    twitter_html = """
    <a class="twitter-timeline" data-height="1200" data-theme="dark" href="https://twitter.com/ReporteYa?ref_src=twsrc%5Etfw">Reportes de X</a> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(twitter_html, height=1200)

with col_prensa:
    st.subheader("📰 Noticias de Última Hora")
    contenedor_noticias = st.empty()

def buscar_noticias_avanzadas():
    # Búsqueda con tus nuevas palabras clave estratégicas
    # Filtramos por Maduro, Trump, Libertad, Caracas y la relación con USA
    query = "(Venezuela AND (Maduro OR Trump OR 'Donald Trump' OR 'USA' OR 'Estados Unidos' OR 'libertad' OR 'ultima hora' OR 'Caracas'))"
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize=15&apiKey={API_KEY}"
    
    try:
        r = requests.get(url)
        return r.json().get('articles', [])
    except:
        return []

# Bucle infinito de monitoreo
while True:
    noticias = buscar_noticias_avanzadas()
    
    with contenedor_noticias.container():
        if not noticias:
            st.warning("Buscando nuevos reportes en las agencias de noticias...")
        else:
            for art in noticias:
                with st.container():
                    # Formato de noticia profesional
                    st.markdown(f"#### {art['title']}")
                    st.caption(f"🗓️ {art['publishedAt']} | 🏛️ Fuente: {art['source']['name']}")
                    
                    if art.get('urlToImage'):
                        st.image(art['urlToImage'], use_container_width=True)
                    
                    st.write(art['description'])
                    st.markdown(f"[➡️ Ver análisis completo]({art['url']})")
                    st.divider()
    
    #
