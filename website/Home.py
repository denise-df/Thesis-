import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import base64

# ========================================================================
# PAGE CONFIG
# ========================================================================
st.set_page_config(
    page_title="EcoFleet Analytics | Quantifying the Cost of Speed",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================================================
# IMAGE PROCESSING FOR BACKGROUND
# ========================================================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Costruiamo il percorso relativo dell'immagine
img_path = os.path.join(os.path.dirname(__file__), 'background_van.jpg')

try:
    bin_str = get_base64_of_bin_file(img_path)
    bg_img_style = f"url('data:image/jpg;base64,{bin_str}')"
except Exception:
    # Fallback elegante se l'immagine non viene trovata
    bg_img_style = "linear-gradient(135deg, rgba(8,28,21,0.9), rgba(27,67,50,0.8))"

# ========================================================================
# NAVIGATION (Ripristinata integrale)
# ========================================================================
def render_navigation(current_page="Home"):
    logo_svg = (
        r'<svg width="170" height="45" viewBox="0 0 180 50">'
        r'<g transform="translate(5, 12)">'
        r'<rect x="8" y="8" width="18" height="12" fill="#2D6A4F" rx="2"/>'
        r'<rect x="0" y="12" width="8" height="8" fill="#40916C" rx="1"/>'
        r'<circle cx="8" cy="22" r="3" fill="#1B4332"/>'
        r'<circle cx="22" cy="22" r="3" fill="#1B4332"/>'
        r'<ellipse cx="22" cy="8" rx="3" ry="4" fill="#95D5B2" opacity="0.7"/>'
        r'</g>'
        r'<text x="45" y="32" font-family="Inter, sans-serif" font-weight="800" font-size="22" fill="#D8F3DC">EcoFleet</text>'
        r'</svg>'
    )
    
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 1rem 0 2rem 0;'>
        <div>{logo_svg}</div>
        <div style='display: flex; gap: 2rem; align-items: center;'>
            <a href='/' style='text-decoration: none; color: {"#D8F3DC" if current_page=="Home" else "#74c69d"}; font-weight: 600;'>Home</a>
            <a href='/Fleet_Impact_Simulator' style='text-decoration: none; color: {"#D8F3DC" if current_page=="Simulator" else "#74c69d"};'>Simulator</a>
            <a href='/Methodology' style='text-decoration: none; color: {"#D8F3DC" if current_page=="Methodology" else "#74c69d"};'>Methodology</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================
# GLOBAL CSS (Aggiornato con immagine di sfondo)
# ========================================================================
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #081C15;
        font-family: 'Inter', sans-serif;
    }

    /* HERO SECTION CON SFONDO */
    .hero-massive {
        background: 
            linear-gradient(90deg, rgba(8,28,21,1) 0%, rgba(8,28,21,0.8) 45%, rgba(8,28,21,0.1) 100%),
            """ + bg_img_style + r""";
        background-size: cover;
        background-position: center right;
        padding: 5rem 4rem;
        border-radius: 32px;
        margin: 1rem 0 3.5rem 0;
        border: 1px solid rgba(82,183,136,.25);
        box-shadow: 0 30px 100px rgba(0,0,0,0.5);
    }

    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 0.95;
        margin-bottom: 2rem;
        background: linear-gradient(120deg, #D8F3DC 30%, #52B788 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        font-size: 1.3rem;
        max-width: 600px;
        line-height: 1.6;
        color: #95D5B2;
        font-weight: 300;
    }

    .hero-hi {
        color: #D8F3DC;
        font-weight: 600;
        padding: 0 4px;
        background: rgba(82,183,136,0.15);
        border-radius: 4px;
    }

    /* KPI CARDS */
    .kpi-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 4rem;
    }

    .kpi-card {
        flex: 1;
        background: rgba(27, 67, 50, 0.3);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(82,183,136,0.15);
        transition: transform 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(82,183,136,0.4);
    }

    .kpi-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #D8F3DC;
        margin-bottom: 0.2rem;
    }

    .kpi-lab {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #74C69D;
        font-weight: 600;
    }

    /* CTA BOX */
    .cta-box {
        background: linear-gradient(135deg, #1B4332 0%, #081C15 100%);
        padding: 3.5rem;
        border-radius: 32px;
        text-align: center;
        border: 1px solid #2D6A4F;
        margin: 4rem 0;
    }

    .cta-t { font-size: 2rem; font-weight: 800; color: #D8F3DC; margin-bottom: 1rem; }
    .cta-s { color: #95D5B2; font-size: 1.1rem; margin-bottom: 2.5rem; }

    /* Nascondi header Streamlit standard */
    [data-testid="stHeader"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ========================================================================
# RENDER PAGE
# ========================================================================
render_navigation("Home")

# HERO SECTION
st.markdown(r"""
<div class='hero-massive'>
    <h1 class='hero-title'>The Hidden Cost<br>of Speed</h1>
    <p class='hero-sub'>
        Every delivery decision is a trade-off. 
        <span class='hero-hi'>Same-Day (<4h)</span> convenience comes at an environmental price — 
        up to <span class='hero-hi'>+150% more CO₂</span> than Standard delivery.
    </p>
</div>
""", unsafe_allow_html=True)

# KPI ROW
st.markdown(r"""
<div class='kpi-container'>
    <div class='kpi-card'>
        <div class='kpi-val'>13.6k</div>
        <div class='kpi-lab'>Total Miles Traveled</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-val'>67.4%</div>
        <div class='kpi-lab'>On-Time Accuracy</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-val'>2.4 kg</div>
        <div class='kpi-lab'>Avg CO₂ per Drop</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-val'>18 min</div>
        <div class='kpi-lab'>Service Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Qui iniziano i tuoi contenuti analitici (quelli delle 500 righe)
# Esempio di riga con grafici che avevi:
col_l, col_r = st.columns([1.2, 0.8])

with col_l:
    st.subheader("💡 Core Insight: The Efficiency Gap")
    st.write("La velocità richiede una densità di percorso inferiore, portando a viaggi a metà carico.")
    # Inserisci qui i tuoi grafici Plotly originali
    # fig = px.line(...) 
    # st.plotly_chart(fig)

with col_r:
    st.markdown(r"""
    <div style='background:rgba(116,198,157,0.05); padding:2rem; border-radius:20px; border-left:4px solid #52B788;'>
        <h4 style='margin-top:0;'>Why it matters?</h4>
        <p style='font-size:0.95rem; color:#95D5B2;'>
        Our ML models (XGBoost & CatBoost) indicate that <b>Route Overlap</b> is the primary driver of wasted emissions in urban areas.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sezione CTA
st.markdown(r"""
<div class='cta-box'>
    <div class='cta-t'>🚀 Ready to Optimize?</div>
    <p class='cta-s'>Test different fleet configurations and see the environmental impact in real-time.</p>
</div>
""", unsafe_allow_html=True)

# Bottoni di navigazione
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("🚗 Launch Simulator", use_container_width=True):
        st.switch_page("pages/1 Fleet Impact Simulator.py")
with b2:
    if st.button("📊 Explore Data", use_container_width=True):
        st.switch_page("pages/2 Data Explorer.py")
with b3:
    if st.button("📚 Methodology", use_container_width=True):
        st.switch_page("pages/3 Methodology.py")

# FOOTER
st.markdown(r"""
<hr style='border:none;border-top:1px solid rgba(255,255,255,.08);margin:5rem 0 2rem;'>
<div style='text-align:center; padding-bottom:3rem; color:#40916C; font-size:0.85rem;'>
    Thesis Project: Eco-Logistics Optimization · 2024
</div>
""", unsafe_allow_html=True)
