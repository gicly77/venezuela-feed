import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de Terminal de Nueva Generación
st.set_page_config(page_title="MONITOR ESTRATÉGICO", layout="wide", page_icon="📡")

# CSS Avanzado: UI Moderna, Barra de Progreso y Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    .main { background-color: #0d1117; padding-top: 0px; }

    /* Barra de Progreso Animada */
    .progress-container {
        width: 100%;
        height: 4px;
        background-color: #161b22;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #58a6ff, #f85149);
        width: 0%;
        animation: progress-animation 10s linear infinite;
    }
    
    @keyframes progress-animation {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    /* Título Estilizado */
    .main-title {
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.05rem;
        color: #f0f6fc;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }

    /* Tarjetas de Noticias Modernas */
    .noticia-card {
        background-color: #161b22;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #30363d;
        transition: transform 0.2s, border-color 0.2s;
    }
    
    .noticia-card:hover {
        border-color: #58a6ff;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    /* Borde sutil para noticias con palabras clave de alerta */
    .noticia-importante {
        border-left: 4px solid #f85149;
    }

    .fuente-tag {
        text-transform: uppercase;
        font-size: 0.65rem;
        font-weight: 700;
        color: #8b949e;
        letter-spacing: 0.1rem;
        margin-bottom: 0.6rem;
        display: block;
    }

    .noticia-titulo {
        font-size: 1.05rem;
        font-weight: 600;
        color: #adbac7;
        text-decoration: none;
        line-height: 1.4;
    }
    
    .noticia-titulo:hover { color: #58a6ff; }

    .timestamp {
        font-size: 0.7rem;
        color: #7d8590;
        margin-top: 0.8rem;
        display: block;
    }

    /* Columnas */
    .column-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #30363d;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    
    <div class="progress-container">
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Monitor de Eventos en Directo</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #8b949e; margin-top: -10px; font-size: 0.9rem;">Inteligencia Geopolítica Estricta: Venezuela</p>', unsafe_allow_html=True)

# --- CONFIGURACIÓN DE FUENTES RSS ---
RSS_MASTER = {
    "SEÑAL OFICIAL": [
        ("White House", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("State Dept", "https://www.state.gov/rss-feed/press-releases/feed/"),
        ("ONU News", "https://news.un.org/feed/subscribe/es/news/region/latin-america-and-the-caribbean/feed/rss.xml"),
        ("OEA", "https://www.oas.org/es/centro_noticias/rss.asp")
    ],
    "PRENSA GLOBAL": [
        ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"),
        ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Reuters", "https://www.reutersagency.com/feed/"),
        ("El Mundo", "https://
