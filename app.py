import streamlit as st
from summarizer import ArticleSummarizer
import os

# Page configuration
st.set_page_config(
    page_title="NEURAL OVERRIDE | HUD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Implementation of ArticleSummarizer remains the same, but we make sure session state is handled
@st.cache_resource
def get_summarizer():
    return ArticleSummarizer()

summarizer = get_summarizer()

# --- CSS: NO SCROLL, FULL IMMERSION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&family=Inter:wght@400;600&display=swap');

    /* BASE RESET: NO SCROLL */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden;
        background: #050508 !important;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] { visibility: hidden; height: 0; }
    [data-testid="stToolbar"] { visibility: hidden; }
    
    .main .block-container {
        padding: 1rem 3rem !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* THEME VARIABLES */
    :root {
        --neon-cyan: #00e5ff;
        --neon-purple: #9d00ff;
        --neon-red: #ff2d55;
        --bg-glass: rgba(10, 10, 15, 0.95); /* DARKER */
        --border-glow: inset 0 0 15px rgba(0, 229, 255, 0.1), 0 0 10px rgba(0, 229, 255, 0.1);
    }

    /* GLOBAL ANIMATIONS */
    @keyframes scanline {
        0% { transform: translateY(-100vh); }
        100% { transform: translateY(100vh); }
    }

    @keyframes flicker {
        0% { opacity: 0.95; }
        50% { opacity: 1; }
        100% { opacity: 0.98; }
    }

    .stApp::after {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: rgba(0, 229, 255, 0.1);
        animation: scanline 8s linear infinite;
        pointer-events: none;
        z-index: 100;
    }

    /* TOP HUD BAR */
    .hud-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid var(--neon-cyan);
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        position: relative;
        animation: flicker 0.2s infinite;
    }

    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        color: var(--neon-cyan);
        letter-spacing: 5px;
        text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan);
    }

    .hud-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--neon-purple);
        display: flex;
        gap: 1.5rem;
    }

    /* MAIN CONSOLE AREA */
    .console-grid {
        display: flex;
        gap: 1.5rem;
        flex: 1;
        height: 70vh;
    }

    .panel {
        flex: 1;
        background: var(--bg-glass);
        border: 2px solid rgba(0, 229, 255, 0.3);
        position: relative;
        display: flex;
        flex-direction: column;
        clip-path: polygon(0 0, 98% 0, 100% 2%, 100% 100%, 2% 100%, 0 98%);
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);
        transition: all 0.3s ease;
    }

    .panel:hover {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.3);
    }

    .panel-header {
        background: rgba(0, 229, 255, 0.2);
        padding: 0.5rem 1rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        color: var(--neon-cyan);
        letter-spacing: 2px;
        display: flex;
        justify-content: space-between;
    }

    .panel-content {
        flex: 1;
        padding: 1rem;
        position: relative;
    }

    /* TEXT AREAS */
    .stTextArea textarea {
        background: #020204 !important; /* ULTRA DARK */
        border: none !important;
        color: #00ffcc !important; /* NEON TEXT */
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        height: 60vh !important;
        padding: 1.5rem !important;
        border-radius: 0 !important;
    }

    .summary-display {
        height: 60vh;
        overflow-y: auto;
        color: #e0e0e0;
        line-height: 1.6;
        font-size: 1rem;
        padding-right: 10px;
    }

    /* IDLE STATE IN SECOND BOX */
    .idle-overlay {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        opacity: 0.2;
    }

    .pulse-ring {
        border: 2px solid var(--neon-cyan);
        border-radius: 50%;
        height: 100px; width: 100px;
        animation: pulse-ring 2s infinite;
    }

    @keyframes pulse-ring {
        0% { transform: scale(0.5); opacity: 1; }
        100% { transform: scale(2); opacity: 0; }
    }

    /* FOOTER CONTROLS */
    .hud-bottom {
        display: flex;
        gap: 2rem;
        background: rgba(157, 0, 255, 0.05);
        border: 1px solid rgba(157, 0, 255, 0.2);
        padding: 0.8rem 2rem;
        margin-top: 1rem;
        align-items: center;
        justify-content: space-between;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(45deg, var(--neon-cyan), var(--neon-purple)) !important;
        color: #fff !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 3rem !important;
        clip-path: polygon(10% 0, 100% 0, 90% 100%, 0 100%);
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
    }

    /* SELECTBOX OVERRIDE */
    .stSelectbox div[data-baseweb="select"] {
        background-color: transparent !important;
        border: 1px solid var(--neon-cyan) !important;
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        font-size: 0.7rem !important;
    }

    /* METRICS */
    .metric-box {
        font-family: 'JetBrains Mono', monospace;
        color: var(--neon-purple);
        font-size: 0.7rem;
        text-transform: uppercase;
    }

</style>
""", unsafe_allow_html=True)

# --- TOP HUD ---
st.markdown("""
<div class="hud-top">
    <div class="hud-title">SYSTEM.OVERRIDE</div>
    <div class="hud-status">
        <span>LINK: STABLE</span>
        <span>LATENCY: 42ms</span>
        <span>CORE: LLAMA_3.1</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CONSOLE AREA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="panel"><div class="panel-header">SOURCE_INJECTION // SECTOR_01</div><div class="panel-content">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="WAITING FOR DATA INJECTION...", label_visibility="collapsed")
    st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="panel"><div class="panel-header">NEURAL_RESOLVE // SECTOR_02</div><div class="panel-content">', unsafe_allow_html=True)
    
    if "final_summary" in st.session_state:
        st.markdown(f'<div class="summary-display">{st.session_state.final_summary}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="idle-overlay">
            <div class="pulse-ring"></div>
            <p style="margin-top: 1rem; font-family: 'Orbitron', sans-serif;">AWAITING_DECODE_SIGNAL</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- BOTTOM CONTROLS ---
st.markdown('<div class="hud-bottom">', unsafe_allow_html=True)
bot_c1, bot_c2, bot_c3 = st.columns([1, 1, 2])

with bot_c1:
    length = st.selectbox("DENSITY", options=["brief", "detailed"], index=1, label_visibility="collapsed")

with bot_c2:
    if st.button("RUN_DECODE"):
        if user_input.strip():
            with st.spinner("SYNCHRONIZING..."):
                result = summarizer.summarize(user_input, length=length)
                st.session_state.final_summary = result
                st.rerun()
        else:
            st.error("DATA_REQUIRED")

with bot_c3:
    # Live HUD Metrics Area
    in_len = len(user_input)
    if "final_summary" in st.session_state and not st.session_state.final_summary.startswith("Error"):
        out_len = len(st.session_state.final_summary)
        comp = round((1 - out_len/(in_len if in_len > 0 else 1))*100, 1)
        st.markdown(f"""
        <div style="display: flex; gap: 2rem; justify-content: flex-end;">
            <div class="metric-box">BUFFER: {in_len}b</div>
            <div class="metric-box">RESULT: {out_len}b</div>
            <div class="metric-box">RATIO: {comp}%</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="metric-box">SYNC_STATUS: READY // BUFFER: {in_len}b</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
