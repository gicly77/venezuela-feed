import streamlit as st
import feedparser
import time
import html
import re
import streamlit.components.v1 as components

# ───────────────────────────────
# 1. Configuración de la app
# ───────────────────────────────
st.set_page_config(
    page_title="WAR ROOM: VENEZUELA",
    layout="wide",
    page_icon="🛡️"
)

# Auto-refresh cada 20s
components.html("""
<script>
if (window.__refreshTimer) { clearTimeout(window.__refreshTimer); }
window.__refreshTimer = setTimeout(() => { window.location.reload(); }, 20000);
</script>
""", height=0)

# ───────────────────────────────
# 2. CSS Profesional WAR ROOM
# ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter',sans-serif; }

.loading-bar-bg { position:fixed; top:0; left:0; width:100%; height:4px; background:#161b22; z-index:9999; }
.loading-bar-fill { height:100%; background: linear-gradient(90deg, #58a6ff, #1f6feb); animation:progress 20s linear both; }
@keyframes progress { from { width:0% } to { width:100% } }

.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:.9rem; margin-bottom:.8rem; transition: transform .2s; }
.card:hover { transform: scale(1.01); }
.card-potus { border:2px solid #58a6ff; box-shadow:0 0 12px rgba(88,166,255,.15); background:#0d1117; }
.card-video { border-left:4px solid #a371f7; background:#1c1526; }

.tag { font-size:.65rem; color:#8b949e; font-weight:700; text-transform:uppercase; margin-bottom:4px; display:block; }
.title { font-size:1.05rem; color:#f0f6fc; font-weight:600; line-height:1.3; text-decoration:none; display:block; margin-bottom:8px; }
.time-badge { font-size:.6rem; background:#238636; color:#fff; padding:2px 6px; border-radius:4px; font-weight:bold; }

.header-col { font-size:.85rem; color:#8b949e; text-transform:uppercase; letter-spacing:2px; border-bottom:1px solid #30363d; padding-bottom:10px; margin-bottom:15px; font-weight:600; }
[data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
<div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px; letter-spacing:-1px;">WAR ROOM: VENEZUELA</h1>', unsafe_allow_html=True)

# ───────────────────────────────
# 3. Fuentes y palabras clave
# ───────────────────────────────
SOURCES = [
    ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("AP News", "https://apnews.com/hub/venezuela.rss"),
    ("BBC News", "http://feeds.bbci.co.uk/news/world/latin_america/rss.xml"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("📹 YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
    ("📹 YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
    ("Infobae", "https://www.infobae.com/feeds/rss/")
]

KEYWORDS = ["venezuela","maduro","attack","strike","explosion","capture","padrino","corina","edmundo","sanciones"]

# ───────────────────────────────
# 4. Funciones de recopilación
# ───────────────────────────────
@st.cache_data(ttl=60)
def fetch_entries(url):
    try:
        f = feedparser.parse(url, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")
        return [{"title": e.get("title",""), "link": e.get("link",""), "pub": e.get("published_parsed", e.get("updated_parsed")), "summary": e.get("summary","")} for e in f.entries]
    except:
        return []

def get_yt_id(url):
    m = re.search(r"(?:v=|/videos/|embed/|youtu.be/)([a-zA-Z0-9_-]{11})", url)
    return m.group(1) if m else None

def collect_news():
    pool, seen = [], set()
    for source, url in SOURCES:
        is_official = "🏛️" in source
        for e in fetch_entries(url)[:12]:
            if not e["link"] or e["link"] in seen:
                continue
            text_to_scan = (e["title"] + " " + e.get("summary","")).lower()
            relevant = any(k in text_to_scan for k in KEYWORDS)
            if not is_official and "venezuela" not in text_to_scan:
                relevant = False
            if not relevant:
                continue
            seen.add(e["link"])
            ts = time.mktime(e["pub"]) if e["pub"] else time.time()
            pool.append({
                "source": source,
                "title": html.escape(e["title"]),
                "link": e["link"],
                "timestamp": ts,
                "time_str": time.strftime("%H:%M", e["pub"]) if e["pub"] else "--:--",
                "is_video": "📹" in source,
                "is_potus": is_official
            })
    return sorted(pool, key=lambda x: x["timestamp"], reverse=True)[:25]

# ───────────────────────────────
# 5. Renderizado profesional
# ───────────────────────────────
c1, c2 = st.columns([1,1])

# Columna 1: Noticias y Videos
with c1:
    st.markdown('<div class="header-col">📡 SEÑAL NOTICIAS & VIDEO</div>', unsafe_allow_html=True)
    items = collect_news()
    if not items:
        st.info("Buscando actualizaciones de inteligencia...")
    for n in items:
        cls = "card card-potus" if n["is_potus"] else ("card card-video" if n["is_video"] else "card")
        st.markdown(f'''
            <div class="{cls}">
                <span class="tag">{n["source"]}</span>
                <a class="title" href="{n["link"]}" target="_blank">{n["title"]}</a>
                <span class="time-badge">{n["time_str"]}</span>
            </div>
        ''', unsafe_allow_html=True)
        if n["is_video"]:
            vid = get_yt_id(n["link"])
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")

# Columna 2: Twitter/X en tiempo real
with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X / TIEMPO REAL</div>', unsafe_allow_html=True)
    components.html("""
        <a class="twitter-timeline" data-theme="dark" data-chrome="noheader nofooter noborders transparent"
        href="https://twitter.com/search?q=venezuela%20OR%20maduro%20lang%3Aes%20f%3Dlive" data-height="1000"></a>
        <script async src="https://platform.twitter.com/widgets.js"></script>
    """, height=1000, scrolling=True)
