import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import base64  # Necessario per l'immagine

# ========================================================================
# PAGE CONFIG  — must be the very first Streamlit call
# ========================================================================
st.set_page_config(
    page_title="EcoFleet Analytics | Quantifying the Cost of Speed",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================================================
# LOGICA IMMAGINE DI SFONDO (CORRETTA PER GITHUB)
# ========================================================================
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Assicurati di caricare 'background_van.jpg' nella stessa cartella di Home.py su GitHub
img_path = os.path.join(os.path.dirname(__file__), 'background_van.jpg')

try:
    bin_str = get_base64(img_path)
    bg_img_style = f"url('data:image/jpg;base64,{bin_str}')"
except Exception as e:
    # Se l'immagine manca, usa un gradiente scuro di backup
    bg_img_style = "linear-gradient(135deg, #081C15, #1B4332)"

# ========================================================================
# NAVIGATION
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
        r'<text x="45" y="20" font-size="18" font-weight="700" fill="#95D5B2">Eco</text>'
        r'<text x="45" y="38" font-size="18" font-weight="700" fill="#FFFFFF">Fleet</text>'
        r'<text x="100" y="32" font-size="11" fill="#95D5B2">Analytics</text>'
        r'</svg>'
    )
    st.markdown(
        r"<style>"
        r"[data-testid='stSidebar']{display:none;}"
        r".nav-bar{background:linear-gradient(90deg,#081C15,#1B4332,#2D6A4F);"
        r"padding:1rem 2rem;margin:-1rem -1rem 0 -1rem;border-bottom:3px solid #52B788;}"
        r"</style>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='nav-bar'>{logo_svg}</div>", unsafe_allow_html=True)

    sp1, c1, c2, c3, c4, c5, sp2 = st.columns([0.5, 1, 1, 1, 1, 1, 0.5])
    cols = [c1, c2, c3, c4, c5] 

    nav = [
        ("🚗 Simulator", "Simulator", "pages/1 Fleet Impact Simulator.py"),
        ("🗺️ Topology",  "Topology",  "pages/6 Topological Analysis.py"),
        ("🚛 Fleet",      "Fleet",      "pages/5 Fleet Comparison.py"),
        ("📖 Glossary",  "Glossary",  "pages/4 Glossary.py"),
        ("📚 Methods",    "Methods",    "pages/3 Methodology.py"),
    ]

    for col, (label, key, page) in zip(cols, nav):
        with col:
            if st.button(label, use_container_width=True,
                        type="primary" if current_page == key else "secondary"):
                st.switch_page(page)

render_navigation("Home")

