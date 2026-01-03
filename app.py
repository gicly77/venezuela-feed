import streamlit as st
import requests
import feedparser
import time
import html
import re
import streamlit.components.v1 as components

# --- 1. CREDENCIALES DE INTELIGENCIA ---
YT_KEY = "TU_YOUTUBE_API_KEY_AQUI"  # Sustituye por tu clave válida
X_TOKEN = "TU_X_BEARER_TOKEN_AQUI"  # Sustituye por tu token válido

st.set_page_config(page_title="WAR ROOM: VENEZUELA", layout="wide", page_icon="🛡️")

# --- 2. ESTILOS PROFESIONALES WAR ROOM ---
st.markdown("""
<style>
.stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter', sans-serif; }
.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:15px; margin-bottom:12px; }
.card-alert { border:2px solid #d73a49; box-shadow:0 0 12px rgba(215,58,73,.25); }
.card-potus { border:2px solid #58a6ff; }
.card-video { border-left:4px solid #a371f7; background:#1c1526; }
.source-tag { font-size:0.7rem; color:#8b949e; text-transform:uppercase; font-weight:bold; letter-spacing:1px; }
.headline { color:#58a6ff; text-decoration:none; font-weight:600; font-size:1.05rem; display:block; margin:5px 0; }
.time-badge { font-size:0.65rem; background:#238636; color:white; padding:2px 6px; border-radius:4px; }
.header-col { border-bottom: 2px solid #30363d; padding-bottom:10px; margin-bottom:20px; color:#f0f6fc; font-weight:600; font-size:1.2rem; }
[data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA</h1>', unsafe_allow_html=True)

# --- 3. FUENTES RSS Y KEYWORDS ---
SOURCES = [
    ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("AP News", "https://apnews.com/hub/venezuela.rss"),
    ("📹 VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
    ("📹 NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
    ("Infobae", "https://www.infobae.com/feeds/rss/"),
    ("Efecto Cocuyo", "https://efectococuyo.com/feed/")
]
KEYWORDS = ["venezuela", "maduro", "ataque", "attack", "strike", "explosion", "captura", "corina", "edmundo"]

# --- 4. FUNCIONES ---
def get_yt_id(url):
    m = re.search(r"(?:v=|/videos/|embed/|youtu.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    return m.group(1) if m else None

@st.cache_data(ttl=60)
def fetch_entries(url):
    try:
        f = feedparser.parse(url, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")
        return [{"title": e.get("title",""), "link": e.get("link",""), "pub": e.get("published_parsed", e.get("updated_parsed")), "summary": e.get("summary","")} for e in f.entries]
    except: return []

def collect_news():
    pool, seen = [], set()
    for source, url in SOURCES:
        is_priority = "🏛️" in source or "📹" in source
        for e in fetch_entries(url)[:10]:
            if not e["link"] or e["link"] in seen: continue
            text = (e["title"] + " " + e.get("summary","")).lower()
            relevant = any(k in text for k in KEYWORDS)
            if not is_priority and "venezuela" not in text: relevant = False
            if not relevant: continue
            seen.add(e["link"])
            ts = time.mktime(e["pub"]) if e["pub"] else time.time()
            pool.append({
                "source": source, "title": html.escape(e["title"]), "link": e["link"],
                "timestamp": ts, "time_str": time.strftime("%H:%M", e["pub"]) if e["pub"] else "--:--",
                "is_video": "📹" in source, "is_potus": "🏛️" in source,
                "alert": any(w in text for w in ["ataque","explosion","strike"])
            })
    return sorted(pool, key=lambda x: x["timestamp"], reverse=True)[:25]

# --- 5. INTERFAZ: DOS COLUMNAS ---
c1, c2 = st.columns([1,1])

with c1:
    st.markdown('<div class="header-col">📡 SEÑAL NOTICIAS & VIDEO</div>', unsafe_allow_html=True)
    items = collect_news()
    if not items:
        st.info("Sincronizando señal de inteligencia...")
    for n in items:
        cls = "card"
        if n["alert"]: cls += " card-alert"
        elif n["is_potus"]: cls += " card-potus"
        elif n["is_video"]: cls += " card-video"
        
        st.markdown(f'<div class="{cls}"><span class="source-tag">{n["source"]}</span><a class="headline" href="{n["link"]}" target="_blank">{n["title"]}</a><span class="time-badge">{n["time_str"]}</span></div>', unsafe_allow_html=True)
        if n["is_video"]:
            vid = get_yt_id(n["link"])
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")

    # --- Video en vivo adicional vía YouTube API ---
    try:
        yt_api_url = f"https://www.googleapis.com/youtube/v3/search?key={YT_KEY}&channelId=UC_uH_S9X_Xqh6u_K6M9mB2Q&part=snippet,id&order=date&maxResults=1"
        yt_res = requests.get(yt_api_url).json()
        video_id = yt_res['items'][0]['id']['videoId']
        st.video(f"https://www.youtube.com/watch?v={video_id}")
    except:
        st.info("Sincronizando señal de video en vivo...")

with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X / TIEMPO REAL</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        query = "venezuela (maduro OR edmundo OR urgencia OR 'última hora') -is:retweet lang:es"
        x_url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields=created_at&max_results=10"
        response = requests.get(x_url, headers=headers).json()
        if 'data' in response:
            for tweet in response['data']:
                txt = html.escape(tweet['text'])
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid #1da1f2;">
                    <div class="source-tag">X INTELLIGENCE</div>
                    <div style="font-size:0.95rem; color:#f0f6fc; line-height:1.4; margin-top:5px;">{txt}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Buscando nuevas señales en X...")
    except:
        st.warning("⚠️ Error en la conexión con X. Verifica tu token de API.")

# --- 6. REFRESCO AUTOMÁTICO ---
components.html("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", height=0)
