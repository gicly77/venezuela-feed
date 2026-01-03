import streamlit as st
import requests
import feedparser
import time
import html
import re
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WAR ROOM - MONITOR ESTRATÉGICO",
    layout="wide",
    page_icon="📡"
)

# Auto-refresh real cada 20s (sincronizado con barra de progreso)
components.html("""
<script>
if (window.__refreshTimer) { clearTimeout(window.__refreshTimer); }
window.__refreshTimer = setTimeout(() => { window.location.reload(); }, 20000);
</script>
""", height=0)

# ─────────────────────────────────────────────────────────────
# 2. ESTILOS PROFESIONALES WAR ROOM
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter',sans-serif; }

/* Barra de progreso 20s */
.loading-bar-bg { position:fixed; top:0; left:0; width:100%; height:4px; background:#161b22; z-index:9999; }
.loading-bar-fill { height:100%; background: linear-gradient(90deg, #58a6ff, #1f6feb); animation:progress 20s linear forwards; }
@keyframes progress { from {width:0%} to {width:100%} }

/* Cards de Noticias */
.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:.9rem; margin-bottom:.8rem; transition:transform .2s; }
.card:hover { transform:scale(1.01); }
.card-potus { border:2px solid #58a6ff; box-shadow:0 0 12px rgba(88,166,255,.3); }
.card-video { border-left:4px solid #a371f7; background:#1c1526; }

/* Textos */
.tag { font-size:.65rem; color:#8b949e; font-weight:700; text-transform:uppercase; }
.title { font-size:1rem; color:#f0f6fc; font-weight:600; line-height:1.3; text-decoration:none; display:block; margin-bottom:8px; }
.time-badge { font-size:.6rem; background:#238636; color:#fff; padding:1px 6px; border-radius:4px; float:right; }

/* Column headers */
.header-col { font-size:.85rem; color:#8b949e; text-transform:uppercase; letter-spacing:2px; border-bottom:1px solid #30363d; padding-bottom:8px; margin-bottom:15px; font-weight:600; }

/* Hide sidebar y menu */
[data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
<div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px;">WAR ROOM - Monitor de Eventos</h1>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 3. FUENTES DE FEED Y PALABRAS CLAVE
# ─────────────────────────────────────────────────────────────
SOURCES = [
    ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("AP News", "https://apnews.com/hub/venezuela.rss"),
    ("📹 YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
    ("📹 YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
    ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
    ("El Pitazo", "https://elpitazo.net/feed/"),
    ("Infobae", "https://www.infobae.com/feeds/rss/")
]

KEYWORDS = ["venezuela","maduro","caracas","miraflores","padrino","delcy","cabello","corina","edmundo","ataque","captura","sanciones","elecciones"]

# ─────────────────────────────────────────────────────────────
# 4. FUNCIONES DE EXTRACCIÓN DE FEED
# ─────────────────────────────────────────────────────────────
def fetch_entries(url):
    """Descarga feed con headers simulando navegador."""
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) WARROOM/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200: return []
        feed = feedparser.parse(resp.content)
        return [{"title": e.get("title",""), "link": e.get("link",""), "pub": e.get("published_parsed", e.get("updated_parsed"))} 
                for e in feed.entries]
    except:
        return []

def get_yt_id(url):
    m = re.search(r"(?:v=|/videos/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return m.group(1) if m else None

# ─────────────────────────────────────────────────────────────
# 5. AGREGADOR INTELIGENTE
# ─────────────────────────────────────────────────────────────
def collect_news():
    pool, seen = [], set()
    for source, url in SOURCES:
        for e in fetch_entries(url)[:10]:
            if not e["link"] or e["link"] in seen: continue
            text = e["title"].lower()
            score = sum(text.count(k) for k in KEYWORDS)
            is_official = "🏛️" in source
            if (is_official and score<1) or (not is_official and score<2): continue
            seen.add(e["link"])
            pool.append({
                "source": source,
                "title": html.escape(e["title"]),
                "link": e["link"],
                "timestamp": time.mktime(e["pub"]) if e["pub"] else time.time(),
                "time_str": time.strftime("%H:%M", e["pub"]) if e["pub"] else "--:--",
                "is_video": "📹" in source,
                "is_potus": "🏛️" in source
            })
    return sorted(pool, key=lambda x:x["timestamp"], reverse=True)[:25]

# ─────────────────────────────────────────────────────────────
# 6. LAYOUT WAR ROOM
# ─────────────────────────────────────────────────────────────
c1, c2 = st.columns([1,1])

with c1:
    st.markdown('<div class="header-col">📡 SEÑAL NOTICIAS & VIDEO</div>', unsafe_allow_html=True)
    news = collect_news()
    for n in news:
        cls = "card card-potus" if n["is_potus"] else ("card card-video" if n["is_video"] else "card")
        st.markdown(f'<div class="{cls}"><span class="tag">{n["source"]}</span><a class="title" href="{n["link"]}" target="_blank">{n["title"]}</a><span class="time-badge">{n["time_str"]}</span></div>', unsafe_allow_html=True)
        if n["is_video"]:
            vid = get_yt_id(n["link"])
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")

with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X</div>', unsafe_allow_html=True)
    components.html("""
        <a class="twitter-timeline" data-theme="dark" data-chrome="noheader nofooter noborders transparent"
        href="https://twitter.com/POTUS" data-height="1000"></a>
        <script async src="https://platform.twitter.com/widgets.js"></script>
    """, height=1000, scrolling=True)
