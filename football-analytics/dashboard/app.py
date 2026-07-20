import streamlit as st
from streamlit_option_menu import option_menu

from data import (
    load_denormalized,
    search_entities,
    player_latest_context,
    team_latest_context
)

from pages_lib import (
    home,
    player_season,
    team_season,
    league_ranking,
    similarity
)

st.set_page_config(
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide"
)

CUSTOM_CSS = """
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
.sidebar-brand { display:flex; align-items:center; gap:12px; padding:10px 4px 18px; border-bottom:1px solid #26363a; margin-bottom:16px; }
.sidebar-brand-mark { width:42px; height:42px; display:flex; align-items:center; justify-content:center; border-radius:13px; color:#65e6b7; background:linear-gradient(145deg,#173e38,#102522); border:1px solid #2e8c76; box-shadow:0 0 22px rgba(68,215,167,.13); }
.sidebar-brand-mark svg { width:25px; height:25px; fill:none; stroke:currentColor; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round; }
.sidebar-brand-title { color:#f4faf8; font-size:17px; font-weight:800; line-height:1.1; }
.sidebar-brand-subtitle { color:#8da8a2; font-size:11px; margin-top:4px; letter-spacing:.3px; }
.sidebar-block-title { color:#b7d0ca; font-size:11px; font-weight:750; letter-spacing:1px; text-transform:uppercase; margin:8px 0; }
[data-testid="stSidebar"] .stTextInput input { height:42px; background:#172022 !important; border:1px solid #2c4546 !important; border-radius:12px !important; color:#eefaf6 !important; }
[data-testid="stSidebar"] .stTextInput input:focus { border-color:#44d7a7 !important; box-shadow:0 0 0 1px #44d7a7 !important; }
[data-testid="stSidebar"] .stButton button { border:1px solid #294343; background:#172323; color:#d8ebe6; border-radius:10px; text-align:left; }
[data-testid="stSidebar"] .stButton button:hover { border-color:#44d7a7; color:#fff; }

[data-testid="stSidebar"] [data-testid="stSelectbox"] label,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] label,
[data-testid="stSidebar"] [data-testid="stSlider"] label {
    color:#c7ddd7 !important;
    font-size:13px !important;
    font-weight:600 !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] svg,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] svg {
    color:#62e6b5 !important;
    fill:#62e6b5 !important;
}

[data-testid="stSlider"] [role="slider"] {
    background:#44d7a7 !important;
    border:2px solid #0e2623 !important;
    box-shadow:0 0 0 2px rgba(68,215,167,.2) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {
    background:#44d7a7 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    background:#203334 !important;
}

div[data-baseweb="switch"] input:checked + div {
    background:#44d7a7 !important;
}

[data-testid="stMetric"] {
    background-color: rgba(45, 212, 191, 0.06);
    border: 1px solid rgba(45, 212, 191, 0.18);
    border-radius: 10px;
    padding: 10px 14px;
}

[data-testid="stMetricLabel"] {
    opacity: 0.75;
    font-size: 0.8rem;
}

[data-testid="stMetricValue"] {
    font-size: 1.35rem;
}

[data-testid="stSidebar"] {
    background: #111418;
    border-right: 1px solid #232a33;
}

.stTextInput input {
    background: #181c21 !important;
    color: white !important;
    border: 1px solid #2b313a !important;
    border-radius: 12px !important;
}

.search-hit-btn button {
    width: 100%;
    text-align: left;
}

hr {
    margin: 0.6rem 0;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


st.markdown("""
<style>

/* Toggle OFF */
div[data-baseweb="switch"] > div {
    background-color: #4b5563 !important;
}

