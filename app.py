import streamlit as st
import feedparser
import time
import html
import re
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN
st.set_page_config(page_title="WAR ROOM: VENEZUELA", layout="wide", page_icon="🛡️")

# Auto-refresh 20s
components.html("""
<script>
if (window.__refreshTimer) { clearTimeout(window.__refreshTimer); }
window.__refreshTimer = setTimeout(() => { window.location.reload(); }, 20000);
</script>
""", height=0)

# 2. ESTILOS WAR ROOM
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
.stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter',sans-serif; }
.loading-bar-bg { position:fixed; top:0; left:0; width:100%; height:4px; background:#161b22; z-index:9999; }
.loading-bar-fill { height:100%; background: linear-gradient(90deg, #58a6ff, #1f6feb); animation:progress 20s linear forwards; }
@keyframes progress { from { width:0% } to { width:100% } }
.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:.9rem; margin-bottom:.8rem; }
.card-alert { border:2px solid #d73a49; box-shadow:0 0 12px rgba(215,58,73,.25); }
.card-potus { border:2px solid #58a6ff; }
.card-video { border-left:4px solid #a371f7; background:#1c1526; }
.tag { font-size:.65rem; color:#8b949e; font-weight:700; text-transform:uppercase; margin-bottom:4px; display:block;}
.title { font-size:1rem; color:#f0f6fc; font-weight:600; text-decoration:none; display:block; margin-bottom:5px; }
.time-badge { font-size:.6rem; background:#238636; color:#fff; padding:2px 6px; border-radius:4px; font-weight:bold;}
.header-col { font-size:.85rem; color:#8b949e; text-transform:uppercase; letter-spacing:2px; border-bottom:1px solid #30363d; padding-bottom:10px; margin-bottom:15px; font-weight:600; }
[data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
<div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px; letter-spacing:-1px;">WAR ROOM: VENEZUELA</h1>', unsafe_allow_html=True)

# 3. FUENTES
SOURCES = [
    ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
    ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
    ("Reuters", "https://www.reuters.com/world/americas/rss"),
    ("📹 VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"),
    ("📹 NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
    ("Infobae", "https://www.infobae.com/feeds/rss/"),
    ("Efecto Cocuyo", "https://efectococuyo.com/feed/")
]
KEYWORDS = ["venezuela", "maduro", "ataque", "attack", "strike", "explosion", "captura", "corina", "edmundo"]

# 4. FUNCIONES
def get_yt_id(url):
    m = re.search(r"(?:v=|/videos/|embed/|youtu.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    return m.group(1) if m else None

@st.cache_data(ttl=60)
def fetch_entries(url):
    try:
        # User-Agent real para evitar bloqueos de feeds
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
    return sorted(pool, key=lambda x: x["timestamp"], reverse=True)[:20]

# 5. RENDERIZADO
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
        
        st.markdown(f'<div class="{cls}"><span class="tag">{n["source"]}</span><a class="title" href="{n["link"]}" target="_blank">{n["title"]}</a><span class="time-badge">{n["time_str"]}</span></div>', unsafe_allow_html=True)
        if n["is_video"]:
            vid = get_yt_id(n["link"])
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")

with c2:
    st.markdown('<div class="header-col">🐦 SEÑAL X / TIEMPO REAL</div>', unsafe_allow_html=True)
    # Cambiado a perfil oficial de VPItv para máxima compatibilidad de carga
    x_widget = """
    <div style="height:1000px; overflow-y:auto;">
        <a class="twitter-timeline" data-theme="dark" href="https://twitter.com/VPItv?ref_src=twsrc%5Etfw"></a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>
    """
    components.html(x_widget, height=1000)
