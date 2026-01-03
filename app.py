import streamlit as st
import requests
import feedparser
import time
from datetime import datetime
import html
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN Y CREDENCIALES ---
st.set_page_config(page_title="WAR ROOM: VENEZUELA", layout="wide", page_icon="🛡️")

try:
    X_TOKEN = st.secrets["X_TOKEN"]
except Exception:
    st.error("⚠️ ERROR: Configura el X_TOKEN en los Secrets de Streamlit.")
    st.stop()

# --- 2. ESTILO VISUAL (DARK COMMAND CENTER) ---
st.markdown("""
<style>
    .stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter', sans-serif; }
    .card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; margin-bottom:10px; border-left: 3px solid #30363d; }
    .venezuela-hit { border-left-color: #f1e05a; background: #1c1c15; }
    .source-tag { font-size:0.7rem; color:#8b949e; text-transform:uppercase; font-weight:bold; }
    .headline { color:#58a6ff; text-decoration:none; font-weight:600; font-size:1rem; display:block; margin-top:2px; }
    .time-badge { font-size:0.7rem; background:#238636; color:white; padding:2px 6px; border-radius:4px; float:right; font-weight:bold; }
    .header-col { border-bottom: 2px solid #30363d; padding-bottom:10px; margin-bottom:20px; color:#f0f6fc; font-weight:600; font-size:1.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA</h1>', unsafe_allow_html=True)

# --- 3. FUNCIONES DE EXTRACCIÓN ---
def get_latest_video():
    """Obtiene el video más reciente vía RSS"""
    try:
        yt_rss = "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q"
        feed = feedparser.parse(yt_rss)
        if feed.entries:
            return feed.entries[0].link
    except:
        return None

@st.cache_data(ttl=60) # Actualiza los medios cada 60 segundos
def radar_search():
    medios = [
        ("Reuters", "https://www.reuters.com/world/americas/rss"),
        ("Associated Press", "https://apnews.com/hub/venezuela.rss"),
        ("AFP", "https://www.france24.com/es/america-latina/rss"),
        ("State Dept", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("CNN Latam", "http://rss.cnn.com/rss/edition_americas.rss"),
        ("BBC Mundo", "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml"),
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada"),
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/")
    ]
    pool, seen = [], set()
    for nombre, url in medios:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:8]:
                text = (e.title + " " + e.get("summary", "")).lower()
                if "venezuela" in text and e.link not in seen:
                    seen.add(e.link)
                    ts = e.published_parsed if "published_parsed" in e else time.gmtime()
                    pool.append({"source": nombre, "title": e.title, "link": e.link, "ts": ts, "sort": time.mktime(ts)})
        except: continue
    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:30]

# --- 4. INTERFAZ EN COLUMNAS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL & VIDEO</div>', unsafe_allow_html=True)
    
    # VIDEO: Intento con st.video, si falla, nada.
    video_url = get_latest_video()
    if video_url:
        st.video(video_url)
        st.caption("🔴 ÚLTIMA SEÑAL DISPONIBLE: VPItv")
    else:
        st.info("Buscando señal de video activa...")

    # NOTICIAS RSS
    for n in radar_search():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{time.strftime('%H:%M', n['ts'])}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 SEÑAL X / TIEMPO REAL</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=15&tweet.fields=created_at"
        res_x = requests.get(url_x, headers=headers).json()
        
        if 'data' in res_x:
            for t in res_x['data']:
                dt = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z')
                hora = dt.strftime('%H:%M')
                st.markdown(f"""
                <div class="card" style="border-left-color: #1da1f2;">
                    <span class="time-badge" style="background:#1da1f2;">{hora}</span>
                    <div class="source-tag">X INTELLIGENCE</div>
                    <div style="font-size:0.95rem; margin-top:5px; line-height:1.4;">{html.escape(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron tweets recientes o la API no devolvió datos.")
    except Exception as e:
        st.error("Señal de X en espera (Límite de cuota alcanzado).")

# Recarga automática de la página cada 60 segundos
components.html("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", height=0)
