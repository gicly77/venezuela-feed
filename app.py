import streamlit as st
import feedparser
import time
from datetime import datetime, timezone

# 1. CONFIGURACIÓN DE LA TERMINAL
st.set_page_config(page_title="MONITOR ESTRATÉGICO", layout="wide", page_icon="📡")

# 2. CSS: UI MODERNA Y ALERTAS DE ALTA PRIORIDAD
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Barra de carga superior */
    .loading-bar-bg { position: fixed; top: 0; left: 0; width: 100%; height: 4px; background: #161b22; z-index: 9999; }
    .loading-bar-fill { height: 100%; background: linear-gradient(90deg, #58a6ff, #f85149); width: 0%; animation: progress 10s linear infinite; }
    @keyframes progress { from { width: 0%; } to { width: 100%; } }

    /* Tarjetas Estándar */
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem; position: relative; }
    
    /* Tarjeta URGENTE (Rojo) */
    .card-urgent { border-left: 5px solid #f85149; background: linear-gradient(90deg, #1c1314 0%, #161b22 100%); }
    
    /* ALERTA POTUS (Azul Brillante - Llamativa) */
    .card-potus { 
        border: 2px solid #58a6ff; 
        background: linear-gradient(145deg, #0d1117, #161b22);
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.3);
        animation: pulse-blue 2s infinite;
    }
    
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(88, 166, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
    }

    .tag-potus { color: #58a6ff !important; font-weight: 800 !important; }
    
    .tag { font-size: 0.7rem; color: #8b949e; text-transform: uppercase; font-weight: 600; margin-bottom: 5px; display: block; }
    .title { font-size: 1.1rem; color: #c9d1d9; text-decoration: none; font-weight: 600; display: block; margin: 5px 0; line-height: 1.4; }
    .title:hover { color: #58a6ff; }
    .time-badge { font-size: 0.7rem; color: #ffffff; background: #238636; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
    .time-ago { font-size: 0.7rem; color: #7d8590; margin-left: 10px; }
    
    .header { font-size: 0.9rem; color: #8b949e; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 25px; font-weight: 600; }
    
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    <div class="loading-bar-bg"><div class="loading-bar-fill"></div></div>
    """, unsafe_allow_html=True)

st.markdown('<h1 style="color:#f0f6fc; font-weight:600; margin-top:-40px;">Monitor de Eventos en Directo</h1>', unsafe_allow_html=True)

# 3. FUENTES SELECCIONADAS
SOURCES = {
    "INTER_OFICIAL": [
        ("CASA BLANCA", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("DEPARTAMENTO DE ESTADO", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("OEA", "https://www.oas.org/es/centro_noticias/rss.asp"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("AP News", "https://apnews.com/hub/venezuela.rss"),
        ("NY Times", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
        ("BBC News", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada")
    ],
    "LOCAL_VZLA": [
        ("Efecto Cocuyo", "https://efectococuyo.com/feed/"),
        ("El Pitazo", "https://elpitazo.net/feed/"),
        ("Infobae", "https://www.infobae.com/feeds/rss/"),
        ("NTN24", "https://www.ntn24.com/rss.xml"),
        ("La Patilla", "https://www.lapatilla.com/feed/"),
        ("YouTube: NTN24", "https://www.youtube.com/feeds/videos.xml?channel_id=UC8HqZ6G_YmshN0L_z94P-Lw"),
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
        impact_keys = ['gobierno', 'trump', 'guerra', 'ejército', 'golpe', 'sanciones', 'ataque', 'captura', 'urgente']
        
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
                            "is_potus": "WHITE HOUSE" in name or "DEPARTAMENTO DE ESTADO" in name,
                            "urgent": any(i in content for i in impact_keys)
                        })
            except: continue
        
        pool.sort(key=lambda x: x['sort_key'], reverse=True)
        
        for n in pool[:40]:
            # Lógica de Clases CSS
            card_class = "card"
