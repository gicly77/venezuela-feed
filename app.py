import streamlit as st
import requests
import time

# Configuración de la página (esto debe ir al principio)
st.set_page_config(page_title="VENEZUELA LIVE", layout="wide", page_icon="🇻🇪")

# Estilo visual
st.title("🇻🇪 Venezuela: Monitor de Noticias en Vivo")
st.markdown("---")
st.info("El sistema está buscando actualizaciones automáticamente cada 30 segundos.")

# Tu API Key ya integrada
API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

def buscar_noticias():
    # Buscamos 'Venezuela' como palabra clave principal y ordenamos por las más recientes
    url = f"https://newsapi.org/v2/everything?q=Venezuela&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        datos = r.json()
        return datos.get('articles', [])
    except:
        return []

# Creamos un espacio vacío que se refrescará solo
placeholder = st.empty()

# Bucle de actualización constante
while True:
    noticias = buscar_noticias()
    
    with placeholder.container():
        if not noticias:
            st.warning("No se encontraron noticias recientes. Reintentando...")
        else:
            for art in noticias[:12]:  # Mostramos las 12 noticias más frescas
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if art.get('urlToImage'):
                        st.image(art['urlToImage'], use_container_width=True)
                    else:
                        st.write("📷 (Sin imagen)")
                
                with col2:
                    st.subheader(art['title'])
                    st.caption(f"Fuente: {art['source']['name']} | Publicado: {art['publishedAt']}")
                    st.write(art['description'])
                    st.markdown(f"[🔗 Abrir noticia oficial]({art['url']})")
                
                st.markdown("---")
    
    # Espera 30 segundos antes de la siguiente búsqueda
    time.sleep(30)