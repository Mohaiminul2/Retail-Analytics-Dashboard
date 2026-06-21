"""
Design System for Retail-Lens Sales Dashboard
Reference: Twill-AI/partner-dashboard-v2 (dashboard-specific patterns)
Adapted: google-labs-code/design.md (token format)

A professional, data-dense enterprise sales dashboard aesthetic.
Light theme with midnight blue accent, mono-spaced numerals for financial figures.
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ── SVG ICONS (vector-based, not emoji) ───────────────────────────────────────
ICONS = {
    "sales": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
    "profit": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>',
    "margin": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>',
    "orders": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>',
    "warning": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
    "loss": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>',
    "circle": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="8"></circle></svg>',
    "stop": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
    "check": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
    "chart": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
    "coin": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path><path d="M12 18V6"></path></svg>',
    "alert": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
}

# ── COLOR TOKENS ──────────────────────────────────────────────────────────────
C = {
    "neutrals": {
        "bg":          "#f0f2f7",
        "surface":     "#ffffff",
        "elevated":    "#f8f9fc",
        "hover":       "rgba(15,27,61,0.04)",
        "selected":    "rgba(24,71,194,0.08)",
    },
    "text": {
        "primary":     "#0f1b3d",
        "secondary":   "#4a5568",
        "muted":       "#64748b",
        "disabled":    "#94a3b8",
        "inverse":     "#ffffff",
    },
    "border": {
        "default":     "#d4d9e8",
        "strong":      "#b0b8d0",
        "faint":       "rgba(15,27,61,0.06)",
    },
    "brand": {
        "primary":     "#1847c2",
        "secondary":   "#6c4de6",
        "accent":      "#0891b2",
        "positive":    "#0e9e6e",
        "negative":    "#e02d4b",
        "warning":     "#f59e0b",
    },
    "chart": {
        "bg":          "#ffffff",
        "grid":        "#eaecf4",
        "palette":     ["#1847c2", "#6c4de6", "#0891b2", "#0e9e6e", "#f59e0b", "#e02d4b"],
    },
}

# ── TYPOGRAPHY TOKENS ─────────────────────────────────────────────────────────
FONT_FAMILY = {
    "heading": "'Syne', sans-serif",
    "body":    "'DM Sans', sans-serif",
    "mono":    "'DM Mono', 'JetBrains Mono', 'SF Mono', monospace",
}

TYPE = {
    "h1":       {"family": FONT_FAMILY["heading"], "size": "2rem",     "weight": 600, "ltr_spacing": "-0.02em", "line_height": 1.1},
    "h2":       {"family": FONT_FAMILY["heading"], "size": "1.5rem",   "weight": 600, "ltr_spacing": "-0.01em", "line_height": 1.15},
    "h3":       {"family": FONT_FAMILY["heading"], "size": "0.7rem",   "weight": 700, "ltr_spacing": "0.15em",  "line_height": 1.2},
    "subhead":  {"family": FONT_FAMILY["body"],    "size": "0.9rem",   "weight": 400, "ltr_spacing": "0",       "line_height": 1.4},
    "body":     {"family": FONT_FAMILY["body"],    "size": "0.8rem",   "weight": 400, "ltr_spacing": "0",       "line_height": 1.5},
    "caption":  {"family": FONT_FAMILY["body"],    "size": "0.69rem",  "weight": 400, "ltr_spacing": "0",       "line_height": 1.3},
    "label":    {"family": FONT_FAMILY["body"],    "size": "0.61rem",  "weight": 600, "ltr_spacing": "0.1em",  "line_height": 1.2},
    "kpi":      {"family": FONT_FAMILY["heading"], "size": "1.25rem",  "weight": 400, "ltr_spacing": "-0.02em", "line_height": 1.1},
    "kpi_sm":   {"family": FONT_FAMILY["heading"], "size": "1.05rem",  "weight": 400, "ltr_spacing": "-0.02em", "line_height": 1.1},
    "mono":     {"family": FONT_FAMILY["mono"],    "size": "0.8rem",   "weight": 500, "ltr_spacing": "0",       "line_height": 1.4},
    "mono_sm":  {"family": FONT_FAMILY["mono"],    "size": "0.7rem",   "weight": 500, "ltr_spacing": "0",       "line_height": 1.3},
}

# ── SPACING SCALE (base 4px → rem) ───────────────────────────────────────────
S = {
    "2xs": "0.25rem",
    "xs":  "0.5rem",
    "sm":  "0.75rem",
    "md":  "1rem",
    "lg":  "1.5rem",
    "xl":  "2rem",
    "2xl": "3rem",
}

# ── BORDER RADIUS ─────────────────────────────────────────────────────────────
R = {
    "sm":   "6px",
    "md":   "8px",
    "lg":   "10px",
    "xl":   "12px",
    "2xl":  "14px",
    "pill": "9999px",
}

# ── SHADOW TOKENS ─────────────────────────────────────────────────────────────
SHADOW = {
    "sm":  "0 1px 3px rgba(15,27,61,0.06)",
    "md":  "0 4px 12px rgba(15,27,61,0.08)",
    "lg":  "0 8px 24px rgba(15,27,61,0.10)",
    "xl":  "0 12px 36px rgba(15,27,61,0.12)",
    "kpi": "0 10px 28px rgba(15,27,61,0.12)",
}

# ── BREAKPOINTS ───────────────────────────────────────────────────────────────
BP = {
    "sm":  "640px",
    "md":  "768px",
    "lg":  "1024px",
    "xl":  "1280px",
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS — Injected once via st.markdown
# ─────────────────────────────────────────────────────────────────────────────
def inject_global_css():
    st.markdown(f"""
    <style>
    *, *::before, *::after {{ box-sizing: border-box; }}

    /* ── Force Light Mode (override system/browser dark mode) ── */
    :root {{
        color-scheme: light !important;
        --background-color: {C['neutrals']['bg']} !important;
        --secondary-background-color: {C['neutrals']['surface']} !important;
        --text-color: {C['text']['primary']} !important;
    }}

    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stApp"],
    [data-testid="stAppViewBlockContainer"], .stApp {{
        background-color: {C['neutrals']['bg']} !important;
        color: {C['text']['primary']} !important;
        font-family: {FONT_FAMILY['body']} !important;
    }}

    /* Override ALL Streamlit dark mode variables */
    [data-theme="dark"],
    .stThemeLight[data-theme="dark"],
    html[data-theme="dark"] {{
        --background-color: {C['neutrals']['bg']} !important;
        --secondary-background-color: {C['neutrals']['surface']} !important;
        --text-color: {C['text']['primary']} !important;
        color-scheme: light !important;
    }}

    /* Force all containers to light background */
    [data-theme="dark"] [data-testid="stAppViewContainer"],
    [data-theme="dark"] .main,
    [data-theme="dark"] [data-testid="stApp"],
    [data-theme="dark"] [data-testid="stAppViewBlockContainer"],
    [data-theme="dark"] .stApp {{
        background-color: {C['neutrals']['bg']} !important;
    }}

    [data-theme="dark"] [data-testid="stSidebar"] {{
        background: {C['text']['primary']} !important;
    }}

    #MainMenu, footer {{ visibility: hidden !important; }}

    /* ── Sidebar collapse button — must be visible ── */
    [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] ~ [data-testid="stSidebarCollapseButton"],
    [data-testid="stDecoration"] [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
    }}

    ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
    ::-webkit-scrollbar-track {{ background: {C['neutrals']['elevated']}; }}
    ::-webkit-scrollbar-thumb {{ background: {C['text']['disabled']}; border-radius: {R['pill']}; }}

    .block-container {{
        padding: {S['lg']} {S['xl']} {S['2xl']} {S['xl']} !important;
        max-width: 100% !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {C['text']['primary']} !important;
        border-right: 1px solid #1a2d5a !important;
    }}
    [data-testid="stSidebar"] > div {{ padding-top: 0 !important; }}
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label {{
        color: {C['text']['muted']} !important;
        font-size: {TYPE['label']['size']} !important;
        letter-spacing: {TYPE['label']['ltr_spacing']} !important;
        text-transform: uppercase !important;
        font-family: {FONT_FAMILY['body']} !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: #1a2d5a !important;
        border: 1px solid #2a4080 !important;
        border-radius: {R['md']} !important;
        color: #e8edf8 !important;
    }}

    /* ── Tabs ── */
    [data-testid="stTabs"] [role="tablist"] {{
        border-bottom: 1px solid {C['text']['disabled']} !important;
        gap: 0 !important;
        background: #0B1929 !important;
        border-radius: {R['md']} !important;
        padding: 0.5rem 0.5rem 0 0.5rem !important;
        display: flex !important;
        justify-content: center !important;
    }}
    [data-testid="stTabs"] button[role="tab"] {{
        background: transparent !important;
        color: #d0d8e8 !important;
        font-family: {FONT_FAMILY['heading']} !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        letter-spacing: {TYPE['h3']['ltr_spacing']} !important;
        text-transform: uppercase !important;
        padding: 1rem 2.2rem !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        border-radius: {R['md']} {R['md']} 0 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        position: relative !important;
    }}
    [data-testid="stTabs"] button[role="tab"]:hover {{
        color: #ffffff !important;
        background: rgba(255,255,255,0.1) !important;
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        color: #ffffff !important;
        background: rgba(255,255,255,0.15) !important;
        border-bottom: 3px solid {C['brand']['primary']} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stTabs"] [role="tabpanel"] {{
        padding-top: {S['lg']} !important;
    }}

    /* ── DataFrames ── */
    [data-testid="stDataFrame"] {{
        border: 1px solid {C['border']['default']} !important;
        border-radius: {R['xl']} !important;
        overflow: hidden !important;
    }}

    /* ── Focus States (Accessibility) ── */
    button:focus-visible, a:focus-visible, [role="tab"]:focus-visible {{
        outline: 3px solid {C['brand']['primary']} !important;
        outline-offset: 2px !important;
    }}

    [data-baseweb="select"]:focus-within {{
        border-color: {C['brand']['primary']} !important;
        box-shadow: 0 0 0 3px rgba(24,71,194,0.2) !important;
    }}

    /* ── Interactive Elements Hover States ── */
    .ds-kpi-card {{
        cursor: default !important;
    }}

    [data-testid="stDataFrame"]:hover {{
        box-shadow: {SHADOW['md']} !important;
        transition: box-shadow 0.2s ease !important;
    }}

    /* ── Plotly chart containers ── */
    [data-testid="stPlotlyChart"] {{
        background: transparent !important;
    }}

    [data-testid="stPlotlyChart"] > div {{
        border-radius: {R['2xl']} !important;
        border: 1px solid {C['border']['faint']} !important;
        box-shadow: {SHADOW['sm']};
        transition: box-shadow 0.2s ease !important;
    }}

    [data-testid="stPlotlyChart"]:hover > div {{
        box-shadow: {SHADOW['md']} !important;
    }}

    [data-testid="metric-container"] {{
        background: transparent !important;
        border: none !important;
    }}

    /* ── Responsive container tweaks ── */
    @media (max-width: {BP['md']}) {{
        .block-container {{
            padding: {S['md']} !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# COMPONENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def kpi_card(title, value, subtitle="", accent=None, icon=""):
    if accent is None:
        accent = C["brand"]["primary"]
    icon_html = ICONS.get(icon, "")
    st.markdown(f"""
    <div class="ds-kpi-card" style="
        background: {C['neutrals']['surface']};
        border: 1px solid {C['border']['default']};
        border-top: 3px solid {accent};
        border-radius: {R['xl']};
        padding: {S['md']} 1.1rem 0.9rem 1.1rem;
        position: relative;
        overflow: visible;
        min-height: 115px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: {SHADOW['sm']};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: default;
    " onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='{SHADOW['kpi']}'"
       onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='{SHADOW['sm']}'">
        <div style="
            position: absolute; top: -8px; right: -4px;
            opacity: 0.06; line-height: 1;
            pointer-events: none; color: {accent};
        ">{icon_html}</div>
        <p style="
            color: {C['text']['muted']}; font-size: {TYPE['label']['size']}; font-weight: {TYPE['label']['weight']};
            letter-spacing: {TYPE['label']['ltr_spacing']}; text-transform: uppercase;
            font-family: {FONT_FAMILY['body']}; margin: 0 0 0.35rem 0;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        ">{title}</p>
        <h2 style="
            color: {C['text']['primary']}; font-family: {FONT_FAMILY['heading']};
            font-size: {TYPE['kpi']['size']}; font-weight: {TYPE['kpi']['weight']}; line-height: {TYPE['kpi']['line_height']};
            margin: 0 0 0.35rem 0; letter-spacing: {TYPE['kpi']['ltr_spacing']};
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        ">{value}</h2>
        <p style="
            color: {C['text']['muted']}; font-size: {TYPE['caption']['size']}; margin: 0;
            overflow: hidden; text-overflow: ellipsis;
            white-space: nowrap; line-height: {TYPE['caption']['line_height']};
        ">{subtitle}</p>
        <div style="
            position: absolute; bottom: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, {accent}, transparent);
            opacity: 0.25; border-radius: 0 0 {R['xl']} {R['xl']};
        "></div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title, subtitle=""):
    sub_html = (
        f'<p style="color:{C["text"]["muted"]}; font-size:{TYPE["subhead"]["size"]}; '
        f'margin:0.2rem 0 0 0; font-family:{FONT_FAMILY["body"]};">{subtitle}</p>'
    ) if subtitle else ""
    st.markdown(f"""
    <div style="margin: {S['xl']} 0 {S['lg']} 0;">
        <h3 style="
            font-family: {FONT_FAMILY['heading']};
            font-size: {TYPE['h3']['size']}; font-weight: {TYPE['h3']['weight']};
            letter-spacing: {TYPE['h3']['ltr_spacing']}; text-transform: uppercase;
            color: {C['brand']['primary']}; margin: 0 0 0.3rem 0;
        ">◆ {title}</h3>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def status_bar():
    st.markdown(f"""
    <div style="
        height: 3px;
        background: linear-gradient(90deg, {C['brand']['primary']}, {C['brand']['secondary']}, {C['brand']['positive']});
        border-radius: {R['pill']};
        margin-bottom: {S['xl']};
    "></div>
    """, unsafe_allow_html=True)


def chart_wrap(fig, height=340):
    fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def chart_container(fig, height=340):
    fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────

def register_plotly_theme():
    pio.templates["ds-theme"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(family=FONT_FAMILY["body"], color=C["text"]["primary"], size=11),
            colorway=C["chart"]["palette"],
            xaxis=dict(
                gridcolor=C["chart"]["grid"],
                linecolor=C["chart"]["grid"],
                tickcolor=C["border"]["strong"],
                tickfont=dict(size=10),
                zeroline=False,
            ),
            yaxis=dict(
                gridcolor=C["chart"]["grid"],
                linecolor=C["chart"]["grid"],
                tickcolor=C["border"]["strong"],
                tickfont=dict(size=10),
                zeroline=False,
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor=C["chart"]["grid"],
                font=dict(color=C["text"]["primary"], size=10),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
            margin=dict(l=16, r=16, t=50, b=16),
            hoverlabel=dict(
                bgcolor=C["text"]["primary"],
                bordercolor=C["brand"]["primary"],
                font=dict(color=C["text"]["inverse"], size=11, family=FONT_FAMILY["body"]),
            ),
            title=dict(
                font=dict(family=FONT_FAMILY["heading"], color=C["text"]["primary"], size=13),
                x=0,
                xanchor="left",
            ),
        )
    )
    pio.templates.default = "ds-theme"
