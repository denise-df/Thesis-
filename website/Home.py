import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

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
# NAVIGATION
# ========================================================================
def render_navigation(current_page="Home"):
    logo_svg = (
        '<svg width="170" height="45" viewBox="0 0 180 50">'
        '<g transform="translate(5, 12)">'
        '<rect x="8" y="8" width="18" height="12" fill="#2D6A4F" rx="2"/>'
        '<rect x="0" y="12" width="8" height="8" fill="#40916C" rx="1"/>'
        '<circle cx="8" cy="22" r="3" fill="#1B4332"/>'
        '<circle cx="22" cy="22" r="3" fill="#1B4332"/>'
        '<ellipse cx="22" cy="8" rx="3" ry="4" fill="#95D5B2" opacity="0.7"/>'
        '</g>'
        '<text x="45" y="20" font-size="18" font-weight="700" fill="#95D5B2">Eco</text>'
        '<text x="45" y="38" font-size="18" font-weight="700" fill="#FFFFFF">Fleet</text>'
        '<text x="100" y="32" font-size="11" fill="#95D5B2">Analytics</text>'
        '</svg>'
    )
    st.markdown(
        "<style>"
        "[data-testid='stSidebar']{display:none;}"
        ".nav-bar{background:linear-gradient(90deg,#081C15,#1B4332,#2D6A4F);"
        "padding:1rem 2rem;margin:-1rem -1rem 0 -1rem;border-bottom:3px solid #52B788;}"
        "</style>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='nav-bar'>{logo_svg}</div>", unsafe_allow_html=True)

    cols = st.columns(6)
    # Sostituisci la vecchia definizione di "cols" con questa:
    # [0.5, 1, 1, 1, 1, 1, 0.5] crea spazio ai bordi e c'entra i 5 bottoni
    sp1, c1, c2, c3, c4, c5, sp2 = st.columns([0.5, 1, 1, 1, 1, 1, 0.5])
    cols = [c1, c2, c3, c4, c5] # Passiamo solo le colonne centrali al ciclo for

    nav = [
        ("🚗 Simulator", "Simulator", "pages/1 Fleet Impact Simulator.py"),
        ("🗺️ Topology",  "Topology",  "pages/6 Topological Analysis.py"),
        ("🚛 Fleet",     "Fleet",     "pages/5 Fleet Comparison.py"),
        ("📖 Glossary",  "Glossary",  "pages/4 Glossary.py"),
        ("📚 Methods",   "Methods",   "pages/3 Methodology.py"),
    ]

    for col, (label, key, page) in zip(cols, nav):
        with col:
            if st.button(label, use_container_width=True,
                        type="primary" if current_page == key else "secondary"):
                st.switch_page(page)

render_navigation("Home")

# ========================================================================
# GLOBAL CSS  — iniettato UNA SOLA VOLTA, nessun display:grid qui dentro
# ========================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { background: linear-gradient(135deg, #0A1F17 0%, #1B4332 100%) !important; }

