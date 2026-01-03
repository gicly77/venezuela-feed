import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURACIÓN BÁSICA ---
st.set_page_config(page_title="WAR ROOM", layout="wide")

# --- HORA MADRID ---
madrid_tz = pytz.timezone('Europe/Madrid')
hora_madrid = datetime.now(madrid_tz).strftime("%H:%M:%S")

# --- ESTILO SIN CONFLICTOS ---
st.markdown("""
<style>
    .stApp { background:#05070a; color:#e1e1e1; }
    [data-testid="stSidebar"], header, footer { display:none !important; }
    
    /* Columna de noticias limpia */
    .main-container { max-width: 850px; margin-left: 20px; }
    .news-card { 
        background:#10141b; border:1px solid #1f2937; padding:15px; 
        margin-bottom:10px; border-left: 4px solid #ffcc00; 
    }
    .headline { color:#60a5fa !important; text-decoration:none; font-weight:bold; font-size:1.1rem; }

    /* Monitor X pequeño en la esquina */
    .x-mini-monitor {
        position: fixed; top: 10px; right: 10px;
        width: 300px; height: 400px; z-index: 999;
