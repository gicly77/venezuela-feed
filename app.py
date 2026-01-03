import streamlit as st
import feedparser
import time
from datetime import datetime, timezone

# 1. CONFIGURACIÓN DE LA TERMINAL
st.set_page_config(page_title="MONITOR MÓVIL", layout="wide", page_icon="📡")

# 2. CSS ADAPTATIVO (PC y MÓVIL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Barra de carga superior */
    .loading-bar-bg { position: fixed; top: 0; left: 0; width: 100%; height: 4px; background: #161b22; z-index: 9999; }
    .loading-bar-fill { height: 100%; background: linear-gradient(90deg, #58a6ff, #f85149); width: 0%; animation: progress 10s linear infinite; }
    @keyframes progress { from { width: 0%; } to { width: 100%; } }

    /* Contenedor de Tarjetas */
    .card { 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px; 
        padding: 1rem; 
        margin-bottom: 0.8rem; 
        word-wrap: break-word;
    }
    
    /* Alerta POTUS (Muy llamativa) */
    .card-potus { 
        border: 2px solid #58a6ff; 
        background: linear-gradient(145deg, #0d1117, #1c2128);
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
        animation: pulse-blue 2s infinite;
    }
    
    @keyframes pulse-blue {
        0% { border-color: #58a6ff; }
        50% { border-color: #f0f6fc; }
        100% { border-color: #58a6ff; }
    }

    .card-urgent { border-left: 5px solid #f85149; }
    
    .tag { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; font-weight: 600; display: block; margin-bottom: 4px; }
    .title { font-size: 1rem; color: #c9d1d9; text-decoration: none; font-weight: 600; display: block; line-height: 1.3; }
    .time-badge { font-size: 0.65rem; color: #ffffff; background: #238636; padding: 2px 6px; border-radius: 10px; font-weight: 600; }
    
    /* Ajustes para Móvil (Pantallas pequeñas) */
    @media (max-width: 768px) {
        .title { font-size: 0.95rem; }
        .header { font-size: 0.8rem; letter-spacing: 1px; }
        .stMarkdown h1 { font-size: 1.5rem !important; }
    }

    .header { font-size: 0.9rem; color: #8b949e; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px; font-weight: 600; }
    
    /* Ocultar elementos de Streamlit */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    <div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
    """, unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px;">Monitor Directo</h1>', unsafe_allow_html=True)

# 3. FUENTES (DICCIONARIO CORREGIDO Y CERRADO)
SOURCES = {
    "INTER_OFICIAL": [
        ("🏛️ WHITE HOUSE", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("🏛️ STATE DEPT", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("AP News", "https://apnews.com/hub/venezuela.rss"),
        ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada")
    ],
    "LOCAL_VZLA": [
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("NTN24", "https://www.ntn24.com/rss.xml"),
        ("YouTube: VPItv", "https://www.youtube.com/feeds/videos.xml?channel_id=UC_uH_S9X_Xqh6u_K6M9mB2Q")
    ]
}

def get_time_ago(struct_time):
    try:
        dt = datetime.fromtimestamp(time.mktime(struct_time), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = now - dt
        mins = int(diff.total_seconds() / 60)
        if mins < 1: return "Ahora"
        if mins < 60: return f"Hace {mins}m"
        return f"Hace {int(mins/60)}h"
    except: return "Reciente"

def run_monitor(col, label, feeds):
    with col:
        st.markdown(f'<div class="header">{label}</div>', unsafe_allow_html=True)
        vzla_keys = ['venezuela', 'maduro', 'caracas', 'miraflores', 'padrino', 'delcy', 'cabello', 'corina', 'edmundo']
        impact_keys = ['gobierno', 'trump', 'guerra', 'ejército', 'golpe', 'sanciones', 'ataque', 'urgente']
        
        pool = []
        for name, url in feeds:
            try:
                data = feedparser.parse(url)
                for entry in data.entries[:5]:
                    content = (entry.title + entry.get('summary', '')).lower()
                    if any(k in content for k in vzla_keys):
                        pub_time = entry.get('published_parsed', time.gmtime())
                        pool.append({
                            "source": name,
                            "title": entry.title,
                            "link": entry.link,
                            "sort_key": pub_time,
                            "time_str": time.strftime('%H:%M', pub_time),
                            "time_ago": get_time_ago(pub_time),
                            "is_potus": "🏛️" in name,
                            "urgent": any(i in content for i in impact_keys)
                        })
            except: continue
        
        pool.sort(key=lambda x: x['sort_key'], reverse=True)
        
        if pool:
            for n in pool[:25]:
                card_class = "card"
                if n['is_potus']: card_class += " card-potus"
                elif n['urgent']: card_class += " card-urgent"
                
                st.markdown(f"""
                <div class="{card_class}">
                    <span class="tag">{n['source']}</span>
                    <a class="title" href="{n['link']}" target="_blank">{n['title']}</a>
                    <div style="margin-top:8px;">
                        <span class="time-badge">{n['time_str']}</span>
                        <span style="font-size:0.65rem; color:#7d8590; margin-left:8px;">{n['time_ago']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Buscando noticias relevantes...")

# 4. LAYOUT ADAPTATIVO
# En móvil, Streamlit pondrá c2 debajo de c1 automáticamente.
c1, c2 = st.columns([1, 1])
run_monitor(c1, "🌍 Global y Oficial", SOURCES["INTER_OFICIAL"])
run_monitor(c2, "📍 Local Venezuela", SOURCES["LOCAL_VZLA"])

# 5. REFRESCO AUTOMÁTICO
time.sleep(10)
st.rerun()
