import streamlit as st
import pandas as pd

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Methodology | EcoFleet Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Navigation ─────────────────────────────────────────────────────────
def render_navigation(current_page="Methods"):
    logo_svg = (
        '<svg width="170" height="45" viewBox="0 0 180 50">'
        '<g transform="translate(5, 12)"><rect x="8" y="8" width="18" height="12" fill="#2D6A4F" rx="2"/>'
        '<rect x="0" y="12" width="8" height="8" fill="#40916C" rx="1"/>'
        '<circle cx="8" cy="22" r="3" fill="#1B4332"/><circle cx="22" cy="22" r="3" fill="#1B4332"/>'
        '<ellipse cx="22" cy="8" rx="3" ry="4" fill="#95D5B2" opacity="0.7"/></g>'
        '<text x="45" y="20" font-size="18" font-weight="700" fill="#95D5B2">Eco</text>'
        '<text x="45" y="38" font-size="18" font-weight="700" fill="#FFFFFF">Fleet</text>'
        '<text x="100" y="32" font-size="11" fill="#95D5B2">Analytics</text></svg>'
    )
    st.markdown(
        "<style>[data-testid='stSidebar']{display:none;}"
        ".nav-bar{background:linear-gradient(90deg,#081C15,#1B4332,#2D6A4F);"
        "padding:1rem 2rem;margin:-1rem -1rem 0 -1rem;border-bottom:3px solid #52B788;}</style>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='nav-bar'>{logo_svg}</div>", unsafe_allow_html=True)
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

render_navigation("Methods")

