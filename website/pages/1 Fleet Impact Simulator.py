import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
from pathlib import Path

st.set_page_config(
    page_title="Carbon Emission Prediction | EcoFleet Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GLOBAL_GRID_INTENSITY = 0.475  
GLOBAL_DIESEL_CO2 = 2.640      
GLOBAL_SCC = 80.0              

def render_navigation(current_page="Simulator"):
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
    
    sp1, c1, c2, c3, c4, c5, c6, sp2 = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])
    cols = [c1, c2, c3, c4, c5, c6] 

    nav = [
        ("🚗 Simulator", "Simulator", "pages/1 Carbon Emission Prediction.py"),
        ("📊 Results",   "Results",   "pages/7 Result Analysis.py"), 
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

render_navigation("Simulator")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0D1F17 !important;
    color: #D8F3DC !important;
}
.stApp { background: linear-gradient(160deg, #0D1F17 0%, #152A1E 100%) !important; }

.fleet-hero {
    border-left: 5px solid #52B788;
    padding: 2.5rem;
    margin: 2rem 0 3rem 0;
    background: rgba(82,183,136,.05);
    border-radius: 0 12px 12px 0;
}
.fleet-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem; letter-spacing: 3px;
    color: #52B788; text-transform: uppercase; margin-bottom: .8rem;
}
.fleet-title { font-size: 3rem; font-weight: 800; color: #D8F3DC; line-height: 1.1; margin-bottom: .8rem; }
.fleet-sub   { font-size: 1.05rem; color: #95D5B2; line-height: 1.7; opacity: .85; }

.sec-h {
    font-size: 1.5rem; font-weight: 700; color: #95D5B2;
    margin: 3rem 0 1.5rem 0; padding-bottom: .5rem;
    border-bottom: 1px solid rgba(82,183,136,.25);
}

.v-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(82,183,136,.15);
    border-radius: 10px; padding: 1.5rem 1rem;
    text-align: center; transition: all .2s ease; height: 100%;
}
.v-card:hover { background: rgba(255,255,255,.08); border-color: #52B788; transform: translateY(-2px); }
.v-card.active { background: rgba(45,106,79,.4); border: 2px solid #52B788; box-shadow: 0 0 15px rgba(82,183,136,.2); }
.v-icon { font-size: 2.5rem; margin-bottom: .5rem; }
.v-name { font-weight: 600; color: #D8F3DC; font-size: .9rem; margin-bottom: .2rem; }
.v-type { font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #52B788; opacity: .8; }

.control-box {
    background: rgba(13,31,23,.6);
    border: 1px solid rgba(82,183,136,.2);
    border-radius: 12px; padding: 2rem; margin-bottom: 2rem;
}
.ctrl-lbl {
    font-family: 'JetBrains Mono', monospace; color: #52B788;
    font-size: .8rem; margin-bottom: .5rem; text-transform: uppercase; letter-spacing: 1px;
}

.res-card {
    background: linear-gradient(135deg, rgba(45,106,79,.3), rgba(13,31,23,.8));
    border: 1px solid #52B788; border-radius: 12px;
    padding: 2rem; text-align: center; margin-bottom: 1rem;
}
.res-val  { font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 700; color: #D8F3DC; line-height: 1; }
.res-unit { font-size: 1.2rem; color: #52B788; margin-left: 5px; }
.res-lbl  { color: #95D5B2; font-size: .9rem; text-transform: uppercase; letter-spacing: 1px; margin-top: .5rem; }

.m-box { background: rgba(255,255,255,.04); border: 1px solid rgba(82,183,136,.15); border-radius: 8px; padding: 1rem; text-align: center; }
.m-val { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: #D8F3DC; font-weight: 600; }
.m-lbl { font-size: .7rem; color: #95D5B2; margin-top: 3px; }

.eq-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(82,183,136,.15);
    border-radius: 10px; padding: 1.2rem 1rem;
    text-align: center; transition: all .2s ease;
}
div.stButton > button {
    background: rgba(45,106,79,.3) !important; color: #95D5B2 !important;
    border: 1px solid rgba(82,183,136,.3) !important; border-radius: 8px !important;
}
div.stButton > button:hover {
    background: rgba(45,106,79,.6) !important; border-color: #52B788 !important; color: #D8F3DC !important;
}
button[kind="primary"] {
    background: linear-gradient(135deg, #2D6A4F, #40916C) !important;
    border: 1px solid #52B788 !important; color: #FFF !important;
}
</style>
""", unsafe_allow_html=True)

def format_time(hours):
    total_s = int(hours * 3600)
    m, s = divmod(total_s, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m" if h > 0 else f"{m}m {s}s"

def co2_equivalents(kg):
    return {
        "🌳": {"val": round(kg / 21.77, 1), "label": "trees needed\n1 year to absorb"},   
        "🚗": {"val": round(kg / 0.170, 1), "label": "km driven in\nan average diesel car"},
        "📱": {"val": round(kg / 0.0085, 0), "label": "smartphone\nfull charges"},         
        "🍔": {"val": round(kg / 2.5, 1),   "label": "beef burgers\nin carbon footprint"}, 
    }

@st.cache_resource(show_spinner=False)
def load_models():
    base = Path(__file__).parent
    candidates = [
        base / "model_thermal_co2.pkl",
        base.parent / "model_thermal_co2.pkl",
        Path("model_thermal_co2.pkl"),
    ]
    for p in candidates:
        if p.exists():
            try:
                ice = joblib.load(str(p))
                ev  = joblib.load(str(p).replace("thermal", "electric"))
                return ice, ev, "ML models loaded and active"
            except Exception:
                pass
    return None, None, "Physics simulation active please place pkl files to enable ML"

model_ice, model_ev, model_status = load_models()

VEHICLES = {
    "Electric Bike":   {"icon": "🚴", "type": "EV",  "scale": 0.15, "src": "Rome Shared Mobility"},
    "Electric Van":    {"icon": "🚐", "type": "EV",  "scale": 1.4, "src": "Milan BMS Logs"},
    "Thermal Scooter": {"icon": "🏍️", "type": "ICE", "scale": 0.65, "src": "India Urban Fleet"},
    "Thermal Van":     {"icon": "🚚", "type": "ICE", "scale": 1.8, "src": "Fiat Ducato OBD-II"},
    "Thermal Truck":   {"icon": "🚛", "type": "ICE", "scale": 3.5, "src": "7.5t Rigid Diesel"},
}

def get_physics(traffic, sla, dist_km):
    t_map = {"Light": 1.0, "Moderate": 1.3, "Heavy": 1.8, "Gridlock": 2.5}
    s_map = {"Standard": 1.0, "Two-Day": 1.05, "Express": 1.28, "Same-Day": 1.55}
    stress   = t_map[traffic] * s_map[sla]
    avg_kmh  = max(5, 50 / stress)
    dur_h    = dist_km / avg_kmh
    rpm      = 1200 + (800 * (stress - 1))
    load     = 20   + (15  * stress)
    return {"kmh": avg_kmh, "sec": dur_h * 3600, "h": dur_h,
            "rpm": rpm, "load": load, "stress": stress}

def calc_co2(veh_name, traffic, sla, dist_km):
    v = VEHICLES[veh_name]
    p = get_physics(traffic, sla, dist_km)
    
    if v["type"] == "ICE":
        if model_ice is not None:
            speed_mps = p["kmh"] / 3.6
            accel = 0.5 * p["stress"]
            kinetic = speed_mps * accel * v["scale"] * 1000 
            df_features = pd.DataFrame([{
                "Speed_mps": speed_mps,
                "Acceleration": accel,
                "RPM": p["rpm"],
                "Load_Pct": p["load"],
                "Engine_Stress": p["stress"] * 10000, 
                "Kinetic_Power": kinetic,
                "Road_Grade": 0.0
            }])
            pred_gs = model_ice.predict(df_features)[0]
            total_kg = (pred_gs * p["sec"]) / 1000
            return total_kg * v["scale"]
        else:
            return ((p["rpm"] * p["load"]) / 150_000 * p["sec"] * v["scale"]) / 1000
    else:
        base_consumption = 165.2 
        energy_kwh = (dist_km * base_consumption * p["stress"] * v["scale"]) / 1000
        return energy_kwh * GLOBAL_GRID_INTENSITY

st.markdown("""
<div class='fleet-hero'>
    <div class='fleet-eyebrow'>Predictive Analytics · Global Benchmarks</div>
    <div class='fleet-title'>Carbon Emission Prediction</div>
    <p class='fleet-sub'>
        Physics based emission prediction powered by real time machine learning inference
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;"
    f"color:#52B788;margin-bottom:2rem;opacity:.8;'>{model_status}</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='sec-h'>1 Select Vehicle</div>", unsafe_allow_html=True)
if "sim_veh" not in st.session_state:
    st.session_state.sim_veh = "Thermal Van"

vcols = st.columns(len(VEHICLES))
for col, (name, vdata) in zip(vcols, VEHICLES.items()):
    active = "active" if st.session_state.sim_veh == name else ""
    with col:
        st.markdown(f"""
        <div class='v-card {active}'>
            <div class='v-icon'>{vdata['icon']}</div>
            <div class='v-name'>{name}</div>
            <div class='v-type'>{vdata['type']}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Select", key=f"vbtn_{name}", use_container_width=True):
            st.session_state.sim_veh = name
            st.rerun()

st.markdown("<div class='sec-h'>2 Configure Scenario</div>", unsafe_allow_html=True)
st.markdown("<div class='control-box'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='ctrl-lbl'>📍 Distance km</div>", unsafe_allow_html=True)
    dist = st.slider("dist", 1, 200, 25, label_visibility="collapsed")
with c2:
    st.markdown("<div class='ctrl-lbl'>🚦 Traffic Intensity</div>", unsafe_allow_html=True)
    traffic = st.select_slider("traf", ["Light","Moderate","Heavy","Gridlock"],
                               value="Moderate", label_visibility="collapsed")
with c3:
    st.markdown("<div class='ctrl-lbl'>📦 Service Level Agreement</div>", unsafe_allow_html=True)
    sla = st.select_slider("sla", ["Standard","Two-Day","Express","Same-Day"],
                           value="Standard", label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("RUN PREDICTION", type="primary", use_container_width=True):
    veh_data  = VEHICLES[st.session_state.sim_veh]
    p         = get_physics(traffic, sla, dist)
    co2_total = calc_co2(st.session_state.sim_veh, traffic, sla, dist)
    
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='res-card'>
        <div class='res-val'>{co2_total:.2f}<span class='res-unit'>kg</span></div>
        <div class='res-lbl'>Predicted CO₂ Emission</div>
    </div>""", unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.markdown(f"<div class='m-box'><div class='m-val'>{format_time(p['h'])}</div><div class='m-lbl'>Duration</div></div>", unsafe_allow_html=True)
    mc2.markdown(f"<div class='m-box'><div class='m-val'>{p['kmh']:.0f}</div><div class='m-lbl'>km/h avg</div></div>", unsafe_allow_html=True)
    mc3.markdown(f"<div class='m-box'><div class='m-val'>{p['stress']:.1f}x</div><div class='m-lbl'>Stress Factor</div></div>", unsafe_allow_html=True)
    mc4.markdown(f"<div class='m-box'><div class='m-val'>{(co2_total/dist*1000):.0f}</div><div class='m-lbl'>g/km</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='sec-h' style='margin-top:2rem;'>🌿 What does this mean in real life?</div>", unsafe_allow_html=True)
    eqs = co2_equivalents(co2_total)
    eq_cols = st.columns(4)
    for col, (icon, data) in zip(eq_cols, eqs.items()):
        with col:
            st.markdown(f"""
            <div class='eq-card'>
                <div class='eq-icon' style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
                <div class='eq-val' style='font-family:JetBrains Mono, monospace; font-size:1.5rem; font-weight:700; color:#52B788;'>{data['val']:,}</div>
                <div class='eq-label' style='font-size:0.75rem; color:#95D5B2;'>{data['label'].replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)
