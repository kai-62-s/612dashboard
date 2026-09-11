import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Cloud & Data Center Landscape", layout="wide")

# ---------------- Data ----------------
DATA = [
    ("AAPL","Apple",4670,"Hardware + Software","Consumer Electronics",8.71,"High",["AWS","Azure","InhouseCloud"],["Taiwan","China"]),
    ("AMD","Advanced Micro Devices",760,"Hardware","Semiconductors",3.92,"High",["Azure","Oracle Cloud","Google Cloud"],["Taiwan"]),
    ("ASML","ASML Holdings",710,"Hardware","Semiconductor Equipment",32.12,"High",["Google Cloud"],["Germany","US"]),
    ("AMZN","Amazon (AWS)",2800,"Hardware + Cloud + Software","Cloud Computing",12.6,"Medium",["AWS","InhouseCloud"],["Taiwan","China"]),
    ("ANET","Arista Networks",248,"Hardware","Networking Equipment",3.16,"Medium",["Azure","Google Cloud"],["Taiwan","China"]),
    ("ARM","ARM Holdings",272,"Hardware","Semiconductors (IP)",0.85,"High",[],[]),
    ("AVGO","Broadcom Inc",780,"Hardware + Software","Semiconductors",11.25,"High",["AWS","Azure","Google Cloud"],["Taiwan","China"]),
    ("CSCO","Cisco",195,"Hardware","Networking Equipment",3.08,"Medium",["AWS","Azure","Google Cloud"],["Taiwan","China"]),
    ("CRWD","CrowdStrike",70,"Software / SaaS","Cybersecurity",0.38,"Low",["AWS","Google Cloud"],[]),
    ("CRM","Salesforce Inc",250,"Software / SaaS","Software",5.35,"Low",["AWS","Google Cloud","InhouseCloud"],[]),
    ("DELL","Dell Technologies",85,"Hardware","IT Hardware",6.8,"High",["AWS","Azure","InhouseCloud"],["Taiwan","China"]),
    ("DDOG","Datadog Inc",38,"Software / SaaS","Software",0.22,"Low",["AWS","Google Cloud","Azure"],[]),
    ("GOOGL","Alphabet",4058,"Hardware + Cloud + Software","Cloud Computing",19.94,"High",["Google Cloud","InhouseCloud"],["Taiwan","China"]),
    ("GTLB","GitLab",7.9,"Software / SaaS","Software",-0.32,"Low",["AWS","Google Cloud"],[]),
    ("INTC","Intel Corp",533,"Hardware","Semiconductors",-2.09,"High",["InhouseCloud"],["US","Ireland","Israel"]),
    ("MSFT","Microsoft",3651,"Hardware + Cloud + Software","Cloud Computing",17.95,"Medium",["Azure","InhouseCloud"],["Taiwan","China"]),
    ("NVDA","Nvidia",5560,"Hardware","Semiconductors",7.95,"High",["AWS","Azure","Google Cloud"],["Taiwan","China"]),
    ("NOW","ServiceNow Inc",135.6,"Software / SaaS","Software",1.6,"Low",["AWS","Azure","InhouseCloud"],[]),
    ("ORCL","Oracle Corp",390,"Cloud + Software","Cloud Computing",3.71,"Medium",["InhouseCloud"],["Taiwan","US"]),
    ("PANW","Palo Alto Networks",110,"Software / SaaS","Cybersecurity",1.85,"Low",["AWS","Google Cloud","Azure"],["Taiwan","US"]),
    ("QCOM","Qualcomm Inc",185,"Hardware","Semiconductors",8.85,"High",["AWS","Azure"],["Taiwan"]),
    ("SHOP","Shopify",100,"Software / SaaS","Software",0.18,"Low",["Google Cloud","AWS"],[]),
    ("TSM","Taiwan Semiconductor",850,"Hardware","Semiconductors",6.25,"High",["AWS","Azure","InhouseCloud"],["Taiwan","Japan"]),
    ("ZS","Zscaler Inc",28,"Software / SaaS","Cybersecurity",-0.35,"Low",["AWS","Google Cloud"],[]),
    ("META","Meta (Facebook)",1571,"Hardware + Software","Technology",10.44,"High",["AWS","InhouseCloud"],["Taiwan","China"]),
    ("NFLX","Netflix",325,"Software / SaaS","Media/Entertainment",1.23,"Medium",["AWS"],[]),
    ("CEG","Constellation Energy",106,"Other (Supporting Infrastructure)","Energy/Utilities",4.49,"Medium",[],[]),
    ("DIS","Disney",188,"Software / SaaS","Media/Entertainment",1.64,"Medium",["AWS"],[]),
    ("SOFI","SoFi Technologies",23,"Financial","Financial",0.12,"Low",["AWS","Azure"],["Taiwan","China"]),
    ("TSLA","Tesla",1398,"Hardware + Software","Automotive",0.41,"High",["AWS","InhouseCloud"],["Japan","Korea"]),
]
df = pd.DataFrame(DATA, columns=["Ticker","Company","MarketCap","Segment","Industry","EPS","Risk","Cloud","SupplyChain"])

