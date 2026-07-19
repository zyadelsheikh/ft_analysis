import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data import (
    RADAR_DEFAULT_METRICS, per90, percentile_rank, metric_has_data, player_trend,
)
from pages_lib.filters import (
    season_league_filters, min_minutes_filter, team_filter,
    any_league_season_player_picker, export_buttons,
)

STAT_CARDS = [
    ("Goals", "Goals"), ("Assists", "Assists"),
    ("Expected_Goals", "xG"), ("Expected_Assists", "xA"),
    ("Shots", "Shots"), ("Shots_On_Target", "SoT"),
    ("Key_Passes", "Key Passes"), ("Tackles", "Tackles"),
    ("Interceptions", "Interceptions"), ("xg_diff", "Finishing Overperformance"),
]

EXTRA_STAT_CARDS = [
    ("pass_accuracy", "Pass Accuracy %"),
    ("shot_accuracy", "Shot Accuracy %"),
    ("goals_per90", "Goals / 90"),
    ("assists_per90", "Assists / 90"),
]

TREND_METRICS = ["Goals", "Assists", "Expected_Goals", "Expected_Assists"]


def _with_extra_stats(row: pd.Series) -> dict:
    extra = {}
    pass_att, pass_cmp = row.get("Pass_Attempts"), row.get("Pass_Completed")
    extra["pass_accuracy"] = (pass_cmp / pass_att * 100) if pass_cmp is not None and pd.notna(pass_att) and pass_att > 0 else np.nan
    shots, sot = row.get("Shots"), row.get("Shots_On_Target")
    extra["shot_accuracy"] = (sot / shots * 100) if sot is not None and pd.notna(shots) and shots > 0 else np.nan
    nineties = row.get("Full_Match_Equivalents")
    extra["goals_per90"] = (row.get("Goals", np.nan) / nineties) if nineties and pd.notna(nineties) and nineties > 0 else np.nan
    extra["assists_per90"] = (row.get("Assists", np.nan) / nineties) if nineties and pd.notna(nineties) and nineties > 0 else np.nan
    return extra


def _inject_styles():
    st.markdown("""
    <style>
    .ps-hero { background: linear-gradient(135deg,#172b2b 0%,#102020 55%,#0c1515 100%); border:1px solid #274444; border-radius:20px; padding:26px 28px 22px; margin:4px 0 22px; box-shadow:0 14px 36px rgba(0,0,0,.18); }
    .ps-kicker { color:#62e6b5; font-size:12px; font-weight:700; letter-spacing:1.6px; text-transform:uppercase; margin-bottom:7px; }
    .ps-name { color:#f8fafc; font-size:34px; font-weight:800; line-height:1.1; margin:0; }
    .ps-subtitle { color:#b3c6c3; font-size:14px; margin-top:8px; }
    .ps-meta { color:#d4e1df; font-size:13px; margin-top:16px; }
    .ps-kpi { background:rgba(255,255,255,.055); border:1px solid rgba(130,239,203,.18); border-radius:13px; padding:13px 14px; min-height:74px; }
    .ps-kpi-label { color:#9db6b1; font-size:11px; text-transform:uppercase; letter-spacing:.7px; }
    .ps-kpi-value { color:#f8fafc; font-size:23px; font-weight:750; margin-top:5px; }
    .ps-section { color:#e7f5f1; font-size:19px; font-weight:750; margin:12px 0 14px; }
    .ps-card { background:#122323; border:1px solid #274141; border-radius:14px; padding:14px 15px; margin-bottom:10px; }
    .ps-stat-label { color:#a7bfba; font-size:12px; }
    .ps-stat-value { color:#f4faf8; font-size:21px; font-weight:750; margin-top:4px; }
    .ps-compare-label { color:#dbeae6; font-size:13px; font-weight:650; }
    .ps-compare-values { color:#eefaf6; font-size:12px; display:flex; justify-content:space-between; margin-top:8px; }
    .ps-bar { height:6px; border-radius:99px; background:#29403e; margin-top:6px; overflow:hidden; }
    .ps-fill { height:100%; border-radius:99px; background:#44d7a7; }
    .ps-fill.alt { background:#fb923c; }
    .ps-table { border:1px solid #274141; border-radius:14px; overflow:hidden; }
    div[data-testid="stPlotlyChart"] { background:#122323; border:1px solid #274141; border-radius:16px; padding:8px; }
    </style>
    """, unsafe_allow_html=True)


def render(full_df: pd.DataFrame):
    _inject_styles()
    with st.sidebar:
        pool, league, season, _ = season_league_filters(full_df, "ps")
        pool = min_minutes_filter(pool, "ps")
        st.markdown("### Player Selection")
        pool, team = team_filter(pool, "ps")

        players = sorted(pool["player"].dropna().unique())
        if not players:
            st.warning("No players match these filters.")
            return
        player = st.selectbox("Select Player", players, key="ps_player")

        compare_on = st.toggle("Compare Player", value=False, key="ps_compare_toggle")
        compare_player, compare_pool = None, None
        if compare_on:
            st.caption("Compare against any player, from any league/season:")
            compare_player, compare_pool = any_league_season_player_picker(full_df, "ps_cmp")

    row = pool[pool["player"] == player]
    if row.empty:
        st.warning("No player data available for this competition / season.")
        return
    row = row.iloc[0]

    _render_header(player, league, season, row)

    advanced_available = metric_has_data(pool, "Expected_Goals")
    if not advanced_available:
        st.warning(f"Advanced stats are not available in the source data for {season}. Showing available basic stats below.")

    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<div class="ps-section">Player Scouting Report</div>', unsafe_allow_html=True)
        metrics = [m for m in RADAR_DEFAULT_METRICS if metric_has_data(pool, m)]
        if len(metrics) >= 3:
            fig = _build_radar(pool, player, metrics, compare_pool, compare_player)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            if compare_player:
                st.caption("Percentiles are calculated against each player's own league and season peer group.")
        else:
            st.info("Not enough metrics with data in this season to draw a radar chart.")

    with right:
        if compare_player and compare_pool is not None:
            _render_compare_table(pool, player, compare_pool, compare_player)
        else:
            _render_stat_cards("Key Player Stats", row, STAT_CARDS, columns=2)
            _render_stat_cards("Advanced Stats", row, EXTRA_STAT_CARDS, columns=2, extras=_with_extra_stats(row))

    st.markdown(f'<div class="ps-section">{player} — Performance Trend Across Seasons</div>', unsafe_allow_html=True)
    trend_metrics = [m for m in TREND_METRICS if metric_has_data(full_df, m)]
    trend_df = player_trend(full_df, player, trend_metrics)
    if len(trend_df) >= 2:
        trend_df = trend_df.rename(columns={"Expected_Goals": "xG", "Expected_Assists": "xA"})
        plot_metrics = [c for c in ["Goals", "Assists", "xG", "xA"] if c in trend_df.columns]
        fig = px.line(trend_df, x="season", y=plot_metrics, markers=True, labels={"value": "Total", "season": "Season", "variable": "Metric"})
