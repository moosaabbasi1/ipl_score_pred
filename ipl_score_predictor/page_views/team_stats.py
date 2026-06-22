"""
pages/team_stats.py  —  Page 4: Team & Player Explorer + Head-to-Head
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, get_unique_values, head_to_head

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,21,48,0.6)",
    font=dict(family="Rajdhani, sans-serif", color="#e6f1ff"),
    title_font=dict(family="Orbitron, monospace", color="#00e5ff", size=14),
    xaxis=dict(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)"),
    yaxis=dict(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)"),
    margin=dict(l=20, r=20, t=50, b=20),
)


def show():
    df   = load_data()
    uniq = get_unique_values(df)
    teams = uniq["teams"]

    st.markdown("""
    <div style="padding: 1.5rem 0 1rem 0;">
        <div class="neon-title" style="font-size:2rem;">⚔️ Team & Player Explorer</div>
        <div class="neon-subtitle" style="font-size:0.85rem; margin-top:0.4rem;">
            Compare teams, explore player stats, head-to-head records
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["⚔️  Head-to-Head", "🏏  Team Deep Dive", "👤  Player Lookup"])

    # ── Tab 1: Head to Head ───────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">Head-to-Head Battle</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            team_a = st.selectbox("🏏 Team A", teams, index=0, key="h2h_a")
        with col2:
            team_b_options = [t for t in teams if t != team_a]
            team_b = st.selectbox("🏏 Team B", team_b_options, index=0, key="h2h_b")

        h2h_df = head_to_head(df, team_a, team_b)

        if h2h_df.empty:
            st.markdown(f"""
            <div class="warning-badge">
                No data found for {team_a} vs {team_b}. Try a different combination.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Summary metrics
            a_batting = h2h_df[h2h_df["bat_team"] == team_a]
            b_batting = h2h_df[h2h_df["bat_team"] == team_b]

            a_avg = round(a_batting["runs"].mean(), 1) if not a_batting.empty else 0
            b_avg = round(b_batting["runs"].mean(), 1) if not b_batting.empty else 0
            a_max = int(a_batting["runs"].max()) if not a_batting.empty else 0
            b_max = int(b_batting["runs"].max()) if not b_batting.empty else 0

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric(f"📈 {team_a} Avg Runs", a_avg)
            with col_m2:
                st.metric(f"📈 {team_b} Avg Runs", b_avg)
            with col_m3:
                st.metric(f"💥 {team_a} Max", a_max)
            with col_m4:
                st.metric(f"💥 {team_b} Max", b_max)

            st.markdown("<br>", unsafe_allow_html=True)

            # Runs comparison
            st.markdown('<div class="section-header">Runs Scored Comparison</div>', unsafe_allow_html=True)
            fig_h2h = go.Figure()
            if not a_batting.empty:
                fig_h2h.add_trace(go.Box(
                    y=a_batting["runs"],
                    name=team_a,
                    marker_color="#00e5ff",
                    line_color="#00e5ff",
                ))
            if not b_batting.empty:
                fig_h2h.add_trace(go.Box(
                    y=b_batting["runs"],
                    name=team_b,
                    marker_color="#7c4dff",
                    line_color="#7c4dff",
                ))
            fig_h2h.update_layout(title=f"{team_a} vs {team_b} — Run Distributions", **PLOTLY_LAYOUT)
            st.plotly_chart(fig_h2h, use_container_width=True)

            # Venue breakdown
            if not h2h_df.empty:
                st.markdown('<div class="section-header">Venues Played</div>', unsafe_allow_html=True)
                venue_counts = h2h_df["venue"].value_counts().reset_index()
                venue_counts.columns = ["Venue", "Rows"]
                fig_v = px.bar(venue_counts.head(10), x="Venue", y="Rows",
                               color_discrete_sequence=["#2979ff"])
                fig_v.update_layout(title="Matches Breakdown by Venue", **PLOTLY_LAYOUT)
                st.plotly_chart(fig_v, use_container_width=True)

    # ── Tab 2: Team Deep Dive ─────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">Team Deep Dive</div>', unsafe_allow_html=True)
        sel_team = st.selectbox("Select Team", teams, key="team_dive")

        team_df = df[df["bat_team"] == sel_team]

        if team_df.empty:
            st.warning("No batting data for this team.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏃 Total Runs (all balls)", f"{int(team_df['runs'].sum()):,}")
            with col2:
                st.metric("💀 Total Wickets Lost", f"{int(team_df['wickets'].sum()):,}")
            with col3:
                st.metric("📊 Avg Runs / Ball", f"{team_df['runs'].mean():.2f}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Runs over overs
            st.markdown('<div class="section-header">Scoring Rate by Over</div>', unsafe_allow_html=True)
            over_runs = team_df.groupby(team_df["overs"].astype(int))["runs"].mean().reset_index()
            over_runs.columns = ["Over", "Avg Runs"]
            fig_or = go.Figure()
            fig_or.add_trace(go.Scatter(
                x=over_runs["Over"], y=over_runs["Avg Runs"],
                mode="lines+markers",
                line=dict(color="#00e5ff", width=2),
                marker=dict(size=6, color="#00e5ff"),
                fill="tozeroy",
                fillcolor="rgba(0,229,255,0.06)",
                name=sel_team,
            ))
            fig_or.update_layout(title=f"{sel_team} — Avg Runs per Over", **PLOTLY_LAYOUT)
            st.plotly_chart(fig_or, use_container_width=True)

            # Top batsmen for team
            st.markdown('<div class="section-header">Top Batsmen</div>', unsafe_allow_html=True)
            team_bat = team_df.groupby("batsman")["striker"].sum().sort_values(ascending=False).head(10).reset_index()
            team_bat.columns = ["Batsman", "Total Runs"]
            fig_tb = px.bar(team_bat, x="Total Runs", y="Batsman", orientation="h",
                            color_discrete_sequence=["#2979ff"])
            fig_tb.update_layout(title=f"Top 10 Batsmen for {sel_team}", **PLOTLY_LAYOUT)
            st.plotly_chart(fig_tb, use_container_width=True)

            # Opponents faced most
            st.markdown('<div class="section-header">Most Faced Opponents</div>', unsafe_allow_html=True)
            opp_counts = team_df["bowl_team"].value_counts().head(8).reset_index()
            opp_counts.columns = ["Opponent", "Balls Faced"]
            fig_opp = px.pie(
                opp_counts, names="Opponent", values="Balls Faced",
                color_discrete_sequence=["#00e5ff","#2979ff","#7c4dff","#00bcd4","#448aff",
                                          "#40c4ff","#80d8ff","#64b5f6"],
                hole=0.4,
            )
            fig_opp.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e6f1ff"))
            st.plotly_chart(fig_opp, use_container_width=True)

    # ── Tab 3: Player Lookup ──────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">Player Lookup</div>', unsafe_allow_html=True)
        player_type = st.radio("View as", ["Batsman", "Bowler"], horizontal=True, key="player_type")

        if player_type == "Batsman":
            sel_player = st.selectbox("Select Batsman", uniq["batsmen"], key="sel_bat")
            p_df = df[df["batsman"] == sel_player]

            if p_df.empty:
                st.warning("No data found.")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🏃 Career Runs", f"{int(p_df['striker'].sum()):,}")
                with col2:
                    st.metric("🏟️ Venues Played", p_df["venue"].nunique())
                with col3:
                    st.metric("🏏 Teams Played For", p_df["bat_team"].nunique())

                st.markdown('<div class="section-header">Runs per Venue</div>', unsafe_allow_html=True)
                venue_runs = p_df.groupby("venue")["striker"].sum().sort_values(ascending=False).head(10).reset_index()
                venue_runs.columns = ["Venue", "Runs"]
                fig_vr = px.bar(venue_runs, x="Runs", y="Venue", orientation="h",
                                color_discrete_sequence=["#00e5ff"])
                fig_vr.update_layout(title=f"{sel_player} — Runs by Venue", **PLOTLY_LAYOUT)
                st.plotly_chart(fig_vr, use_container_width=True)

        else:
            sel_bowler = st.selectbox("Select Bowler", uniq["bowlers"], key="sel_bowl")
            b_df = df[df["bowler"] == sel_bowler]

            if b_df.empty:
                st.warning("No data found.")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💀 Max Wickets (single match)", int(b_df["wickets"].max()))
                with col2:
                    st.metric("🏟️ Venues Bowled At", b_df["venue"].nunique())
                with col3:
                    st.metric("🏏 Teams Bowled Against", b_df["bat_team"].nunique())

                st.markdown('<div class="section-header">Wickets by Venue</div>', unsafe_allow_html=True)
                v_wk = b_df.groupby("venue")["wickets"].max().sort_values(ascending=False).head(10).reset_index()
                v_wk.columns = ["Venue", "Max Wickets"]
                fig_vw = px.bar(v_wk, x="Max Wickets", y="Venue", orientation="h",
                                color_discrete_sequence=["#7c4dff"])
                fig_vw.update_layout(title=f"{sel_bowler} — Wickets by Venue", **PLOTLY_LAYOUT)
                st.plotly_chart(fig_vw, use_container_width=True)
