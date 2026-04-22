import streamlit as st

st.set_page_config(
    page_title="Glossary | EcoFleet Analytics",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Navigation ─────────────────────────────────────────────────────────
def render_navigation(current_page="Glossary"):
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

render_navigation("Glossary")

# ── CSS ────────────────────────────────────────────────────────────────
# Tema: sfondo verde molto chiaro (#E8F5E9), testo dark-green
# Unico rispetto alle altre pagine: è il solo con sfondo CHIARO
# Ma rimane completamente nel brand verde
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #E8F5E9 !important;
    color: #1B4332 !important;
}
.stApp { background: linear-gradient(160deg, #E8F5E9 0%, #C8E6C9 100%) !important; }

/* ── hero ── */
.gloss-hero {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
    border-radius: 16px;
    padding: 3rem 3rem 2.5rem 3rem;
    margin: 2rem 0 3rem 0;
    position: relative;
    overflow: hidden;
}
.gloss-hero::after {
    content: '📖';
    position: absolute;
    right: 2.5rem;
    top: 1.5rem;
    font-size: 6rem;
    opacity: .12;
    pointer-events: none;
}
.gloss-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    letter-spacing: 3px;
    color: #95D5B2;
    text-transform: uppercase;
    margin-bottom: .8rem;
}
.gloss-title {
    font-size: 3rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
    margin-bottom: .8rem;
}
.gloss-sub {
    font-size: 1.05rem;
    color: #B7E4C7;
    line-height: 1.7;
    max-width: 600px;
}

/* ── category header ── */
.cat-header {
    background: linear-gradient(135deg, #2D6A4F, #40916C);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 3rem 0 1.5rem 0;
    font-size: 1.2rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: .8rem;
}
.cat-count {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: .2rem .8rem;
    font-size: .78rem;
    font-weight: 500;
}

/* ── term card ── */
.term-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    border-left: 4px solid #2D6A4F;
    box-shadow: 0 2px 12px rgba(27,67,50,0.08);
    transition: box-shadow .2s ease, transform .2s ease, border-left-color .2s ease;
}
.term-card:hover {
    box-shadow: 0 8px 28px rgba(27,67,50,0.14);
    transform: translateX(4px);
    border-left-color: #52B788;
}
.term-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1B4332;
    margin-bottom: .4rem;
    display: flex;
    align-items: center;
    gap: .5rem;
    flex-wrap: wrap;
}
.term-abbr {
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    background: #1B4332;
    color: #95D5B2;
    padding: .2rem .55rem;
    border-radius: 4px;
}
.term-def {
    font-size: .98rem;
    color: #40916C;
    font-style: italic;
    border-left: 3px solid #95D5B2;
    padding-left: 1rem;
    margin: .7rem 0 1.1rem 0;
    line-height: 1.6;
}
.term-body {
    font-size: .95rem;
    color: #2D6A4F;
    line-height: 1.75;
}
.term-body strong { color: #1B4332; }
.term-body ul { padding-left: 1.3rem; margin: .5rem 0; }
.term-body li { margin-bottom: .35rem; }
.term-body ol { padding-left: 1.3rem; margin: .5rem 0; }

/* ── formula ── */
.formula {
    background: #1B4332;
    color: #95D5B2;
    font-family: 'JetBrains Mono', monospace;
    font-size: .88rem;
    padding: .9rem 1.2rem;
    border-radius: 6px;
    margin: .8rem 0;
    letter-spacing: .4px;
}

/* ── highlight box ── */
.hl {
    background: rgba(82,183,136,0.12);
    border: 1px solid rgba(82,183,136,0.3);
    border-radius: 6px;
    padding: .9rem 1.2rem;
    margin: .8rem 0;
    font-size: .92rem;
    color: #1B4332;
}

/* ── data tag ── */
.dtag {
    display: inline-block;
    background: #D8F3DC;
    color: #2D6A4F;
    border-radius: 4px;
    padding: .15rem .55rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .73rem;
    margin: .15rem .15rem 0 0;
    border: 1px solid #B7E4C7;
}

/* ── buttons ── */
div.stButton > button {
    background: #2D6A4F !important;
    color: #D8F3DC !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s ease !important;
}
div.stButton > button:hover {
    background: #1B4332 !important;
}

/* ── footer ── */
.gloss-footer {
    background: #1B4332;
    color: #52B788;
    font-size: .82rem;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin: 4rem 0 1rem 0;
    line-height: 1.9;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='gloss-hero'>
    <div class='gloss-eyebrow'>EcoFleet Analytics · Reference</div>
    <div class='gloss-title'>Technical Glossary</div>
    <p class='gloss-sub'>
        Definitions for every term, acronym and metric used in this platform —
        from operational logistics to machine learning and environmental science.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Helper functions ───────────────────────────────────────────────────
def cat(icon, label, n):
    st.markdown(f"""
    <div class='cat-header'>
        <span>{icon}</span>
        <span>{label}</span>
        <span class='cat-count'>{n} terms</span>
    </div>""", unsafe_allow_html=True)

def term(title, abbr, definition, body_html):
    abbr_html = f"<span class='term-abbr'>{abbr}</span>" if abbr else ""
    st.markdown(f"""
    <div class='term-card'>
        <div class='term-title'>{title} {abbr_html}</div>
        <div class='term-def'>{definition}</div>
        <div class='term-body'>{body_html}</div>
    </div>""", unsafe_allow_html=True)

def f(code):   return f"<div class='formula'>{code}</div>"
def hl(text):  return f"<div class='hl'>{text}</div>"
def tag(t):    return f"<span class='dtag'>{t}</span>"

# ── 1. OPERATIONAL TERMS ───────────────────────────────────────────────
cat("🚚", "Operational Terms", 4)

term("Service Level Agreement", "SLA",
     "The contractual delivery timeframe committed between a logistics provider and a customer.",
     """<strong>Emission impact by tier:</strong>
     <ul>
         <li><strong>Standard (3–5 days):</strong> Optimised consolidation · fill rate 80–95%</li>
         <li><strong>Next-Day (24-48h):</strong> Moderate consolidation · fill rate 60–80%</li>
         <li><strong>Express (&lt;24 h):</strong> Limited consolidation · fill rate 50–70%</li>
         <li><strong>Same-Day (&lt;4 h):</strong> Near-zero consolidation · fill rate 30–50% · peak-traffic exposure</li>
     </ul>"""
     + hl("📊 <strong>Key finding:</strong> Same-Day (<4h) generates <strong>2.4× more CO₂</strong> than Standard (3-5 days) for equivalent routes (this dataset, 15,591 trips)."))

term("Fill Rate", "",
     "Percentage of a vehicle's cargo capacity actually utilised on a delivery trip.",
     f("Fill Rate (%) = (Actual Load ÷ Maximum Capacity) × 100")
     + """<ul>
         <li>95% fill → ≈ 100 g CO₂/parcel (consolidated)</li>
         <li>50% fill → ≈ 200 g CO₂/parcel</li>
         <li>30% fill → ≈ 330 g CO₂/parcel (typical Same-Day)</li>
     </ul>
     <em>Lower fill = more trips needed = higher total emissions.</em>""")

term("Consolidation", "",
     "Grouping multiple deliveries into a single optimised route to maximise vehicle utilisation.",
     """Reduces total km · increases fill rate · lowers CO₂ per parcel by <strong>40–70%</strong> vs
     individual point-to-point trips.<br><br>
     <strong>Trade-off:</strong> requires wider delivery windows — incompatible with Same-Day SLAs.""")

term("Last-Mile Delivery", "",
     "The final segment of the logistics chain: from a distribution hub to the end customer.",
     """<strong>Why it is disproportionately carbon-intensive:</strong>
     <ul>
         <li>Frequent stop-start cycles (idling losses, acceleration spikes)</li>
         <li>High urban congestion exposure</li>
         <li>Structurally low vehicle utilisation</li>
     </ul>"""
     + hl("Last-mile represents <strong>53% of total shipping costs</strong> and <strong>41% of supply-chain CO₂</strong> despite covering only 15% of total distance. <em>(McKinsey, 2016)</em>"))

# ── 2. TECHNICAL & SENSOR ──────────────────────────────────────────────
cat("🔧", "Technical & Sensor Terms", 3)

term("On-Board Diagnostics II", "OBD-II",
     "Standardised automotive port providing real-time engine telemetry at 1 Hz sampling rate.",
     f"""<strong>Sensors used in this research:</strong>
     <ul>
         <li>{tag("MAF")} Mass Air Flow (g/s) — proportional to fuel combustion rate</li>
         <li>{tag("RPM")} Engine revolutions per minute</li>
         <li>{tag("Load%")} Engine workload 0–100%</li>
         <li>{tag("Speed")} Vehicle velocity (m/s)</li>
     </ul>
     <strong>Dataset:</strong> Fiat Ducato / Ford Transit fleet · <strong>4,187 trips</strong>.""")

term("Battery Management System", "BMS",
     "The electronic control unit monitoring and protecting an EV battery pack in real time.",
     f"""<strong>Metrics logged:</strong>
     <ul>
         <li>{tag("SOC")} State of Charge (%) — remaining battery level</li>
         <li>{tag("Power")} Instantaneous consumption (Wh)</li>
         <li>{tag("Regen")} Energy recovered via regenerative braking (kWh/trip)</li>
         <li>{tag("T_cell")} Cell temperature — affects efficiency in extreme weather</li>
     </ul>
     <strong>Dataset:</strong> Mercedes eSprinter · <strong>4,116 trips</strong> · Milan operations.""")

term("Engine Stress", "",
     "Compound variable capturing combustion intensity — the primary CO₂ predictor in the thermal model.",
     f("Engine_Stress = RPM × Load_Pct")
     + """<ul>
         <li>High RPM + High Load → maximum fuel burn (hard acceleration)</li>
         <li>Low RPM + High Load → inefficient combustion (hill climbing at low gear)</li>
     </ul>"""
     + hl("📊 <strong>Feature importance:</strong> Engine_Stress accounts for <strong>62%</strong> of CO₂ variance in the Gradient Boosting model — outranking speed and acceleration combined."))

# ── 3. ENVIRONMENTAL ───────────────────────────────────────────────────
cat("🌍", "Environmental Metrics", 4)

term("CO₂ equivalent", "CO₂e",
     "Standard unit expressing the combined warming impact of all GHGs as an equivalent mass of CO₂.",
     """<strong>Conversion factors (GWP100):</strong>
     <ul>
         <li>Methane CH₄ → <strong>28× CO₂</strong></li>
         <li>Nitrous oxide N₂O → <strong>265× CO₂</strong></li>
     </ul>
     This study reports operational (tank-to-wheel) CO₂ only.""")

term("Emission Factor", "",
     "Grams of CO₂ released per unit of fuel or energy consumed.",
     f"""<ul>
         <li>{tag("Diesel")} 2,640 g CO₂/L · stoichiometric combustion</li>
         <li>{tag("Petrol")} 2,310 g CO₂/L</li>
         <li>{tag("CNG")} 1,920 g CO₂/m³</li>
         <li>{tag("EU grid")} 233 g CO₂/kWh · 2024 average</li>
     </ul>
     <span style='font-size:.85rem;opacity:.7;'>Source: UK Government GHG Conversion Factors 2024</span>""")

term("Grid Carbon Intensity", "",
     "Grams of CO₂ emitted per kilowatt-hour of electricity generated.",
     f("EV Emissions (g/km) = (Energy kWh/km) × Grid Intensity (g/kWh)")
     + """<ul>
         <li>🇳🇴 Scandinavia: ~50 g/kWh (hydro + wind)</li>
         <li>🇪🇺 EU average: ~233 g/kWh (mixed)</li>
         <li>🇮🇳 India: ~720 g/kWh (coal-heavy)</li>
     </ul>"""
     + hl("⚠️ An EV charged on the Indian grid (~720 g/kWh) can emit <em>more</em> lifecycle CO₂/km than a modern hybrid on the Norwegian grid (~50 g/kWh)."))

term("Well-to-Wheel", "WTW",
     "Full lifecycle accounting of emissions from fuel extraction to vehicle use.",
     """<ul>
         <li><strong>Well-to-Tank (WTT):</strong> extraction, refining, electricity generation</li>
         <li><strong>Tank-to-Wheel (TTW):</strong> combustion or discharge at the vehicle</li>
     </ul>
     <strong>Scope of this study:</strong> Tank-to-Wheel operational emissions only.""")

# ── 4. MACHINE LEARNING ────────────────────────────────────────────────
cat("🤖", "Machine Learning Terms", 6)

term("R² Score", "R²",
     "Coefficient of Determination — proportion of variance in the target explained by the model.",
     """<ul>
         <li><strong>0.95–1.0:</strong> Excellent (verify for data leakage)</li>
         <li><strong>0.80–0.94:</strong> Good — typical for physical systems</li>
         <li><strong>0.60–0.79:</strong> Moderate — acceptable in social sciences</li>
         <li><strong>&lt;0.60:</strong> Poor — model fails to explain key variance</li>
     </ul>"""
     + hl("📊 <strong>This study:</strong> ICE Gradient Boosting R² = <strong>0.79</strong> · EV Random Forest R² = <strong>0.96</strong> (validated on hold-out set)."))

term("Feature Importance", "",
     "A measure of each input variable's contribution to a model's predictive accuracy.",
     """<strong>Thermal (ICE) model — top features:</strong>
     <ol>
         <li><strong>Engine_Stress (RPM × Load):</strong> 62% importance</li>
         <li><strong>Speed_mps:</strong> 21% importance</li>
         <li><strong>Acceleration:</strong> 12% importance</li>
     </ol>
     Engine stress alone explains more CO₂ variance than speed and acceleration combined.""")

term("Gradient Boosting", "",
     "An ensemble that builds trees sequentially, each correcting residual errors of the previous.",
     """<strong>Why chosen for ICE/thermal vehicles:</strong>
     <ul>
         <li>Captures non-linear combustion curves (peak efficiency ~1,800–2,200 RPM)</li>
         <li>Handles multiplicative interactions: RPM × Load × Speed</li>
         <li>Robust to stop-and-go outliers in urban driving data</li>
     </ul>"""
     + hl("Baseline: Linear Regression achieved R² = 0.42 on the same data — rejected for insufficient fit."))

term("Random Forest", "",
     "An ensemble of independently trained decision trees whose predictions are averaged.",
     """<strong>Why chosen for Electric vehicles:</strong>
     <ul>
         <li>EV consumption is largely linear with speed/distance (simpler signal)</li>
         <li>High stochastic variance from auxiliary loads (A/C, heating)</li>
         <li>Averaging across many trees provides a robust central estimate</li>
     </ul>""")

term("Cross-Validation", "k-Fold CV",
     "Evaluation technique that tests generalisation across multiple non-overlapping data splits.",
     """<strong>Protocol (k = 5):</strong>
     <ol>
         <li>Dataset split into 5 equal folds</li>
         <li>Train on 4 folds, test on the held-out fold</li>
         <li>Repeat 5 times (each fold serves as test set once)</li>
         <li>Final score = mean R² across all 5 iterations</li>
     </ol>
     Prevents overfitting: a memorising model will score poorly on held-out folds.""")

term("Data Leakage", "",
     "Unintentional inclusion of information in training data not available at prediction time.",
     """<strong>Common causes:</strong>
     <ul>
         <li>Including target-derived features (e.g. CO₂ → fuel cost → predict CO₂)</li>
         <li>Scaling using statistics from the full dataset before splitting</li>
         <li>Temporal leakage: using future observations to predict the past</li>
     </ul>"""
     + hl("🚩 <strong>Red flag:</strong> R² > 0.95 on real-world noisy data should trigger a leakage audit before publication."))

# ── 5. VEHICLE TERMINOLOGY ─────────────────────────────────────────────
cat("🚗", "Vehicle Terminology", 3)

term("Internal Combustion Engine", "ICE",
     "A power unit that converts chemical energy from fuel combustion into mechanical work.",
     f"""<strong>Key characteristics:</strong>
     <ul>
         <li><strong>Thermal efficiency:</strong> 20–30% (70–80% lost as heat and exhaust)</li>
         <li><strong>Traffic sensitivity:</strong> Very high — idling burns fuel with zero useful output</li>
         <li><strong>Emissions:</strong> Direct tailpipe (CO₂, NOₓ, particulates)</li>
     </ul>
     <strong>Fleet in this study:</strong> {tag("Thermal Van")} {tag("Thermal Truck")} {tag("Thermal Scooter")}""")

term("Electric Vehicle", "EV",
     "A vehicle propelled by electric motors powered by a rechargeable battery pack.",
     f"""<strong>Key characteristics:</strong>
     <ul>
         <li><strong>Drivetrain efficiency:</strong> 85–90% (minimal heat waste)</li>
         <li><strong>Traffic resilience:</strong> Low penalty — recovers 15–20% of kinetic energy via regenerative braking</li>
         <li><strong>Emissions:</strong> Indirect (depends on grid carbon intensity)</li>
     </ul>
     <strong>Fleet in this study:</strong> {tag("Mercedes eSprinter")} {tag("Askoll eS3")}""")

term("Light Commercial Vehicle", "LCV",
     "A goods vehicle ≤ 3.5 t GVW designed for urban freight transport.",
     f"""{tag("Ford Transit")} {tag("Fiat Ducato")} {tag("Mercedes Sprinter")} {tag("Renault Master")}<br><br>
     LCVs account for ≈ <strong>80% of last-mile delivery operations</strong> in European urban logistics.
     Electrification of LCV fleets is considered the highest-impact decarbonisation lever in urban freight.
     <span style='font-size:.83rem;opacity:.65;'>(ICCT 2023)</span>""")

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='gloss-footer'>
    <strong style='color:#D8F3DC;'>References</strong><br>
    UK Government GHG Conversion Factors 2024 &nbsp;·&nbsp;
    ICCT Clean Freight 2023 &nbsp;·&nbsp;
    European Environment Agency (EEA) &nbsp;·&nbsp;
    Chester &amp; Horvath, "Environmental assessment of passenger transportation" (2010) &nbsp;·&nbsp;
    McKinsey Global Institute, "Urban freight 2025" (2016)
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([4,1])
with c2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")