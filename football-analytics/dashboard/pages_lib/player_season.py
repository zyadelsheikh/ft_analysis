
def _render_compare_table(
    pool: pd.DataFrame,
    player: str,
    compare_pool: pd.DataFrame,
    compare_player: str
):

    st.markdown("### ⚔️ Head-to-Head Comparison")

    row_a = pool[
        pool["player"] == player
    ].iloc[0]

    row_b = compare_pool[
        compare_pool["player"] == compare_player
    ].iloc[0]


    left, right = st.columns(2)


    def player_card(container, name, row):

        with container:

            st.markdown(
                f"""
                <div class="player-card">

                <h3>👤 {name}</h3>

                <p>
                {row.get('team','—')}
                <br>
                {row.get('league','—')}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            stats = [
                ("Goals","Goals"),
                ("Assists","Assists"),
                ("xG","Expected_Goals"),
                ("xA","Expected_Assists"),
                ("Shots","Shots"),
                ("Tackles","Tackles"),
            ]


            cols = st.columns(2)

            for i,(title,col) in enumerate(stats):

                value = row.get(col,0)

                if pd.isna(value):
                    value="—"


                cols[i % 2].markdown(
                    f"""
                    <div class="stat-box">

                    <div class="stat-title">
                    {title}
                    </div>

                    <div class="stat-value">
                    {value}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    player_card(left, player, row_a)

    player_card(right, compare_player, row_b)
