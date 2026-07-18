import streamlit as st
from data import (
    RADAR_DEFAULT_METRICS,
    per90,
    percentile_rank,
    metric_has_data,
    player_trend
)
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from data import load_denormalized, search_entities, player_latest_context, team_latest_context
from pages_lib import home, player_season, team_season, league_ranking
df = load_denormalized()


st.title("🔍 Similar Players")


season = st.selectbox(
    "Choose Season",
    sorted(df["season"].unique())
)


season_df = df[
    df["season"] == season
]

FEATURES = [
    "Goals",
    "Assists",
    "Expected_Goals",
    "Expected_Assists",
    "Shots",
    "Key_Passes",
    "Progressive_Carries",
    "Tackles",
    "Interceptions"
]

season_df = season_df.dropna(
    subset=FEATURES
).reset_index(drop=True)

scaler = StandardScaler()

X = scaler.fit_transform(
    season_df[FEATURES]
)


similarity_matrix = cosine_similarity(X)

player_to_idx = {
    player: idx
    for idx, player in enumerate(season_df["player"])
}

player = st.selectbox(
    "Choose Player",
    sorted(season_df["player"].unique())
)

print(player)
print(player_to_idx[player])



def get_similar_players(player_name, top_n=5):
    
    idx = player_to_idx[player_name]

    scores = similarity_matrix[idx]

    similar_idx = (
        scores.argsort()[::-1][1:top_n+1]
    )

    result = season_df.iloc[
        similar_idx
    ][
        ["player", "team"]
    ].copy()

    result["Similarity"] = (
        scores[similar_idx] * 100
    ).round(1)

    return result



print(
    get_similar_players(
        "Mohamed Salah"
    )
)
