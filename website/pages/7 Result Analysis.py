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

render_navigation("Results")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family:'Inter',sans-serif !important; background-color:#0D1F17 !important; color:#D8F3DC !important; }
.stApp { background: linear-gradient(160deg,#0D1F17 0%,#152A1E 100%) !important; }
div.stButton > button { background:rgba(45,106,79,0.3) !important; color:#95D5B2 !important; border:1px solid rgba(82,183,136,0.3) !important; border-radius:8px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='font-size: 3rem; color: #E65100; font-weight: 800; line-height: 1.1; margin-top: 2rem;'><span style='font-size: 6.5rem;'>THE COST</span> of doing nothing <br>€ 7.3M / year</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 3rem; color: #52B788; font-weight: 800; line-height: 1.1; margin-top: 2rem;'><span style='font-size: 6.5rem;'>THE VALUE</span> of acting <br>€ 12.8M / year</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 4rem; font-size: 2rem; color: #D8F3DC; font-weight: 700;'>Strategic Optimum Curve</div>", unsafe_allow_html=True)

ev_share = [0, 25, 50, 75, 100]
capex_annualized = [0, 1.6, 3.3, 5.3, 7.3] 
savings = [0, 3.2, 6.4, 9.6, 12.8] 
net_value = [s - c for s, c in zip(savings, capex_annualized)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=ev_share, y=net_value, mode="lines+markers", name="Net Value Generated",
    line=dict(color="#52B788", width=4, shape="spline"),
    marker=dict(size=[10 if s != 75 else 20 for s in ev_share],
                color=["#52B788" if s != 75 else "#F9C74F" for s in ev_share],
                line=dict(width=2, color="#0D1F17"))
))

fig.add_annotation(
    x=75, y=net_value[3], text="Strategic Optimum", showarrow=True, arrowhead=2,
    arrowsize=1, arrowwidth=2, arrowcolor="#F9C74F",
    font=dict(color="#0D1F17", size=14, weight="bold"), bgcolor="#F9C74F",
    bordercolor="#F9C74F", borderwidth=2, borderpad=4, ax=0, ay=-40
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#D8F3DC", family="Inter"),
    xaxis=dict(title="Electrification Share", showgrid=False, tickvals=ev_share, ticksuffix="%"),
    yaxis=dict(title="Net Financial Value", gridcolor="rgba(82,183,136,0.15)", tickprefix="€", ticksuffix="M"),
    height=500, margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig, use_container_width=True)
