import streamlit as st
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from pages_lib.ui import inject_styles, hero, section


def render(df):
    inject_styles()

    hero(
        "Player Analytics",
        "Player Similarity Comparison",
        "Find players with a similar statistical profile",
    )
    section("Similarity Filters", "chart")

    filter_left, filter_right = st.columns(2)
    with filter_left:
        season = st.selectbox("Season", sorted(df["season"].unique()))
    with filter_right:
        league = st.selectbox(
            "League",
            ["All Leagues"] + sorted(df["league"].dropna().unique()),
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

    player_col, number_col = st.columns([1.4, 1])
    with player_col:
        player = st.selectbox("Player", sorted(season_df["player"].unique()))

    section("Selected Player Profile", "users")

    scaler = StandardScaler()

    X = scaler.fit_transform(
        season_df[FEATURES]
    )

    similarity_matrix = cosine_similarity(X)

    player_to_idx = {
        player: idx
        for idx, player in enumerate(season_df["player"])
    }

    with number_col:
        top_n = st.slider(
            "Number of Similar Players",
            min_value=3,
            max_value=15,
            value=5,
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

    section(f"Players Similar to {player}", "target")

    if len(result) >= 3:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Best Match",
                result.iloc[0]["player"],
                f"{result.iloc[0]['Similarity']}%"
            )

        with col2:
            st.metric(
                "Second Match",
                result.iloc[1]["player"],
                f"{result.iloc[1]['Similarity']}%"
            )

        with col3:
            st.metric(
                "Third Match",
                result.iloc[2]["player"],
                f"{result.iloc[2]['Similarity']}%"
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
            autorange="reversed",
            gridcolor="#29403e",
            zeroline=False,
        ),
        xaxis_title="Similarity %",
        yaxis_title="",
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b8cfca", size=13),
        xaxis=dict(gridcolor="#29403e", zeroline=False, tickfont=dict(size=12)),
        margin=dict(l=10, r=20, t=10, b=16),
    )

    fig.update_traces(
        marker_color="#44d7a7",
        textfont=dict(color="#effaf7", size=12),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )
