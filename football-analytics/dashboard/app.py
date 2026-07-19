import streamlit as st

from data import load_denormalized, search_entities, player_latest_context, team_latest_context
from pages_lib import (
    home,
    player_season,
    team_season,
    league_ranking,
    similarity
)
st.set_page_config(page_title="Football Analytics", page_icon="⚽", layout="wide")

CUSTOM_CSS = """
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background-color: rgba(45, 212, 191, 0.06);
    border: 1px solid rgba(45, 212, 191, 0.18);
    border-radius: 10px;
    padding: 10px 14px;
}
[data-testid="stMetricLabel"] {opacity: 0.75; font-size: 0.8rem;}
[data-testid="stMetricValue"] {font-size: 1.35rem;}
section[data-testid="stSidebar"] {border-right: 1px solid rgba(255,255,255,0.06);}
.search-hit-btn button {width: 100%; text-align: left;}
hr {margin: 0.6rem 0;}
</style>
"""


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




st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown("""
<style>

div[role="radiogroup"] label {
    font-size: 18px !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
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
    st.error("No data found. Run prj_fixed.ipynb first to generate the processed/*.csv files.")
    st.stop()

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Analytics Hub"

with st.sidebar:

    st.markdown("#⚽ Football Data Analytics")

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


    if st.button("Analytics Hub", use_container_width=True):
        st.session_state["nav_page"] = "Analytics Hub"
    
    if st.button("Player Scout", use_container_width=True):
        st.session_state["nav_page"] = "Player Scout"
    
    if st.button("Team Analysis", use_container_width=True):
        st.session_state["nav_page"] = "Team Analysis"
    
    if st.button("League Leaderboards", use_container_width=True):
        st.session_state["nav_page"] = "League Leaderboards"
    
    if st.button("Player Similarity Finder", use_container_width=True):
        st.session_state["nav_page"] = "Player Similarity Finder"
    
    page = st.session_state["nav_page"]

    st.caption("Top-5 European Leagues • 2017–2026")

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "📊 Analytics Hub"

if page == "Analytics Hub":
    home.render(df)

elif page == "Player Scout":
    player_season.render(df)

elif page == "Team Analysis":
    team_season.render(df)

elif page == "League Leaderboards":
    league_ranking.render(df)

elif page == "Player Similarity Finder":
    similarity.render(df) 
    
