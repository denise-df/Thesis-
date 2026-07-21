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

    # MENU CORRETTO BASATO SUI NOMI REALI DEI FILE
    nav = [
        ("🚗 Simulator", "Simulator", "pages/1 Fleet Impact Simulator.py"),
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
.status-pill { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.68rem; padding:.15rem .6rem; border-radius:12px; margin-right:.4rem; }
.status-ml { background: rgba(82,183,136,.18); color:#52B788; border:1px solid rgba(82,183,136,.4); }
.status-fallback { background: rgba(230,81,0,.12); color:#E65100; border:1px solid rgba(230,81,0,.35); }

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
    
    ice_filename = "model_thermal_co2.pkl"
    ev_filename = "model_ev_eu_efficiency.pkl"
    
    # Costruiamo i percorsi
    search_dirs = [base.parent, base, Path(".")]
    
    model_ice = None
    model_ev = None
    ice_error = None
    
    # Cerca e carica il modello termico (con cattura dell'errore)
    for d in search_dirs:
        p = d / ice_filename
        if p.exists():
            try:
                model_ice = joblib.load(str(p))
                break
            except Exception as e:
                ice_error = str(e)
                
    # Cerca e carica il modello elettrico
    for d in search_dirs:
        p = d / ev_filename
        if p.exists():
            try:
                model_ev = joblib.load(str(p))
                break
            except Exception:
                pass
                
    # Determina lo stato per l'interfaccia
    if model_ice is not None and model_ev is not None:
        status = "✅ ML models loaded and active"
    elif model_ice is None and model_ev is not None:
        err_msg = f" (Error: {ice_error})" if ice_error else " (File not found)"
        status = f"⚠️ Partial ML load — ICE: fallback{err_msg} · EV: active"
    elif model_ice is not None and model_ev is None:
        status = "⚠️ Partial ML load — ICE: active · EV: fallback"
    else:
        status = "⚙️ Physics simulation active (place .pkl files to enable ML)"
        
    return model_ice, model_ev, status
    
model_ice, model_ev, model_status = load_models()

# VEHICLES: "scale" is the physics-fallback size factor for ICE vehicles.
# For EV vehicles, "ice_equivalent" points to the ICE vehicle of the same
# size class — used both by the physics fallback and by the traffic/SLA
# modulation applied on top of the EV model's static prediction (see note
# on EV_STRESS_DAMPENING below).
VEHICLES = {
    "Electric Bike":   {"icon": "🚴", "type": "EV",  "scale": 0.15, "src": "Rome Shared Mobility",
                         "ice_equivalent": "Thermal Scooter",
                         "ev_specs": {"Battery capacity (kWh)": 1.0, "Curb weight (kg)": 25,
                                      "Electric range (km)": 60, "Segment": 0, "Battery_Chem_Code": 0,
                                      "Energy density (Wh/kg)": 150}},
    "Electric Van":    {"icon": "🚐", "type": "EV",  "scale": 1.4, "src": "Milan BMS Logs",
                         "ice_equivalent": "Thermal Van",
                         # Matches Table 3.2's own Electric Van baseline (147.5 Wh/km raw,
                         # 2,200 kg, 75 kWh LFP battery) instead of an arbitrary guess.
                         "ev_specs": {"Battery capacity (kWh)": 75, "Curb weight (kg)": 2200,
                                      "Electric range (km)": 300, "Segment": 2, "Battery_Chem_Code": 1,
                                      "Energy density (Wh/kg)": 160}},
    "Thermal Scooter": {"icon": "🏍️", "type": "ICE", "scale": 0.65, "src": "India Urban Fleet"},
    "Thermal Van":     {"icon": "🚚", "type": "ICE", "scale": 1.8, "src": "Fiat Ducato OBD-II"},
    "Thermal Truck":   {"icon": "🚛", "type": "ICE", "scale": 3.5, "src": "7.5t Rigid Diesel"},
}

# The EV Ridge model (FEATS_EV / FEATS_EU) is trained ONLY on vehicle specs
# (battery, weight/range, segment, chemistry) — it has NO traffic or SLA
# feature and cannot respond to those inputs by itself. To keep the
# simulator interactive while staying honest about what the model can and
# can't do, we scale its static Wh/km output by a small, explicitly
# labelled multiplier tied to the validated finding that EV emissions are
# far less traffic-sensitive than ICE (Appendix B.3: ICE +55% vs EV +11%
# in congestion) — this modulation is NOT part of the trained model.
EV_STRESS_DAMPENING = 0.15

def get_physics(traffic, sla, dist_km, stress_override=None):
    t_map = {"Light": 1.0, "Moderate": 1.3, "Heavy": 1.8, "Gridlock": 2.5}
    s_map = {"Standard": 1.0, "Two-Day": 1.05, "Express": 1.28, "Same-Day": 1.55}
    stress = stress_override if stress_override is not None else t_map[traffic] * s_map[sla]
    avg_kmh  = max(5, 50 / stress)
    dur_h    = dist_km / avg_kmh
    rpm      = 1200 + (800 * (stress - 1))
    load     = 20   + (15  * stress)
    speed_mps = avg_kmh / 3.6
    # Expected value of |N(0, 0.12*stress)|, matching the stochastic
    # acceleration model used in NB03 to build the simulated training data.
    acceleration = 0.7979 * (0.12 * stress)
    kinetic_power = speed_mps * max(0, acceleration)
    return {"kmh": avg_kmh, "sec": dur_h * 3600, "h": dur_h,
            "rpm": rpm, "load": load, "stress": stress,
            "speed_mps": speed_mps, "acceleration": acceleration,
            "kinetic_power": kinetic_power}

def _ice_fallback_kg(scale, p):
    return ((p["rpm"] * p["load"]) / 150_000 * p["sec"] * scale) / 1000

def _ev_fallback_kg(ice_equivalent_scale, real_stress, dist_km):
    ev_stress = 1 + (real_stress - 1) * EV_STRESS_DAMPENING
    p = get_physics(None, None, dist_km, stress_override=ev_stress)
    ice_equiv_kg = _ice_fallback_kg(ice_equivalent_scale, p)
    return ice_equiv_kg * 0.20  # 1 - 0.80 validated ICE->EV reduction (external validation, Amazon)

def calc_co2(veh_name, traffic, sla, dist_km):
    """Returns (kg CO2, source). Tries the real trained model first (with a
    plausibility check on its output); falls back to the physics heuristic
    otherwise. NOTE: scale is applied exactly ONCE — either inside the ML
    branch (on top of the model's own g/s or Wh/km output) or inside the
    fallback branch — never both, unlike the previous version."""
    v = VEHICLES[veh_name]
    t_map = {"Light": 1.0, "Moderate": 1.3, "Heavy": 1.8, "Gridlock": 2.5}
    s_map = {"Standard": 1.0, "Two-Day": 1.05, "Express": 1.28, "Same-Day": 1.55}
    real_stress = t_map[traffic] * s_map[sla]
    p = get_physics(traffic, sla, dist_km)

    if v["type"] == "ICE":
        if model_ice is not None:
            try:
                X = pd.DataFrame([{
                    "Speed_mps": p["speed_mps"],
                    "Acceleration": p["acceleration"],
                    "Kinetic_Power": p["kinetic_power"],
                    "RPM": p["rpm"],
                    "Load_Pct": p["load"],
                    "Engine_Stress": p["rpm"] * p["load"],
                    "Road_Grade": 0.0,
                }])
                g_per_sec = float(model_ice.predict(X)[0])
                if 0 < g_per_sec < 50:
                    return (g_per_sec * p["sec"] * v["scale"]) / 1000, "ml"
            except Exception:
                pass
        return _ice_fallback_kg(v["scale"], p), "fallback"
    else:
        if model_ev is not None:
            specs = v["ev_specs"]
            for cols in (
                ["Battery capacity (kWh)", "Electric range (km)", "Segment", "Battery_Chem_Code"],
                ["Battery capacity (kWh)", "Curb weight (kg)", "Segment",
                 "Battery_Chem_Code", "Energy density (Wh/kg)"],
            ):
                try:
                    X = pd.DataFrame([{c: specs[c] for c in cols}])
                    wh_km = float(model_ev.predict(X)[0])
                    if 0 < wh_km < 500:
                        ev_stress = 1 + (real_stress - 1) * EV_STRESS_DAMPENING
                        return (dist_km * wh_km * ev_stress / 1000) * GLOBAL_GRID_INTENSITY, "ml"
                except Exception:
                    continue
        return _ev_fallback_kg(VEHICLES[v["ice_equivalent"]]["scale"], real_stress, dist_km), "fallback"

st.markdown("""
<div class='fleet-hero'>
    <div class='fleet-eyebrow'>Predictive Analytics · Global Benchmarks</div>
    <div class='fleet-title'>Carbon Emission Prediction</div>
    <p class='fleet-sub'>
        Hybrid ML + physics emission prediction: uses the trained ICE Gradient Boosting
        and EV Ridge models when available, with a physics-based fallback otherwise.
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
    co2_total, co2_source = calc_co2(st.session_state.sim_veh, traffic, sla, dist)

    pill_cls = "status-ml" if co2_source == "ml" else "status-fallback"
    pill_txt = "🧠 ML model" if co2_source == "ml" else "⚙️ physics fallback"
    st.markdown(f"<span class='status-pill {pill_cls}'>{pill_txt}</span>", unsafe_allow_html=True)

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
