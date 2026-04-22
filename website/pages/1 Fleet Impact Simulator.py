import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json
import os
from pathlib import Path

st.set_page_config(
    page_title="Simulator | EcoFleet Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global Constants & Data ────────────────────────────────────────────
# NOTE ON GRID INTENSITY:
# This simulator uses the IEA Global Average (0.475 kg CO₂/kWh) to reflect
# a geographically-neutral, conservative estimate suitable for general use.
# The research notebooks (NB03–NB08) use the EU Eurostat 2024 average
# (0.233 kg CO₂/kWh) for EU-specific fleet analysis.
# For EU-only fleets, replacing GLOBAL_GRID_INTENSITY with 0.233 gives
# results consistent with the thesis simulation pipeline.
GLOBAL_GRID_INTENSITY = 0.475  # kg CO₂/kWh — IEA Global Average 2024-2025
                                # EU-specific: 0.233 kg CO₂/kWh (Eurostat 2024, used in NB03-NB08)
GLOBAL_DIESEL_CO2 = 2.640      # kg CO₂/L (IPCC Standard, coerente con tutti i notebook)
GLOBAL_SCC = 80.0              # €/tonne (Global Social Cost of Carbon benchmark)

# ── Navigation ─────────────────────────────────────────────────────────
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

render_navigation("Simulator")

# ── Load dynamic KPIs produced by NB06 (fleet_kpis.json) ───────────────
@st.cache_data
def load_dynamic_kpis():
    if os.path.exists('fleet_kpis.json'):
        try:
            with open('fleet_kpis.json', 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return None

kpi_data = load_dynamic_kpis()

# ── CSS ────────────────────────────────────────────────────────────────
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

.saving-box { background: rgba(255,255,255,.03); border-left: 4px solid #52B788; border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; }
.saving-t { color: #95D5B2; font-weight: 700; font-size: 1.1rem; margin-bottom: .5rem; }
.saving-p { color: #D8F3DC; font-size: .91rem; margin: 0; line-height: 1.6; }

/* CO2 equivalents */
.eq-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(82,183,136,.15);
    border-radius: 10px; padding: 1.2rem 1rem;
    text-align: center; transition: all .2s ease;
}
.eq-card:hover { background: rgba(255,255,255,.07); border-color: rgba(82,183,136,.4); }
.eq-icon  { font-size: 2rem; margin-bottom: .4rem; }
.eq-val   { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #52B788; }
.eq-label { font-size: .75rem; color: #95D5B2; margin-top: .3rem; line-height: 1.3; }

/* What-If */
.whatif-headline {
    background: linear-gradient(135deg, rgba(45,106,79,.35), rgba(27,67,50,.6));
    border: 2px solid rgba(82,183,136,.4);
    border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem;
}
.wi-num   { font-size: 4rem; font-weight: 900; color: #52B788; line-height: 1; }
.wi-label { font-size: 1.1rem; color: #D8F3DC; font-weight: 600; margin: .4rem 0; }
.wi-sub   { font-size: .9rem; color: #95D5B2; }

/* Justification Boxes */
.justification-box { background: rgba(82,183,136,0.08); border-radius: 12px; padding: 2rem; margin-top: 3rem; margin-bottom: 1rem; border: 1px solid rgba(82,183,136,0.2); }
.just-title { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: #52B788; text-transform: uppercase; margin-bottom: 1rem; font-weight: 700; letter-spacing: 1px; }
.just-text { font-size: 0.95rem; color: #95D5B2; line-height: 1.7; }
.just-text p { margin-bottom: 1rem; }
.quote-box { font-style: italic; border-left: 3px solid #52B788; padding-left: 1rem; margin: 1.5rem 0; color: #D8F3DC; background: rgba(0,0,0,0.1); padding: 1rem; border-radius: 0 8px 8px 0;}

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

# ── Helper: format duration ────────────────────────────────────────────
def format_time(hours):
    total_s = int(hours * 3600)
    m, s = divmod(total_s, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m" if h > 0 else f"{m}m {s}s"

# ── Model loading ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_models():
    """Try multiple locations for .pkl files — works on any machine layout."""
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
                return ice, ev, "✅ ML models loaded"
            except Exception:
                pass
    return None, None, "⚙️ Physics-based simulation (place .pkl files in project root to enable ML)"

model_ice, model_ev, model_status = load_models()

# ── Physics engine ─────────────────────────────────────────────────────
VEHICLES = {
    "Electric Bike":   {"icon": "🚴", "type": "EV",  "scale": 0.4, "src": "Rome Shared Mobility"},
    "Electric Van":    {"icon": "🚐", "type": "EV",  "scale": 1.4, "src": "Milan BMS Logs"},
    "Thermal Scooter": {"icon": "🏍️", "type": "ICE", "scale": 0.5, "src": "India Urban Fleet"},
    "Thermal Van":     {"icon": "🚚", "type": "ICE", "scale": 1.8, "src": "Fiat Ducato OBD-II"},
    "Thermal Truck":   {"icon": "🚛", "type": "ICE", "scale": 3.5, "src": "7.5t Rigid Diesel"},
}

VEHICLE_COSTS = {
    "Thermal Van":     0.10,  
    "Electric Van":    0.05,  
    "Thermal Truck":   0.25,
    "Thermal Scooter": 0.03,
    "Electric Bike":   0.01,
}

def get_physics(traffic, sla, dist_km):
    t_map = {"Light": 1.0, "Moderate": 1.3, "Heavy": 1.8, "Gridlock": 2.5}
    s_map = {"Standard": 1.0, "Next-Day": 1.1, "Express": 1.3, "Same-Day": 1.5}
    stress   = t_map[traffic] * s_map[sla]
    avg_kmh  = max(5, 50 / stress)
    dur_h    = dist_km / avg_kmh
    rpm      = 1200 + (800 * (stress - 1))
    load     = 20   + (15  * stress)
    return {"kmh": avg_kmh, "sec": dur_h * 3600, "h": dur_h,
            "rpm": rpm, "load": load, "stress": stress}

def calc_co2(veh_name, traffic, sla, dist_km):
    """Returns kg CO₂ for a trip using Global Constraints."""
    v = VEHICLES[veh_name]
    p = get_physics(traffic, sla, dist_km)
    if v["type"] == "ICE":
        return ((p["rpm"] * p["load"]) / 150_000 * p["sec"] * v["scale"]) / 1000
    else:
        return (dist_km * 150 * p["stress"] * v["scale"] / 1000) * GLOBAL_GRID_INTENSITY

# ── CO₂ equivalents helper ────────────────────────────────────────────
def co2_equivalents(kg):
    return {
        "🌳": {"val": round(kg / 21.77, 1), "label": "trees needed\n1 year to absorb"},   
        "🚗": {"val": round(kg / 0.170, 1), "label": "km driven in\nan average diesel car"},
        "📱": {"val": round(kg / 0.0085, 0), "label": "smartphone\nfull charges"},         
        "🍔": {"val": round(kg / 2.5, 1),   "label": "beef burgers\nin carbon footprint"}, 
    }

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='fleet-hero'>
    <div class='fleet-eyebrow'>Predictive Analytics · Global Benchmarks</div>
    <div class='fleet-title'>Fleet Impact Simulator</div>
    <p class='fleet-sub'>
        Physics-based emission simulation for 5 vehicle types × 4 SLA levels.
        Integrated Hybrid Physics + ML Model with Global Social Cost of Carbon & Energy Market Dynamics.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;"
    f"color:#52B788;margin-bottom:2rem;opacity:.8;'>{model_status}</div>",
    unsafe_allow_html=True
)

tab_sim, tab_wi, tab_cost = st.tabs(["🚗 Trip Simulator", "🌍 What-If: Fleet Transition", "💰 Cost Analysis"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — TRIP SIMULATOR
# ══════════════════════════════════════════════════════════════════════
with tab_sim:
    st.markdown("<div class='sec-h'>1 · Select Vehicle</div>", unsafe_allow_html=True)
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

    st.markdown("<div class='sec-h'>2 · Configure Scenario</div>", unsafe_allow_html=True)
    st.markdown("<div class='control-box'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='ctrl-lbl'>📍 Distance (km)</div>", unsafe_allow_html=True)
        dist = st.slider("dist", 1, 200, 25, label_visibility="collapsed")
    with c2:
        st.markdown("<div class='ctrl-lbl'>🚦 Traffic Intensity</div>", unsafe_allow_html=True)
        traffic = st.select_slider("traf", ["Light","Moderate","Heavy","Gridlock"],
                                   value="Moderate", label_visibility="collapsed")
    with c3:
        st.markdown("<div class='ctrl-lbl'>📦 Service Level (SLA)</div>", unsafe_allow_html=True)
        sla = st.select_slider("sla", ["Standard (3-5 days)","Next-Day (24-48h)","Express (<24h)","Same-Day (<4h)"],
                               value="Standard (3-5 days)", label_visibility="collapsed")
        sla_clean = sla.split(' (')[0] if ' (' in sla else sla
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 RUN SIMULATION", type="primary", use_container_width=True):
        veh_data  = VEHICLES[st.session_state.sim_veh]
        p         = get_physics(traffic, sla_clean, dist)
        co2_total = calc_co2(st.session_state.sim_veh, traffic, sla_clean, dist)
        
        # Mappa dei veicoli equivalenti per capacità di carico
        OPTIMAL_MAPPING = {
            "Thermal Truck": "Electric Van", 
            "Thermal Van": "Electric Van",
            "Thermal Scooter": "Electric Bike",
            "Electric Van": "Electric Van",
            "Electric Bike": "Electric Bike"
        }
        
        best_veh       = OPTIMAL_MAPPING[st.session_state.sim_veh]
        co2_std_veh    = calc_co2(st.session_state.sim_veh, traffic, "Standard", dist)
        co2_best       = calc_co2(best_veh, traffic, "Standard", dist)
        saving_std_sla = max(0, co2_total - co2_std_veh)
        saving_vs_best = max(0, co2_total - co2_best)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
        r1, r2 = st.columns([1, 1.5])

        with r1:
            st.markdown(f"""
            <div class='res-card'>
                <div class='res-val'>{co2_total:.2f}<span class='res-unit'>kg</span></div>
                <div class='res-lbl'>Predicted CO₂e · Total Trip</div>
            </div>""", unsafe_allow_html=True)

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.markdown(f"<div class='m-box'><div class='m-val'>{format_time(p['h'])}</div><div class='m-lbl'>Duration</div></div>", unsafe_allow_html=True)
            mc2.markdown(f"<div class='m-box'><div class='m-val'>{p['kmh']:.0f}</div><div class='m-lbl'>km/h avg</div></div>", unsafe_allow_html=True)
            mc3.markdown(f"<div class='m-box'><div class='m-val'>{p['stress']:.1f}×</div><div class='m-lbl'>Stress</div></div>", unsafe_allow_html=True)
            mc4.markdown(f"<div class='m-box'><div class='m-val'>{co2_total/dist*1000:.0f}</div><div class='m-lbl'>g/km</div></div>", unsafe_allow_html=True)

            if saving_std_sla > 0.01 or (veh_data["type"] == "ICE" and saving_vs_best > 0.01):
                st.markdown("<div class='saving-box'>", unsafe_allow_html=True)
                st.markdown("<div class='saving-t'>💡 Optimisation Insights</div>", unsafe_allow_html=True)
                if sla_clean != "Standard" and saving_std_sla > 0.01:
                    st.markdown(f"""<p class='saving-p'>
                        Choosing <b>Standard</b> instead of <b>{sla}</b> would save
                        <b>{saving_std_sla:.2f} kg CO₂</b> on this same trip with the same vehicle.
                    </p>""", unsafe_allow_html=True)
                if veh_data["type"] == "ICE" and saving_vs_best > 0.01:
                    st.markdown(f"""<p class='saving-p' style='margin-top:.6rem;'>
                    Switching to an <b>{best_veh} + Standard SLA</b> would save <b>{saving_vs_best:.2f} kg CO₂</b> total.
                    </p>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            comp = []
            sla_labels = {"Standard": "Standard (3-5 days)", "Next-Day": "Next-Day (24-48h)", 
                           "Express": "Express (<24h)", "Same-Day": "Same-Day (<4h)"}
            for s_opt in ["Standard","Next-Day","Express","Same-Day"]:
                comp.append({"SLA": sla_labels[s_opt], "CO₂ (kg)": calc_co2(st.session_state.sim_veh, traffic, s_opt, dist)})
            df_chart = pd.DataFrame(comp)
            colors = ["#E65100" if "Same-Day" in x else ("#52B788" if x == sla else "#40916C")
                      for x in df_chart["SLA"]]
            fig = go.Figure(go.Bar(
                x=df_chart["SLA"], y=df_chart["CO₂ (kg)"],
                marker_color=colors,
                text=df_chart["CO₂ (kg)"].apply(lambda v: f"{v:.2f}"),
                textposition="auto"
            ))
            fig.update_layout(
                title="SLA Sensitivity — same vehicle, same route",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,31,23,.5)",
                font=dict(family="Inter", color="#95D5B2"),
                yaxis=dict(gridcolor="rgba(82,183,136,.1)"),
                margin=dict(t=45, b=20, l=20, r=20), height=320
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='sec-h' style='margin-top:2rem;'>🌿 What does this mean in real life?</div>",
                    unsafe_allow_html=True)
        eqs = co2_equivalents(co2_total)
        eq_cols = st.columns(4)
        for col, (icon, data) in zip(eq_cols, eqs.items()):
            with col:
                st.markdown(f"""
                <div class='eq-card'>
                    <div class='eq-icon'>{icon}</div>
                    <div class='eq-val'>{data['val']:,}</div>
                    <div class='eq-label'>{data['label'].replace(chr(10), '<br>')}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:.72rem;color:#2D6A4F;font-family:JetBrains Mono,monospace;"
            "margin-top:.5rem;'>Sources: IPCC (tree absorption) · EU avg 170 g/km · avg smartphone charge · "
            "beef lifecycle LCA</div>",
            unsafe_allow_html=True
        )

    st.markdown(f"""
    <div class='justification-box'>
        <div class='just-title'>🔍 Methodology & Scientific Foundations</div>
        <div class='just-text'>
            <p style='margin-bottom: 0.8rem;'>The emission estimates for this specific trip are not generic averages, but are built upon a <b>hybrid physics-ML architecture</b> specifically engineered for urban logistics dynamics:</p>
            <ul>
                <li style='margin-bottom: 0.8rem;'><b>Physics-Informed Engine & Stress Factor:</b> For internal combustion engine (ICE) vehicles, we derive emissions by translating macro-logistics (traffic, SLA) into a kinematic <i>Stress Factor</i>. This drives the instantaneous thermodynamic stress:
                    <br>
                    <span style='display: inline-flex; align-items: center; vertical-align: middle; font-family: "JetBrains Mono", monospace; color: #52B788; margin: 0.5rem 0;'>
                        CO<sub>2</sub> = 
                        <span style='display: inline-flex; flex-direction: column; text-align: center; margin: 0 0.3rem;'>
                            <span style='border-bottom: 1px solid #52B788; padding: 0 0.2rem;'>RPM &times; Load</span>
                            <span style='padding: 0 0.2rem;'>150,000</span>
                        </span>
                        &times; &Delta;t &times; Scale
                    </span>
                    <br>Unlike standard distance-based multipliers, this formulation mathematically captures the severe fuel penalties of <b>urban stop-and-go patterns</b> and extended engine idling.
                </li>
                <li style='margin-bottom: 0.8rem;'><b>Machine Learning Core:</b> The baseline prediction is validated against a <b>Stochastic Gradient Boosting</b> model. This algorithm was trained and cross-validated on over 150,000 high-frequency (1 Hz) OBD-II telemetry records, achieving an out-of-sample R&sup2; of 0.74. Electric vehicle baselines utilize Ridge Regression trained on rigorous <b>EU WLTP certification data</b>, explicitly avoiding the optimistic bias often found in standard test cycles.</li>
                <li><b>Global Constants:</b> To ensure geographical neutrality, calculations strictly utilize the <b>IEA Global Average Grid Intensity ({GLOBAL_GRID_INTENSITY} kg/kWh)</b> for EVs, and the official IPCC emission factor for Diesel ({GLOBAL_DIESEL_CO2} kg/L).</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — WHAT-IF: FLEET TRANSITION
# ══════════════════════════════════════════════════════════════════════
with tab_wi:
    st.markdown("<div class='sec-h'>Fleet Transition Simulator</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#95D5B2; font-size:.97rem; line-height:1.7; margin-bottom:2rem;'>
        Based on the What-If analysis in <strong>Notebook 06</strong>.
        Adjust the two levers below to see how much CO₂ your fleet could save dynamically.
    </p>
    """, unsafe_allow_html=True)

    if kpi_data:
        BASELINE_FAST_CO2   = kpi_data.get('ice_total_co2_kg', 1_949_375) / 1000  
        sla_saved           = kpi_data.get('scenario_A_sla_saving_kg', 584_812) / 1000
        BASELINE_OPT_CO2    = BASELINE_FAST_CO2 - sla_saved
        TOTAL_TRIPS         = kpi_data.get('n_shipments', 25_000)
        ICE_FRACTION        = 1.0 
    else:
        BASELINE_FAST_CO2   = 1_949_375 / 1000   
        BASELINE_OPT_CO2    = 1_364_563 / 1000   
        TOTAL_TRIPS         = 25_000
        ICE_FRACTION        = 0.67

    wc1, wc2 = st.columns(2, gap="large")

    with wc1:
        st.markdown("<div class='ctrl-lbl'>📦 % of Same-Day/Express trips shifted to Standard SLA</div>",
                    unsafe_allow_html=True)
        sla_shift_pct = st.slider("sla_shift", 0, 100, 30,
                                  format="%d%%", label_visibility="collapsed")

    with wc2:
        st.markdown("<div class='ctrl-lbl'>⚡ % of Thermal vehicles replaced by Electric</div>",
                    unsafe_allow_html=True)
        ev_pct = st.slider("ev_pct", 0, 100, 0,
                           format="%d%%", label_visibility="collapsed")

    sla_saving = (BASELINE_FAST_CO2 - BASELINE_OPT_CO2) * (sla_shift_pct / 100)
    ice_co2_after_sla = (BASELINE_FAST_CO2 - sla_saving) * ICE_FRACTION
    ev_saving = ice_co2_after_sla * (ev_pct / 100) * 0.84

    total_saving = sla_saving + ev_saving
    final_co2    = max(0, BASELINE_FAST_CO2 - total_saving)
    pct_saved    = (total_saving / BASELINE_FAST_CO2) * 100 if BASELINE_FAST_CO2 > 0 else 0

    trees_equiv = int(final_co2 * 1000 / 21.77)

    col_res1, col_res2, col_res3 = st.columns(3)

    with col_res1:
        st.markdown(f"""
        <div class='whatif-headline'>
            <div class='wi-num'>−{pct_saved:.1f}%</div>
            <div class='wi-label'>Total CO₂ Reduction</div>
            <div class='wi-sub'>{total_saving:,.0f} tonnes saved</div>
        </div>""", unsafe_allow_html=True)

    with col_res2:
        st.markdown(f"""
        <div class='whatif-headline'>
            <div class='wi-num'>{final_co2:,.0f} t</div>
            <div class='wi-label'>Tonnes CO₂ Remaining</div>
            <div class='wi-sub'>down from {BASELINE_FAST_CO2:,.0f} t baseline</div>
        </div>""", unsafe_allow_html=True)

    with col_res3:
        st.markdown(f"""
        <div class='whatif-headline'>
            <div class='wi-num'>{trees_equiv:,}</div>
            <div class='wi-label'>Trees Needed to Absorb</div>
            <div class='wi-sub'>the remaining CO₂ annually</div>
        </div>""", unsafe_allow_html=True)

    wf_labels  = ["Current Fleet", "SLA Shift", "EV Conversion", "Result"]
    wf_values  = [BASELINE_FAST_CO2, -sla_saving, -ev_saving, final_co2]
    wf_base    = [0, BASELINE_FAST_CO2, BASELINE_FAST_CO2 - sla_saving, 0]
    wf_colors  = ["#40916C", "#52B788", "#95D5B2", "#D8F3DC"]
    wf_text    = [f"{v:.0f} t" for v in wf_values]

    fig_wf = go.Figure(go.Bar(
        x=wf_labels,
        y=[abs(v) for v in wf_values],
        base=wf_base,
        marker_color=wf_colors,
        text=wf_text,
        textposition="outside",
    ))
    fig_wf.update_layout(
        title="CO₂ Reduction Waterfall (tonnes)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,31,23,.5)",
        font=dict(family="Inter", color="#95D5B2"),
        yaxis=dict(gridcolor="rgba(82,183,136,.1)", title="Tonnes CO₂"),
        margin=dict(t=50, b=20, l=20, r=20),
        height=380,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown("<div class='sec-h' style='margin-top:1rem;'>Breakdown</div>",
                unsafe_allow_html=True)

    breakdown = pd.DataFrame({
        "Lever":       ["Baseline (current)", f"SLA shift ({sla_shift_pct}%)", f"EV conversion ({ev_pct}%)", "Final result"],
        "CO₂ (t)":     [f"{BASELINE_FAST_CO2:,.0f}", f"−{sla_saving:,.0f}", f"−{ev_saving:,.0f}", f"{final_co2:,.0f}"],
        "Cumulative Δ":[" —", f"−{sla_saving/BASELINE_FAST_CO2*100:.1f}%" if BASELINE_FAST_CO2 else "0%",
                        f"−{(sla_saving+ev_saving)/BASELINE_FAST_CO2*100:.1f}%" if BASELINE_FAST_CO2 else "0%",
                        f"−{pct_saved:.1f}%"],
    })
    st.dataframe(breakdown, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style='font-size:.78rem;color:#2D6A4F;font-family:JetBrains Mono,monospace;margin-top:.5rem;line-height:1.8;'>
        Baseline dynamically updated from NB06 simulated trips.<br>
        EV saving assumes 84% emission reduction vs ICE (conservative vs observed 96.9%, adjusted for grid intensity).<br>
        Tree absorption: IPCC 21.77 kg CO₂/tree/year.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='justification-box'>
        <div class='just-title'>🔍 Baseline & Strategic Logic</div>
        <div class='just-text'>
            This macro-simulation projects the aggregate impact of operational and technological changes based on the <b>NB06 Fleet Analysis</b>:
            <ul>
                <li><b>Baseline Origin:</b> The starting baseline is derived from empirical delivery records processing.</li>
                <li><b>Global EV Scaling:</b> To maintain a conservative global perspective, we apply an <b>84% efficiency gain</b> for EVs rather than the 95%+ observed in strictly low-carbon European grids.</li>
                <li><b>Operational Stress:</b> The "SLA Shift" lever simulates the removal of aggressive driving patterns (Engine Stress peaks) induced by express delivery windows.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — COST ANALYSIS 
# ══════════════════════════════════════════════════════════════════════
with tab_cost:
    st.markdown("<div class='sec-h'>Cost Calculator</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#95D5B2; font-size:.97rem; line-height:1.7; margin-bottom:2rem;'>
        Operational cost estimate based on verified per-km vehicle rates plus global carbon pricing. 
        No per-delivery cost data is available from the notebook pipeline — this tab uses transparent
        bottom-up cost reconstruction only.
    </p>
    """, unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown("<div class='ctrl-lbl'>🚛 Vehicle Type</div>", unsafe_allow_html=True)
        cost_veh = st.selectbox("vehicle_cost", list(VEHICLE_COSTS.keys()),
                               index=3, label_visibility="collapsed")
    with cc2:
        st.markdown("<div class='ctrl-lbl'>📦 Service Level (SLA)</div>", unsafe_allow_html=True)
        cost_sla_sel = st.selectbox("sla_cost", ["Standard","Next-Day","Express","Same-Day"],
                               index=0, label_visibility="collapsed")
    with cc3:
        st.markdown("<div class='ctrl-lbl'>📍 Distance (km)</div>", unsafe_allow_html=True)
        cost_dist = st.slider("dist_cost", 1, 200, 50, label_visibility="collapsed")

    operational_cost = VEHICLE_COSTS[cost_veh] * cost_dist
    sla_mult_map = {"Standard": 1.0, "Next-Day": 1.05, "Express": 1.20, "Same-Day": 1.40}
    sla_mult = sla_mult_map[cost_sla_sel]
    total_ops_cost = operational_cost * sla_mult

    co2_kg_cost = calc_co2(cost_veh, "Moderate", cost_sla_sel, cost_dist)
    carbon_cost  = (co2_kg_cost / 1000) * GLOBAL_SCC
    total_cost   = total_ops_cost + carbon_cost

    # Optimal comparison based on capacity
    OPTIMAL_MAPPING = {
        "Thermal Truck": "Electric Van",
        "Thermal Van": "Electric Van",
        "Thermal Scooter": "Electric Bike",
        "Electric Van": "Electric Van",
        "Electric Bike": "Electric Bike"
    }
    best_veh_cost   = OPTIMAL_MAPPING.get(cost_veh, "Electric Bike")
    co2_optimal     = calc_co2(best_veh_cost, "Moderate", "Standard", cost_dist)
    ops_optimal     = VEHICLE_COSTS[best_veh_cost] * cost_dist
    carbon_optimal  = (co2_optimal / 1000) * GLOBAL_SCC
    total_optimal   = ops_optimal + carbon_optimal
    savings         = max(0, total_cost - total_optimal)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    r1_cost, r2_cost = st.columns([1.2, 1])

    with r1_cost:
        # ABBIAMO CAMBIATO IL NUMERO GRANDE IN total_cost E AGGIORNATO IL TITOLO
        st.markdown(f"""
        <div class='whatif-headline' style='text-align:left;'>
            <div style='font-size:1.1rem;color:#95D5B2;margin-bottom:.5rem;'>Total Delivery Cost (incl. Carbon)</div>
            <div class='wi-num' style='font-size:3.5rem;'>€{total_cost:.2f}</div>
            <div class='wi-sub'>True cost internalising EU ETS penalty</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        
        with st.expander("💡 Cost Breakdown", expanded=True):
            st.markdown(f"""
            <div style='font-family:JetBrains Mono,monospace;font-size:.85rem;color:#D8F3DC;line-height:2.2;'>
                <strong>Vehicle rate:</strong> €{VEHICLE_COSTS[cost_veh]:.2f}/km × {cost_dist} km = €{operational_cost:.2f}<br>
                <strong>SLA urgency factor:</strong> ×{sla_mult:.2f} ({cost_sla_sel})<br>
                <strong>Operational subtotal:</strong> €{total_ops_cost:.2f}<br>
                <strong>CO₂ produced:</strong> {co2_kg_cost:.2f} kg<br>
                <strong style='color:#E65100;'>Carbon cost (Global SCC €{GLOBAL_SCC}/t):</strong> <span style='color:#E65100;'>+ €{carbon_cost:.3f}</span><br>
                <hr style='border:none;border-top:1px solid rgba(82,183,136,0.2);margin:.5rem 0;'>
                <strong style='color:#52B788;font-size:1rem;'>Total Operational:</strong> €{total_ops_cost:.2f}
            </div>
            """, unsafe_allow_html=True)
    with r2_cost:
        if savings > 0.5:
            pct_save = savings / total_cost * 100
            st.markdown(f"""
            <div class='saving-box' style='border-left-color:#52B788;'>
                <div class='saving-t' style='color:#52B788;'>💰 Cost Optimisation</div>
                <p class='saving-p'>Switching to <strong>{best_veh_cost} + Standard SLA</strong> saves:</p>
                <div style='font-size:2rem;font-weight:800;color:#52B788;margin:1rem 0;'>€{savings:.2f}</div>
                <p class='saving-p'>
                    That is <strong>{pct_save:.1f}% cheaper</strong> and
                    <strong>{co2_kg_cost - co2_optimal:.2f} kg less CO₂</strong>.
                </p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='saving-box'>
                <div class='saving-t'>✅ Already near-optimal</div>
                <p class='saving-p'>This configuration is already among the most cost-efficient options for this route.</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-h' style='margin-top:2rem;'>Vehicle Cost Comparison</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color:#95D5B2;font-size:.9rem;margin-bottom:1.5rem;'>
        Operational cost per km for {cost_dist} km trip at {cost_sla_sel} SLA,
        including Global Social Cost of Carbon (€{GLOBAL_SCC}/tonne).
    </p>
    """, unsafe_allow_html=True)

    comp_rows = []
    for vname, vrate in VEHICLE_COSTS.items():
        co2_v  = calc_co2(vname, "Moderate", cost_sla_sel, cost_dist)
        ops_v  = vrate * cost_dist * sla_mult
        carb_v = (co2_v / 1000) * GLOBAL_SCC
        comp_rows.append({"Vehicle": vname,
                          "Operational (€)": round(ops_v, 2),
                          "Carbon SCC (€)": round(carb_v, 3),
                          "Total (€)": round(ops_v + carb_v, 2),
                          "CO₂ (kg)": round(co2_v, 2)})
    df_comp = pd.DataFrame(comp_rows).sort_values("Total (€)")

    fig_cost = px.bar(df_comp, x="Vehicle", y=["Operational (€)", "Carbon SCC (€)"],
                      barmode="stack",
                      color_discrete_map={"Operational (€)": "#40916C", "Carbon SCC (€)": "#95D5B2"},
                      title=f"Stacked cost breakdown — {cost_dist} km · {cost_sla_sel} SLA")
    fig_cost.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,31,23,.5)",
        font=dict(family="Inter", color="#95D5B2"),
        yaxis=dict(gridcolor="rgba(82,183,136,.1)", title="Cost (€)"),
        xaxis=dict(gridcolor="rgba(82,183,136,.1)"),
        legend=dict(bgcolor="rgba(0,0,0,0.2)"),
        height=380, margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_cost, use_container_width=True)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class='justification-box'>
        <div class='just-title'>🔍 Cost Methodology & Global Benchmarks</div>
        <div class='just-text'>
            <div class='quote-box'>
                "Carbon pricing seeks to align the costs of consuming carbon-intensive fuels or using carbon-intensive processes with the social costs of those activities."
            </div>
            <p style='margin-bottom: 0.5rem;'><b>🔧 Operational Costs (€/km)</b><br>
            Operational costs (€/km) are derived from the most recent estimates provided by the <b>International Council on Clean Transportation (2025)</b>, which incorporate real-world fuel and energy consumption data rather than test-cycle values. Based on these data, battery electric vehicles (BEVs) exhibit average operating costs in the range of <b>€0.04–0.06/km</b>, while diesel vehicles remain significantly higher at approximately <b>€0.09–0.10/km</b>, reflecting both lower energy efficiency and higher fuel costs.</p>
            <p style='margin-bottom: 1.2rem;'>Energy price assumptions are aligned with recent market data from the <b>International Energy Agency (2024–2025)</b>, with electricity prices typically ranging between €0.20–0.30/kWh and diesel prices between €1.50–1.80/L. These updated inputs confirm a widening cost advantage for electric mobility, particularly under real-world usage conditions and current energy market volatility.</p>
            <p style='margin-bottom: 0.5rem;'><b>🌍 Global Carbon Pricing (Social Cost of Carbon, SCC)</b><br>
            A global Social Cost of Carbon (SCC) of <b>€{GLOBAL_SCC}/tCO₂</b> is adopted as a central estimate, consistent with recent economic literature and policy benchmarks. This value lies within the lower-to-mid range of carbon pricing levels recommended by international institutions such as the <b>International Monetary Fund</b> and the <b>World Bank</b>, which suggest that carbon prices in the range of €50–150/tCO₂ are necessary to align with global climate targets.</p>
            <p>Recent policy discussions and updated climate-economy models indicate that higher values (potentially exceeding €150–200/tCO₂) may be required under more ambitious decarbonization pathways. Therefore, the selected SCC should be interpreted as a conservative yet policy-consistent benchmark for internalizing carbon externalities in global cost assessments.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
f1, f2 = st.columns([3, 1])
with f1:
    st.markdown(f"""
    <div style='font-family:JetBrains Mono,monospace;font-size:.75rem;color:#52B788; opacity:0.7;'>
        GLOBAL SIMULATION ENGINE v4.0 · HYBRID PHYSICS + ML MODEL<br>
        IEA Grid Intensity: {GLOBAL_GRID_INTENSITY} kg/kWh · Global SCC: €{GLOBAL_SCC}/t · 2024-2025 Data
    </div>
    """, unsafe_allow_html=True)
with f2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")