/* Toggle ON */
div[data-baseweb="switch"] input:checked + div {
    background-color: #2dd4bf !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Data Editor */
[data-testid="stDataEditor"] {
    border: 1px solid #374151;
    border-radius: 12px;
}

/* Header */
[data-testid="stDataEditor"] thead th {
    background: #111827 !important;
    color: #e5e7eb !important;
    font-weight: 600 !important;
}

/* Cells */
[data-testid="stDataEditor"] tbody td {
    background: #0f172a !important;
    color: #d1d5db !important;
}

/* Hover */
[data-testid="stDataEditor"] tbody tr:hover td {
    background: #1e293b !important;
}

/* Unified dataframe styling */
[data-testid="stDataFrame"] {
    border: 1px solid #274141 !important;
    border-radius: 15px !important;
    overflow: hidden !important;
    background: #122323 !important;
}

[data-testid="stDataFrame"] [role="columnheader"] {
    background: #173331 !important;
    color: #d7ebe5 !important;
    border-color: #294a47 !important;
    font-weight: 700 !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {
    background: #122323 !important;
    color: #c7ddd7 !important;
    border-color: #203c3a !important;
}

[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] {
    background: #1a3533 !important;
}

</style>
""", unsafe_allow_html=True)

def _go_to_player(player_name: str, latest: dict):
    st.session_state["nav_page"] = "Player Scout"
    st.session_state["ps_league"] = latest["league"]
    st.session_state["ps_season"] = latest["season"]
    st.session_state["ps_team"] = "All Teams"
    st.session_state["ps_min_minutes"] = 0
    st.session_state["ps_player"] = player_name
    st.session_state["ps_compare_toggle"] = False
    st.session_state["global_search"] = ""


def _go_to_team(team_name: str, latest: dict):
    st.session_state["nav_page"] = "Team Analysis"
    st.session_state["ts_league"] = latest["league"]
    st.session_state["ts_season"] = latest["season"]
    st.session_state["ts_team"] = team_name
    st.session_state["global_search"] = ""


df = load_denormalized()

if df.empty:
    st.error(
        "No data found. Run prj_fixed.ipynb first to generate the processed/*.csv files."
    )
    st.stop()

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Analytics Hub"

with st.sidebar:



    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-mark">
            <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9"/>
                <path d="m12 7 2.2 1.6-.8 2.6h-2.8l-.8-2.6L12 7Z"/>
                <path d="m5.1 9.2 3.3.7M15.6 9.9l3.3-.7M10.6 11.2 8.8 15M13.4 11.2l1.8 3.8M8.8 15l3.2 2.1 3.2-2.1"/>
            </svg>
        </div>
        <div><div class="sidebar-brand-title">Football Analytics</div><div class="sidebar-brand-subtitle">Football Intelligence Platform</div></div>
    </div>
    <div class="sidebar-block-title">Global Search</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-mark">
            <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9"/>
                <path d="m12 7 2.2 1.6-.8 2.6h-2.8l-.8-2.6L12 7Z"/>
                <path d="m5.1 9.2 3.3.7M15.6 9.9l3.3-.7M10.6 11.2 8.8 15M13.4 11.2l1.8 3.8M8.8 15l3.2 2.1 3.2-2.1"/>
            </svg>
        </div>
        <div><div class="sidebar-brand-title">Football Analytics</div><div class="sidebar-brand-subtitle">Football Intelligence Platform</div></div>
    </div>
    <div class="sidebar-block-title">Global Search</div>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div class="sidebar-block-title">
        Find a player or club
    </div>
    """,
    unsafe_allow_html=True,
    )

    query = st.text_input(
        "Find a player or club",
        key="global_search",
        placeholder="e.g. Messi, Arsenal..",
        label_visibility="collapsed",
    )
    
    if query:

        matching_players, matching_teams = search_entities(df, query)

        if not matching_players and not matching_teams:
            st.caption("No matches found")

        for p in matching_players:
            st.button(
                f"👤 {p}",
                key=f"hit_player_{p}",
                on_click=_go_to_player,
                args=(p, player_latest_context(df, p))
            )

        for t in matching_teams:
            st.button(
                f"🏟️ {t}",
                key=f"hit_team_{t}",
                on_click=_go_to_team,
                args=(t, team_latest_context(df, t))
            )

        st.divider()

    st.markdown('<div class="sidebar-block-title">Workspace</div>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=[
            "Analytics Hub",
            "Player Scout",
            "Team Analysis",
            "League Rankings",
            "Similar Players"
        ],
        icons=[
            "house",
            "person",
            "shield",
            "trophy",
            "bullseye"
        ],
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#111418"
            },
            "icon": {
                "color": "#20c997",
                "font-size": "16px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "padding": "10px",
                "margin": "3px 0",
                "border-radius": "10px"
            },
            "nav-link-selected": {
                "background-color": "#1f252d"
            }
        }
    )

    page = selected
    st.session_state["nav_page"] = selected

    st.markdown("""
    <div style="border-top:1px solid #26363a;margin:18px 0 14px;padding-top:14px;color:#8da8a2;font-size:12px;line-height:1.7">
        <span style="color:#62e6b5">TOP 5 LEAGUES</span><br>
        European football data · 2017–2026
    </div>
    """, unsafe_allow_html=True)

if page == "Analytics Hub":
    home.render(df)

elif page == "Player Scout":
    player_season.render(df)

elif page == "Team Analysis":
    team_season.render(df)

elif page == "League Rankings":
    league_ranking.render(df)

elif page == "Similar Players":
    similarity.render(df)
