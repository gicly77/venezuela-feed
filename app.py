import streamlit as st
import requests
import feedparser
import time
from datetime import datetime, timezone
import html
import re
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN E INTELIGENCIA ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# AUTO-DIAGNÓSTICO DE SECRETS
st.sidebar.title("🛠️ Status de Conexión")
keys_ready = True

for key in ["X_TOKEN", "NEWS_API_KEY"]:
    if key in st.secrets:
        st.sidebar.success(f"✅ {key} detectado")
    else:
        st.sidebar.error(f"❌ {key} NO detectado")
        keys_ready = False

if not keys_ready:
    st.error("⚠️ ERROR CRÍTICO: No se detectan las llaves en los Secrets de Streamlit. Revisa la barra lateral.")
    st.info("💡 Consejo: Asegúrate de haber guardado los Secrets en Streamlit Cloud y dale a 'Rerun' en el menú superior derecho.")
    st.stop()

# Asignación de variables
X_TOKEN = st.secrets["X_TOKEN"]
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# --- 2. ESTILO VISUAL COMANDO CENTRAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; font-family:'Roboto', sans-serif; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:12px; margin-bottom:10px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; background: #1a1a10; }
    .source-tag { font-size:0.7rem; color:#9ca3af; text-transform:uppercase; font-weight:900; letter-spacing: 1px; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; display:block; margin-top:5px; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; font-weight:bold; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"] { background-color: #0c1017; }
    #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

# Reloj Maestro
st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA | {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. FUNCIONES DE APOYO ---
def linkify(text):
    url_pattern = re.compile(r"(https?://\S+)")
    return url_pattern.sub(r'<a href="\1" target="_blank" style="color:#60a5fa;">\1</a>', html.escape(text))

def fetch_radar():
    pool, seen = [], set()
    try:
        url = f"https://newsapi.org/v2/everything?q=Venezuela&sortBy=publishedAt&language=es&apiKey={NEWS_API_KEY}"
        res = requests.get(url).json()
        if res.get("articles"):
            for art in res["articles"][:20]:
                if art["title"] not in seen:
                    dt = datetime.strptime(art["publishedAt"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    pool.append({"source": art["source"]["name"], "title": art["title"], "link": art["url"], "sort": dt.timestamp(), "time": dt.strftime('%H:%M')})
                    seen.add(art["title"])
    except: pass
    return sorted(pool, key=lambda x: x["sort"], reverse=True)

# --- 4. AUTOREFRESH ---
st_autorefresh(interval=60 * 1000, key="war_room_refresher")

# --- 5. INTERFAZ ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL (.M3U8 HLS)</div>', unsafe_allow_html=True)
    
    # SEÑAL ABC NEWS LIVE (Formato .m3u8 nativo - No se bloquea como YouTube)
    m3u8_url = "https://content.uplynk.com/channel/3324f2467c494ef3bca755583620992b.m3u8"
    
    components.html(f"""
        <html>
            <head><link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" /></head>
            <body style="margin:0; background:black;">
                <video id="v-room" class="video-js vjs-fluid vjs-big-play-centered" controls autoplay muted preload="auto">
                    <source src="{m3u8_url}" type="application/x-mpegURL">
                </video>
                <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
            </body>
        </html>
    """, height=360)
    
    st.markdown('<div class="header-col" style="margin-top:20px;">📰 RADAR DE NOTICIAS</div>', unsafe_allow_html=True)
    for n in fetch_radar():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 FEED DE INTELIGENCIA X</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=15&tweet.fields=created_at"
        res_x = requests.get(url_x, headers=headers).json()
        
        if 'data' in res_x:
            for t in res_x['data']:
                created = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                diff = datetime.now(timezone.utc) - created
                mins = max(0, int(diff.total_seconds() / 60))
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid #1d9bf0;">
                    <span class="time-badge" style="background:#1d9bf0;">HACE {mins}M</span>
                    <div class="source-tag">REPORTE X</div>
                    <div style="font-size:1rem; margin-top:8px;">{linkify(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Sin datos de X. Revisa cuota de la API.")
    except:
        st.error("Fallo de conexión con X.")

st.toast("Sincronización completa", icon="🛡️")
