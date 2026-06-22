"""
pages/analytics.py  —  Page 3: Data Analytics Dashboard
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, top_batsmen, top_bowlers, venue_match_counts, team_batting_stats

# ── Plotly neon theme ──────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,21,48,0.6)",
    font=dict(family="Rajdhani, sans-serif", color="#e6f1ff"),
    title_font=dict(family="Orbitron, monospace", color="#00e5ff", size=14),
    xaxis=dict(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)"),
    yaxis=dict(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)"),
    margin=dict(l=20, r=20, t=50, b=20),
)

NEON_COLORS = [
    "#00e5ff", "#2979ff", "#7c4dff", "#00bcd4", "#448aff",
    "#40c4ff", "#b388ff", "#80d8ff", "#64b5f6", "#ce93d8"
]


def neon_bar(df, x, y, title, color="#00e5ff", horizontal=False):
    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation="h", color_discrete_sequence=[color])
    else:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=[color])
    fig.update_traces(
        marker_line_color="rgba(0,229,255,0.3)",
        marker_line_width=1,
    )
    fig.update_layout(title=title, **PLOTLY_LAYOUT)
    return fig


def show():
    df = load_data()

    st.markdown("""
    <div style="padding: 1.5rem 0 1rem 0;">
        <div class="neon-title" style="font-size:2rem;">📊 Analytics Dashboard</div>
        <div class="neon-subtitle" style="font-size:0.85rem; margin-top:0.4rem;">
            Explore IPL data with interactive charts
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏟️  Venues", "🏏  Batsmen", "🎳  Bowlers", "📈  Teams"
    ])

    # ── Tab 1: Venues ─────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">Matches by Venue</div>', unsafe_allow_html=True)

        vdf = venue_match_counts(df)
        top_n = st.slider("Show top N venues", 5, len(vdf), 15, key="venue_slider")
        vdf_top = vdf.head(top_n)

        fig_venue = neon_bar(vdf_top, "Venue", "Matches",
                             f"Top {top_n} Venues by Match Count", horizontal=True)
        st.plotly_chart(fig_venue, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Score distribution by venue
        st.markdown('<div class="section-header">Average Score by Venue</div>', unsafe_allow_html=True)
        venue_scores = df.groupby("venue")["runs"].mean().sort_values(ascending=False).head(15).reset_index()
        venue_scores.columns = ["Venue", "Avg Runs"]
        fig_vs = neon_bar(venue_scores, "Venue", "Avg Runs",
                          "Top 15 Venues by Average Runs per Ball", color="#2979ff", horizontal=True)
        st.plotly_chart(fig_vs, use_container_width=True)

    # ── Tab 2: Batsmen ────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">Top Run Scorers</div>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([3, 1])
        with col_f2:
            n_bat = st.number_input("Show top N", 5, 30, 10, key="bat_n")
        with col_f1:
            team_filter = st.selectbox("Filter by team", ["All Teams"] + sorted(df["bat_team"].unique()), key="bat_team_f")

        df_bat = df if team_filter == "All Teams" else df[df["bat_team"] == team_filter]
        bat_df = top_batsmen(df_bat, n=int(n_bat))

        fig_bat = neon_bar(bat_df, "Batsman", "Total Runs",
                           f"Top {n_bat} Batsmen — {team_filter}", horizontal=True)
        st.plotly_chart(fig_bat, use_container_width=True)

        st.markdown('<div class="section-header">Run Distribution</div>', unsafe_allow_html=True)
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df["striker"],
            nbinsx=40,
            marker_color="#00e5ff",
            marker_line_color="rgba(0,229,255,0.3)",
            marker_line_width=1,
            opacity=0.85,
            name="Striker Runs",
        ))
        fig_hist.update_layout(title="Distribution of Striker Runs per Ball", **PLOTLY_LAYOUT)
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Tab 3: Bowlers ────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">Top Wicket Takers</div>', unsafe_allow_html=True)

        col_bf1, col_bf2 = st.columns([3, 1])
        with col_bf2:
            n_bowl = st.number_input("Show top N", 5, 30, 10, key="bowl_n")
        with col_bf1:
            bowl_team_f = st.selectbox("Filter by team", ["All Teams"] + sorted(df["bowl_team"].unique()), key="bowl_team_f")

        df_bowl = df if bowl_team_f == "All Teams" else df[df["bowl_team"] == bowl_team_f]
        bowl_df = top_bowlers(df_bowl, n=int(n_bowl))

        fig_bowl = neon_bar(bowl_df, "Bowler", "Max Wickets",
                            f"Top {n_bowl} Bowlers — {bowl_team_f}", color="#7c4dff", horizontal=True)
        st.plotly_chart(fig_bowl, use_container_width=True)

        st.markdown('<div class="section-header">Wickets by Over</div>', unsafe_allow_html=True)
        wickets_by_over = df.groupby(df["overs"].astype(int))["wickets"].sum().reset_index()
        wickets_by_over.columns = ["Over", "Wickets"]
        fig_wo = go.Figure()
        fig_wo.add_trace(go.Bar(
            x=wickets_by_over["Over"],
            y=wickets_by_over["Wickets"],
            marker_color=NEON_COLORS[2],
            marker_line_color="rgba(124,77,255,0.4)",
            marker_line_width=1,
        ))
        fig_wo.update_layout(title="Wickets Fallen per Over (all matches)", **PLOTLY_LAYOUT)
        st.plotly_chart(fig_wo, use_container_width=True)

    # ── Tab 4: Teams ──────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">Team Batting Performance</div>', unsafe_allow_html=True)

        team_df = team_batting_stats(df)
        fig_team = go.Figure()
        fig_team.add_trace(go.Bar(
            name="Avg Runs",
            x=team_df["Team"],
            y=team_df["Avg_Runs"],
            marker_color="#00e5ff",
        ))
        fig_team.add_trace(go.Bar(
            name="Max Runs",
            x=team_df["Team"],
            y=team_df["Max_Runs"],
            marker_color="#2979ff",
            opacity=0.7,
        ))
        fig_team.update_layout(
            title="Team Batting Stats — Avg vs Max Runs",
            barmode="group",
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_team, use_container_width=True)

        st.markdown('<div class="section-header">Runs Over Overs (Avg Scoring Rate)</div>', unsafe_allow_html=True)
        scoring_rate = df.groupby(df["overs"].astype(int))["runs"].mean().reset_index()
        scoring_rate.columns = ["Over", "Avg Runs"]
        fig_sr = go.Figure()
        fig_sr.add_trace(go.Scatter(
            x=scoring_rate["Over"],
            y=scoring_rate["Avg Runs"],
            mode="lines+markers",
            line=dict(color="#00e5ff", width=2),
            marker=dict(color="#00e5ff", size=6,
                        line=dict(color="rgba(0,229,255,0.5)", width=2)),
            fill="tozeroy",
            fillcolor="rgba(0,229,255,0.05)",
        ))
        fig_sr.update_layout(title="Average Scoring Rate by Over", **PLOTLY_LAYOUT)
        st.plotly_chart(fig_sr, use_container_width=True)
