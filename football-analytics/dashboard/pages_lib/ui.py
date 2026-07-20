import pandas as pd
import plotly.graph_objects as go
import streamlit as st


CHART_TEXT = "#d8ebe6"
CHART_MUTED = "#a8c1bb"
CHART_GRID = "#29403e"
CHART_PANEL = "rgba(18,35,35,.94)"


def style_chart(fig: go.Figure) -> go.Figure:
    """Apply the shared dark theme and readable hover treatment to every chart."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=CHART_TEXT, size=12),
        hoverlabel=dict(
            bgcolor="#173331",
            bordercolor="#55dcb2",
            font=dict(color="#f4faf8", size=13, family="Arial"),
            align="left",
        ),
        legend=dict(
            bgcolor=CHART_PANEL,
            bordercolor="#35635b",
            borderwidth=1,
            font=dict(color=CHART_TEXT, size=12),
        ),
    )
    return fig


def styled_dataframe(df: pd.DataFrame):
    """Return a dataframe styled to remain legible inside the dark dashboard."""
    return (
        df.style
        .set_properties(**{
            "background-color": "#122323",
            "color": "#e1f0ec",
            "border-color": "#294a47",
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#173331"),
                    ("color", "#f0faf7"),
                    ("font-weight", "700"),
                    ("border-color", "#35635b"),
                ],
            },
            {
                "selector": "tbody tr:hover td",
                "props": [("background-color", "#1d403c"), ("color", "#ffffff")],
            },
        ])
    )


def inject_styles():
    st.markdown(
        """
        <style>
        .app-hero { background: linear-gradient(135deg,#172b2b 0%,#102020 55%,#0c1515 100%); border:1px solid #274444; border-radius:20px; padding:26px 28px 22px; margin:4px 0 22px; box-shadow:0 14px 36px rgba(0,0,0,.18); }
        .app-kicker { color:#62e6b5; font-size:12px; font-weight:700; letter-spacing:1.6px; text-transform:uppercase; margin-bottom:7px; }
        .app-title { color:#f8fafc; font-size:34px; font-weight:800; line-height:1.1; margin:0; }
        .app-subtitle { color:#b3c6c3; font-size:14px; margin-top:8px; }
        .app-section { color:#e7f5f1; font-size:19px; font-weight:750; margin:18px 0 14px; }
        .app-section-row { display:flex; align-items:center; gap:11px; }
        .app-section-icon { width:36px; height:36px; display:flex; align-items:center; justify-content:center; border-radius:11px; color:#62e6b5; background:linear-gradient(135deg,#193c38,#122323); border:1px solid #2d6258; }
        .app-section-icon svg { width:21px; height:21px; fill:none; stroke:currentColor; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
        .filter-panel-title { color:#b7d0ca; font-size:11px; font-weight:750; letter-spacing:1px; text-transform:uppercase; margin:12px 0 8px; }
        [data-testid="stSelectbox"] label, [data-testid="stSlider"] label { color:#c7ddd7 !important; font-size:14px !important; font-weight:650 !important; }
        [data-testid="stSelectbox"] > div > div, [data-testid="stMultiSelect"] > div > div { background:#172323; border-color:#2c4546; border-radius:11px; }
        [data-testid="stSlider"] { padding:4px 2px 8px; }
        [data-testid="stSelectbox"] svg, [data-testid="stMultiSelect"] svg { color:#62e6b5 !important; fill:#62e6b5 !important; }
        [data-testid="stSlider"] [role="slider"] { background:#44d7a7 !important; border:2px solid #0e2623 !important; box-shadow:0 0 0 2px rgba(68,215,167,.2) !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div { background:#44d7a7 !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child { background:#203334 !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] { background:#44d7a7 !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] { background:#44d7a7 !important; }
        .app-card { background:#122323; border:1px solid #274141; border-radius:14px; padding:14px 15px; margin-bottom:10px; }
        div[data-testid="stMetric"] {
            position:relative;
            min-height:88px;
            background:linear-gradient(145deg,rgba(28,52,51,.92),rgba(17,31,31,.96));
            border:1px solid rgba(68,215,167,.24);
            border-radius:15px;
            padding:14px 16px;
            box-shadow:0 8px 24px rgba(0,0,0,.12);
            overflow:hidden;
        }
        div[data-testid="stMetric"]::before {
            content:"";
            position:absolute;
            left:0;
            top:0;
            width:100%;
            height:3px;
            background:linear-gradient(90deg,#44d7a7,#60a5fa);
            opacity:.85;
        }
        div[data-testid="stMetric"]:hover {
            border-color:rgba(68,215,167,.5);
            transform:translateY(-1px);
            transition:all .18s ease;
        }
        div[data-testid="stMetricLabel"] {
            color:#9db6b1 !important;
            font-size:11px !important;
            font-weight:700 !important;
            letter-spacing:.7px;
            text-transform:uppercase;
        }
        div[data-testid="stMetricValue"] {
            color:#f4faf8 !important;
            font-size:25px !important;
            font-weight:800 !important;
            line-height:1.15;
            margin-top:5px;
        }
        div[data-testid="stMetricDelta"] { font-size:11px !important; }
        div[data-testid="stPlotlyChart"] { background:#122323; border:1px solid #274141; border-radius:16px; padding:8px; }
        div[data-testid="stPlotlyChart"] > div { background:#122323 !important; border-radius:12px; }
        div[data-testid="stPlotlyChart"] iframe { background:#122323 !important; }
        [data-testid="stDataFrame"] { background:#122323 !important; border:1px solid #35635b !important; border-radius:15px !important; overflow:hidden !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(kicker: str, title: str, subtitle: str):
    st.markdown(
        f'<div class="app-hero"><div class="app-kicker">{kicker}</div>'
        f'<div class="app-title">{title}</div>'
        f'<div class="app-subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def section(title: str, icon: str = "chart"):
    icons = {
        "trophy": '<svg viewBox="0 0 24 24"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4Z"/><path d="M7 7H4a3 3 0 0 0 3 3M17 7h3a3 3 0 0 1-3 3"/></svg>',
        "target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
        "chart": '<svg viewBox="0 0 24 24"><path d="M4 19V5M4 19h16M7 15l3-4 3 2 5-6"/></svg>',
        "users": '<svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    }

    st.markdown(
        f'<div class="app-section app-section-row">'
        f'<span class="app-section-icon">{icons.get(icon, icons["chart"])}</span>'
        f'<span>{title}</span></div>',
        unsafe_allow_html=True,
    )