# ========================================================================
# GLOBAL CSS
# ========================================================================
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { background: linear-gradient(135deg, #0A1F17 0%, #1B4332 100%) !important; }

.hero-massive {
    background: 
        linear-gradient(90deg, rgba(8,28,21,1) 0%, rgba(8,28,21,0.8) 45%, rgba(8,28,21,0.1) 100%),
        """ + bg_img_style + r""";
    background-size: cover;
    background-position: center right;
    padding: 4rem 3rem;
    border-radius: 24px;
    margin: 2rem 0 3rem 0;
    border: 1px solid rgba(82,183,136,.3);
    box-shadow: 0 20px 80px rgba(0,0,0,.4);
    position: relative;
    overflow: hidden;
}
.hero-title {
    font-size: 4.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #fff 0%, #95D5B2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
}
.hero-sub  { font-size:1.4rem; color:#B7E4C7; line-height:1.7; margin-bottom:2rem; }
.hero-hi   { color:#52B788; font-weight:700; }
.badge {
    display: inline-block;
    background: rgba(82,183,136,.2);
    border: 1px solid rgba(82,183,136,.4);
    border-radius: 20px;
    padding: .35rem .9rem;
    font-size: .82rem;
    color: #95D5B2;
    font-weight: 600;
    margin: .3rem;
}

.stat-box {
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(82,183,136,.2);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: all .4s cubic-bezier(.4,0,.2,1);
}
.stat-box:hover {
    transform: translateY(-8px);
    background: rgba(255,255,255,.08);
    border-color: #52B788;
    box-shadow: 0 12px 40px rgba(82,183,136,.3);
}
.s-icon   { font-size: 2.4rem; margin-bottom: .7rem; }
.s-num     { font-size: 2.6rem; font-weight: 800; color: #52B788; line-height: 1; }
.s-label  { font-size: .8rem; color: #95D5B2; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: .4rem; }
.s-detail { font-size: .78rem; color: #B7E4C7; margin-top: .3rem; opacity: .8; }

.ins-card {
    background: rgba(255,255,255,.03);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2.5rem;
    border: 2px solid;
    height: 100%;
    transition: all .3s ease;
}
.ins-card:hover { border-width: 3px; }
.ins-thermal  { border-color: rgba(82,183,136,.35); }
.ins-electric { border-color: rgba(45,106,79,.4); }
.ins-title   { font-size: 1.7rem; font-weight: 800; color: #fff; margin-bottom: .4rem; }
.ins-metric  { font-size: 3.2rem; font-weight: 900; line-height: 1; margin: 1rem 0; }
.m-thermal   { color: #95D5B2; }
.m-electric  { color: #52B788; }
.ins-text     { color: #D8F3DC; font-size: .92rem; line-height: 1.7; }
.ins-li      { color: #B7E4C7; padding: .35rem 0 .35rem 1.4rem; position: relative; font-size: .88rem; }
.ins-li::before { content: '▸'; position: absolute; left: 0; color: #52B788; font-weight: bold; }
.ins-foot     { margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(82,183,136,.2); font-size: .78rem; opacity: .8; }

.feat-card {
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(82,183,136,.2);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    height: 100%;
    transition: all .3s ease;
}
.feat-card:hover {
    transform: translateY(-6px);
    background: rgba(255,255,255,.08);
    border-color: #52B788;
    box-shadow: 0 15px 50px rgba(82,183,136,.3);
}
.f-icon  { font-size: 3.2rem; margin-bottom: .8rem; }
.f-title { font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: .7rem; }
.f-desc  { color: #B7E4C7; font-size: .88rem; line-height: 1.6; }

.sec-h {
    font-size: 2rem; font-weight: 800; color: #fff;
    margin: 3.5rem 0 1.5rem; padding-left: 1rem;
    border-left: 5px solid #52B788;
}

.cta-box {
    background: linear-gradient(135deg, rgba(45,106,79,.2), rgba(82,183,136,.1));
    border: 2px solid rgba(82,183,136,.3);
    border-radius: 20px;
    padding: 2.5rem 2rem 1rem;
    text-align: center;
    margin: 3rem 0 .5rem;
}
.cta-t { font-size: 1.7rem; font-weight: 800; color: #fff; margin-bottom: .4rem; }
.cta-s { color: #B7E4C7; font-size: .97rem; margin-bottom: 1.5rem; }

div.stButton > button {
    background: linear-gradient(135deg, #2D6A4F, #40916C) !important;
    color: #fff !important;
    border: 2px solid #52B788 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all .3s ease !important;
    box-shadow: 0 6px 20px rgba(82,183,136,.35);
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 40px rgba(82,183,136,.55) !important;
}
</style>
""", unsafe_allow_html=True)

# ========================================================================
# HERO
# ========================================================================
st.markdown(r"""
<div class='hero-massive'>
    <h1 class='hero-title'>The Hidden Cost<br>of Speed</h1>
    <p class='hero-sub'>
        Every delivery decision is a trade-off.
        <span class='hero-hi'>Same-Day (<4h)</span> convenience comes at an environmental price —
        <span class='hero-hi'>+150% more CO₂</span> than Standard (3-5 days) delivery.
        This platform quantifies that cost using
        <span class='hero-hi'>AI-powered prediction models</span>
        trained on <span class='hero-hi'>real OBD-II telemetry</span> and validated on
        <span class='hero-hi'>25,000 simulated logistics trips</span>.
    </p>
    <span class='badge'>🔬 2 ML Models (ICE R²=0.79 · EV R²≈0.77)</span>
    <span class='badge'>🚛 6 Vehicle Types</span>
    <span class='badge'>⚡ 4 SLA Profiles</span>
    <span class='badge'>📊 25,000 Simulated Logistics Trips</span>
    <span class='badge'>🌐 904k Amazon Validation Stops</span>
    <span class='badge'>🤖 Agentic AI Dispatch (Gemini)</span>
    <span class='badge'>🗺️ Real Road Topology (OpenStreetMap)</span>
</div>
""", unsafe_allow_html=True)

# ========================================================================
# STAT CARDS
# ========================================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(r"""
    <div class='stat-box'>
        <div class='s-icon'>🚛</div>
        <div class='s-num'>25,000</div>
        <div class='s-label'>Simulated Trips</div>
        <div class='s-detail'>Synthetic India Logistics dataset · NB01</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(r"""
    <div class='stat-box'>
        <div class='s-icon'>🤖</div>
        <div class='s-num'>0.77</div>
        <div class='s-label'>EV Model R²</div>
        <div class='s-detail'>Ridge+Poly(2) · EU WLTP specs (Mai et al. 2025)</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(r"""
    <div class='stat-box'>
        <div class='s-icon'>⚠️</div>
        <div class='s-num'>2.5×</div>
        <div class='s-label'>Same-Day CO₂ Penalty</div>
        <div class='s-detail'>vs Standard delivery (+150%)</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(r"""
    <div class='stat-box'>
        <div class='s-icon'>⚡</div>
        <div class='s-num'>85%</div>
        <div class='s-label'>EV Drivetrain Efficiency</div>
        <div class='s-detail'>vs 20–30% for ICE engines</div>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# RESEARCH FINDINGS
# ========================================================================
st.markdown(r"<h2 class='sec-h'>💡 Research Findings</h2>", unsafe_allow_html=True)

col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown(r"""
    <div class='ins-card ins-thermal'>
        <div style='font-size:2.8rem;margin-bottom:.5rem;'>🔥</div>
        <div class='ins-title'>The Speed Penalty</div>
        <div class='ins-metric m-thermal'>+150%</div>
        <p class='ins-text'>
            <strong>Same-Day (<4h) delivery generates 2.5× more CO₂</strong> than Standard (3-5 days)
            for comparable routes, based on <strong>8,332 thermal trips</strong>.
        </p>
        <div class='ins-li'><strong>Fill Rate Collapse:</strong> 95% → 30%</div>
        <div class='ins-li'><strong>Traffic Exposure:</strong> Peak-hour gridlock</div>
        <div class='ins-foot' style='color:#95D5B2;'>
            <strong>📡 Source: OBD-II telemetry · Real fleet data</strong>
        </div>
    </div>""", unsafe_allow_html=True)

with col_r:
    st.markdown(r"""
    <div class='ins-card ins-electric'>
        <div style='font-size:2.8rem;margin-bottom:.5rem;'>⚡</div>
        <div class='ins-title'>The Gridlock Advantage</div>
        <div class='ins-metric m-electric'>−85%</div>
        <p class='ins-text'>
            <strong>EVs reduce traffic penalty by 85%</strong> vs thermal in gridlock,
            based on <strong>4,767 electric trips</strong>.
        </p>
        <div class='ins-li'><strong>Zero Idling Loss:</strong> No energy burned at standstill</div>
        <div class='ins-li'><strong>Energy Recovery:</strong> Regenerative braking</div>
        <div class='ins-foot' style='color:#95D5B2;'>
            <strong>📡 Source: EU WLTP BEV specs · Eurostat 2024</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# PLATFORM CAPABILITIES
# ========================================================================
st.markdown(r"<h2 class='sec-h'>🎯 Platform Capabilities</h2>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="large")

with f1:
    st.markdown(r"""
    <div class='feat-card'>
        <div class='f-icon'>🚗</div>
        <div class='f-title'>Fleet Impact Simulator</div>
        <p class='f-desc'>AI predictions via Gradient Boosting (ICE, R²=0.79).</p>
    </div>""", unsafe_allow_html=True)

with f2:
    st.markdown(r"""
    <div class='feat-card'>
        <div class='f-icon'>🔬</div>
        <div class='f-title'>SHAP Causal Analysis</div>
        <p class='f-desc'>Explainable AI for engine stress factors.</p>
    </div>""", unsafe_allow_html=True)

with f3:
    st.markdown(r"""
    <div class='feat-card'>
        <div class='f-icon'>🤖</div>
        <div class='f-title'>Agentic AI Dispatch</div>
        <p class='f-desc'>Gemini 2.5-Pro acts as an autonomous agent.</p>
    </div>""", unsafe_allow_html=True)

# --- Second Row Features ---
st.write("")
f4, f5, f6 = st.columns(3, gap="large")
with f4:
    st.markdown(r"""<div class='feat-card'><div class='f-icon'>🌐</div><div class='f-title'>Amazon Validation</div></div>""", unsafe_allow_html=True)
with f5:
    st.markdown(r"""<div class='feat-card'><div class='f-icon'>🗺️</div><div class='f-title'>Topology</div></div>""", unsafe_allow_html=True)
with f6:
    st.markdown(r"""<div class='feat-card'><div class='f-icon'>📊</div><div class='f-title'>Analytics</div></div>""", unsafe_allow_html=True)


# ========================================================================
# FLEET COMPOSITION CHART
# ========================================================================
st.markdown(r"<h2 class='sec-h'>🚛 Fleet Composition</h2>", unsafe_allow_html=True)

fleet = pd.DataFrame({
    "Vehicle":  ["Thermal Truck", "Thermal Van", "Thermal Scooter", "EV Van", "E-Bike", "Pedal Bike"],
    "Trips":    [4145, 4187, 2080, 4116, 651, 412],
})

fig = px.bar(fleet, x="Trips", y="Vehicle", orientation="h", color="Vehicle",
             color_discrete_sequence=px.colors.sequential.Greens_r)

fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(27,67,50,.25)",
                  font=dict(family="Inter", color="#D8F3DC"), showlegend=False, height=350)

st.plotly_chart(fig, use_container_width=True)

# ========================================================================
# CTA
# ========================================================================
st.markdown(r"""
<div class='cta-box'>
    <div class='cta-t'>🚀 Start Exploring</div>
    <p class='cta-s'>Use AI-powered tools to simulate scenarios and analyse real fleet data</p>
</div>""", unsafe_allow_html=True)

b1, b2, b3 = st.columns(3)
with b1:
    if st.button("🚗 Launch Simulator", use_container_width=True):
        st.switch_page("pages/1 Fleet Impact Simulator.py")
with b2:
    if st.button("📚 Read Methodology", use_container_width=True):
        st.switch_page("pages/3 Methodology.py")

# ========================================================================
# FOOTER
# ========================================================================
st.markdown(r"""
<hr style='border:none;border-top:1px solid rgba(255,255,255,.08);margin:3rem 0 1rem;'>
<div style='text-align:center;padding:1.5rem 0;color:#95D5B2;'>
    <strong>Master's Thesis Project</strong><br>
    <span style='font-size:.88rem;opacity:.75;'>
        Denise Di Franza &nbsp;·&nbsp; Data Science &amp; Management &nbsp;·&nbsp; LUISS University
    </span>
</div>""", unsafe_allow_html=True)
