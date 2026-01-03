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

# --- 2. DISEÑO "WAR MODE" ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; font-family:'Roboto', sans-serif; }
    .card { background:#10141b; border:1px solid #1f2937; border-radius:4px; padding:10px; margin-bottom:8px; }
    .venezuela-hit { border-left: 5px solid #ffcc00; background: #1a1a10; }
    .source-tag { font-size:0.7rem; color:#9ca3af; text-transform:uppercase; font-weight:900; }
    .headline { color:#60a5fa; text-decoration:none; font-weight:700; font-size:1.1rem; line-height:1.2; }
    .time-badge { font-size:0.75rem; background:#dc2626; color:white; padding:2px 6px; border-radius:3px; float:right; font-weight:bold; }
    .header-col { border-bottom: 3px solid #1f2937; padding-bottom:8px; margin-bottom:15px; color:#f9fafb; font-size:1.4rem; font-weight:800; text-transform: uppercase; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE NOTICIAS (ANTI-CACHÉ) ---
def get_news():
    feeds = [
        ("REUTERS", "https://www.reuters.com/world/americas/rss"),
        ("AP NEWS", "https://apnews.com/hub/venezuela.rss"),
        ("EL PAÍS", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada"),
        ("INFOBAE", "https://www.infobae.com/feeds/rss/"),
        ("EL PITAZO", "https://elpitazo.net/feed/"),
        ("EFECTO COCUYO", "https://efectococuyo.com/feed/")
    ]
    pool = []
    now_ts = int(time.time())
    for name, url in feeds:
        try:
            d = feedparser.parse(f"{url}?nocache={now_ts}")
            for entry in d.entries[:10]:
                if "venezuela" in (entry.title + entry.get("summary", "")).lower():
                    ts = entry.published_parsed if "published_parsed" in entry else time.gmtime()
                    pool.append({
                        "source": name,
                        "title": entry.title,
                        "link": entry.link,
                        "sort": time.mktime(ts),
                        "time": time.strftime('%H:%M', ts)
                    })
        except: continue
    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:30]

# --- 4. INTERFAZ ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="header-col">📡 SEÑAL GLOBAL Y VIDEO</div>', unsafe_allow_html=True)
    
    # VIDEO: Cambiamos a la señal estable de VPItv (link directo de YouTube)
    # Si el video no carga, es un problema de restricciones del navegador, pero este es el más estable.
    st.video("https://www.youtube.com/watch?v=UC_uH_S9X_Xqh6u_K6M9mB2Q")
    
    for n in get_news():
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (REAL-TIME)</div>', unsafe_allow_html=True)
    
    if st.button("🔄 REFRESCAR X"):
        try:
            headers = {"Authorization": f"Bearer {X_TOKEN}"}
            url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=15&tweet.fields=created_at"
            res = requests.get(url_x, headers=headers).json()
            
            if 'data' in res:
                for t in res['data']:
                    created = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                    diff = datetime.now(timezone.utc) - created
                    mins = int(diff.total_seconds() / 60)
                    st.markdown(f"""
                    <div class="card" style="border-left: 4px solid #1d9bf0;">
                        <span class="time-badge" style="background:#1d9bf0;">HACE {mins}m</span>
                        <div class="source-tag">X INTELLIGENCE</div>
                        <div style="font-size:1rem; margin-top:8px;">{html.escape(t['text'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("X no devolvió datos. Es posible que hayas llegado al límite de tu plan gratuito.")
        except:
            st.error("Error crítico de conexión con X.")
    else:
        st.info("Haz clic en el botón superior para cargar señales de X sin agotar tu cuota.")

# Recarga automática más lenta (90 seg) para proteger tu cuenta de X
components.html("<script>setTimeout(function(){ window.location.reload(); }, 90000);</script>", height=0)
