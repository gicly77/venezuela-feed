import streamlit as st
import requests
import time

# Configuración profesional de la página
st.set_page_config(page_title="VENEZUELA CRÍTICO", layout="wide", page_icon="🇻🇪")

# Estilo de encabezado
st.title("🇻🇪 Venezuela: Monitor de Eventos en Tiempo Real")
st.markdown("---")

# Tu API Key
API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

def buscar_noticias_criticas():
    # Esta búsqueda es mucho más específica: busca reportes oficiales, alertas y última hora
    terminos = "(Venezuela AND (oficial OR urgente OR alerta OR 'ultima hora' OR comunicado OR crisis))"
    url = f"https://newsapi.org/v2/everything?q={terminos}&language=es&sortBy=publishedAt&pageSize=20&apiKey={API_KEY}"
    
    try:
        r = requests.get(url)
        datos = r.json()
        return datos.get('articles', [])
    except:
        return []

# Contenedor dinámico
feed = st.empty()

while True:
    articulos = buscar_noticias_criticas()
    
    with feed.container():
        if not articulos:
            st.info("Esperando nuevos reportes oficiales...")
        else:
            for art in articulos:
                # Formato detallado de noticia
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if art.get('urlToImage'):
                            st.image(art['urlToImage'], use_container_width=True)
                    with col2:
                        st.subheader(art['title'])
                        st.caption(f"📢 FUENTE: {art['source']['name']} | ⏱️ PUBLICADO: {art['publishedAt']}")
                        st.write(f"**Resumen:** {art['description']}")
                        st.markdown(f"[🔗 Leer reporte completo y detalles]({art['url']})")
                    st.markdown("---")
    
    # Pausa de 30 segundos antes de la siguiente búsqueda
    time.sleep(30)
