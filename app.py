import streamlit as st
import feedparser
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide")

# 2. HORA MADRID
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# 3. ESTILO CSS RECUPERADO
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

# 4. ESTRUCTURA DE COLUMNAS
col_noticias, col_x = st.columns([2, 1])

with col_noticias:
    st.markdown(f"## 🛡️ RADAR VENEZUELA | MADRID: {hora_madrid}")
    st.markdown("---")
    
    # Motor de noticias RSS (Restaurado)
    try:
        url_rss = "https://news.google.com/rss/search?q=venezuela+when:1h&hl=es-419&gl=VE&ceid=VE:es-419"
        feed = feedparser.parse(url_rss)
        if feed.entries:
            for e in feed.entries[:10]:
                st.markdown(f"""
                <div class="news-card">
                    <div style="font-size:0.7rem; color:#888;">{e.source.get('title', 'Noticia')}</div>
                    <a class="headline" href="{e.link}" target="_blank">{e.title.rsplit(' - ', 1)[0]}</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Esperando nuevas actualizaciones del radar...")
    except Exception:
        st.error("Reconectando radar de noticias...")

with col_x:
    st.markdown("### 🐦 INTELIGENCIA X")
    
    # Método 3 Oficial: Línea de tiempo incrustada (Perfil Público)
    # He usado el perfil de AlertaNews24 como fuente por ser de alta actividad
    components.html(
        """
        <div style="height: 800px; overflow-y: auto;">
            <a class="twitter-timeline" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw">
                Cargando Inteligencia X...
            </a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        """,
        height=850,
    )