/* ── hero ── */
.hero-massive {
    background: linear-gradient(135deg, rgba(8,28,21,.95), rgba(27,67,50,.9));
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

/* ── stat cards  (layout via st.columns, non CSS grid) ── */
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
.s-num    { font-size: 2.6rem; font-weight: 800; color: #52B788; line-height: 1; }
.s-label  { font-size: .8rem; color: #95D5B2; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: .4rem; }
.s-detail { font-size: .78rem; color: #B7E4C7; margin-top: .3rem; opacity: .8; }

/* ── insight cards ── */
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
.ins-text    { color: #D8F3DC; font-size: .92rem; line-height: 1.7; }
.ins-li      { color: #B7E4C7; padding: .35rem 0 .35rem 1.4rem; position: relative; font-size: .88rem; }
.ins-li::before { content: '▸'; position: absolute; left: 0; color: #52B788; font-weight: bold; }
.ins-foot    { margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(82,183,136,.2); font-size: .78rem; opacity: .8; }

/* ── feature cards ── */
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

/* ── section header ── */
.sec-h {
    font-size: 2rem; font-weight: 800; color: #fff;
    margin: 3.5rem 0 1.5rem; padding-left: 1rem;
    border-left: 5px solid #52B788;
}

/* ── CTA box ── */
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

/* ── buttons ── */
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
# HERO  — un solo div, nessun layout CSS dentro
# ========================================================================
st.markdown("""
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
# STAT CARDS  — layout con st.columns(), NON con display:grid nell'HTML
# ========================================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class='stat-box'>
        <div class='s-icon'>🚛</div>
        <div class='s-num'>25,000</div>
        <div class='s-label'>Simulated Trips</div>
        <div class='s-detail'>Synthetic India Logistics dataset · NB01</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='stat-box'>
        <div class='s-icon'>🤖</div>
        <div class='s-num'>0.77</div>
        <div class='s-label'>EV Model R²</div>
        <div class='s-detail'>Ridge+Poly(2) · EU WLTP specs (Mai et al. 2025)</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='stat-box'>
        <div class='s-icon'>⚠️</div>
        <div class='s-num'>2.5×</div>
        <div class='s-label'>Same-Day CO₂ Penalty</div>
        <div class='s-detail'>vs Standard delivery (+150%)</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='stat-box'>
        <div class='s-icon'>⚡</div>
        <div class='s-num'>85%</div>
        <div class='s-label'>EV Drivetrain Efficiency</div>
        <div class='s-detail'>vs 20–30% for ICE engines</div>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# RESEARCH FINDINGS  — 2 colonne Streamlit, una card per colonna
# ========================================================================
st.markdown("<h2 class='sec-h'>💡 Research Findings</h2>", unsafe_allow_html=True)

col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown("""
    <div class='ins-card ins-thermal'>
        <div style='font-size:2.8rem;margin-bottom:.5rem;'>🔥</div>
        <div class='ins-title'>The Speed Penalty</div>
        <div class='ins-metric m-thermal'>+150%</div>
        <p class='ins-text'>
            <strong>Same-Day (<4h) delivery generates 2.5× more CO₂</strong> than Standard (3-5 days)
            for comparable routes, based on <strong>8,332 thermal trips</strong>
            (4,187 Van + 4,145 Truck).
        </p>
        <div class='ins-li'><strong>Fill Rate Collapse:</strong> 95% → 30% (vehicles half-empty)</div>
        <div class='ins-li'><strong>Traffic Exposure:</strong> Forced entry into peak-hour gridlock</div>
        <div class='ins-li'><strong>Engine Stress:</strong> +40% RPM × Load vs Standard</div>
        <div class='ins-li'><strong>Distance Penalty:</strong> Fragmented routing (+30% total km)</div>
        <div class='ins-foot' style='color:#95D5B2;'>
            <strong>📡 Source: OBD-II telemetry · Fiat Ducato / Ford Transit fleet (real data)</strong>
        </div>
    </div>""", unsafe_allow_html=True)

with col_r:
    st.markdown("""
    <div class='ins-card ins-electric'>
        <div style='font-size:2.8rem;margin-bottom:.5rem;'>⚡</div>
        <div class='ins-title'>The Gridlock Advantage</div>
        <div class='ins-metric m-electric'>−85%</div>
        <p class='ins-text'>
            <strong>EVs reduce traffic penalty by 85%</strong> vs thermal in gridlock,
            based on <strong>4,767 electric trips</strong>
            (4,116 EV Van + 651 E-bike).
        </p>
        <div class='ins-li'><strong>Zero Idling Loss:</strong> No energy burned at standstill</div>
        <div class='ins-li'><strong>Energy Recovery:</strong> 15–20% regenerated via braking</div>
        <div class='ins-li'><strong>Thermal Gridlock:</strong> +250% emissions vs free-flow</div>
        <div class='ins-li'><strong>EV Gridlock:</strong> only +38% consumption (A/C load)</div>
        <div class='ins-foot' style='color:#95D5B2;'>
            <strong>📡 Source: EU WLTP BEV specs · Mai et al. (2025) Scientific Data · EU grid 233 g/kWh (Eurostat 2024)</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# PLATFORM CAPABILITIES  — 3 colonne Streamlit
# ========================================================================
st.markdown("<h2 class='sec-h'>🎯 Platform Capabilities</h2>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="large")

with f1:
    st.markdown("""
    <div class='feat-card'>
        <div class='f-icon'>🚗</div>
        <div class='f-title'>Fleet Impact Simulator</div>
        <p class='f-desc'>
            AI predictions via Gradient Boosting (ICE, R²=0.79) and Ridge+Poly(2) (EV, R²≈0.77).
            Simulate 6 vehicle types × 4 SLA levels with real physics parameters and EU ETS carbon pricing.
        </p>
    </div>""", unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class='feat-card'>
        <div class='f-icon'>🔬</div>
        <div class='f-title'>SHAP Causal Analysis</div>
        <p class='f-desc'>
            SHapley Additive exPlanations open the ICE model black-box. 
            Identifies the exact contribution of speed, acceleration and engine stress to the Same-Day CO₂ penalty.
        </p>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

f4, f5, f6 = st.columns(3, gap="large")

with f4:
    st.markdown("""
    <div class='feat-card'>
        <div class='f-icon'>🤖</div>
        <div class='f-title'>Agentic AI Dispatch</div>
        <p class='f-desc'>
            Gemini 2.5-Pro acts as an autonomous dispatch agent: it calls ML tools, tracks the fleet CO₂ budget
            and generates daily operational reports — true agentic reasoning, not just text generation.
        </p>
    </div>""", unsafe_allow_html=True)

with f5:
    st.markdown("""
    <div class='feat-card'>
        <div class='f-icon'>🌐</div>
        <div class='f-title'>Amazon LMRRC Validation</div>
        <p class='f-desc'>
            External robustness check: EcoFleet models applied to 904,527 real Amazon stops across 5 US cities.
            Confirms that the urgency–emissions relationship generalises beyond the training dataset.
        </p>
    </div>""", unsafe_allow_html=True)

with f6:
    st.markdown("""
    <div class='feat-card'>
        <div class='f-icon'>🗺️</div>
        <div class='f-title'>Topological Analysis</div>
        <p class='f-desc'>
            Real-road routing via OpenStreetMap for Urban (Rome EUR) and Rural (Castelli Romani) contexts.
            Quantifies how delivery density amplifies the CO₂ penalty of fragmented Express dispatching.
        </p>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# FLEET COMPOSITION CHART
# Sunburst sostituito: il nodo "tipo" era figlio dello stesso nodo "All Vehicles"
# dei singoli veicoli → struttura confusa. Sostituito con bar chart orizzontale
# raggruppato per propulsione — più chiaro e informativo.
# ========================================================================
st.markdown("<h2 class='sec-h'>🚛 Fleet Composition</h2>", unsafe_allow_html=True)

fleet = pd.DataFrame({
    "Vehicle":  ["Thermal Van", "Thermal Truck", "Thermal Scooter",
                 "EV Van", "E-Bike", "Pedal Bike"],
    "Trips":    [4187, 4145, 2080, 4116, 651, 412],
    "Propulsion": ["Thermal", "Thermal", "Thermal",
                   "Electric", "Electric", "Human"],
    "CO₂ g/km": [220, 600, 65, 35, 8, 21],
})

# Palette interamente verde: thermal=verde scuro, electric=verde medio, human=verde chiaro
color_map = {
    "Thermal Van":     "#1B4332",
    "Thermal Truck":   "#2D6A4F",
    "Thermal Scooter": "#40916C",
    "EV Van":          "#52B788",
    "E-Bike":          "#74C69D",
    "Pedal Bike":      "#95D5B2",
}

# Ordine: dal più pesante al più leggero
order = ["Thermal Truck", "Thermal Van", "Thermal Scooter", "EV Van", "E-Bike", "Pedal Bike"]
fleet["Vehicle"] = pd.Categorical(fleet["Vehicle"], categories=order, ordered=True)
fleet = fleet.sort_values("Vehicle")

fig = __import__("plotly.express", fromlist=["bar"]).bar(
    fleet,
    x="Trips",
    y="Vehicle",
    orientation="h",
    color="Vehicle",
    color_discrete_map=color_map,
    text="Trips",
    custom_data=["CO₂ g/km", "Propulsion"],
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
    marker_line_color="rgba(0,0,0,0)",
    hovertemplate="<b>%{y}</b><br>Trips: %{x:,}<br>CO₂: %{customdata[0]} g/km<br>%{customdata[1]}<extra></extra>",
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(27,67,50,.25)",
    font=dict(family="Inter", color="#D8F3DC", size=13),
    showlegend=False,
    title=dict(
        text="15,591 total trips — breakdown by vehicle type",
        font=dict(size=14, color="#95D5B2"),
    ),
    xaxis=dict(
        title="Number of Trips",
        gridcolor="rgba(82,183,136,.12)",
        tickfont=dict(color="#95D5B2"),
    ),
    yaxis=dict(
        title="",
        tickfont=dict(color="#D8F3DC", size=13),
    ),
    margin=dict(t=50, b=20, l=10, r=80),
    height=380,
)

st.plotly_chart(fig, use_container_width=True)

# Leggenda propulsione sotto il grafico — 3 colonne Streamlit
leg1, leg2, leg3 = st.columns(3)
with leg1:
    st.markdown("""
    <div style='text-align:center; padding:.8rem; background:rgba(27,67,50,.4);
    border-radius:8px; border:1px solid rgba(82,183,136,.2);'>
        <span style='font-size:1.4rem;'>🔥</span><br>
        <strong style='color:#D8F3DC;'>Thermal (ICE)</strong><br>
        <span style='color:#95D5B2;font-size:.85rem;'>10,412 trips · 67%</span>
    </div>""", unsafe_allow_html=True)
with leg2:
    st.markdown("""
    <div style='text-align:center; padding:.8rem; background:rgba(27,67,50,.4);
    border-radius:8px; border:1px solid rgba(82,183,136,.2);'>
        <span style='font-size:1.4rem;'>⚡</span><br>
        <strong style='color:#D8F3DC;'>Electric (EV)</strong><br>
        <span style='color:#95D5B2;font-size:.85rem;'>4,767 trips · 31%</span>
    </div>""", unsafe_allow_html=True)
with leg3:
    st.markdown("""
    <div style='text-align:center; padding:.8rem; background:rgba(27,67,50,.4);
    border-radius:8px; border:1px solid rgba(82,183,136,.2);'>
        <span style='font-size:1.4rem;'>🚲</span><br>
        <strong style='color:#D8F3DC;'>Human Power</strong><br>
        <span style='color:#95D5B2;font-size:.85rem;'>412 trips · 2.6%</span>
    </div>""", unsafe_allow_html=True)

# ========================================================================
# CTA
# ========================================================================
st.markdown("""
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
st.markdown("""
<hr style='border:none;border-top:1px solid rgba(255,255,255,.08);margin:3rem 0 1rem;'>
<div style='text-align:center;padding:1.5rem 0;color:#95D5B2;'>
    <strong>Master's Thesis Project</strong><br>
    <span style='font-size:.88rem;opacity:.75;'>
        Denise Di Franza &nbsp;·&nbsp; Data Science &amp; Management &nbsp;·&nbsp; LUISS University<br>
    </span>
</div>""", unsafe_allow_html=True)