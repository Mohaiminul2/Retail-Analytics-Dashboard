import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from design_system import (
    C, S, R, SHADOW, TYPE, FONT_FAMILY, ICONS,
    inject_global_css, kpi_card, section_header,
    register_plotly_theme, chart_wrap
)

st.set_page_config(
    page_title="Retail-Lens | Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

inject_global_css()
register_plotly_theme()

# ── SIDEBAR — Branding + Filters ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.8rem 1rem 1.4rem 1rem; border-bottom: 1px solid #1a2d5a; margin-bottom: {S['lg']};">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.4rem;">
            <div style="
                width: 28px; height: 28px; border-radius: {R['sm']};
                background: linear-gradient(135deg, {C['brand']['primary']}, {C['brand']['secondary']});
                display:flex; align-items:center; justify-content:center;
                color: white;
            ">{ICONS['chart']}</div>
            <span style="
                font-family: {FONT_FAMILY['heading']}; font-size: 1rem;
                font-weight: 600; color: {C['text']['inverse']}; letter-spacing: -0.01em;
            ">Retail-Lens</span>
        </div>
        <p style="color:#3a5080; font-size:{TYPE['h3']['size']}; letter-spacing:{TYPE['h3']['ltr_spacing']}; text-transform:uppercase; margin:0;">
            Sales Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:#3a5080; font-size:{TYPE['caption']['size']}; letter-spacing:0.12em;
              text-transform:uppercase; padding: 0 0 {S['xs']} 0;">Filters</p>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin-1")
        df.columns = df.columns.str.strip()
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Year"]  = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month
        df["Month Name"] = df["Order Date"].dt.strftime("%b")
        df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
        df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
        return df

    df = load_data()

    years   = sorted(df["Year"].unique())
    regions = ["All Regions"] + sorted(df["Region"].unique().tolist())
    cats    = ["All Categories"] + sorted(df["Category"].unique().tolist())

    selected_year   = st.selectbox("Year", years, index=len(years)-1)
    selected_region = st.selectbox("Region", regions)
    selected_cat    = st.selectbox("Category", cats)

    st.markdown(f"<div style='height:{S['md']}'></div>", unsafe_allow_html=True)

    latest = df["Order Date"].max().strftime("%d %b %Y")
    st.markdown(f"""
    <div style="
        border: 1px solid #1a2d5a; border-radius: {R['lg']};
        padding: {S['sm']} {S['md']}; margin-top: {S['md']};
    ">
        <p style="color:#3a5080; font-size:{TYPE['caption']['size']}; letter-spacing:0.1em;
                  text-transform:uppercase; margin:0 0 0.3rem 0;">Data Freshness</p>
        <p style="color:{C['brand']['positive']}; font-size:{TYPE['body']['size']}; margin:0; font-weight:500;">
            ● Live · Last updated {latest}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── APPLY FILTERS ──────────────────────────────────────────────────────────────
fdf = df[df["Year"] == selected_year].copy()
if selected_region != "All Regions":
    fdf = fdf[fdf["Region"] == selected_region]
if selected_cat != "All Categories":
    fdf = fdf[fdf["Category"] == selected_cat]

prev_year = selected_year - 1
pdf = df[df["Year"] == prev_year].copy()
if selected_region != "All Regions":
    pdf = pdf[pdf["Region"] == selected_region]
if selected_cat != "All Categories":
    pdf = pdf[pdf["Category"] == selected_cat]


def yoy_delta(current, previous):
    if previous == 0:
        return "N/A"
    delta = ((current - previous) / previous) * 100
    arrow = "▲" if delta >= 0 else "▼"
    color = C["brand"]["positive"] if delta >= 0 else C["brand"]["negative"]
    return f'<span style="color:{color}; font-size:{TYPE["caption"]["size"]};">{arrow} {abs(delta):.1f}% vs {prev_year}</span>'


# ── PAGE HEADER ────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style="margin-bottom: {S['xl']};">
    <h1 style="
        font-family: {FONT_FAMILY['heading']};
        font-size: {TYPE['h1']['size']}; font-weight: {TYPE['h1']['weight']};
        color: {C['text']['primary']}; letter-spacing: {TYPE['h1']['ltr_spacing']};
        line-height: {TYPE['h1']['line_height']}; margin-bottom: 0.4rem;
    ">Sales Performance <span style="color:{C['brand']['primary']};">Intelligence</span></h1>
    <p style="color:{C['text']['muted']}; font-size:{TYPE['subhead']['size']}; font-family:{FONT_FAMILY['body']};">
        Retail analytics · {selected_year} · {selected_region} · {selected_cat}
    </p>
</div>
""", unsafe_allow_html=True)


