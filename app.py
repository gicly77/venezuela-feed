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

# Carga de credenciales
try:
    X_TOKEN = st.secrets["X_TOKEN"]
except Exception:
    st.error("⚠️ ERROR: Configura el X_TOKEN en los Secrets de Streamlit.")
    st.stop()

# --- 2. ESTILO VISUAL COMANDO CENTRAL ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; font-family:'Roboto', sans-serif; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:12px; margin-bottom:10px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; background: #1a1a10; }
    .source-tag { font-size:0.7rem; color:#9ca3af; text-transform:uppercase; font-weight:900; letter-spacing: 1px; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; display:block; margin-top:5px; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 8px; border-radius:3px; float:right; font-weight:bold; }
    .x-badge { background:#1d9bf0; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA (LIVE)</h1>', unsafe_allow_html=True)

# --- 3. FUNCIONES DE FETCH (ANTI-CACHÉ AGRESIVO) ---
def fetch_radar():
    medios = [
        ("Reuters", "https://www.reuters.com/world/americas/rss"),
        ("Fox News", "https://feeds.foxnews.com/foxnews/world"),
        ("AP News", "https://apnews.com/hub/venezuela.rss"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/")
    ]
    pool, seen = [], set()
    now = int(time.time())
    for nombre, url in medios:
        try:
            f = feedparser.parse(f"{url}?update={now}")
            for e in f.entries[:7]: 
                text = (e.title + " " + e.get("summary", "")).lower()
                if "venezuela" in text and e.link not in seen:
                    seen.add(e.link)
                    ts = e.published_parsed if "published_parsed" in e else time.gmtime()
                    pool.append({
                        "source": nombre,
                        "title": e.title,
                        "link": e.link,
                        "sort": time.mktime(ts),
                        "time": time.strftime('%H:%M', ts)
                    })
        except: continue
    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:30]

# --- 4. UTILIDADES DE TEXTO ---
def linkify(text):
    url_pattern = re.compile(r"(https?://\S+)")
    return url_pattern.sub(r'<a href="\1" target="_blank" style="color:#60a5fa;">\1</a>', html.escape(text))

# --- 5. ACTUALIZACIÓN AUTOMÁTICA (60 SEGUNDOS) ---
st_autorefresh(interval=60 * 1000, key="war_room_refresher")

# --- 6. DISEÑO DE INTERFAZ ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 FOX NEWS LIVE & GLOBAL RADAR</div>', unsafe_allow_html=True)
    
    # VIDEO: Fox News (Autoplay + Mute)
    fox_id = "UCXIJgGwMWgu497gsyqW2mYw"
    components.html(f"""
        <div style="background:#000; width:100%; height:350px; border-radius:8px; overflow:hidden;">
            <iframe width="100%" height="350" 
            src="https://www.youtube.com/embed/live_stream?channel={fox_id}&autoplay=1&mute=1&controls=1&rel=0" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """, height=355)
    
    for n in fetch_radar():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (REAL-TIME)</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=15&tweet.fields=created_at"
        res = requests.get(url_x, headers=headers).json()
        
        if 'data' in res:
            for t in res['data']:
                created = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                diff = datetime.now(timezone.utc) - created
                mins = max(0, int(diff.total_seconds() / 60))
                
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid #1d9bf0;">
                    <span class="time-badge x-badge">HACE {mins}M</span>
                    <div class="source-tag">REPORTE X</div>
                    <div style="font-size:1rem; margin-top:8px; line-height:1.4;">{linkify(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.error("Error de conexión con la señal de X.")

st.toast("Radar sincronizado", icon="📡")
