import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data import (
    RADAR_DEFAULT_METRICS,
    per90,
    percentile_rank,
    metric_has_data,
    player_trend,
)

from pages_lib.filters import (
    season_league_filters,
    min_minutes_filter,
    team_filter,
    any_league_season_player_picker,
    export_buttons,
)

st.markdown("""
<style>

[data-testid="stMetric"]{
    background:#111827;
    border:1px solid #1f2937;
    padding:14px;
    border-radius:12px;
}

[data-testid="stMetricLabel"]{
    font-size:14px;
}

[data-testid="stMetricValue"]{
    font-size:24px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

STAT_CARDS = [
    ("Goals", "Goals"),
    ("Assists", "Assists"),
    ("Expected_Goals", "xG"),
    ("Expected_Assists", "xA"),
    ("Shots", "Shots"),
    ("Shots_On_Target", "SoT"),
    ("Key_Passes", "Key Passes"),
    ("Tackles", "Tackles"),
    ("Interceptions", "Interceptions"),
    ("xg_diff", "Finishing Overperformance"),
]

EXTRA_STAT_CARDS = [
    ("pass_accuracy", "Pass Accuracy %"),
    ("shot_accuracy", "Shot Accuracy %"),
    ("goals_per90", "Goals / 90"),
    ("assists_per90", "Assists / 90"),
]

TREND_METRICS = [
    "Goals",
    "Assists",
    "Expected_Goals",
    "Expected_Assists"
]


def _with_extra_stats(row: pd.Series) -> dict:

    extra = {}

    pass_att = row.get("Pass_Attempts")
    pass_cmp = row.get("Pass_Completed")

    extra["pass_accuracy"] = (
        pass_cmp / pass_att * 100
        if pass_att
        and pd.notna(pass_att)
        and pass_att > 0
        else np.nan
    )

    shots = row.get("Shots")
    sot = row.get("Shots_On_Target")

    extra["shot_accuracy"] = (
        sot / shots * 100
        if shots
        and pd.notna(shots)
        and shots > 0
        else np.nan
    )

    nineties = row.get("Full_Match_Equivalents")

    extra["goals_per90"] = (
        row.get("Goals", np.nan) / nineties
        if nineties
        and pd.notna(nineties)
        and nineties > 0
        else np.nan
    )

    extra["assists_per90"] = (
        row.get("Assists", np.nan) / nineties
        if nineties
        and pd.notna(nineties)
        and nineties > 0
        else np.nan
    )

    return extra


def render(full_df: pd.DataFrame):

    with st.sidebar:

        pool, league, season, _ = season_league_filters(
            full_df,
            "ps"
        )

        pool = min_minutes_filter(
            pool,
            "ps"
        )

        st.markdown("### Player Selection")

        pool, team = team_filter(
            pool,
            "ps"
        )

        players = sorted(
            pool["player"]
            .dropna()
            .unique()
        )

        if not players:
            st.warning(
                "No players match these filters."
            )
            return

        player = st.selectbox(
            "Select Player",
            players,
            key="ps_player"
        )

        compare_on = st.toggle(
            "Compare Player",
            value=False,
            key="ps_compare_toggle"
        )

        compare_player = None
        compare_pool = None

        if compare_on:

            st.caption(
                "Compare against any player, from any league/season:"
            )

            compare_player, compare_pool = (
                any_league_season_player_picker(
                    full_df,
                    "ps_cmp"
                )
            )

    row = pool[
        pool["player"] == player
    ]

    if row.empty:

        st.warning(
            "No player data available for this competition / season."
        )
        return

    row = row.iloc[0]

    _render_header(
        player,
        league,
        season,
        row
    )

    st.divider()

    advanced_available = metric_has_data(
        pool,
        "Expected_Goals"
    )

    if not advanced_available:

        st.warning(
            f"Advanced stats (xG, xA, Shots, Progressive actions, Tackles, etc.) "
            f"are not available in the source data for {season}."
        )

    left, right = st.columns([1.1, 1])

    with left:

        st.markdown(
            "## Player Performance Profile"
        )

        metrics = [
            m
            for m in RADAR_DEFAULT_METRICS
            if metric_has_data(pool, m)
        ]

        if len(metrics) >= 3:

            fig = _build_radar(
                pool,
                player,
                metrics,
                compare_pool,
                compare_player
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if compare_player:

                st.caption(
                    "Each player's percentile is computed against their own league/season peer group."
                )

        else:

            st.info(
                "Not enough metrics with data in this season to draw a radar chart."
            )
            
        with right:

         if compare_player and compare_pool is not None:
 
            _render_compare_table(
                pool,
                player,
                compare_pool,
                compare_player
            )

         else:

            st.markdown(
                "### Performance Statistics"
            )

            cols = st.columns(2)

            for i, (col, label) in enumerate(STAT_CARDS):

                val = row.get(col, np.nan)

                display = (
                    f"{val:.2f}"
                    if pd.notna(val)
                    else "—"
                )

                cols[i % 2].metric(
                    label,
                    display
                )

            st.markdown(
                "### Advanced Metrics"
            )

            extra = _with_extra_stats(row)

            cols2 = st.columns(2)

            for i, (key, label) in enumerate(EXTRA_STAT_CARDS):

                val = extra.get(
                    key,
                    np.nan
                )

                display = (
                    f"{val:.1f}"
                    if pd.notna(val)
                    else "—"
                )

                cols2[i % 2].metric(
                    label,
                    display
                )

    st.divider()

    st.markdown(
        "## Performance Trend"
    )

    trend_metrics = [
        m
        for m in TREND_METRICS
        if metric_has_data(
            full_df,
            m
        )
    ]

    trend_df = player_trend(
        full_df,
        player,
        trend_metrics
    )

    if len(trend_df) >= 2:

        trend_df = trend_df.rename(
            columns={
                "Expected_Goals": "xG",
                "Expected_Assists": "xA"
            }
        )

        plot_metrics = [
            c
            for c in [
                "Goals",
                "Assists",
                "xG",
                "xA"
            ]
            if c in trend_df.columns
        ]

        fig = px.line(
            trend_df,
            x="season",
            y=plot_metrics,
            markers=True,
            labels={
                "value": "Total",
                "season": "Season",
                "variable": "Metric"
            }
        )

        fig.update_traces(
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=8)
        )

        colors = {
            "Goals": "#22c55e",
            "Assists": "#06b6d4",
            "xG": "#f59e0b",
            "xA": "#a855f7"
        }

        for trace in fig.data:

            if trace.name in colors:

                trace.line.color = colors[
                    trace.name
                ]

        fig.update_layout(

            height=520,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                size=16
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="center",
                x=0.5
            ),

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),

            xaxis_title="Season",

            yaxis_title="Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            f"{player} only has one season on record."
        )

    st.divider()

    st.markdown(
        "## Career Statistics"
    )

    log_cols = [
        "season",
        "league",
        "team",
        "Pos",
        "Age",
        "Matches_Played",
        "Minutes_Played",
        "Goals",
        "Assists",
    ]

    if metric_has_data(
        full_df,
        "Expected_Goals"
    ):

        log_cols += [
            "Expected_Goals",
            "Expected_Assists",
            "Shots",
            "Key_Passes",
            "Tackles"
        ]

    player_rows = (
        full_df[
            full_df["player"] == player
        ]
        .sort_values("season_id")
    )

    st.dataframe(
        player_rows[log_cols],
        use_container_width=True,
        hide_index=True
    )

    export_buttons(
        player_rows,
        f"{player.replace(' ', '_')}_stats",
        "ps"
    )        
    
            
def _render_header(player, league, season, row):
    
    st.markdown(
        f"""
        <div style="
            background:#111827;
            border:1px solid #1f2937;
            border-radius:14px;
            padding:24px;
            margin-bottom:20px;
        ">
            <div style="
                font-size:38px;
                font-weight:700;
                color:white;
            ">
                {player}
            </div>

            <div style="
                margin-top:8px;
                color:#9ca3af;
                font-size:15px;
            ">
                {row['team']} • {league} • {season}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Minutes",
        f"{int(row['Minutes_Played']):,}"
    )

    c2.metric(
        "Matches",
        int(row["Matches_Played"])
    )

    avg_min = (
        row["Minutes_Played"] /
        row["Matches_Played"]
        if row["Matches_Played"]
        else 0
    )

    c3.metric(
        "Avg Minutes",
        f"{avg_min:.0f}"
    )

    c4.metric(
        "90s",
        f"{row['Full_Match_Equivalents']:.1f}"
        if pd.notna(
            row["Full_Match_Equivalents"]
        )
        else "—"
    )

    c5.metric(
        "Goals",
        int(row["Goals"])
        if pd.notna(
            row.get("Goals")
        )
        else 0
    )

    pos = row.get(
        "Pos",
        "—"
    )

    nation = row.get(
        "Nation",
        "—"
    )

    born = row.get(
        "Born",
        "—"
    )

    st.caption(
        f"🌍 {nation} • 🎂 {int(born) if pd.notna(born) else '—'} • {pos}"
    )


