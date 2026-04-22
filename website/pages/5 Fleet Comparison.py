import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Fleet Comparison | EcoFleet Analytics",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Navigation ─────────────────────────────────────────────────────────
def render_navigation(current_page="Fleet"):
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

render_navigation("Fleet")

# ── CSS ────────────────────────────────────────────────────────────────
# Tema: dark verde profondo, accent teal-verde (#52B788 dominante)
# Leggermente più "tecnico/freddo" della Home ma stessa famiglia
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0D1F17 !important;
    color: #D8F3DC !important;
}
.stApp { background: linear-gradient(160deg, #0D1F17 0%, #152A1E 100%) !important; }

/* ── hero ── */
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

/* ── section title ── */
.sec-h {
    font-size: 1.5rem;
    font-weight: 700;
    color: #95D5B2;
    margin: 3rem 0 1.5rem 0;
    padding-bottom: .5rem;
    border-bottom: 1px solid rgba(82, 183, 136, 0.25);
}

/* ── spec card — shared ── */
.spec-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(82, 183, 136, 0.15);
    border-radius: 10px;
    padding: 1.8rem;
    height: 100%;
    transition: all .25s ease;
    position: relative;
    overflow: hidden;
}
.spec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 10px 10px 0 0;
}
.spec-card:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(82, 183, 136, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transform: translateY(-3px);
}

