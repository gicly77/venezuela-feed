import streamlit as st
import requests
import feedparser
import time
import html
import streamlit.components.v1 as components

# --- 1. CARGA DE CREDENCIALES (SECRETS) ---
try:
    YT_KEY = st.secrets["YT_KEY"]
    X_TOKEN = st.secrets["X_TOKEN"]
except Exception:
    st.error("⚠️ ERROR: Configura YT_KEY y X_TOKEN en los Secrets de Streamlit.")
    st.stop()

st.set_page_config(page_title="GLOBAL RADAR: VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILO VISUAL "WAR ROOM" ---
st.markdown("""
<style>
    .stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter', sans-serif; }
    .card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; margin-bottom:10px; border-left: 3px solid #30363d; transition: 0.3s; }
    .card:hover { border-left-color: #58a6ff; background: #1c2128; }
    .venezuela-hit { border-left-color: #f1e05a; background: #1c1c15; }
    .source-tag { font-size:0.7rem; color:#8b949e; text-transform:uppercase; font-weight:bold; }
    .headline { color:#58a6ff; text-decoration:none; font-weight:600; font-size:1rem; display:block; margin-top:2px; }
    .time-badge { font-size:0.65rem; background:#238636; color:white; padding:2px 6px; border-radius:4px; float:right; }
    .header-col { border-bottom: 2px solid #30363d; padding-bottom:10px; margin-bottom:20px; color:#f0f6fc; font-weight:600; font-size:1.2rem; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ GLOBAL RADAR: VENEZUELA</h1>', unsafe_allow_html=True)

# --- 3. RADAR DE MEDIOS GLOBALES ---
MEDIOS = [
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("Associated Press (AP)", "https://apnews.com/hub/venezuela.rss"),
    ("AFP (Americas)", "https://www.france24.com/es/america-latina/rss"),
    ("White House", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("State Dept", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("CNN World", "http://rss.cnn.com/rss/edition_americas.rss"),
    ("The New York Times", "https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml"),
    ("BBC World", "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml"),
    ("Deutsche Welle (DW)", "https://rss.dw.com/rdf/rss-es-am-lat"),
    ("El País (España)", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada"),
    ("Infobae", "https://www.infobae.com/feeds/rss/"),
    ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
    ("El Pitazo", "https://elpitazo.net/feed/"),
    ("NTN24 (Latam)", "https://www.ntn24.com/noticias-venezuela/feed"),
    ("G1 (Brasil)", "https://g1.globo.com/rss/g1/mundo/"),
    ("El Tiempo (Colombia)", "https://www.eltiempo.com/rss/mundo_latinoamerica.xml")
]

def radar_search():
    pool = []
    seen_links = set()
    for nombre, url in MEDIOS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                content = (entry.title + " " + entry.get("summary", "")).lower()
                # Solo entradas que mencionen "venezuela"
                if "venezuela" in content and entry.link not in seen_links:
                    seen_links.add(entry.link)
                    pool.append({
                        "source": nombre,
                        "title": entry.title,
                        "link": entry.link,
                        "ts": entry.published_parsed if "published_parsed" in entry else time.gmtime()
                    })
        except:
            continue
    return sorted(pool, key=lambda x: x["ts"], reverse=True)[:30]

col1, col2 = st.columns([1, 1])

# --- COLUMNA 1: SEÑAL DE VIDEO Y NOTICIAS ---
with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL & VIDEO</div>', unsafe_allow_html=True)

    # Video en vivo de VPItv
    try:
        yt_url = f"https://www.googleapis.com/youtube/v3/search?key={YT_KEY}&channelId=UC_uH_S9X_Xqh6u_K6M9mB2Q&part=snippet,id&order=date&maxResults=1"
        video_id = requests.get(yt_url).json()['items'][0]['id']['videoId']
        st.video(f"https://www.youtube.com/watch?v={video_id}")
    except:
        st.info("Sincronizando señal de video...")

    # Noticias filtradas
    noticias = radar_search()
    if not noticias:
        st.info("Esperando menciones de 'Venezuela' en el radar internacional...")
    for n in noticias:
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{time.strftime('%H:%M', n['ts'])}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

# --- COLUMNA 2: X (TWITTER) EN TIEMPO REAL ---
with col2:
    st.markdown('<div class="header-col">🐦 SEÑAL X / TIEMPO REAL</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        q = "venezuela -is:retweet lang:es"
        url_x = f"https://api.twitter.com/2/tweets/search/recent?query={q}&max_results=15&tweet.fields=created_at"
        res_x = requests.get(url_x, headers=headers).json()

        if 'data' in res_x:
            for t in res_x['data']:
                st.markdown(f"""
                <div class="card" style="border-left-color: #1da1f2;">
                    <div class="source-tag">X INTELLIGENCE</div>
                    <div style="font-size:0.95rem; margin-top:5px; line-height:1.4;">{html.escape(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Buscando nuevas señales en X...")
    except:
        st.error("Señal de X temporalmente fuera de línea.")

# --- RECARGA AUTOMÁTICA CADA 3 MINUTOS ---
components.html("<script>setTimeout(function(){window.location.reload();}, 180000);</script>", height=0)
