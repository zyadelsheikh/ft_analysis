import streamlit as st
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def render(df):

    st.subheader("📊 Player Similarity Comparison")

    season = st.selectbox(
        "Season",
        sorted(df["season"].unique())
    )

    league = st.selectbox(
        "League",
        ["All Leagues"] + sorted(df["league"].dropna().unique())
    )

    season_df = df[
        df["season"] == season
    ].copy()

    if league != "All Leagues":
        season_df = season_df[
            season_df["league"] == league
        ]

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
        "Player",
        sorted(season_df["player"].unique())
    )

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

    st.markdown("---")

    st.subheader(
        f"Players Similar to {player}"
    )

    if len(result) >= 3:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🥇 Most Similar",
                result.iloc[0]["player"],
                f"{result.iloc[0]['Similarity']}%"
            )

        with col2:
            st.metric(
                "🥈 Second Closest",
                result.iloc[1]["player"],
                f"{result.iloc[1]['Similarity']}%"
            )

        with col3:
            st.metric(
                "🥉 Third Closest",
                result.iloc[2]["player"],
                f"{result.iloc[2]['Similarity']}%"
            )

    

    st.markdown("---")

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
        yaxis_title="",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
