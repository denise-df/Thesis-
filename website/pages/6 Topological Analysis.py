import streamlit as st
import streamlit.components.v1 as components
import os

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Topological Analysis | EcoFleet", 
    page_icon="🗺️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Navigation ─────────────────────────────────────────────────────────
def render_navigation(current_page="Topology"):
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
    
    # [0.5, 1, 1, 1, 1, 1, 0.5] crea spazio ai bordi e c'entra i 5 bottoni
    sp1, c1, c2, c3, c4, c5, sp2 = st.columns([0.5, 1, 1, 1, 1, 1, 0.5])
    cols = [c1, c2, c3, c4, c5]

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

render_navigation("Topology")

# ── CSS (Dark Theme & Page Styles) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0D1F17 !important;
    color: #D8F3DC !important;
}
.stApp { background: linear-gradient(160deg, #0D1F17 0%, #152A1E 100%) !important; }

/* Typography */
.fleet-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem;
    letter-spacing: 3px;
    color: #52B788;
    text-transform: uppercase;
    margin-bottom: .8rem;
    margin-top: 2rem;
}
.title-text { 
    color: #D8F3DC; 
    font-weight: 800; 
    font-size: 3rem; 
    margin-bottom: 0.5rem; 
    line-height: 1.1;
}
.subtitle-text { 
    color: #95D5B2; 
    font-size: 1.05rem; 
    line-height: 1.7; 
    opacity: .85;
    margin-bottom: 2rem;
}

/* Containers */
.map-container { 
    border: 1px solid rgba(82, 183, 136, 0.2); 
    border-radius: 12px; 
    padding: 10px; 
    background: rgba(13, 31, 23, 0.6); 
    margin-top: 1rem;
}

/* Buttons */
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

# ── Header ─────────────────────────────────────────────────────────────
st.markdown("<div class='fleet-eyebrow'>SPATIAL NETWORK ANALYSIS</div>", unsafe_allow_html=True)
st.markdown("<div class='title-text'>🗺️ Topological Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Spatial impact of delivery urgency: Urban vs Rural networks</div>", unsafe_allow_html=True)

# ── Explanatory Expanders (Academic Context) ───────────────────────────
with st.expander("📚 Study Methodology & Scenarios", expanded=True):
    st.markdown("""
    **Network Routing Analysis:** This module compares two real-world operational scenarios rendered on OpenStreetMap road networks using `osmnx` and `networkx`. 
    * **🟦 Scenario A: Standard (Consolidated Loop)**. Models traditional next-day delivery. A single vehicle departs the central hub at 07:00 AM (off-peak hours) and visits all nodes via an optimized continuous path.
    * **🟥 Scenario B: Express (Fragmented Same-Day)**. Models hyper-urgent logistics. The fleet is forced to execute multiple low-density trips (batches of 5 drops), resulting in "empty return trips" to the hub and departures during heavy traffic hours (10:00, 12:00, 15:00, 18:00).
    """)

with st.expander("🧮 Mathematical Model & ML Integration", expanded=False):
    st.markdown("""
    Emissions are calculated dynamically based on real road distance, vehicle kinematics, and congestion patterns:
    
    `CO₂ (kg) = Network_Distance (km) × ML_Base_Rate (kg/km) × Congestion_Multiplier`
    
    * **Network Distance:** Calculated using Dijkstra's shortest path algorithm over the physical road infrastructure provided by OpenStreetMap.
    * **Micro-to-Macro ML Integration:** OpenStreetMap provides distances but lacks the high-frequency telematics (1 Hz speed, acceleration, engine load) required for direct, real-time ML inference. To bridge this gap, we adopt a hierarchical approach: the EcoFleet Machine Learning pipeline is pre-queried using two distinct kinematic profiles (a relaxed driving cycle and a high-stress cycle).
    * **ML Base Rates:** The expected values extracted from the models are **0.1588 kg/km** (Standard) and **0.2053 kg/km** (Express). These rates were obtained by pre-querying `model_thermal_co2.pkl` (GradientBoosting, R²=0.79, trained in NB02) with two kinematic profiles: a relaxed cycle (Standard SLA, off-peak traffic) and a high-stress cycle (Express SLA, peak-hour congestion). This methodology effectively translates microscopic AI predictions into macroscopic spatial routing, ensuring computational efficiency without losing the behavioral accuracy learned by the model.
    * **Congestion Multiplier:** Scales the final emissions according to departure time (1.0x for off-peak, up to 1.8x for rush hour gridlock).
    """)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# ── Maps Layout ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

def load_map(file_name):
    base_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(base_path)
    
    paths_to_check = [
        os.path.join(base_path, file_name),
        os.path.join(parent_path, file_name),
        file_name
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    return None

with col1:
    st.markdown("### 🌆 Urban Context (Rome, EUR)")
    st.write("High population density. Routes tend to overlap significantly, but the short overall distance partially mitigates the emission penalty caused by urgency.")
    
    map_urban = load_map("thesis_result_map_REAL_ROADS_urban.html")
    if map_urban:
        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        components.html(map_urban, height=550)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Urban map not found. Please ensure 'thesis_result_map_REAL_ROADS_urban.html' is generated via NB09 (Topological Analysis — Urban) and placed in the project root folder.")

with col2:
    st.markdown("### 🌲 Rural Context (Castelli Romani)")
    st.write("Low density. Here, the lack of consolidation is critical: every urgent or fragmented delivery generates massive amounts of empty, unproductive kilometers.")
    
    map_rural = load_map("thesis_result_map_REAL_ROADS_rural.html")
    if map_rural:
        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        components.html(map_rural, height=550)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Rural map not found. Please ensure 'thesis_result_map_REAL_ROADS_rural.html' is generated via NB10 (Topological Analysis — Rural) and placed in the project root folder.")

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# ── Key Takeaway ───────────────────────────────────────────────────────
st.success("""
    **Key Thesis Takeaway:** The analysis demonstrates that **Drop Density** acts as a powerful multiplier for the emission penalty. 
    In rural contexts, logistical urgency (such as Same-Day service) can effectively triple the carbon footprint compared to a consolidated, standard delivery schedule.
""")