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

# Carga de credenciales desde Secrets
try:
    X_TOKEN = st.secrets["X_TOKEN"]
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"] # Asegúrate de añadir esta en Settings > Secrets
except Exception:
    st.error("⚠️ ERROR: Configura X_TOKEN y NEWS_API_KEY en los Secrets de Streamlit.")
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
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:20px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

# Reloj maestro para verificar sincronización
ahora_server = datetime.now().strftime('%H:%M:%S')
st.markdown(f'<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA | LIVE: {ahora_server}</h1>', unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS HÍBRIDO (API + RSS) ---
def fetch_news():
    pool = []
    seen_titles = set()

    # A. INTENTO CON NEWSAPI (MÁXIMA PRECISIÓN)
    try:
        # Filtro Pro: Venezuela AND (Trump OR Maduro OR Ataque OR EE.UU.)
        q = "Venezuela AND (Trump OR Maduro OR Ataque OR USA)"
        url = f"https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&language=es&apiKey={NEWS_API_KEY}"
        res = requests.get(url).json()
        
        if res.get("status") == "ok":
            for art in res.get("articles", [])[:20]:
                title = art["title"]
                if title not in seen_titles:
                    dt = datetime.strptime(art["publishedAt"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    pool.append({
                        "source": f"⭐ {art['source']['name']}",
                        "title": title,
                        "link": art["url"],
                        "sort": dt.timestamp(),
                        "time": dt.strftime('%H:%M')
                    })
                    seen_titles.add(title)
    except:
        pass # Si falla la API, el pool queda vacío y pasamos al RSS

    # B. RESPALDO CON RSS (SIEMPRE DISPONIBLE)
    if len(pool) < 5:
        medios_rss = [
            ("Reuters", "https://www.reuters.com/world/americas/rss"),
            ("Fox News", "https://feeds.foxnews.com/foxnews/world"),
            ("AP News", "https://apnews.com/hub/venezuela.rss")
        ]
        for nombre, url in medios_rss:
            try:
                f = feedparser.parse(f"{url}?t={int(time.time())}")
                for e in f.entries[:5]:
                    if "venezuela" in e.title.lower() and e.title not in seen_titles:
                        ts = e.published_parsed if "published_parsed" in e else time.gmtime()
                        pool.append({
                            "source": nombre,
                            "title": e.title,
                            "link": e.link,
                            "sort": time.mktime(ts),
                            "time": time.strftime('%H:%M', ts)
                        })
                        seen_titles.add(e.title)
            except: continue

    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:30]

# --- 4. ACTUALIZACIÓN AUTOMÁTICA ---
st_autorefresh(interval=60 * 1000, key="war_room_refresher")

# --- 5. INTERFAZ EN COLUMNAS ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL & VIDEO</div>', unsafe_allow_html=True)
    
    # REPRODUCTOR FOX NEWS (AUTOPLAY)
    components.html("""
        <div style="background:#000; width:100%; height:350px; border-radius:8px; overflow:hidden;">
            <iframe width="100%" height="350" 
            src="https://www.youtube.com/embed/live_stream?channel=UCXIJgGwMWgu497gsyqW2mYw&autoplay=1&mute=1&controls=1" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """, height=355)
    
    # RENDER DE NOTICIAS
    for n in fetch_news():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
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
                created = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                diff = datetime.now(timezone.utc) - created
                mins = max(0, int(diff.total_seconds() / 60))
                
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid #1d9bf0;">
                    <span class="time-badge" style="background:#1d9bf0;">HACE {mins}M</span>
                    <div class="source-tag">INTELIGENCIA X</div>
                    <div style="font-size:1rem; margin-top:8px;">{html.escape(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.error("Señal X en espera...")