# ── KPI ROW ────────────────────────────────────────────────────────────────────
total_sales   = fdf["Sales"].sum()
total_profit  = fdf["Profit"].sum()
total_orders  = fdf["Order ID"].nunique()
margin        = (total_profit / total_sales * 100) if total_sales else 0
loss_products = (fdf.groupby("Product Name")["Profit"].sum() < 0).sum()

prev_sales  = pdf["Sales"].sum()
prev_profit = pdf["Profit"].sum()
prev_orders = pdf["Order ID"].nunique()
prev_margin = (prev_profit / prev_sales * 100) if prev_sales else 0

margin_color = C["brand"]["positive"] if margin >= 15 else C["brand"]["negative"]

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi_card("Total Sales", f"${total_sales:,.0f}",
             yoy_delta(total_sales, prev_sales), C["brand"]["primary"], "sales")
with c2:
    kpi_card("Net Profit", f"${total_profit:,.0f}",
             yoy_delta(total_profit, prev_profit), C["brand"]["positive"], "profit")
with c3:
    kpi_card("Profit Margin", f"{margin:.1f}%",
             yoy_delta(margin, prev_margin), margin_color, "margin")
with c4:
    kpi_card("Total Orders", f"{total_orders:,}",
             yoy_delta(total_orders, prev_orders), C["brand"]["secondary"], "orders")
with c5:
    kpi_card("Loss Products", f"{loss_products}",
             "Products with negative profit", C["brand"]["negative"], "warning")

