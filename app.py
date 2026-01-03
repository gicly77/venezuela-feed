import streamlit as st
import requests
import feedparser
import time
from datetime import datetime, timezone
import html
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN DE EMERGENCIA ---
st.set_page_config(page_title="WAR ROOM VENEZUELA", layout="wide", page_icon="🛡️")

try:
    X_TOKEN = st.secrets["X_TOKEN"]
except Exception:
    st.error("⚠️ ERROR: No hay X_TOKEN en los Secrets.")
    st.stop()

# --- 2. DISEÑO DE ALTA VISIBILIDAD (WAR MODE) ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; font-family:'Roboto', sans-serif; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:10px; margin-bottom:8px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; background: #1a1a10; }
    .source-tag { font-size:0.7rem; color:#9ca3af; text-transform:uppercase; font-weight:900; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; line-height:1.2; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 6px; border-radius:3px; float:right; font-weight:bold; }
    .x-badge { background:#1d9bf0; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:15px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (ANTI-CACHÉ AGRESIVO) ---
def get_news():
    feeds = [
        ("REUTERS", "https://www.reuters.com/world/americas/rss"),
        ("AP NEWS", "https://apnews.com/hub/venezuela.rss"),
        ("AFP", "https://www.france24.com/es/america-latina/rss"),
        ("EL PAÍS", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada"),
        ("INFOBAE", "https://www.infobae.com/feeds/rss/"),
        ("EL PITAZO", "https://elpitazo.net/feed/"),
        ("EFECTO COCUYO", "https://efectococuyo.com/feed/")
    ]
    pool = []
    # Usamos el timestamp para obligar al servidor a darnos datos nuevos
    now_ts = int(time.time())
    for name, url in feeds:
        try:
            # Forzamos la descarga sin usar caché del servidor
            d = feedparser.parse(f"{url}?nocache={now_ts}")
            for entry in d.entries[:12]:
                title = entry.title
                summary = entry.get("summary", "")
                if "venezuela" in (title + summary).lower():
                    # Priorizamos el tiempo de publicación real
                    ts = entry.published_parsed if "published_parsed" in entry else time.gmtime()
                    pool.append({
                        "source": name,
                        "title": title,
                        "link": entry.link,
                        "sort": time.mktime(ts),
                        "time": time.strftime('%H:%M', ts)
                    })
        except: continue
    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:40]

# --- 4. PANEL DE CONTROL ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL EN VIVO Y NOTICIAS</div>', unsafe_allow_html=True)
    
    # VIDEO: Sistema de triple fallback (En vivo -> Canal -> Fallback)
    # Si el video de arriba no sale, este es un embed directo del streaming de VPItv
    components.html("""
        <div style="background:#000; width:100%; height:350px;">
            <iframe width="100%" height="350" src="https://www.youtube.com/embed/live_stream?channel=UC_uH_S9X_Xqh6u_K6M9mB2Q&autoplay=1&mute=1" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """, height=355)

    # RENDER DE NOTICIAS
    for n in get_news():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (MINUTO A MINUTO)</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        # Búsqueda ultra-reciente
        url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=20&tweet.fields=created_at"
        res = requests.get(url_x, headers=headers).json()
        
        if 'data' in res:
            for t in res['data']:
                # Cálculo de tiempo relativo exacto
                created = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                diff = datetime.now(timezone.utc) - created
                mins = int(diff.total_seconds() / 60)
                time_str = f"{mins}m" if mins < 60 else created.strftime('%H:%M')
                
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid #1d9bf0;">
                    <span class="time-badge x-badge">HACE {time_str}</span>
                    <div class="source-tag">REPORTE EN TIEMPO REAL</div>
                    <div style="font-size:1rem; margin-top:8px; font-weight:500;">{html.escape(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Error de conexión con X (API Down)")
    except:
        st.error("🚨 Límite de cuota de X alcanzado.")

# --- 5. RECARGA AUTOMÁTICA (CADA 30 SEGUNDOS) ---
components.html("""
    <script>
    setTimeout(function(){ window.location.reload(); }, 30000);
    </script>
""", height=0)