def _render_compare_table(
    pool: pd.DataFrame,
    player: str,
    compare_pool: pd.DataFrame,
    compare_player: str
):

    st.markdown(
        "### Head-to-Head Comparison"
    )

    row_a = pool[
        pool["player"] == player
    ].iloc[0]

    row_b = compare_pool[
        compare_pool["player"] == compare_player
    ].iloc[0]

    data = {
        "Stat": [
            label
            for _, label
            in STAT_CARDS
        ],

        player: [
            row_a.get(
                col,
                np.nan
            )
            for col, _
            in STAT_CARDS
        ],

        compare_player: [
            row_b.get(
                col,
                np.nan
            )
            for col, _
            in STAT_CARDS
        ],
    }

    table = pd.DataFrame(
        data
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


def _build_radar(
    pool: pd.DataFrame,
    player: str,
    metrics: list,
    compare_pool: pd.DataFrame = None,
    compare_player: str = None
):

    def values_for(
        name,
        ref_pool
    ):

        vals = []

        for m in metrics:

            if not metric_has_data(
                ref_pool,
                m
            ):
                vals.append(0)
                continue

            pct_series = percentile_rank(
                per90(
                    ref_pool,
                    m
                )
            )

            idx = ref_pool.index[
                ref_pool["player"] == name
            ]

            this_pct = (
                pct_series.loc[idx].mean()
                if len(idx)
                else np.nan
            )

            vals.append(
                0
                if pd.isna(this_pct)
                else round(
                    this_pct,
                    1
                )
            )

        return vals

    labels = [
        m.replace(
            "_",
            " "
        )
        for m in metrics
    ]

    values = values_for(
        player,
        pool
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=player,
            line_color="#22c55e"
        )
    )
    if compare_player and compare_pool is not None:

        cmp_values = values_for(
            compare_player,
            compare_pool
        )

        fig.add_trace(
            go.Scatterpolar(
                r=cmp_values + [cmp_values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name=compare_player,
                line_color="#f59e0b",
                fillcolor="rgba(245,158,11,0.15)",
                opacity=0.80
            )
        )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        polar=dict(

            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#374151",
                linecolor="#374151",
                tickfont=dict(
                    color="#9ca3af"
                )
            ),

            angularaxis=dict(
                gridcolor="#374151",
                linecolor="#374151",
                tickfont=dict(
                    color="#e5e7eb",
                    size=12
                )
            )
        ),

        showlegend=bool(
            compare_player
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(
                size=13
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        height=500
    )

    return fig            
