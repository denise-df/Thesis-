import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Economic Strategy | EcoFleet Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_navigation(current_page="Results"):
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

render_navigation("Results")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family:'Inter',sans-serif !important; background-color:#0D1F17 !important; color:#D8F3DC !important; }
.stApp { background: linear-gradient(160deg,#0D1F17 0%,#152A1E 100%) !important; }
.fleet-eyebrow { font-family:'JetBrains Mono',monospace; font-size:.75rem; letter-spacing:3px; color:#52B788; text-transform:uppercase; margin:1rem 0 .8rem 0; }
.title-text { color:#D8F3DC; font-weight:800; font-size:3rem; margin-bottom:.5rem; line-height:1.1; }
.subtitle-text { color:#95D5B2; font-size:1.05rem; line-height:1.7; opacity:.85; margin-bottom:1rem; }
.sec-h { font-size:1.5rem; font-weight:700; color:#95D5B2; margin:3rem 0 .6rem 0; padding-bottom:.5rem; text-align:center; }
.sec-explain { font-size:.95rem; color:#95D5B2; opacity:.8; line-height:1.6; margin-bottom:1.5rem; text-align:center; max-width:800px; margin-left:auto; margin-right:auto; }
.nm-badge { display:inline-block; background:rgba(82,183,136,0.15); border:1px solid #52B788; border-radius:20px; padding:.4rem 1.1rem; margin-bottom:1rem; font-family:'JetBrains Mono',monospace; font-size:.8rem; letter-spacing:1px; color:#95D5B2; }

.line-wrap { margin:1rem 0 3.5rem 0; }
.line-track { position:relative; height:8px; border-radius:4px; margin: 6rem 8rem 4rem 8rem; }

.line-risk { background:linear-gradient(90deg, #FF8A50, #E63946); box-shadow: 0 2px 10px rgba(230,57,70,0.3); }
.pole-risk-l { background:#FF8A50; } 
.pole-risk-r { background:#E63946; } 
.pole-risk-m { background:#F0624D; }

.line-opp { background:linear-gradient(90deg, #2EC4B6, #20B2AA); box-shadow: 0 2px 15px rgba(46,196,182,0.4); }
.pole-opp-l { background:#2EC4B6; } 
.pole-opp-r { background:#20B2AA; }

.pole { position:absolute; top:-4px; width:16px; height:16px; border-radius:50%; border:3px solid #0D1F17; transform:translate(-50%,0); }
.pole.left{left:0;} .pole.right{left:100%;} .pole.mid{left:50%; opacity:.6; width:12px; height:12px; top:-2px;}

.plabel { position:absolute; width:220px; text-align:center; transform:translateX(-50%); }
.plabel.left{left:0;} .plabel.right{left:100%;}
.plabel.top{top:-5.5rem;} 
.plabel.bottom{top:1.8rem;} 
.plabel .val { font-size:2rem; font-weight:800; line-height:1.1; }
.plabel .desc { font-size:.82rem; color:#95D5B2; opacity:.85; line-height:1.4; margin-top:.4rem; }

.risk .val { color:#E63946; } 
.opp .val { color:#2EC4B6; } 

.co2-note { font-size:.85rem; color:#95D5B2; opacity:.9; margin-top:2.5rem; border-left:2px solid rgba(82,183,136,0.4); padding-left:.8rem; line-height:1.5; text-align:center; max-width:800px; margin-left:auto; margin-right:auto;}
.capex-tbl { width:100%; border-collapse:collapse; font-size:.9rem; }
.capex-tbl th { color:#52B788; text-align:left; padding:.6rem .5rem; border-bottom:1px solid rgba(82,183,136,0.3); font-family:'JetBrains Mono',monospace; font-size:.75rem; letter-spacing:1px; text-transform:uppercase; }
.capex-tbl td { padding:.6rem .5rem; border-bottom:1px solid rgba(82,183,136,0.1); color:#D8F3DC; }
.capex-tbl tr.hi td { background:rgba(249,199,79,0.08); color:#F9C74F; font-weight:600; }
.mini-card { background:rgba(255,255,255,0.04); border:1px solid rgba(82,183,136,0.15); border-radius:10px; padding:1.3rem; height:100%; position:relative; }
.mini-lbl { font-size:.85rem; color:#95D5B2; opacity:.8; margin-bottom:.5rem; }
.mini-num { font-size:1.8rem; font-weight:800; color:#D8F3DC; }
.mini-num small { font-size:.9rem; color:#95D5B2; font-weight:500; }
.mini-asterisk { font-size:.75rem; color:#95D5B2; opacity:.7; margin-top:.4rem; line-height:1.3;}
div.stButton > button { background:rgba(45,106,79,0.3) !important; color:#95D5B2 !important; border:1px solid rgba(82,183,136,0.3) !important; border-radius:8px !important; }
div.stButton > button:hover { background:rgba(45,106,79,0.6) !important; border-color:#52B788 !important; color:#D8F3DC !important; }
</style>
""", unsafe_allow_html=True)

# ── Main Content ───────────────────────────────────────────────────────
st.markdown("<div class='nm-badge'> NextMile Italia — Case Study</div>", unsafe_allow_html=True)
st.markdown("<div class='fleet-eyebrow'>STRATEGIC DECISION LAYER</div>", unsafe_allow_html=True)
st.markdown("<div class='title-text'> The Economics of Speed</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle-text'>What the carbon findings mean in euros, for one representative operator: "
    "50,000 deliveries a day, a 100% thermal fleet emitting ~135 tonnes of CO₂ daily. "
    "All figures below describe <b>this</b> operator — they scale with the size of the business.</div>",
    unsafe_allow_html=True
)

st.markdown("""
<div class='sec-h' style='border-bottom: 1px solid rgba(230,57,70,0.3); padding-bottom: 0.8rem;'>
    1 · The <span style='font-size:2rem; color:#E63946; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin: 0 4px;'>Cost</span> of doing nothing
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='sec-explain'>Maintaining a fully thermal fleet transforms CO₂ emissions into a direct financial liability. "
    "Under the upcoming EU carbon pricing framework (ETS2, active from 2027), this environmental cost will steadily increase "
    "each year, representing a severe financial drain for operators who choose not to adapt.</div>",
    unsafe_allow_html=True
)
st.markdown("""
<div class='line-wrap'>
  <div class='line-track line-risk'>
    <div class='plabel left top risk'><div class='val'>€3.2M<span style='font-size:1rem;'>/yr</span></div><div class='desc'>Today's carbon price<br>(65 €/tonne, 2024)</div></div>
    <div class='plabel right top risk'><div class='val'>€7.3M<span style='font-size:1rem;'>/yr</span></div><div class='desc'>2030 scenario<br>(150 €/tonne)</div></div>
    <div class='pole left pole-risk-l'></div>
    <div class='pole mid pole-risk-m'></div>
    <div class='pole right pole-risk-r'></div>
    <div class='plabel left bottom'><div class='desc'>Baseline</div></div>
    <div class='plabel right bottom'><div class='desc'>Financial exposure</div></div>
    <div class='plabel bottom' style='left:50%;'><div class='desc' style='opacity:.6;'>€4.9M · 2027–28 (100 €/tonne)</div></div>
  </div>
</div>
<div class='co2-note'> What drives this bill: the fleet's <b>135 tonnes of CO₂ per day</b>, unpriced today but soon taxed.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='sec-h' style='border-bottom: 1px solid rgba(46,196,182,0.3); padding-bottom: 0.8rem;'>
    2 · The <span style='font-size:2rem; color:#2EC4B6; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin: 0 4px;'>Value</span> of acting
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='sec-explain'>Strategic decarbonization directly translates into annual financial savings. Operators can adopt a spectrum of solutions: "
    "from immediate, zero-cost operational shifts—such as renegotiating delivery timeframes—to a comprehensive, capital-intensive transition toward a 100% electric fleet.</div>",
    unsafe_allow_html=True
)
st.markdown("""
<div class='line-wrap'>
  <div class='line-track line-opp'>
    <div class='plabel left top opp'><div class='val'>€2.3M<span style='font-size:1rem;'>/yr</span></div><div class='desc'>Renegotiating deadlines<br>(no money spent)</div></div>
    <div class='plabel right top opp'><div class='val'>€13.2M<span style='font-size:1rem;'>/yr</span></div><div class='desc'>Going 100% electric</div></div>
    <div class='pole left pole-opp-l'></div>
    <div class='pole right pole-opp-r'></div>
    <div class='plabel left bottom'><div class='desc'>Operational shift</div></div>
    <div class='plabel right bottom'><div class='desc'>Full transition</div></div>
  </div>
</div>
<div class='co2-note'> At the top end, the fleet avoids <b>541,800 kg of CO₂ every day</b> versus a fully thermal baseline.</div>
""", unsafe_allow_html=True)

st.markdown("<div class='sec-h' style='border-bottom: 1px solid rgba(82,183,136,0.3); padding-bottom: 0.8rem;'>3 · Diminishing Marginal Returns: Net Value vs. Upfront Investment</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sec-explain'><b>Net Value</b> is defined as the <em>Annual Economic Benefit</em> (avoided carbon/fuel costs + SLA optimization savings) "
    "minus the <em>Amortized Upfront Investment (CAPEX)</em> spread over a 3-year vehicle lifecycle[cite: 1]. "
    "The marginal return is not a smooth decay: it holds steady up to 50% electrification, then drops sharply past that point. "
    "As a result, moving from 0% to 75% already captures <b>87.6% of the maximum economic value</b>, while the final 25% requires the same capital outlay for a much smaller gain.</div>",
    unsafe_allow_html=True
)

chart_col, table_col = st.columns([1.3, 1])
with chart_col:
    # ── Net Value curve — Corretto l'hover per evitare il doppio % ──
    ev_share        = [0, 25, 50, 75, 100]
    annual_value    = [2.30, 5.04, 7.77, 10.51, 13.24]   # M€/yr
    capex           = [0, 5, 10, 16, 22]                 # M€ upfront
    VEHICLE_LIFE_YEARS = 3
    amortised_capex = [c / VEHICLE_LIFE_YEARS for c in capex]
    net_value       = [round(v - a, 2) for v, a in zip(annual_value, amortised_capex)]
    STRATEGIC_IDX   = 3  # 75%

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ev_share, y=net_value, name="Net Economic Value (M€/yr)", mode="lines+markers", yaxis="y1",
        line=dict(color="#52B788", width=3, shape="spline"),
        marker=dict(size=[9 if i != STRATEGIC_IDX else 16 for i in range(len(ev_share))],
                    color=["#52B788" if i != STRATEGIC_IDX else "#F9C74F" for i in range(len(ev_share))],
                    line=dict(width=2, color="#0D1F17")),
        hovertemplate="<b>%{x}% Electric Fleet</b><br>Net Value: €%{y:.2f}M/yr<extra></extra>"))

    fig.add_trace(go.Scatter(
        x=ev_share, y=capex, name="Upfront CAPEX (M€)", mode="lines+markers", yaxis="y2",
        line=dict(color="#E65100", width=2, dash="dot", shape="spline"),
        marker=dict(size=[0 if s == 0 else 7 for s in ev_share],
                    color="#E65100", line=dict(width=2, color="#0D1F17")),
        hovertemplate="<b>%{x}% Electric Fleet</b><br>Upfront CAPEX: €%{y}M<extra></extra>"))

    fig.add_vline(x=75, line_dash="dash", line_color="#F9C74F", opacity=0.7)
    fig.add_annotation(x=75, y=net_value[STRATEGIC_IDX], yref="y1",
                       text="◆ 75%: Structural Threshold<br>(87.6% max value captured, €6M saved)",
                       showarrow=True, arrowhead=2, ax=0, ay=-45,
                       font=dict(color="#F9C74F", size=11), bgcolor="rgba(13,31,23,0.95)",
                       bordercolor="#F9C74F", borderwidth=1)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#D8F3DC", family="Inter"),
        xaxis=dict(title="Fleet Electrification Share", showgrid=False, tickvals=ev_share, ticksuffix="%"),
        yaxis=dict(
            title=dict(text="Net Value (M€/yr)", font=dict(color="#52B788")),
            gridcolor="rgba(82,183,136,0.15)", ticksuffix="M",
            tickfont=dict(color="#52B788")
        ),
        yaxis2=dict(
            title=dict(text="Upfront CAPEX (M€)", font=dict(color="#E65100")),
            overlaying="y", side="right", showgrid=False,
            ticksuffix="M", tickfont=dict(color="#E65100")
        ),
        height=380, margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11))
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Net Economic Value = Annual Operational Savings (SLA + Carbon/Fuel) minus Amortized Upfront CAPEX (3-year horizon)[cite: 1].")

with table_col:
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <table class='capex-tbl'>
        <tr><th>Electric</th><th>Annual Value</th><th>Upfront</th><th>Net Value/yr</th></tr>
        <tr><td>0%</td><td>€2.30M</td><td>€0M</td><td>€2.30M</td></tr>
        <tr><td>25%</td><td>€5.04M</td><td>~€5M</td><td>€3.37M</td></tr>
        <tr><td>50%</td><td>€7.77M</td><td>~€10M</td><td>€4.44M</td></tr>
        <tr class='hi'><td>75% ◆</td><td>€10.51M</td><td>~€16M</td><td>€5.18M</td></tr>
        <tr><td>100%</td><td>€13.24M</td><td>~€22M</td><td>€5.91M</td></tr>
    </table>
    <div class='co2-note' style='margin-top:1rem; text-align: left;'>
        <b>Marginal Returns Analysis:</b> Value grows almost linearly up to 50% electrification (+€1.07M, then +€1.06M per 25pp step),
        then flattens sharply beyond it (+€0.74M, then +€0.73M) — a step change, not a gradual decay.
        The final stretch to 100% still requires another €6M in CAPEX for that reduced gain,
        while completely erasing the commercial SLA flexibility lever[cite: 1].
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""<div class='mini-card'><div class='mini-lbl'>Money freed by stopping at 75%</div><div class='mini-num'>~€6M</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class='mini-card'>
        <div class='mini-lbl'>Full electrification CAPEX*</div>
        <div class='mini-num'>€22M</div>
        <div class='mini-asterisk'>*Excluding charging infrastructure costs.</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class='mini-card'><div class='mini-lbl'>Electric = steadier daily costs</div><div class='mini-num'>1.39× <small>more stable</small></div></div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
st.success("""
    **The bottom line:** The choice isn't binary. Stopping at an optimal **75% electrification threshold** captures 
    the vast economic and environmental benefits while avoiding capital lock-in, preserving operational agility[cite: 1].
""")
st.caption("Case study: NextMile Italia (Ch. 5). Cost/benefit from Table 5.3 and NB06 (Scenario C). Carbon valued at EU ETS price (65 €/t, 2024)[cite: 1].")
