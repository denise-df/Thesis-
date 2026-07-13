import streamlit as st
import plotly.graph_objects as go

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Economic Strategy | EcoFleet Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Navigation (identica alle altre pagine) ────────────────────────────
def render_navigation(current_page="Economics"):
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
        (" Simulator", "Simulator", "pages/1 Fleet Impact Simulator.py"),
        (" Topology",  "Topology",  "pages/6 Topological Analysis.py"),
        (" Fleet",     "Fleet",     "pages/5 Fleet Comparison.py"),
        (" Glossary",  "Glossary",  "pages/4 Glossary.py"),
        (" Methods",   "Methods",   "pages/3 Methodology.py"),
    ]
    for col, (label, key, page) in zip(cols, nav):
        with col:
            if st.button(label, use_container_width=True,
                         type="primary" if current_page == key else "secondary"):
                st.switch_page(page)

render_navigation("Economics")

# ── CSS (stesso tema dark verde) ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0D1F17 !important;
    color: #D8F3DC !important;
}
.stApp { background: linear-gradient(160deg, #0D1F17 0%, #152A1E 100%) !important; }

.fleet-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem; letter-spacing: 3px; color: #52B788;
    text-transform: uppercase; margin: 2rem 0 .8rem 0;
}
.title-text { color: #D8F3DC; font-weight: 800; font-size: 3rem; margin-bottom: .5rem; line-height: 1.1; }
.subtitle-text { color: #95D5B2; font-size: 1.05rem; line-height: 1.7; opacity: .85; margin-bottom: 1rem; }
.sec-h {
    font-size: 1.5rem; font-weight: 700; color: #95D5B2;
    margin: 3rem 0 1rem 0; padding-bottom: .5rem;
    border-bottom: 1px solid rgba(82, 183, 136, 0.25);
}

/* KPI cards rischio / opportunità */
.kpi-card { border-radius: 12px; padding: 1.8rem; height: 100%; }
.kpi-risk  { background: rgba(230, 81, 0, 0.10);  border-left: 4px solid #E65100; }
.kpi-opp   { background: rgba(82, 183, 136, 0.10); border-left: 4px solid #52B788; }
.kpi-label { font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:.7rem; }
.kpi-risk .kpi-label { color:#E65100; }
.kpi-opp  .kpi-label { color:#52B788; }
.kpi-num  { font-size: 2.6rem; font-weight: 800; line-height: 1.1; }
.kpi-risk .kpi-num { color:#FF8A50; }
.kpi-opp  .kpi-num { color:#95D5B2; }
.kpi-sub  { font-size: .95rem; color:#D8F3DC; opacity:.8; margin-top:.6rem; line-height:1.5; }
.kpi-co2  { font-size:.85rem; color:#95D5B2; opacity:.9; margin-top:.9rem;
            border-top:1px solid rgba(82,183,136,0.15); padding-top:.7rem; }

/* fascia CO2 proof */
.co2-proof {
    background: rgba(82,183,136,0.06); border:1px solid rgba(82,183,136,0.2);
    border-radius:10px; padding:1rem 1.3rem; margin:1.5rem 0;
    font-size:.95rem; color:#95D5B2; line-height:1.6;
}
.co2-proof b { color:#D8F3DC; }

/* metric cards fondo */
.mini-card { background: rgba(255,255,255,0.04); border:1px solid rgba(82,183,136,0.15);
             border-radius:10px; padding:1.3rem; height:100%; }
.mini-lbl  { font-size:.85rem; color:#95D5B2; opacity:.8; margin-bottom:.5rem; }
.mini-num  { font-size:1.8rem; font-weight:800; color:#D8F3DC; }
.mini-num small { font-size:.9rem; color:#95D5B2; font-weight:500; }

div.stButton > button {
    background: rgba(45,106,79,0.3) !important; color:#95D5B2 !important;
    border:1px solid rgba(82,183,136,0.3) !important; border-radius:8px !important;
}
div.stButton > button:hover {
    background: rgba(45,106,79,0.6) !important; border-color:#52B788 !important; color:#D8F3DC !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────
st.markdown("<div class='fleet-eyebrow'>STRATEGIC DECISION LAYER</div>", unsafe_allow_html=True)
st.markdown("<div class='title-text'> The Economics of Speed</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle-text'>Translating the carbon findings into a financial decision. "
    "Reference case: a typical operator — 50,000 deliveries/day, ~135 tCO₂/day "
    "(NextMile Italia, simulated on real data).</div>",
    unsafe_allow_html=True
)

# ── Blocco 1: Rischio vs Opportunità ───────────────────────────────────
st.markdown("<div class='sec-h'>Risk vs. Opportunity</div>", unsafe_allow_html=True)

col_risk, col_opp = st.columns(2)
with col_risk:
    st.markdown("""
    <div class='kpi-card kpi-risk'>
        <div class='kpi-label'>Cost of inaction</div>
        <div class='kpi-num'>€3.2M → €7.3M</div>
        <div class='kpi-sub'>Annual carbon exposure keeping the fleet 100% diesel —
            rising with the EU ETS price from 65 €/t today to 150 €/t in the 2030 scenario.</div>
        <div class='kpi-co2'> Driven by <b>135 tCO₂/day</b> ≈ <b>49,275 tCO₂/year</b> left unpriced.</div>
    </div>
    """, unsafe_allow_html=True)
with col_opp:
    st.markdown("""
    <div class='kpi-card kpi-opp'>
        <div class='kpi-label'>Value of action</div>
        <div class='kpi-num'>€2.3M → €12.85M</div>
        <div class='kpi-sub'>Annual carbon cost avoided — from SLA renegotiation alone
            (no vehicle investment) up to full fleet electrification.</div>
        <div class='kpi-co2'> Full electrification avoids <b>541,800 kg CO₂/day</b> vs. the diesel baseline.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='co2-proof'>
     <b>The proof beneath the euros.</b> Every euro figure traces back to physical emissions:
    the fleet's <b>135 tCO₂/day</b> valued at the EU ETS carbon price. CO₂ is the cause — the euro is the consequence
    a fleet manager acts on.
</div>
""", unsafe_allow_html=True)

# ── Blocco 2: Curva di decarbonizzazione (dati Tabella 4.3) ────────────
st.markdown("<div class='sec-h'>The decarbonization trajectory</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle-text'>Each 10% of electrification cuts fleet CO₂ linearly (Scenario B). "
    "The 75% threshold is the strategic sweet spot: 58.5% emissions cut while preserving CAPEX and "
    "the commercial flexibility of a mixed fleet.</div>",
    unsafe_allow_html=True
)

ev_share = [0, 25, 50, 75, 100]
co2_reduction = [0, 19.5, 39.0, 58.5, 78.0]      # Tabella 4.3
co2_saved_kg  = [0, 135450, 270900, 406350, 541800]

marker_colors = ["#52B788" if s != 75 else "#F9C74F" for s in ev_share]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=ev_share, y=co2_reduction,
    mode="lines+markers",
    line=dict(color="#52B788", width=3),
    marker=dict(size=[9 if s != 75 else 15 for s in ev_share], color=marker_colors,
                line=dict(width=2, color="#0D1F17")),
    fill="tozeroy", fillcolor="rgba(82,183,136,0.12)",
    customdata=co2_saved_kg,
    hovertemplate="<b>%{x}% EV</b><br>%{y}% CO₂ reduction<br>%{customdata:,.0f} kg CO₂ saved/day<extra></extra>",
))
fig.add_annotation(x=75, y=58.5, text="◆ 75% — optimal threshold<br>58.5% CO₂ cut",
                   showarrow=True, arrowhead=2, arrowcolor="#F9C74F",
                   font=dict(color="#F9C74F", size=13), ax=-60, ay=-50,
                   bgcolor="rgba(13,31,23,0.9)", bordercolor="#F9C74F", borderwidth=1)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#D8F3DC", family="Inter"),
    xaxis=dict(title="Share of electric vehicles (%)", showgrid=False,
               tickvals=ev_share, ticksuffix="%"),
    yaxis=dict(title="Fleet CO₂ reduction (%)", gridcolor="rgba(82,183,136,0.15)", ticksuffix="%"),
    height=380, margin=dict(l=20, r=20, t=20, b=20), showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

# ── Blocco 3: metriche di sintesi ──────────────────────────────────────
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
    <div class='mini-card'>
        <div class='mini-lbl'>CAPEX preserved by stopping at 75%</div>
        <div class='mini-num'>~€6M</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class='mini-card'>
        <div class='mini-lbl'>Full electrification CAPEX (excl. infrastructure)</div>
        <div class='mini-num'>€25–30M</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class='mini-card'>
        <div class='mini-lbl'>EV as a financial shield (ICE/EV sensitivity)</div>
        <div class='mini-num'>1.39× <small>cost stability</small></div>
    </div>""", unsafe_allow_html=True)

# ── Takeaway ───────────────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
st.success("""
    **Managerial takeaway:** The decision is not "green vs. cheap" — it's the optimal mix of a hybrid fleet.
    Electrification up to ~75%, combined with SLA discipline on the remaining thermal vehicles, minimizes
    total cost while turning a growing carbon liability (up to €7.3M/year) into a stable, competitive cost structure.
""")

st.caption("Sources: NextMile Italia case study (Ch. 5) and electrification trajectory Table 4.3 (NB06). "
           "Carbon valued at EU ETS price (65 €/t, 2024 average). Figures are order-of-magnitude estimates for a simulated operator.")