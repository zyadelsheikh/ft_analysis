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
    page_title="TopFive Analytics",
    page_icon="⚽",
    layout="wide"
)

CUSTOM_CSS = """
<style>

/* ---------- APP ---------- */

.stApp{
    background:#0f1318;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"]{
    background:#111418;
    border-right:1px solid #232a33;
}

/* ---------- SEARCH ---------- */

.stTextInput input{
    background:#181c21 !important;
    color:white !important;

    border:1px solid #2b313a !important;
    border-radius:12px !important;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"]{
    background:#181c21;
    border:1px solid #252b33;
    border-radius:12px;
    padding:12px;
}

/* ---------- LAYOUT ---------- */

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

/* ---------- TOGGLES ---------- */

div[data-baseweb="switch"] > div{
    background-color:#4b5563 !important;
}

div[data-baseweb="switch"] input:checked + div{
    background-color:#20c997 !important;
}

/* ---------- RADIO ---------- */

div[role="radiogroup"] label{
    font-size:18px !important;
    font-weight:600 !important;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
        ⚽ TopFive Analytics
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

    pages = [
        "Analytics Hub",
        "Player Scout",
        "Team Analysis",
        "League Rankings",
        "Similar Players"
    ]

    icons = [
        "house",
        "person",
        "shield",
        "trophy",
        "bullseye"
    ]

    current_page = st.session_state.get(
        "nav_page",
        "Analytics Hub"
    )

    page_index = 0

    page_mapping = {
        "Analytics Hub": 0,
        "Player Scout": 1,
        "Team Analysis": 2,
        "League Rankings": 3,
        "League Leaderboards": 3,
        "Similar Players": 4,
        "Player Similarity Finder": 4
    }

    page_index = page_mapping.get(
        current_page,
        0
    )

    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=icons,
        default_index=page_index,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#111418"
            },
            "icon": {
                "color": "#20c997",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "padding": "12px",
                "margin": "4px 0",
                "border-radius": "10px",
                "--hover-color": "#1f252d"
            },
            "nav-link-selected": {
                "background-color": "#1f252d"
            }
        }
    )

    st.session_state["nav_page"] = selected

    st.markdown("""
    <hr>

    <div style='color:#9ca3af;font-size:13px'>
        🌍 Top 5 European Leagues<br>
        2017–2026
    </div>
    """, unsafe_allow_html=True)

page = st.session_state["nav_page"]

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
