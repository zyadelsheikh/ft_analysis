import numpy as np
import pandas as pd
import streamlit as st


FEATURES = [
    "Goals",
    "Assists",
    "Expected_Goals",
    "Expected_Assists",
    "Shots",
    "Key_Passes",
    "Progressive_Carries",
    "Tackles",
    "Interceptions",
]


def render(df: pd.DataFrame):
    st.title("Similar Players")

    available_features = [col for col in FEATURES if col in df.columns]
    if not available_features:
        st.warning("No similarity metrics are available in this dataset.")
        return

    seasons = sorted(df["season"].dropna().unique())
    if not seasons:
        st.warning("No seasons are available.")
        return

    season = st.selectbox("Choose Season", seasons, key="sim_season")
    season_df = df[df["season"] == season].copy()
    season_df = season_df.dropna(subset=available_features).reset_index(drop=True)

    if season_df.empty:
        st.warning("No players have enough data for similarity in this season.")
        return

    players = sorted(season_df["player"].dropna().unique())
    if not players:
        st.warning("No players are available for this season.")
        return

    player = st.selectbox("Choose Player", players, key="sim_player")
    top_n = st.slider("Number of similar players", 3, 20, 10, key="sim_top_n")

    result = _get_similar_players(season_df, player, available_features, top_n)
    st.dataframe(result, use_container_width=True, hide_index=True)


def _get_similar_players(season_df: pd.DataFrame, player: str, features: list[str], top_n: int):
    matrix = season_df[features].astype(float)
    std = matrix.std(ddof=0).replace(0, 1)
    scaled = ((matrix - matrix.mean()) / std).to_numpy()

    player_matches = season_df.index[season_df["player"] == player].tolist()
    if not player_matches:
        return pd.DataFrame(columns=["player", "team", "Similarity"])

    player_idx = player_matches[0]
    norms = np.linalg.norm(scaled, axis=1)
    denom = norms * norms[player_idx]
    scores = np.divide(
        scaled @ scaled[player_idx],
        denom,
        out=np.zeros(len(season_df), dtype=float),
        where=denom != 0,
    )

    similar_idx = np.argsort(scores)[::-1]
    similar_idx = [idx for idx in similar_idx if idx != player_idx][:top_n]

    columns = [col for col in ["player", "team", "league", "season"] if col in season_df.columns]
    result = season_df.iloc[similar_idx][columns].copy()
    result["Similarity"] = (scores[similar_idx] * 100).round(1)
    return result
