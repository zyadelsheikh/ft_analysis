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
        colors = {"Goals": "#60a5fa", "Assists": "#fbbf24", "xG": "#fb7185", "xA": "#44d7a7"}
        fig.update_traces(mode="lines+markers", line=dict(width=2.2), marker=dict(size=7))
        fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=12, color="#c7d9d5"), hovermode="x unified", legend=dict(orientation="h", y=1.08, x=.5, xanchor="center"), margin=dict(l=20, r=20, t=32, b=20), xaxis_title="Season", yaxis_title="Performance")
        for trace in fig.data:
            if trace.name in colors:
                trace.line.color = colors[trace.name]
                trace.marker.color = colors[trace.name]
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info(f"{player} only has one season on record — nothing to trend yet.")

    st.markdown('<div class="ps-section">Season-by-Season Performance</div>', unsafe_allow_html=True)
    log_cols = ["season", "league", "team", "Pos", "Age", "Matches_Played", "Minutes_Played", "Goals", "Assists"]
    if metric_has_data(full_df, "Expected_Goals"):
        log_cols += ["Expected_Goals", "Expected_Assists", "Shots", "Key_Passes", "Tackles"]
    player_rows = full_df[full_df["player"] == player].sort_values("season_id")
    _render_season_table(player_rows, log_cols)
    export_buttons(player_rows, f"{player.replace(' ', '_')}_stats", "ps")


def _render_header(player, league, season, row):
    team = row.get("team", "—")
    pos = row.get("Pos", "—")
    nation = row.get("Nation", "—")
    born = row.get("Born", "—")
    born_display = int(born) if pd.notna(born) else "—"
    minutes = row.get("Minutes_Played", 0)
    matches = row.get("Matches_Played", 0)
    avg_min = minutes / matches if matches else 0
    nineties = row.get("Full_Match_Equivalents")
    nineties_display = f"{nineties:.1f}" if pd.notna(nineties) else "—"
    goals = int(row.get("Goals", 0)) if pd.notna(row.get("Goals")) else 0
    st.markdown(f'''<div class="ps-hero"><div class="ps-kicker">PLAYER PROFILE · {season}</div><div class="ps-name">{player}</div><div class="ps-subtitle">{team} · {league} · {season}</div><div class="ps-meta">{nation} · Born {born_display} · Position: {pos}</div><div style="height:18px"></div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px"><div class="ps-kpi"><div class="ps-kpi-label">Minutes</div><div class="ps-kpi-value">{int(minutes):,}</div></div><div class="ps-kpi"><div class="ps-kpi-label">Matches</div><div class="ps-kpi-value">{int(matches)}</div></div><div class="ps-kpi"><div class="ps-kpi-label">Avg Min</div><div class="ps-kpi-value">{avg_min:.0f}</div></div><div class="ps-kpi"><div class="ps-kpi-label">90s</div><div class="ps-kpi-value">{nineties_display}</div></div><div class="ps-kpi"><div class="ps-kpi-label">Goals</div><div class="ps-kpi-value">{goals}</div></div></div></div>''', unsafe_allow_html=True)


def _format_value(value, decimals=2):
    if pd.isna(value):
        return "—"
    return f"{value:.{decimals}f}" if isinstance(value, (float, np.floating)) else f"{value:,}" if isinstance(value, (int, np.integer)) else str(value)


def _render_stat_cards(title, row, cards, columns=2, extras=None):
    st.markdown(f'<div class="ps-section">{title}</div>', unsafe_allow_html=True)
    cols = st.columns(columns)
    for i, (key, label) in enumerate(cards):
        value = extras.get(key, np.nan) if extras is not None else row.get(key, np.nan)
        decimals = 1 if extras is not None else 2
        with cols[i % columns]:
            st.markdown(f'<div class="ps-card"><div class="ps-stat-label">{label}</div><div class="ps-stat-value">{_format_value(value, decimals)}</div></div>', unsafe_allow_html=True)


def _render_compare_table(pool, player, compare_pool, compare_player):
    st.markdown('<div class="ps-section">Head-to-Head</div>', unsafe_allow_html=True)
    row_a = pool[pool["player"] == player].iloc[0]
    row_b = compare_pool[compare_pool["player"] == compare_player].iloc[0]
    for key, label in STAT_CARDS:
        value_a, value_b = row_a.get(key, np.nan), row_b.get(key, np.nan)
        numeric = [v for v in (value_a, value_b) if pd.notna(v) and isinstance(v, (int, float, np.integer, np.floating))]
        max_value = max(numeric) if numeric else 0
        width_a = max(0, min(100, value_a / max_value * 100)) if max_value and pd.notna(value_a) else 0
        width_b = max(0, min(100, value_b / max_value * 100)) if max_value and pd.notna(value_b) else 0
        st.markdown(f'<div class="ps-card"><div class="ps-compare-label">{label}</div><div class="ps-compare-values"><span>{player}: {_format_value(value_a)}</span><span>{compare_player}: {_format_value(value_b)}</span></div><div class="ps-bar"><div class="ps-fill" style="width:{width_a:.1f}%"></div></div><div class="ps-bar"><div class="ps-fill alt" style="width:{width_b:.1f}%"></div></div></div>', unsafe_allow_html=True)


def _render_season_table(player_rows, log_cols):
    display = player_rows[log_cols].copy()
    display.columns = [str(col).replace("_", " ") for col in display.columns]
    st.markdown('<div class="ps-table">', unsafe_allow_html=True)
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


def _build_radar(pool, player, metrics, compare_pool=None, compare_player=None):
    def values_for(name, ref_pool):
        vals = []
        for metric in metrics:
            if not metric_has_data(ref_pool, metric):
                vals.append(0)
                continue
            pct_series = percentile_rank(per90(ref_pool, metric))
            idx = ref_pool.index[ref_pool["player"] == name]
            this_pct = pct_series.loc[idx].mean() if len(idx) else np.nan
            vals.append(0 if pd.isna(this_pct) else round(this_pct, 1))
        return vals

    labels = [metric.replace("_", " ") for metric in metrics]
    fig = go.Figure()
    values = values_for(player, pool)
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=labels + [labels[0]], fill="toself", name=player, line=dict(color="#44d7a7", width=2), fillcolor="rgba(68,215,167,.22)"))
    if compare_player and compare_pool is not None:
        cmp_values = values_for(compare_player, compare_pool)
        fig.add_trace(go.Scatterpolar(r=cmp_values + [cmp_values[0]], theta=labels + [labels[0]], fill="toself", name=compare_player, line=dict(color="#fb923c", width=2), fillcolor="rgba(251,146,60,.16)"))
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100], gridcolor="#35504c", linecolor="#35504c", tickfont=dict(color="#9db6b1")), angularaxis=dict(gridcolor="#35504c", linecolor="#35504c", tickfont=dict(color="#c7d9d5"))), paper_bgcolor="rgba(0,0,0,0)", showlegend=bool(compare_player), legend=dict(orientation="h", y=-.12, x=.5, xanchor="center"), margin=dict(l=42, r=42, t=18, b=36), height=430, hoverlabel=dict(bgcolor="#142626"))
    return fig
