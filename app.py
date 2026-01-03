import streamlit as st
import requests
import feedparser
import time
from datetime import datetime, timezone
import html
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN E INTELIGENCIA ---
st.set_page_config(page_title="WAR ROOM: VENEZUELA", layout="wide", page_icon="🛡️")

# Intentamos cargar el token, si no, avisamos claramente
try:
    X_TOKEN = st.secrets["X_TOKEN"]
except Exception:
    st.error("⚠️ ERROR: No se detecta X_TOKEN en los Secrets de Streamlit.")
    st.stop()

# --- 2. ESTILO VISUAL COMANDO CENTRAL ---
st.markdown("""
<style>
    .stApp { background:#0d1117; color:#c9d1d9; font-family:'Inter', sans-serif; }
    .card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; margin-bottom:10px; border-left: 3px solid #30363d; }
    .venezuela-hit { border-left-color: #f1e05a; background: #1c1c15; border-left-width: 5px; }
    .source-tag { font-size:0.7rem; color:#8b949e; text-transform:uppercase; font-weight:bold; }
    .headline { color:#58a6ff; text-decoration:none; font-weight:600; font-size:1.05rem; display:block; margin-top:2px; }
    .time-badge { font-size:0.75rem; background:#238636; color:white; padding:3px 8px; border-radius:4px; float:right; font-weight:bold; }
    .x-badge { background:#1da1f2; }
    .header-col { border-bottom: 2px solid #30363d; padding-bottom:10px; margin-bottom:20px; color:#f0f6fc; font-weight:bold; font-size:1.3rem; }
    [data-testid="stSidebar"], #MainMenu, footer, header { display:none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; margin-top:-40px; letter-spacing:-1px;">🛡️ WAR ROOM: VENEZUELA</h1>', unsafe_allow_html=True)

# --- 3. FUNCIONES DE CARGA EN VIVO ---
def radar_global():
    # Forzamos una semilla de tiempo para evitar que RSS use noticias viejas
    medios = [
        ("Reuters", "https://www.reuters.com/world/americas/rss"),
        ("Associated Press", "https://apnews.com/hub/venezuela.rss"),
        ("AFP", "https://www.france24.com/es/america-latina/rss"),
        ("CNN Mundo", "http://rss.cnn.com/rss/edition_americas.rss"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("BBC", "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml")
    ]
    pool, seen = [], set()
    for nombre, url in medios:
        try:
            # Añadimos un parámetro aleatorio al URL para engañar a los servidores y obtener lo último
            f = feedparser.parse(f"{url}?t={int(time.time())}")
            for e in f.entries[:10]:
                content = (e.title + " " + e.get("summary", "")).lower()
                if "venezuela" in content and e.link not in seen:
                    seen.add(e.link)
                    ts = e.published_parsed if "published_parsed" in e else time.gmtime()
                    pool.append({"source": nombre, "title": e.title, "link": e.link, "sort": time.mktime(ts), "time": time.strftime('%H:%M', ts)})
        except: continue
    return sorted(pool, key=lambda x: x["sort"], reverse=True)[:30]

# --- 4. INTERFAZ DE MONITOREO ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="header-col">📡 NOTICIAS & VIDEO EN VIVO</div>', unsafe_allow_html=True)
    
    # VIDEO: Cargador de respaldo directo para VPItv
    # Usamos un iframe directo que suele ser más estable que st.video en servidores cloud
    components.html("""
        <iframe width="100%" height="315" src="https://www.youtube.com/embed/live_stream?channel=UC_uH_S9X_Xqh6u_K6M9mB2Q" 
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """, height=315)
    
    # LISTA DE NOTICIAS
    noticias = radar_global()
    for n in noticias:
        st.markdown(f"""
        <div class="card venezuela-hit">
            <span class="time-badge">{n['time']}</span>
            <div class="source-tag">{n['source']}</div>
            <a class="headline" href="{n['link']}" target="_blank">{n['title']}</a>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-col">🐦 INTELIGENCIA X (TIEMPO REAL)</div>', unsafe_allow_html=True)
    try:
        headers = {"Authorization": f"Bearer {X_TOKEN}"}
        # Buscamos tweets de Venezuela, pidiendo la hora de creación (created_at)
        url_x = "https://api.twitter.com/2/tweets/search/recent?query=venezuela -is:retweet lang:es&max_results=15&tweet.fields=created_at"
        res_x = requests.get(url_x, headers=headers).json()
        
        if 'data' in res_x:
            for t in res_x['data']:
                # Calculamos tiempo relativo
                dt = datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
                ahora = datetime.now(timezone.utc)
                diff = ahora - dt
                minutos = int(diff.total_seconds() / 60)
                h_display = f"Hace {minutos}m" if minutos < 60 else f"{dt.strftime('%H:%M')}"

                st.markdown(f"""
                <div class="card" style="border-left-color: #1da1f2;">
                    <span class="time-badge x-badge">{h_display}</span>
                    <div class="source-tag">REPORTE CIUDADANO</div>
                    <div style="font-size:0.95rem; margin-top:8px; line-height:1.4;">{html.escape(t['text'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Sin conexión con X. Verificando señal...")
    except:
        st.error("📡 Señal de X bloqueada o cuota agotada.")

# --- 5. SISTEMA DE RECARGA FORZADA ---
# Recarga cada 45 segundos para mantener el "Tiempo Real"
components.html(f"""
    <script>
    setTimeout(function(){{
        window.location.reload();
    }}, 45000);
    </script>
""", height=0)
