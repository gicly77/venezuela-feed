import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="VENEZUELA MONITOR", layout="wide", page_icon="🇻🇪")

st.title("🇻🇪 Venezuela Live: Prensa y Redes")

# --- BLOQUE 1: X (TWITTER) - TIEMPO REAL ---
st.subheader("🐦 Última hora en X (Fuentes Clave)")
st.caption("Esta sección muestra lo que está pasando en el segundo exacto.")

# Aquí puedes poner la cuenta que prefieras (ej. @PresidencialVen, @ReporteYa, etc.)
twitter_html = """
<a class="twitter-timeline" data-height="600" data-theme="dark" href="https://twitter.com/PresidencialVen?ref_src=twsrc%5Etfw">Tweets de Venezuela</a> 
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""
components.html(twitter_html, height=600, scrolling=True)

st.divider()

# --- BLOQUE 2: PRENSA (API) ---
st.subheader("📰 Noticias Recientes")
API_KEY = "3f543e8fd9154b5595a075c8bd16b98c"

def buscar_noticias():
    url = f"https://newsapi.org/v2/everything?q=Venezuela+urgente+confirmado&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        return r.json().get('articles', [])[:6]
    except:
        return []

noticias = buscar_noticias()
for art in noticias:
    with st.expander(f"📍 {art['source']['name']}: {art['title']}"):
        if art['urlToImage']:
            st.image(art['urlToImage'])
        st.write(art['description'])
        st.markdown(f"[Leer noticia completa]({art['url']})")