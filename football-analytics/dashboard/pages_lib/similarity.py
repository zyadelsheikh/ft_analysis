import streamlit as st
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def render(df):

    st.title("🔍 Similarity Comparison")

    season = st.selectbox(
        "Choose Season",
        sorted(df["season"].unique())
    )

    season_df = df[
        df["season"] == season
    ].copy()

    # Filter low-minute players
    if "Minutes" in season_df.columns:
        season_df = season_df[
            season_df["Minutes"] >= 900
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

    if season_df.empty:
        st.warning("No data available for this season.")
        return

    player = st.selectbox(
        "Choose Player",
        sorted(season_df["player"].unique())
    )

    # Position Filter
    if "position" in season_df.columns:

        player_position = (
            season_df.loc[
                season_df["player"] == player,
                "position"
            ]
            .iloc[0]
        )

        same_position = st.toggle(
            "Compare only same position",
            value=True
        )

        if same_position:
            season_df = season_df[
                season_df["position"] == player_position
            ].reset_index(drop=True)

    scaler = StandardScaler()

    X = scaler.fit_transform(
        season_df[FEATURES]
    )

    similarity_matrix = cosine_similarity(X)

    player_to_idx = {
        player: idx
        for idx, player in enumerate(season_df["player"])
    }

    top_n = st.slider(
        "Number of Similar Players",
        min_value=3,
        max_value=15,
        value=5
    )

    def get_similar_players(player_name, top_n=5):

        idx = player_to_idx[player_name]

        scores = similarity_matrix[idx]

        similar_idx = (
            scores.argsort()[::-1][1:top_n + 1]
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

    result = get_similar_players(
        player,
        top_n
    )

    st.subheader(
        f"Players Similar to {player}"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

    fig = px.bar(
        result,
        x="Similarity",
        y="player",
        orientation="h",
        text="Similarity"
    )

    fig.update_layout(
        yaxis=dict(
            autorange="reversed"
        ),
        xaxis_title="Similarity %",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