# ── CSS (Dark Theme Fleet Style) ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0D1F17 !important;
    color: #D8F3DC !important;
}
.stApp { background: linear-gradient(160deg, #0D1F17 0%, #152A1E 100%) !important; }

.fleet-hero {
    border-left: 5px solid #52B788;
    padding: 2.5rem 2.5rem;
    margin: 2rem 0 3rem 0;
    background: rgba(82, 183, 136, 0.05);
    border-radius: 0 12px 12px 0;
}
.fleet-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem;
    letter-spacing: 3px;
    color: #52B788;
    text-transform: uppercase;
    margin-bottom: .8rem;
}
.fleet-title {
    font-size: 3rem;
    font-weight: 800;
    color: #D8F3DC;
    line-height: 1.1;
    margin-bottom: .8rem;
}
.fleet-sub {
    font-size: 1.05rem;
    color: #95D5B2;
    line-height: 1.7;
    opacity: .85;
}
.sec-h {
    font-size: 1.5rem;
    font-weight: 700;
    color: #95D5B2;
    margin: 3rem 0 1.5rem 0;
    padding-bottom: .5rem;
    border-bottom: 1px solid rgba(82, 183, 136, 0.25);
}
.method-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(82, 183, 136, 0.15);
    border-radius: 10px;
    padding: 1.5rem;
    height: 100%;
    transition: all .25s ease;
}
.method-card:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(82, 183, 136, 0.4);
    transform: translateY(-2px);
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    color: #52B788;
    font-size: 2rem;
    font-weight: 700;
    opacity: 0.3;
    margin-bottom: -1rem;
}
.card-head {
    font-size: 1.2rem;
    font-weight: 700;
    color: #D8F3DC;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}
.mono-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    background: rgba(82, 183, 136, 0.1);
    color: #95D5B2;
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid rgba(82, 183, 136, 0.2);
}
.dark-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}
.dark-table th {
    text-align: left;
    color: #52B788;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    border-bottom: 1px solid rgba(82, 183, 136, 0.3);
    padding: 0.5rem;
}
.dark-table td {
    color: #D8F3DC;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(82, 183, 136, 0.1);
    padding: 0.8rem 0.5rem;
}
.dark-table tr:last-child td { border-bottom: none; }
.ins-box {
    background: rgba(82, 183, 136, 0.08);
    border-left: 4px solid #52B788;
    border-radius: 6px;
    padding: 1rem 1.4rem;
    margin: 1.5rem 0;
    font-size: .93rem;
    color: #B7E4C7;
}
div.stButton > button {
    background: rgba(45, 106, 79, 0.3) !important;
    color: #95D5B2 !important;
    border: 1px solid rgba(82, 183, 136, 0.3) !important;
    border-radius: 8px !important;
}
div.stButton > button:hover {
    background: rgba(45, 106, 79, 0.6) !important;
    border-color: #52B788 !important;
    color: #D8F3DC !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Section ───────────────────────────────────────────────────────
st.markdown("""
<div class='fleet-hero'>
    <div class='fleet-eyebrow'>Thesis Project · Research Methodology</div>
    <div class='fleet-title'>Bridging Logistics & Data Science</div>
    <p class='fleet-sub'>
        A rigorous 10-notebook framework to quantify the environmental trade-offs between
        operational speed (SLA) and fleet sustainability — from raw telemetry ingestion
        to agentic AI dispatch and real-road topological validation.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 1. Objectives ──────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>🎯 Research Overview</div>", unsafe_allow_html=True)

c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>01</div>
        <div class='card-head'>Objective</div>
        <p style='color:#B7E4C7; line-height:1.6;'>
            To demonstrate that <strong>Same-Day Delivery</strong> strategies impose a non-linear environmental cost
            compared to consolidated options, and to validate <strong>Electric Vehicles (EVs)</strong> as the
            superior operational choice for high-density urban logistics.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='ins-box' style='margin-top:0; height:100%; display:flex; flex-direction:column; justify-content:center;'>
        <strong>💡 Central Hypotheses</strong>
        <ul style='margin-top:1rem; padding-left:1.2rem; line-height:1.5;'>
            <li><strong>H1 (Cost of Speed):</strong> Same-Day (&lt;4h) windows double emissions vs Next-Day (24-48h) due to low fill-rates.</li>
            <li><strong>H2 (Gridlock):</strong> EVs outperform ICE specifically in congestion due to regenerative braking.</li>
            <li><strong>H3 (Density):</strong> Rural fragmented dispatch triples CO₂ vs urban, amplified by low drop density.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ── 2. Data Architecture ───────────────────────────────────────────────
st.markdown("<div class='sec-h'>📡 Data Architecture</div>", unsafe_allow_html=True)
st.markdown("Four distinct high-frequency datasets were integrated to build the analytical pipeline.")

d1, d2, d3, d4 = st.columns(4)

data_layers = [
    ("D1: Thermal", "ICE Telemetry", "OBD-II Dongles (1 Hz)", "MAF, RPM, Load"),
    ("D2: Electric", "EV BEV Specs", "Mai et al. 2025 · Scientific Data", "Wh/km, kWh, Segment"),
    ("D3: Context", "Urban Profile", "Traffic/Weather API", "Congestion Idx, Temp"),
    ("D4: Ops", "Logistics", "TMS Export", "SLA, Weight, Stops")
]

for col, (code, title, source, vars) in zip([d1,d2,d3,d4], data_layers):
    with col:
        st.markdown(f"""
        <div class='method-card' style='text-align:center;'>
            <div style='color:#52B788; font-weight:700; margin-bottom:5px;'>{code}</div>
            <div style='color:#D8F3DC; font-weight:600; font-size:1.1rem;'>{title}</div>
            <div style='font-size:0.8rem; opacity:0.7; margin:5px 0;'>{source}</div>
            <div style='margin-top:10px;'><span class='mono-tag'>{vars}</span></div>
        </div>
        """, unsafe_allow_html=True)

# ── 3. Full Notebook Pipeline ──────────────────────────────────────────
st.markdown("<div class='sec-h'>📓 10-Notebook Research Pipeline</div>", unsafe_allow_html=True)

st.markdown("""
<table class='dark-table'>
    <thead>
        <tr>
            <th style='width:12%'>NOTEBOOK</th>
            <th style='width:28%'>TITLE</th>
            <th style='width:15%'>KEY OUTPUT</th>
            <th>DESCRIPTION</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class='mono-tag'>NB01</span></td>
            <td><strong>EDA & Data Cleaning</strong></td>
            <td><span class='mono-tag'>india_green_final.csv</span></td>
            <td>Processes OBD-II telemetry, EV BMS logs and India Logistics dataset (25,000 shipments). Handles outliers, normalises features.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB02</span></td>
            <td><strong>Model Training & Validation</strong></td>
            <td><span class='mono-tag'>model_thermal_co2.pkl · model_ev_eu_efficiency.pkl</span></td>
            <td>Trains <strong>GradientBoosting</strong> (ICE, R²=0.79) on OBD-II telemetry and <strong>Ridge+PolynomialFeatures(2)</strong> (EV, R²≈0.77) on EU BEV certified specs (Mai et al. 2025). Iterative feature engineering across 7 model versions. EV Trip data (evtripdata.csv) was excluded due to algebraic data leakage.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB03</span></td>
            <td><strong>Fleet Simulation</strong></td>
            <td><span class='mono-tag'>india_sim_results.csv</span></td>
            <td>Applies both ML models to all 25,000 shipments. Confirms Pearson r=0.57 between cost and CO₂ (p&lt;0.001). Baseline for all downstream analyses.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB04</span></td>
            <td><strong>AI Fleet Advisor</strong></td>
            <td><span class='mono-tag'>nb04_batch_matrix.csv</span></td>
            <td><strong>Gemini 2.5 Flash</strong> translates numerical ML results into managerial insights. Interactive widget for real-time scenario exploration; batch matrix of all SLA × traffic combinations.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB05</span></td>
            <td><strong>SHAP Causal Analysis</strong></td>
            <td><span class='mono-tag'>SHAP summary & dependence plots</span></td>
            <td>TreeExplainer on the ICE GradientBoosting model. Identifies <em>engine_stress</em> and <em>kinetic_power</em> as the two primary drivers of the Same-Day CO₂ penalty. Provides causal (not just correlational) evidence for H1.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB06</span></td>
            <td><strong>Fleet Electrification Scenarios</strong></td>
            <td><span class='mono-tag'>fleet_kpis.json · scenario matrices</span></td>
            <td>Three strategic levers: <strong>Scenario A</strong> (SLA downgrade — commercial lever), <strong>Scenario B</strong> (0→100% electrification curve), <strong>Scenario C</strong> (hybrid matrix — diminishing marginal returns). EU ETS carbon pricing at €65/tonne.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB07</span></td>
            <td><strong>Agentic AI Dispatch</strong></td>
            <td><span class='mono-tag'>agentic_decisions.csv · daily reports</span></td>
            <td><strong>Gemini 2.5-Pro</strong> as autonomous dispatch agent: receives raw orders, autonomously calls ML tools (calc_ice, calc_ev, get_traffic), tracks CO₂ budget and fleet EV range. True agentic reasoning with 4–6 tool calls per order.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB08</span></td>
            <td><strong>Amazon LMRRC Validation</strong></td>
            <td><span class='mono-tag'>amazon_sim_results.csv</span></td>
            <td>External robustness check on <strong>904,527 real Amazon stops</strong> across 6,112 routes in 5 US cities. Haversine × 1.35 road-factor for realistic last-mile distances. Confirms H1 pattern generalises to a Western, large-scale dataset.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB09</span></td>
            <td><strong>Topological Analysis — Urban</strong></td>
            <td><span class='mono-tag'>thesis_result_map_urban.html</span></td>
            <td>OpenStreetMap road network for <strong>Rome EUR</strong> (3.5 km radius). Nearest-neighbour routing for 20 drops: Consolidated Loop vs Fragmented Express (batches of 5). Traffic multipliers by departure hour.</td>
        </tr>
        <tr>
            <td><span class='mono-tag'>NB10</span></td>
            <td><strong>Topological Analysis — Rural</strong></td>
            <td><span class='mono-tag'>thesis_result_map_rural.html</span></td>
            <td>OpenStreetMap road network for <strong>Castelli Romani</strong> (5 km radius). Same methodology as NB09 on low-density terrain. Demonstrates that rural fragmentation can <em>triple</em> the CO₂ penalty vs urban, validating H3.</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# ── 4. Hybrid Fleet Strategy ───────────────────────────────────────────
st.markdown("<div class='sec-h'>🚛 Hybrid Fleet Reconstruction</div>", unsafe_allow_html=True)
st.markdown("""
Due to data availability constraints, a **Hybrid Strategy** was employed: real telemetry for core vehicles
and physics-based scaling for edge cases.
""")

st.markdown("""
<table class='dark-table'>
    <thead>
        <tr>
            <th style='width:20%'>VEHICLE CLASS</th>
            <th style='width:20%'>DATA ORIGIN</th>
            <th>METHODOLOGY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Thermal Van</strong></td>
            <td><span class='mono-tag' style='color:#52B788; border-color:#52B788;'>REAL DATA</span></td>
            <td>Direct telemetry from Fiat Ducato / Ford Transit (Diesel Euro 6).</td>
        </tr>
        <tr>
            <td><strong>Electric Van</strong></td>
            <td><span class='mono-tag' style='color:#52B788; border-color:#52B788;'>REAL DATA</span></td>
            <td>BMS Logs from Mercedes eSprinter operations in Milan.</td>
        </tr>
        <tr>
            <td><strong>E-Scooter</strong></td>
            <td><span class='mono-tag' style='color:#52B788; border-color:#52B788;'>REAL DATA</span></td>
            <td>Telemetry from Askoll eS3 shared mobility fleet (Rome). Note: used for ICE scooter benchmark; EV consumption model uses certified BEV specs (Mai et al. 2025), not BMS logs.</td>
        </tr>
        <tr>
            <td><strong>E-Cargo Bike</strong></td>
            <td><span class='mono-tag' style='color:#E65100; border-color:#E65100; background:rgba(230,81,0,0.1);'>SYNTHETIC</span></td>
            <td><strong>Down-scaling:</strong> Derived from E-Scooter by reducing mass (-40%) and capping speed at 25 km/h (physics-based Newton 2nd Law).</td>
        </tr>
        <tr>
            <td><strong>Heavy Truck</strong></td>
            <td><span class='mono-tag' style='color:#E65100; border-color:#E65100; background:rgba(230,81,0,0.1);'>SYNTHETIC</span></td>
            <td><strong>Up-scaling:</strong> Derived from Van ICE by increasing drag coefficient and mass ratio (Newton's 2nd Law + fuel-consumption scaling).</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# ── 5. Modeling ────────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>🤖 Predictive Modeling</div>", unsafe_allow_html=True)

m1, m2 = st.columns(2, gap="large")

with m1:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>ICE</div>
        <div class='card-head' style='color:#E65100;'>Gradient Boosting (XGBoost)</div>
        <p><strong>Why:</strong> Combustion efficiency is non-linear (optimal at ~2000 RPM). Trees capture these thresholds better than linear regression.</p>
        <div style='margin-top:1rem;'>
            <span class='mono-tag' style='color:#E65100; border-color:#E65100;'>Target: gCO₂/sec</span>
            <span class='mono-tag' style='color:#E65100; border-color:#E65100;'>R²: 0.79</span>
        </div>
        <p style='color:#95D5B2; font-size:.85rem; margin-top:.8rem;'>
            SHAP analysis (NB05) confirms <em>engine_stress</em> and <em>kinetic_power</em> as top drivers.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>EV</div>
        <div class='card-head' style='color:#52B788;'>Ridge + PolynomialFeatures(2)</div>
        <p><strong>Why:</strong> With only ~80–160 certified BEV variants, tree-based models overfit severely (Δ train-test ≈ 0.32). Ridge regression with degree-2 polynomial features generalises better on small, low-noise technical datasets.</p>
        <div style='margin-top:1rem;'>
            <span class='mono-tag'>Target: Wh/km (Energy consumption)</span>
            <span class='mono-tag'>R²: ≈0.77</span>
        </div>
        <p style='color:#95D5B2; font-size:.85rem; margin-top:.8rem;'>
            Dataset: Mai et al. (2025) <em>Scientific Data</em> 12, 1449 — EU_Variant_2023 (WLTP, ~80 BEV variants). CN_VAC_2023 (CLTC) used as secondary baseline only. Grid intensity: 233 g CO₂/kWh (EU 2024, Eurostat).
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── 6. SLA Logic ───────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>⏱️ SLA Simulation Logic</div>", unsafe_allow_html=True)
st.markdown("Urgency is quantified by modifying physical constraints in the model at prediction time.")

st.markdown("""
<table class='dark-table'>
    <thead>
        <tr>
            <th>SLA PROFILE</th>
            <th>DESCRIPTION</th>
            <th>PHYSICAL IMPACT (MODEL INPUT)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Standard (3-5 days)</strong></td>
            <td>Consolidated milk-run</td>
            <td><span class='mono-tag'>Baseline</span> Optimal cruising speed, high fill-rate (~95%).</td>
        </tr>
        <tr>
            <td><strong>Next-Day (24-48h)</strong></td>
            <td>Moderate urgency</td>
            <td>Slightly aggressive routing, moderate consolidation (~70% fill-rate).</td>
        </tr>
        <tr>
            <td><strong>Express (&lt;24h)</strong></td>
            <td>Time-slotted delivery</td>
            <td><span class='mono-tag'>+20% Accel</span> Higher RPM/Current, minimal idling, ~40% fill-rate.</td>
        </tr>
        <tr>
            <td><strong>Same-Day (&lt;4h)</strong></td>
            <td>Point-to-point dispatch</td>
            <td><span class='mono-tag'>+40% Accel</span> Aggressive driving, single-parcel trips (~30% fill-rate). Forces peak-hour traffic exposure.</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# ── 7. Scenario Framework ──────────────────────────────────────────────
st.markdown("<div class='sec-h'>🌍 Strategic Scenario Framework (NB06)</div>", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3, gap="large")

with s1:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>A</div>
        <div class='card-head'>SLA Downgrade</div>
        <p style='color:#B7E4C7;'>The <strong>commercial lever</strong>. Forces all Express/Same-Day orders to Standard routing with zero vehicle change. Quantifies the pure cost of urgency.</p>
        <div style='margin-top:1rem;'><span class='mono-tag'>0% EV fleet required</span></div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>B</div>
        <div class='card-head'>Full Electrification</div>
        <p style='color:#B7E4C7;'>The <strong>technology lever</strong>. Progressive 0→100% EV substitution in 10% steps, maintaining current SLA distribution. Produces the decarbonisation curve.</p>
        <div style='margin-top:1rem;'><span class='mono-tag'>SLA unchanged</span></div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>C</div>
        <div class='card-head'>Hybrid Matrix</div>
        <p style='color:#B7E4C7;'>Both levers combined. SLA savings apply only to the remaining thermal fraction — EVs are essentially immune to urgency stress, so slowing them yields negligible benefit.</p>
        <div style='margin-top:1rem;'><span class='mono-tag'>Diminishing marginal returns</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='ins-box'>
    💰 <strong>Financial translation:</strong> EU ETS carbon pricing at <strong>€65/tonne</strong> (2024 transport average).
    All three scenarios are evaluated in both kg CO₂ saved and € financial benefit for the operator.
</div>
""", unsafe_allow_html=True)

# ── 8. External Validation ─────────────────────────────────────────────
st.markdown("<div class='sec-h'>🌐 External Validation — Amazon LMRRC (NB08)</div>", unsafe_allow_html=True)

v1, v2 = st.columns([1.5, 1])

with v1:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>NB08</div>
        <div class='card-head'>Cross-Dataset Robustness Check</div>
        <p style='color:#B7E4C7; line-height:1.6;'>
            The EcoFleet ML models (trained on Indian OBD-II data) are applied to the 
            <strong>Amazon Last Mile Routing Research Challenge (LMRRC)</strong> — 
            <strong>904,527 delivery stops</strong> across 6,112 routes in 5 US cities 
            (Austin, Boston, Chicago, Los Angeles, Seattle).
        </p>
        <p style='color:#B7E4C7; line-height:1.6; margin-top:.7rem;'>
            Distances are reconstructed via <strong>Haversine formula × 1.35</strong> road-tortuosity factor.
            Feature engineering maps Amazon variables to the NB03 schema, with a +0.30 stop-and-go 
            stress base for urban last-mile cycles.
        </p>
        <div style='margin-top:1rem;'>
            <span class='mono-tag'>904,527 stops</span>
            <span class='mono-tag'>6,112 routes</span>
            <span class='mono-tag'>5 US cities</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with v2:
    st.markdown("""
    <div class='ins-box' style='height:100%;'>
        <strong>NB03 (India) vs NB08 (Amazon) — Key Comparison</strong>
        <table style='width:100%; margin-top:1rem; font-size:.85rem;'>
            <tr style='color:#52B788;'>
                <td><strong>Metric</strong></td>
                <td><strong>India (NB03)</strong></td>
                <td><strong>Amazon (NB08)</strong></td>
            </tr>
            <tr><td>ICE g/km</td><td>182.2</td><td>~210 (stop-and-go)</td></tr>
            <tr><td>EV g/km</td><td>27.7</td><td>similar</td></tr>
            <tr><td>EV reduction</td><td>84.8%</td><td>confirms ≈85%</td></tr>
            <tr><td>Same-Day ICE penalty</td><td>+29.3%</td><td>same direction</td></tr>
        </table>
        <p style='margin-top:1rem; font-size:.82rem;'>
            ✓ Cross-dataset consistency confirms model robustness beyond training distribution.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── 9. Topological Analysis ────────────────────────────────────────────
st.markdown("<div class='sec-h'>🗺️ Real-Road Topology (NB09 / NB10)</div>", unsafe_allow_html=True)

t1, t2 = st.columns(2, gap="large")

with t1:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>NB09</div>
        <div class='card-head'>Urban Network — Rome EUR</div>
        <p style='color:#B7E4C7;'>3.5 km radius · OSMnx drive graph · 20 random delivery nodes.<br>
        Hub: Poste Italiane CPD EUR (41.856°N, 12.474°E).<br>
        Traffic multipliers: gridlock ×1.8 (8–9h, 17–19h), heavy ×1.3 (10–16h).</p>
        <div style='margin-top:.8rem;'>
            <span class='mono-tag'>ICE Standard: 158.8 g/km</span>
            <span class='mono-tag'>ICE Express: 205.3 g/km</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    st.markdown("""
    <div class='method-card'>
        <div class='step-num'>NB10</div>
        <div class='card-head'>Rural Network — Castelli Romani</div>
        <p style='color:#B7E4C7;'>5 km radius · Low-density terrain between Frascati and Grottaferrata.<br>
        Hub: isolated peripheral warehouse (41.815°N, 12.660°E).<br>
        Same traffic model applied. Each unmet consolidation = massive empty-km penalty.</p>
        <div style='margin-top:.8rem;'>
            <span class='mono-tag'>Rural multiplier vs Urban</span>
            <span class='mono-tag'>Up to ×3 CO₂ penalty</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='ins-box'>
    🗺️ <strong>Routing methodology:</strong> Nearest-Neighbour Heuristic on the OSMnx shortest-path graph.
    <strong>Scenario A (Standard)</strong>: one consolidated loop from the hub covering all 20 drops.
    <strong>Scenario B (Express)</strong>: 4 fragmented trips of max 5 drops each, departing at different hours.
    The emission gap between scenarios is the measurable cost of dispatch fragmentation.
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)
st.markdown("---")

f1, f2 = st.columns([3, 1])
with f1:
    st.markdown("""
    <div style='font-family:JetBrains Mono,monospace;font-size:.75rem;color:#52B788; opacity:0.7;'>
        METHODOLOGY VERIFIED AGAINST UK GOV GHG REPORTING PROTOCOLS (2024)<br>
        Master's Thesis in Data Science & Management · Denise Di Franza · LUISS University
    </div>
    """, unsafe_allow_html=True)
with f2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")