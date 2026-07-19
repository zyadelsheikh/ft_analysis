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
    <h1 style='margin-bottom:0;color:white'>
        ⚽ Football Analytics
    </h1>

    <p style='color:#9ca3af;margin-top:0'>
        Football Intelligence Platform
    </p>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "Search Players & Clubs",
        key="global_search",
        placeholder="e.g. Messi, Arsenal..."
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
    <hr>

    <div style='color:#9ca3af;font-size:13px'>
        🌍 Top 5 European Leagues<br>
        2017–2026
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