/* thermal = verde caldo / ICE */
.spec-card.thermal::before  { background: linear-gradient(90deg, #B7E4C7, #52B788); }
/* electric = verde brillante */
.spec-card.electric::before { background: linear-gradient(90deg, #52B788, #95D5B2); }
/* human = verde chiaro */
.spec-card.human::before    { background: linear-gradient(90deg, #95D5B2, #D8F3DC); }

.card-icon  { font-size: 2.4rem; margin-bottom: .7rem; }
.card-name  { font-size: 1.2rem; font-weight: 700; color: #D8F3DC; margin-bottom: .2rem; }
.card-model { font-family: 'JetBrains Mono', monospace; font-size: .72rem;
              color: #52B788; margin-bottom: 1rem; opacity: .8; }

/* type badges — tutti verdi ma sfumature diverse */
.badge-t  { display:inline-block; background:rgba(183,228,199,0.12); color:#B7E4C7;
            border:1px solid rgba(183,228,199,0.3); padding:.2rem .7rem;
            border-radius:4px; font-size:.7rem; font-weight:600; letter-spacing:1px; margin-bottom:1rem; }
.badge-ev { display:inline-block; background:rgba(82,183,136,0.15); color:#52B788;
            border:1px solid rgba(82,183,136,0.35); padding:.2rem .7rem;
            border-radius:4px; font-size:.7rem; font-weight:600; letter-spacing:1px; margin-bottom:1rem; }
.badge-h  { display:inline-block; background:rgba(149,213,178,0.12); color:#95D5B2;
            border:1px solid rgba(149,213,178,0.3); padding:.2rem .7rem;
            border-radius:4px; font-size:.7rem; font-weight:600; letter-spacing:1px; margin-bottom:1rem; }

.spec-row   { display:flex; justify-content:space-between; align-items:center;
              padding:.5rem 0; border-bottom:1px solid rgba(82,183,136,0.08); }
.spec-row:last-child { border-bottom:none; }
.spec-key   { font-size:.82rem; color:#52B788; font-weight:500; }
.spec-val   { font-family:'JetBrains Mono', monospace; font-size:.88rem;
              color:#D8F3DC; font-weight:500; }
.spec-val.hi { color:#95D5B2; }      /* valori buoni (EV) */
.spec-val.lo { color:#B7E4C7; }      /* valori medi */

.data-pill  { display:inline-block; background:rgba(82,183,136,0.08);
              color:#52B788; border-radius:4px; padding:.25rem .6rem;
              font-size:.7rem; font-family:'JetBrains Mono',monospace; margin-top:1rem;
              border:1px solid rgba(82,183,136,0.2); }

/* ── ranking bars ── */
.rank-row   { display:flex; align-items:center; gap:1rem;
              padding:.7rem 0; border-bottom:1px solid rgba(82,183,136,0.08); }
.rank-num   { font-family:'JetBrains Mono',monospace; font-size:1rem;
              color:#2D6A4F; width:28px; flex-shrink:0; }
.rank-name  { font-size:.9rem; font-weight:600; color:#D8F3DC; width:140px; flex-shrink:0; }
.rank-track { flex:1; background:rgba(82,183,136,0.08); border-radius:4px; height:9px; overflow:hidden; }
.rank-fill  { height:100%; border-radius:4px;
              background:linear-gradient(90deg, #2D6A4F, #52B788); }
.rank-val   { font-family:'JetBrains Mono',monospace; font-size:.85rem;
              color:#52B788; width:80px; text-align:right; flex-shrink:0; }

/* ── insight box ── */
.ins-box {
    background: rgba(82, 183, 136, 0.08);
    border-left: 4px solid #52B788;
    border-radius: 6px;
    padding: 1rem 1.4rem;
    margin: 1.5rem 0;
    font-size: .93rem;
    color: #B7E4C7;
}

/* ── buttons ── */
div.stButton > button {
    background: rgba(45, 106, 79, 0.3) !important;
    color: #95D5B2 !important;
    border: 1px solid rgba(82, 183, 136, 0.3) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s ease !important;
}
div.stButton > button:hover {
    background: rgba(45, 106, 79, 0.6) !important;
    border-color: #52B788 !important;
    color: #D8F3DC !important;
}

/* tabs */
.stTabs [data-baseweb="tab"] { color:#52B788 !important; }
.stTabs [aria-selected="true"] { color:#D8F3DC !important; }
</style>
""", unsafe_allow_html=True)

# ── Fleet data ─────────────────────────────────────────────────────────
FLEET = {
    "Thermal Van": {
        "icon":"🚚","type":"ICE","badge":"thermal",
        "model":"Fiat Ducato / Ford Transit (Euro 6D)",
        "source":"OBD-II telemetry","trips":4187,
        "co2":220,"eff":"20–30%","cap":1200,"range":600,"cost":0.45,
        "traffic":"×2.5 in gridlock","use":"Standard last-mile, inter-city",
    },
    "Electric Van": {
        "icon":"🚐","type":"EV","badge":"electric",
        "model":"Mercedes eSprinter (2024)",
        "source":"BMS logs · Milan ops","trips":4116,
        "co2":35,"eff":"85–90%","cap":900,"range":150,"cost":0.12,
        "traffic":"×1.4 (regen braking)","use":"Urban last-mile, ZEZ zones",
    },
    "Thermal Truck": {
        "icon":"🚛","type":"ICE","badge":"thermal",
        "model":"7.5 t Diesel Rigid (Euro 6)",
        "source":"Scaled from Van ICE model†","trips":4145,
        "co2":600,"eff":"18–25%","cap":3500,"range":700,"cost":0.85,
        "traffic":"×3.5 in gridlock","use":"Bulk freight, inter-city B2B",
    },
    "Thermal Scooter": {
        "icon":"🏍️","type":"ICE","badge":"thermal",
        "model":"125 cc 4-Stroke (Euro 5)",
        "source":"India fleet telemetry","trips":2080,
        "co2":65,"eff":"15–22%","cap":25,"range":150,"cost":0.08,
        "traffic":"×1.8 in gridlock","use":"Urban express, food delivery",
    },
    "Electric Bike": {
        "icon":"🚴","type":"EV","badge":"electric",
        "model":"Askoll eS3 / E-Cargo (250 W)",
        "source":"Scaled from Askoll eS3 (−40% mass, 25 km/h cap)†","trips":651,
        "co2":8,"eff":"88–92%","cap":40,"range":60,"cost":0.02,
        "traffic":"None (bike lane)","use":"Urban micro-logistics, groceries",
    },
    "Pedal Bike": {
        "icon":"🚲","type":"Human","badge":"human",
        "model":"Cargo Bike (Babboe / Urban Arrow)",
        "source":"Lifecycle food-calorie analysis","trips":412,
        "co2":21,"eff":"—","cap":80,"range":30,"cost":0.01,
        "traffic":"None (bike lane)","use":"Ultra-short urban eco-delivery",
    },
}

rows = [{"Vehicle":k,"Type":v["type"],"CO₂ g/km":v["co2"],
         "Capacity kg":v["cap"],"Range km":v["range"],
         "Cost €/km":v["cost"],"Trips":v["trips"]} for k,v in FLEET.items()]
df = pd.DataFrame(rows)
df_rank = df.sort_values("CO₂ g/km").reset_index(drop=True)

# ── Hero ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='fleet-hero'>
    <div class='fleet-eyebrow'>EcoFleet Analytics · Fleet Intelligence</div>
    <div class='fleet-title'>Six Vehicles. One Benchmark.</div>
    <p class='fleet-sub'>
        Side-by-side analysis of all 6 archetypes across emissions, efficiency, cost and
        traffic resilience — drawn from <strong>15,591 real operational trips</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Ranking ────────────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>📊 CO₂ Emissions Ranking</div>", unsafe_allow_html=True)

max_co2 = df_rank["CO₂ g/km"].max()
for i, row in df_rank.iterrows():
    pct = row["CO₂ g/km"] / max_co2 * 100
    st.markdown(f"""
    <div class='rank-row'>
        <div class='rank-num'>#{i+1}</div>
        <div class='rank-name'>{row['Vehicle']}</div>
        <div class='rank-track'><div class='rank-fill' style='width:{pct:.1f}%;'></div></div>
        <div class='rank-val'>{row['CO₂ g/km']} g/km</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='ins-box'>
    ✓ <strong>Electric Bike (8 g/km)</strong> is the lowest-emission option — lower than even the Pedal Bike
    (21 g/km lifecycle). The Thermal Truck emits <strong>75× more</strong> per km than the Electric Bike.
</div>
""", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>📈 Visual Analysis</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Emissions", "Cost vs Capacity", "Radar"])

BG   = "rgba(0,0,0,0)"
PLOT = "rgba(13,31,23,0.6)"
FONT = dict(family="Inter", color="#95D5B2")
COL  = {"ICE":"#40916C","EV":"#95D5B2","Human":"#D8F3DC"}

with tab1:
    fig = px.bar(df_rank, x="Vehicle", y="CO₂ g/km", color="Type",
                 color_discrete_map=COL, text="CO₂ g/km",
                 title="CO₂ Emissions by Vehicle (g/km)")
    fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT,
                      title_font=dict(color="#D8F3DC", size=15),
                      xaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                      yaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                      legend=dict(bgcolor="rgba(0,0,0,0.2)", bordercolor="rgba(82,183,136,0.2)"),
                      height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.scatter(df, x="Capacity kg", y="Cost €/km",
                      size="CO₂ g/km", color="Type", text="Vehicle",
                      color_discrete_map=COL, size_max=60,
                      title="Cost vs Payload Capacity (bubble = CO₂)")
    fig2.update_traces(textposition="top center")
    fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT,
                       title_font=dict(color="#D8F3DC", size=15),
                       xaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                       yaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                       height=430)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    # 1. Normalizzazione Dati
    norm = df.copy()
    norm["Eco"]      = 100 - norm["CO₂ g/km"] / norm["CO₂ g/km"].max() * 100
    norm["Capacity"] = norm["Capacity kg"] / norm["Capacity kg"].max() * 100
    norm["Range"]    = norm["Range km"] / norm["Range km"].max() * 100
    norm["Economy"]  = 100 - norm["Cost €/km"] / norm["Cost €/km"].max() * 100

    # 2. Definizione Colori (Linea HEX, Riempimento RGBA)
    # Ho convertito i tuoi colori HEX in RGBA con opacità 0.2 per evitare l'errore
    radar_config = {
        "Electric Van":  {"line": "#95D5B2", "fill": "rgba(149, 213, 178, 0.2)"},
        "Thermal Van":   {"line": "#40916C", "fill": "rgba(64, 145, 108, 0.2)"},
        "Thermal Truck": {"line": "#2D6A4F", "fill": "rgba(45, 106, 79, 0.2)"}
    }

    fig3 = go.Figure()

    # 3. Creazione Tracce
    for v, conf in radar_config.items():
        # Filtra il dataframe per il veicolo corrente
        if v in norm["Vehicle"].values:
            r = norm[norm["Vehicle"]==v].iloc[0]
            
            fig3.add_trace(go.Scatterpolar(
                r=[r["Eco"], r["Capacity"], r["Range"], r["Economy"]],
                theta=["Eco","Capacity","Range","Economy"],
                fill="toself", 
                name=v,
                line=dict(color=conf["line"], width=2),
                fillcolor=conf["fill"], # Ora usa RGBA valido
            ))

    # 4. Layout (Stile Dark mantenuto come nel tuo esempio)
    fig3.update_layout(
        polar=dict(
            bgcolor="rgba(13,31,23,0.6)",
            radialaxis=dict(
                visible=True, 
                range=[0,100],
                gridcolor="rgba(82,183,136,0.15)", 
                color="#52B788"
            ),
            angularaxis=dict(
                gridcolor="rgba(82,183,136,0.15)", 
                color="#95D5B2"
            )
        ),
        paper_bgcolor=BG, 
        font=FONT,
        legend=dict(
            bgcolor="rgba(0,0,0,0.2)", 
            bordercolor="rgba(82,183,136,0.2)"
        ),
        title=dict(
            text="Multi-Criteria Performance (0–100)",
            font=dict(color="#D8F3DC", size=15)
        ),
        height=450,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
# ── Spec cards ─────────────────────────────────────────────────────────
def render_card(name, col):
    s = FLEET[name]
    badge_cls = f"badge-{'ev' if s['type']=='EV' else 'h' if s['type']=='Human' else 't'}"
    badge_txt = {"ICE":"THERMAL · ICE","EV":"ELECTRIC · EV","Human":"HUMAN · ZERO"}[s["type"]]
    val_cls   = lambda v: "hi" if s["type"]!="ICE" else "lo"
    with col:
        st.markdown(f"""
        <div class='spec-card {s["badge"]}'>
            <div class='card-icon'>{s['icon']}</div>
            <div class='card-name'>{name}</div>
            <div class='card-model'>{s['model']}</div>
            <span class='{badge_cls}'>{badge_txt}</span>
            <div class='spec-row'><span class='spec-key'>CO₂</span>
                <span class='spec-val {val_cls("co2")}'>{s['co2']} g/km</span></div>
            <div class='spec-row'><span class='spec-key'>Efficiency</span>
                <span class='spec-val'>{s['eff']}</span></div>
            <div class='spec-row'><span class='spec-key'>Payload</span>
                <span class='spec-val'>{s['cap']:,} kg</span></div>
            <div class='spec-row'><span class='spec-key'>Range</span>
                <span class='spec-val'>{s['range']} km</span></div>
            <div class='spec-row'><span class='spec-key'>Cost</span>
                <span class='spec-val {val_cls("cost")}'>€{s['cost']}/km</span></div>
            <div class='spec-row'><span class='spec-key'>Traffic</span>
                <span class='spec-val'>{s['traffic']}</span></div>
            <div class='spec-row'><span class='spec-key'>Use case</span>
                <span class='spec-val' style='font-size:.78rem; font-family:Inter;'>{s['use']}</span></div>
            <div class='data-pill'>📡 {s['trips']:,} trips · {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='sec-h'>🔥 Thermal Fleet (ICE)</div>", unsafe_allow_html=True)
t1, t2, t3 = st.columns(3, gap="medium")
for name, col in zip([k for k,v in FLEET.items() if v["type"]=="ICE"], [t1,t2,t3]):
    render_card(name, col)

st.markdown("<div class='sec-h'>⚡ Electric &amp; Human Fleet</div>", unsafe_allow_html=True)
e1, e2, e3 = st.columns(3, gap="medium")
for name, col in zip([k for k,v in FLEET.items() if v["type"] in ["EV","Human"]], [e1,e2,e3]):
    render_card(name, col)

# ── Decision matrix ────────────────────────────────────────────────────
st.markdown("<div class='sec-h'>🎯 Decision Matrix</div>", unsafe_allow_html=True)

dm = pd.DataFrame({
    "Scenario": ["Urban < 10 km, < 20 kg","Urban 10–50 km, < 100 kg",
                 "Urban 50–100 km, < 500 kg","Inter-city > 100 km","Bulk freight > 1,000 kg",
                 "Same-Day (<4h) urgent urban","Eco-priority / ZEZ zone"],
    "Best Choice": ["Electric Bike","Electric Van","Thermal Van","Thermal Van",
                    "Thermal Truck","Thermal Scooter","Electric Bike / Pedal Bike"],
})
st.dataframe(dm, use_container_width=True, hide_index=True)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border:none;border-top:1px solid rgba(82,183,136,0.15);margin:3rem 0 1rem;'>
<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;color:#2D6A4F;line-height:2;'>
† Thermal Truck: physics-based up-scaling from Van ICE model (mass ratio × drag coefficient).<br>
† Electric Bike: physics-based down-scaling from Askoll eS3 telemetry (−40% mass, capped at 25 km/h).<br>
Sources: ICCT 2023 · UK Gov GHG Conversion Factors 2024 · Mercedes eSprinter spec sheet · Chester &amp; Horvath (2010).
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([4,1])
with c2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")