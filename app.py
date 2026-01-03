import streamlit as st
import feedparser
import time
import streamlit.components.v1 as components

# Configuración de Terminal de Nueva Generación
st.set_page_config(page_title="MONITOR ESTRATÉGICO", layout="wide", page_icon="📡")

# CSS Estilizado y Moderno (UI/UX 2024+)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    .main { background-color: #0d1117; }

    /* Encabezado Estilizado */
    .main-title {
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -1px;
        color: #f0f6fc;
        margin-bottom: 0.5rem;
    }

    /* Contenedores de Noticias (Estilo Moderno) */
    .noticia-card {
        background-color: #161b22;
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #30363d;
        transition: all 0.2s ease-in-out;
    }
    
    .noticia-card:hover {
        border-color: #58a6ff;
        background-color: #1c2128;
        transform: translateY(-2px);
    }

    .noticia-importante {
        border-left: 4px solid #f85149;
        background: linear-gradient(90deg, #1c1314 0%, #161b22 100%);
    }

    .fuente-tag {
        text-transform: uppercase;
        font-size: 0.7rem;
        font-weight: 600;
        color: #8b949e;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        display: block;
    }

    .noticia-titulo {
        font-size: 1.1rem;
        font-weight: 600;
        color: #58a6ff;
        text-decoration: none;
        line-height: 1.4;
    }

    .timestamp {
        font-size: 0.75rem;
        color: #7d8590;
        margin-top: 0.75rem;
        display: block;
    }

    /* Headers de Columnas */
    .column-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
    }

    hr { border-top: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Monitor de Eventos en Directo</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #8b949e; margin-top: -15px;">Filtro Estricto de Inteligencia Geopolítica</p>', unsafe_allow_html=True)

# --- FUENTES RSS (Mantenemos la robustez anterior) ---
RSS_MASTER = {
    "🏛️ OFICIAL": [
        ("White House", "https://www.whitehouse.gov/briefing-room/statements-releases/feed/"),
        ("State Dept", "
