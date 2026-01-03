import streamlit as st
import requests
import feedparser
import time
from datetime import datetime, timezone
import html
import re
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

# Carga silenciosa de llaves
X_TOKEN = st.secrets.get("X_TOKEN", "")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")

# --- 2. ESTILO VISUAL (Limpiado sin Sidebar) ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; font-family:'Roboto', sans-serif; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:12px; margin-bottom:10px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; background: #1a1a10; }
    .source-tag { font-size:0.7rem; color:#9ca3af; text-transform:uppercase; font-weight:900; letter-spacing: 1px; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; display:block; margin-top:5px; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; font-weight:bold; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    .stMainBlockContainer { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-20px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {datetime.now().strftime("%H:%M:%S")}</h1>', unsafe_allow_html=True)

# --- 3. FUNCIONES ---
def linkify(text):
    url_pattern = re.compile(r"(https?://\S+)")
    return url_pattern.sub(r'<a href="\1" target="_blank" style="color:#60a5fa;">\1</a>', html.escape(text))

def fetch_news():
    pool, seen = [], set()
    try:
        url = f"https://newsapi.org/v2/everything?q=Venezuela&sortBy=publishedAt&language=es&apiKey={NEWS_API_KEY}"
        res = requests.get(url).json()
        if res.get("articles"):
            for art in res["articles"][:15]:
                if art["title"] not in seen:
                    dt = datetime.strptime(art["publishedAt"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    pool.append({"source": art["source"]["name"], "title": art["title"], "link": art["url"], "sort": dt.timestamp(), "time": dt.strftime('%H:%M')})
                    seen.add(art["title"])
    except: pass
    return sorted(pool, key=lambda x: x["sort"], reverse=True)

# --- 4. ACTUALIZACIÓN ---
st_autorefresh(interval=60 * 1000, key="war_room_refresher")

# --- 5. INTERFAZ ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL EN VIVO</div>', unsafe_allow_html=True)
    
    # Nuevo Reproductor Universal (HLS)
    m3u8_url = "https://content.uplynk.com/channel/3324f2467c494ef3bca755583620992b.m3u8"
    components.html(f"""
        <body style="margin:0; background:black;">
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            <video id="video" controls autoplay muted style="width:100%; height:350px; background:black;"></video>
            <script>
              var video = document.getElementById('video');
              var videoSrc = '{m3u8_url}';
              if (Hls.isSupported()) {{
                var hls = new Hls();
                hls.loadSource(videoSrc);
                hls.attachMedia(video);
              }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                video.src = videoSrc;
              }}
            </script>
        </body>
    """, height=355)
    
    st.markdown('<div class="header-col" style="margin-top:20px;">📰 RADAR DE NOTICIAS</div>', unsafe_allow_html=True)
    for n in fetch_news():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 FEED DE INTELIGENCIA X</div>', unsafe_allow_html=True)
    
    twitter_success = False
    if X_TOKEN:
        try:
            headers = {"Authorization": f"Bearer {X_TOKEN}"}
            url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=10&tweet.fields=created_at"
            res_x = requests.get(url_x, headers=headers).json()
            
            if 'data' in res_x:
                twitter_success = True
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
        except: pass

    # RESPALDO: Si la API falla, carga el Timeline público para no dejar la columna vacía
    if not twitter_success:
        st.info("🔄 API de X en límite. Cargando señal pública de respaldo...")
        components.html("""
            <a class="twitter-timeline" data-height="800" data-theme="dark" href="https://twitter.com/AlertaNews24?ref_src=twsrc%5Etfw"></a> 
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """, height=800)