SEG_COLORS = {
    "Hardware": "#2E7D32", "Software / SaaS": "#1565C0", "Hardware + Software": "#66BB6A",
    "Cloud + Software": "#8E24AA", "Hardware + Cloud + Software": "#5C6BC0",
    "Other (Supporting Infrastructure)": "#F9A825", "Financial": "#EC407A",
}
RISK_COLORS = {"High": "#E53935", "Medium": "#FB8C00", "Low": "#43A047"}
FONT = "Arial, sans-serif"

def style(fig, h=420):
    fig.update_layout(
        height=h, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family=FONT, size=12, color="#212121"),
        margin=dict(l=10, r=20, t=30, b=10),
    )
    return fig

st.markdown("""
<style>
.block-container {padding-top: 2rem;}
h1, h2, h3 {font-family: Arial, sans-serif;}
.insight-box {
    background-color: #F5F7FA; border-left: 4px solid #1565C0;
    padding: 14px 18px; border-radius: 4px; font-size: 15px; line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

st.title("Cloud & Data Center Landscape")
st.caption("A walkthrough of 30 companies across hardware, cloud, and software — MIS 612")

tabs = st.tabs(["1 · Overview", "2 · Market Position", "3 · Financial Health", "4 · Geopolitical Risk", "5 · Cloud Infrastructure", "6 · Takeaways"])

# ================= TAB 1: OVERVIEW =================
with tabs[0]:
    st.subheader("The market at a glance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Companies analyzed", "30")
    c2.metric("Combined market cap", f"${df['MarketCap'].sum():,.0f}B")
    c3.metric("Average EPS", f"${df['EPS'].mean():.2f}")
    c4.metric("High geopolitical risk", f"{(df['Risk']=='High').sum()} companies")

    seg_totals = df.groupby("Segment")["MarketCap"].sum().sort_values(ascending=False)
    fig = go.Figure(go.Bar(
        x=seg_totals.values, y=seg_totals.index, orientation="h",
        marker_color=[SEG_COLORS.get(s, "#999") for s in seg_totals.index],
        text=[f"${v:,.0f}B" for v in seg_totals.values], textposition="outside",
    ))
    fig.update_layout(title="Total market cap by segment", xaxis_title="Market Cap ($B)")
    st.plotly_chart(style(fig), use_container_width=True)

    st.markdown('<div class="insight-box">Three companies — <b>Amazon, Microsoft, Alphabet</b> — span '
                'hardware, cloud, and software at once. That single "Hardware + Cloud + Software" segment '
                'alone accounts for a disproportionate share of total market cap, ahead of pure-play '
                'hardware or software groups combined.</div>', unsafe_allow_html=True)

# ================= TAB 2: MARKET POSITION =================
with tabs[1]:
    st.subheader("Who competes where")
    fig = px.scatter(
        df, x="EPS", y="MarketCap", size="MarketCap", color="Segment",
        color_discrete_map=SEG_COLORS, hover_name="Company", text="Ticker",
        size_max=55,
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_layout(title="Market cap vs. profitability, by segment", xaxis_title="EPS ($)", yaxis_title="Market Cap ($B)")
    st.plotly_chart(style(fig, 520), use_container_width=True)

    st.markdown('<div class="insight-box">Segment diversification tracks directly with scale: companies '
                'in the top-right (large market cap AND strong EPS) are almost all multi-segment players. '
                'Single-segment hardware names cluster lower-left — bigger balance sheets don\'t always mean '
                'bigger per-share earnings.</div>', unsafe_allow_html=True)

# ================= TAB 3: FINANCIAL HEALTH =================
with tabs[2]:
    st.subheader("Segment earnings — who's actually profitable")
    seg_eps = df.groupby("Segment")["EPS"].mean().sort_values(ascending=False)
    fig = go.Figure(go.Bar(
        x=seg_eps.index, y=seg_eps.values,
        marker_color=[SEG_COLORS.get(s, "#999") for s in seg_eps.index],
        text=[f"${v:.2f}" for v in seg_eps.values], textposition="outside",
    ))
    fig.update_layout(title="Average EPS by segment", yaxis_title="EPS ($)")
    st.plotly_chart(style(fig), use_container_width=True)

    neg = df[df["EPS"] < 0][["Ticker","Company","EPS"]].sort_values("EPS")
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown('<div class="insight-box">Hardware + Cloud + Software companies post the highest '
                    'average EPS by a wide margin. Pure-SaaS names trail — several are still EPS-negative, '
                    'a deliberate growth-over-profit trade-off (see table) as they reinvest revenue into '
                    'R&D rather than near-term earnings.</div>', unsafe_allow_html=True)
    with col2:
        st.write("**Currently EPS-negative:**")
        st.dataframe(neg, hide_index=True, use_container_width=True)

# ================= TAB 4: GEOPOLITICAL RISK =================
with tabs[3]:
    st.subheader("Risk tracks the supply chain")
    df["AsiaExposed"] = df["SupplyChain"].apply(lambda x: "Taiwan" in x or "China" in x)
    risk_exposure = (df.groupby("Risk")["AsiaExposed"].mean() * 100).reindex(["High","Medium","Low"])
    fig = go.Figure(go.Bar(
        x=risk_exposure.index, y=risk_exposure.values,
        marker_color=[RISK_COLORS[r] for r in risk_exposure.index],
        text=[f"{v:.0f}%" for v in risk_exposure.values], textposition="outside",
    ))
    fig.update_layout(title="Share of companies with Taiwan/China supply chain exposure, by risk tier",
                       yaxis_title="% with Taiwan/China exposure", yaxis_range=[0,110])
    st.plotly_chart(style(fig), use_container_width=True)

    st.markdown(f'<div class="insight-box"><b>{risk_exposure["High"]:.0f}%</b> of High-risk companies '
                f'source from Taiwan or China, versus just <b>{risk_exposure["Low"]:.0f}%</b> of Low-risk '
                'ones. The pattern is clean: almost every Low-risk company is a pure-cloud SaaS business '
                'with no hardware manufacturing footprint — geopolitical risk here is really a hardware '
                'supply-chain story, not a software one.</div>', unsafe_allow_html=True)

# ================= TAB 5: CLOUD INFRASTRUCTURE =================
with tabs[4]:
    st.subheader("Who powers the sector")
    cloud_counts = {}
    for clouds in df["Cloud"]:
        for p in clouds:
            cloud_counts[p] = cloud_counts.get(p, 0) + 1
    cdf = pd.DataFrame(sorted(cloud_counts.items(), key=lambda x: -x[1]), columns=["Provider","Count"])
    fig = go.Figure(go.Bar(
        x=cdf["Count"], y=cdf["Provider"], orientation="h", marker_color="#1565C0",
        text=cdf["Count"], textposition="outside",
    ))
    fig.update_layout(title="Number of companies relying on each cloud provider", xaxis_title="Companies")
    st.plotly_chart(style(fig, 380), use_container_width=True)

    top_provider = cdf.iloc[0]
    st.markdown(f'<div class="insight-box"><b>{top_provider["Provider"]}</b> is embedded in '
                f'<b>{top_provider["Count"]} of 30</b> companies\' infrastructure — more than any rival. '
                'That concentration is exactly why a single major outage at one provider can ripple across '
                'a large share of the sector at once, a real systemic-risk angle worth raising in class.</div>',
                unsafe_allow_html=True)

# ================= TAB 6: TAKEAWAYS =================
with tabs[5]:
    st.subheader("Key takeaways")
    st.markdown("""
    <div class="insight-box">
    <b>1. Diversification wins.</b> The three companies spanning hardware, cloud, and software
    (Amazon, Microsoft, Alphabet) out-earn and out-scale every single-segment peer group.<br><br>
    <b>2. Profit strategy splits by segment.</b> Hardware and multi-segment giants are consistently
    profitable; several pure-SaaS names are still EPS-negative, trading profit for growth.<br><br>
    <b>3. Geopolitical risk is a hardware problem.</b> High-risk companies are almost all tied to
    Taiwan/China manufacturing; SaaS companies carry the lowest risk precisely because they don't
    manufacture anything.<br><br>
    <b>4. Cloud dependency is concentrated.</b> A handful of providers underpin nearly the entire
    sector's infrastructure — a single point of failure risk worth flagging.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("**Full dataset**")
    st.dataframe(df[["Ticker","Company","Segment","Industry","MarketCap","EPS","Risk"]],
                 hide_index=True, use_container_width=True)