st.markdown(f"<div style='height:{S['xl']}'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    " Sales Overview",
    " Profit Analysis",
    " Loss Intelligence"
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SALES OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:

    section_header("Revenue Breakdown", "Sales distribution across categories and time")

    col1, col2 = st.columns([1, 1.4])

    with col1:
        cat_df = fdf.groupby("Category")["Sales"].sum().reset_index()
        fig = px.bar(
            cat_df, x="Category", y="Sales", color="Category",
            color_discrete_sequence=C["chart"]["palette"],
            title="Sales by Category"
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(showlegend=False)
        chart_wrap(fig)

    with col2:
        monthly_df = (
            fdf.groupby(["Month", "Month Name"])["Sales"]
            .sum().reset_index().sort_values("Month")
        )
        fig = px.area(
            monthly_df, x="Month Name", y="Sales",
            title="Monthly Sales Trend",
            color_discrete_sequence=[C["brand"]["primary"]]
        )
        fig.update_traces(
            fill="tozeroy",
            fillcolor="rgba(24,71,194,0.07)",
            line=dict(color=C["brand"]["primary"], width=2)
        )
        chart_wrap(fig)

    section_header("Product & Regional Performance")

    col3, col4 = st.columns(2)

    with col3:
        top_products = (
            fdf.groupby("Product Name")["Sales"]
            .sum().sort_values(ascending=True)
            .tail(10).reset_index()
        )
        fig = px.bar(
            top_products, x="Sales", y="Product Name",
            orientation="h", title="Top 10 Products by Sales",
            color="Sales",
            color_continuous_scale=[[0, "#e8edf8"], [1, C["brand"]["primary"]]]
        )
        fig.update_layout(coloraxis_showscale=False, yaxis_title="")
        chart_wrap(fig)

    with col4:
        region_df = fdf.groupby("Region")["Sales"].sum().reset_index()
        fig = px.pie(
            region_df, names="Region", values="Sales",
            title="Sales by Region",
            color_discrete_sequence=C["chart"]["palette"],
            hole=0.55
        )
        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            marker=dict(line=dict(color=C["neutrals"]["bg"], width=3))
        )
        fig.update_layout(showlegend=False)
        chart_wrap(fig)

    section_header("Quarterly Trend")

    q_df = fdf.groupby("Quarter")["Sales"].sum().reset_index()
    fig = px.bar(
        q_df, x="Quarter", y="Sales",
        title="Sales by Quarter",
        color="Quarter", color_discrete_sequence=C["chart"]["palette"]
    )
    fig.update_traces(marker_line_width=0, width=0.4)
    fig.update_layout(showlegend=False)
    chart_wrap(fig, height=280)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PROFIT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:

    section_header("Sub-Category Profitability", "Profit amount and margin % per sub-category")

    subcat_df = (
        fdf.groupby(["Category", "Sub-Category"])
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )
    subcat_df["Margin %"] = (subcat_df["Profit"] / subcat_df["Sales"] * 100).round(1)
    subcat_df = subcat_df.sort_values("Profit", ascending=False)

    fig = px.bar(
        subcat_df, x="Sub-Category", y="Profit",
        color="Category", text="Margin %",
        title="Profit by Sub-Category",
        color_discrete_sequence=C["chart"]["palette"]
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
    fig.add_hline(y=0, line_color=C["brand"]["negative"], line_dash="dot", line_width=1)
    chart_wrap(fig, height=360)

    col1, col2 = st.columns(2)

    with col1:
        section_header("Margin by Region")
        region_profit = (
            fdf.groupby("Region")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
        )
        region_profit["Margin %"] = (region_profit["Profit"] / region_profit["Sales"] * 100).round(1)

        colors = [C["brand"]["positive"] if m >= 15 else C["brand"]["negative"] for m in region_profit["Margin %"]]
        fig = go.Figure(go.Bar(
            x=region_profit["Region"],
            y=region_profit["Margin %"],
            marker_color=colors,
            text=[f"{m}%" for m in region_profit["Margin %"]],
            textposition="outside"
        ))
        fig.update_layout(
            title="Profit Margin % by Region",
            yaxis_title="Margin %",
            showlegend=False
        )
        fig.add_hline(y=15, line_dash="dash", line_color="rgba(15,27,61,0.2)",
                      annotation_text="15% target", annotation_font_color="rgba(15,27,61,0.4)")
        chart_wrap(fig)

    with col2:
        section_header("Profit vs Sales Scatter")
        fig = px.scatter(
            fdf, x="Sales", y="Profit",
            color="Category", hover_name="Product Name",
            title="Profit vs Sales by Product",
            color_discrete_sequence=C["chart"]["palette"],
            opacity=0.75
        )
        fig.add_hline(y=0, line_color=C["brand"]["negative"], line_dash="dot", line_width=1.5,
                      annotation_text="Break-even", annotation_font_color=C["brand"]["negative"])
        fig.update_traces(marker=dict(size=6, line=dict(width=0)))
        chart_wrap(fig)

    section_header("Monthly Profit Trend")

    mp_df = (
        fdf.groupby(["Month", "Month Name"])
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index().sort_values("Month")
    )
    mp_df["Margin %"] = (mp_df["Profit"] / mp_df["Sales"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=mp_df["Month Name"], y=mp_df["Sales"],
        name="Sales",
        marker_color=C["brand"]["primary"],
        marker_line_width=0,
        opacity=0.20,
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=mp_df["Month Name"], y=mp_df["Profit"],
        name="Profit",
        line=dict(color=C["brand"]["positive"], width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=C["brand"]["positive"], line=dict(width=2, color=C["neutrals"]["surface"])),
        yaxis="y2"
    ))
    fig.update_layout(
        title="Monthly Sales vs Profit",
        barmode="overlay",
        legend=dict(orientation="h", y=1.12, x=0, font=dict(size=12)),
        yaxis=dict(
            title="Sales ($)",
            gridcolor=C["chart"]["grid"],
            tickfont=dict(color=C["text"]["muted"], size=11),
            title_font=dict(color=C["text"]["muted"], size=11),
            zeroline=False
        ),
        yaxis2=dict(
            title="Profit ($)",
            overlaying="y",
            side="right",
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color=C["brand"]["positive"], size=11),
            title_font=dict(color=C["brand"]["positive"], size=11),
            zeroline=False
        ),
        margin=dict(l=16, r=64, t=50, b=16),
    )
    chart_wrap(fig, height=340)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — LOSS INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:

    section_header("Loss Overview", "Products and segments operating at a loss")

    loss_df_full = (
        fdf.groupby("Product Name")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )
    loss_df_full["Margin %"] = (loss_df_full["Profit"] / loss_df_full["Sales"] * 100).round(1)
    loss_only = loss_df_full[loss_df_full["Profit"] < 0].sort_values("Profit")

    total_loss    = loss_only["Profit"].sum()
    loss_count    = len(loss_only)
    worst_product = loss_only.iloc[0]["Product Name"] if loss_count > 0 else "None"
    worst_loss    = loss_only.iloc[0]["Profit"] if loss_count > 0 else 0

    lc1, lc2, lc3 = st.columns(3)
    with lc1:
        kpi_card("Total Loss Value", f"${abs(total_loss):,.0f}", "Cumulative loss across products", C["brand"]["negative"], "loss")
    with lc2:
        kpi_card("Loss-Making SKUs", f"{loss_count}", "Products with negative profit", C["brand"]["negative"], "circle")
    with lc3:
        kpi_card("Worst Product Loss", f"${abs(worst_loss):,.0f}",
                 worst_product[:35] + "..." if len(worst_product) > 35 else worst_product, C["brand"]["negative"], "stop")

    st.markdown(f"<div style='height:{S['md']}'></div>", unsafe_allow_html=True)

    section_header("Loss-Making Products Table")

    if loss_count > 0:
        display_df = loss_only.copy()
        display_df["Sales"]   = display_df["Sales"].apply(lambda x: f"${x:,.0f}")
        display_df["Profit"]  = display_df["Profit"].apply(lambda x: f"${x:,.0f}")
        display_df["Margin %"] = display_df["Margin %"].apply(lambda x: f"{x:.1f}%")
        display_df = display_df.rename(columns={
            "Product Name": "Product",
            "Sales": "Revenue",
            "Profit": "Loss",
            "Margin %": "Margin"
        })

        st.dataframe(
            display_df,
            use_container_width=True,
            height=380,
            hide_index=True
        )
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:3rem; color:{C['brand']['positive']};">
            <p style="font-size:2rem;">{ICONS['check']}</p>
            <p style="color:{C['text']['primary']};">No loss-making products for the selected filters.</p>
        </div>
        """, unsafe_allow_html=True)

    section_header("Loss by Sub-Category")

    loss_subcat = (
        fdf.groupby("Sub-Category")
        .agg(Profit=("Profit", "sum"))
        .reset_index()
    )
    loss_subcat = loss_subcat[loss_subcat["Profit"] < 0].sort_values("Profit")

    if not loss_subcat.empty:
        loss_subcat_sorted = loss_subcat.sort_values("Profit", ascending=True)
        fig = go.Figure(go.Bar(
            x=loss_subcat_sorted["Profit"],
            y=loss_subcat_sorted["Sub-Category"],
            orientation="h",
            marker_color=C["brand"]["negative"],
            marker_line_width=0,
            text=[f"-${abs(p):,.0f}" for p in loss_subcat_sorted["Profit"]],
            textposition="inside",
            textfont=dict(color=C["text"]["inverse"], size=12, family=FONT_FAMILY["body"]),
            hovertemplate="<b>%{y}</b><br>Loss: -$%{customdata:,.0f}<extra></extra>",
            customdata=[abs(p) for p in loss_subcat_sorted["Profit"]]
        ))
        fig.update_layout(
            title="Loss-Making Sub-Categories",
            xaxis=dict(
                title="Loss Amount ($)",
                gridcolor=C["chart"]["grid"],
                tickprefix="$",
                tickformat=",.0f",
                zeroline=True,
                zerolinecolor=C["border"]["default"],
                zerolinewidth=1.5,
                autorange="reversed"
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=12, color=C["text"]["primary"])
            ),
            showlegend=False,
            margin=dict(l=16, r=40, t=40, b=16),
        )
        chart_wrap(fig, height=max(300, len(loss_subcat_sorted) * 70))
    else:
        st.info("No loss-making sub-categories for selected filters.")
