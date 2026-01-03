import streamlit as st
import feedparser
import time
import html
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MONITOR ESTRATÉGICO",
    layout="wide",
    page_icon="📡"
)

# Auto-refresh limpio cada 30s (SIN DEPENDENCIAS)
components.html(
    "<meta http-equiv='refresh' content='30'>",
    height=0
)

# ─────────────────────────────────────────────────────────────
# 2. ESTILOS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
.stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter',sans-serif; }

.loading-bar-bg { position:fixed; top:0; left:0; width:100%; height:3px; background:#161b22; z-index:9999; }
.loading-bar-fill { height:100%; background:#58a6ff; animation:progress 30s linear infinite; }
@keyframes progress { from{width:0%} to{width:100%} }

.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:0.9rem; margin-bottom:0.8rem; }
.card-potus { border:2px solid #58a6ff; box-shadow:0 0 12px rgba(88,166,255,.2); }
.card-video { border-left:4px solid #a371f7; }

.tag { font-size:.65rem; color:#8b949e; font-weight:700; text-transform:uppercase; }
.title { font-size:1rem; color:#f0f6fc; font-weight:600; line-height:1.3; text-decoration:none; }
.time-badge { font-size:.6rem; background:#238636; color:#fff; padding:1px 6px; border-radius:4px; }

.header-col { font-size:.85rem; color:#8b949e; text-transform:uppercase;
letter-spacing:2px; border-bottom:1px solid #30363d; padding-bottom:8px;
margin-bottom:15px; font-weight:600; }

[data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>

<div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
""", unsafe_allow_html=True)

st.markdown('<h1 style="margin-top:-40px">Monitor de Eventos</h1>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 3. FUENTES
# ─────────────────────────────────────────────────────────────
SOURCES = [
    ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("AP News", "https://apnews.com/hub/venezuela.rss"),
    ("El Mundo", "https://www.elmundo.es/rss/internacional.xml"),
    ("📹 YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
    ("📹 YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
    ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
    ("El Pitazo", "https://elpitazo.net/feed/"),
    ("Infobae", "https://www.infobae.com/feeds/rss/")
]

KEYWORDS = [
    "venezuela","maduro","caracas","miraflores","padrino",
    "delcy","cabello","corina","edmundo","ataque",
    "captura","sanciones","elecciones"
]

# ─────────────────────────────────────────────────────────────
# 4. CACHE FEEDS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_feed(url):
    return feedparser.parse(
        url,
        agent="Mozilla/5.0 StrategicMonitor/1.0"
    )

# ─────────────────────────────────────────────────────────────
# 5. AGREGADOR ROBUSTO
# ─────────────────────────────────────────────────────────────
def collect_news():
    pool = []
    seen = set()

    for source, url in SOURCES:
        feed = fetch_feed(url)

        for e in feed.entries[:12]:
            if not hasattr(e, "link") or e.link in seen:
                continue

            text = (e.get("title","") + " " + e.get("summary","")).lower()
            score = sum(text.count(k) for k in KEYWORDS)
            if score < 2:
                continue

            pub = e.get("published_parsed") or e.get("updated_parsed")
            if not pub:
                continue

            seen.add(e.link)

            pool.append({
                "source": source,
                "title": html.escape(e.title),
                "link": e.link,
                "timestamp": time.mktime(pub),
                "time_str": time.strftime("%H:%M", pub),
                "is_video": "📹" in source,
                "is_potus": "🏛️" in source,
                "score": score
            })

    pool.sort(key=lambda x: (x["timestamp"], x["score"]), reverse=True)
    return pool[:25]

# ─────────────────────────────────────────────────────────────
# 6. RENDER
# ─────────────────────────────────────────────────────────────
def render_news(items):
    for n in items:
        cls = "card"
        if n["is_potus"]:
            cls += " card-potus"
        elif n["is_video"]:
            cls += " card-video"

        st.markdown(f"""
        <div class="{cls}">
            <span class="tag">{n['source']}</span>
            <a class="title" href="{n['link']}" target="_blank">{n['title']}</a>
            <div style="margin-top:6px">
                <span class="time-badge">{n['time_str']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 7. LAYOUT
# ─────────────────────────────────────────────────────────────
c1, c2 = st.columns([1,1])

with c1:
    st.markdown('<div class="header-col">📡 SEÑAL NOTICIAS & VIDEO</div>', unsafe_allow_html=True)
    render_news(collect_news())

with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X</div>', unsafe_allow_html=True)
    components.html("""
        <a class="twitter-timeline"
           data-theme="dark"
           data-chrome="noheader nofooter noborders transparent"
           href="https://twitter.com/POTUS"
           data-height="1000"></a>
        <script async src="https://platform.twitter.com/widgets.js"></script>
    """, height=1200, scrolling=True)
