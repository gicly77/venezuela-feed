import streamlit as st
import feedparser
import requests
from datetime import datetime
import pytz
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. ACTUALIZACIÓN AUTOMÁTICA GLOBAL (Sin intervención manual)
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide")
st_autorefresh(interval=60 * 1000, key="global_refresh") 

# 2. HORA LOCAL MADRID
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 3. ESTILO VISUAL (Radar de Noticias)
st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #e1e1e1; }
    [data-testid="stSidebar"], header, footer { display: none !important; }
    .news-card { 
        background: #10141b; border: 1px solid #1f2937; padding: 15px; 
        margin-bottom: 12px; border-left: 5px solid #ffcc00; border-radius: 8px;
    }
    .headline { color: #60a5fa !important; text-decoration: none; font-weight: bold; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# 4. FUNCIÓN PARA EVITAR EL RECHAZO DE CONEXIÓN DE X (oEmbed)
def get_x_html(url):
    try:
        # Se solicita el HTML oficial a la API de X para que no rechace la conexión
        api_url = f"https://publish.twitter.com/oembed?url={url}&theme=dark&omit_script=false"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()["html"]
        return None
    except:
        return None

# 5. DISTRIBUCIÓN DE PANTALLA
col_radar, col_x = st.columns([2, 1])

with col_radar:
    st.markdown(f"## 🛡️ RADAR VENEZUELA | {hora_madrid}")
    st.markdown("---")
    
    # Motor de Noticias RSS
    url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
    feed = feedparser.parse(url_rss)
    for e in feed.entries[:10]:
        st.markdown(f"""
        <div class="news-card">
            <div style="font-size:0.7rem; color:#888;">{e.source.get('title')}</div>
            <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
        </div>
        """, unsafe_allow_html=True)

with col_x:
    st.markdown("### 🐦 INTELIGENCIA X")
    
    # URL de un post reciente para disparar el renderizado automático
    tweet_url = "https://twitter.com/AlertaNews24/status/1875323267591602521"
    embed_code = get_x_html(tweet_url)
    
    if embed_code:
        # Renderizado mediante componente HTML de Streamlit
        components.html(
            f"""
            <div style="background-color: transparent;">
                {embed_code}
            </div>
            """,
            height=850,
            scrolling=True
        )
    else:
        # Método de respaldo nativo si la API falla
        components.html(
            """
            <a class="twitter-timeline" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw"></a>
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """,
            height=850
        )
