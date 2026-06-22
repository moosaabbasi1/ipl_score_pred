"""
pages/home.py  —  Page 1: Home / Landing
"""
import streamlit as st
from utils import load_data, get_summary_stats


def show():
    df   = load_data()
    stats = get_summary_stats(df)

    # ── Hero ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 2rem 0;">
        <div style="font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:0.3em;
                    color:#4a6fa5; text-transform:uppercase; margin-bottom:1rem;">
            ◈ IPL Intelligence Platform ◈
        </div>
        <div class="neon-title" style="font-size:clamp(2rem,6vw,3.8rem); margin-bottom:1rem;">
            IPL Score<br>Predictor
        </div>
        <div class="neon-subtitle" style="margin-bottom:2rem;">
            AI-powered cricket intelligence · Deep learning · Real-time analysis
        </div>
        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
            <span class="badge">🏏 Neural Network</span>
            <span class="badge">📊 Data Driven</span>
            <span class="badge">⚡ Live Inference</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Quick Stats ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Tournament Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🏆 Total Matches", f"{stats['total_matches']:,}")
    with c2:
        st.metric("🏏 Teams", stats["total_teams"])
    with c3:
        st.metric("🏟️ Venues", stats["total_venues"])
    with c4:
        st.metric("👤 Players", stats["total_batsmen"])

    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7 = st.columns(3)
    with c5:
        st.metric("🎳 Bowlers", stats["total_bowlers"])
    with c6:
        st.metric("💥 Max Score Seen", f"{stats['max_score']} runs")
    with c7:
        st.metric("📈 Avg Final Score", f"~{stats['avg_score']}")

    st.markdown("---")

    # ── Feature Cards ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">What You Can Do</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="neon-card">
            <div style="font-size:2rem; margin-bottom:0.8rem;">🎯</div>
            <div class="neon-card-title">Score Predictor</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; font-size:0.95rem; line-height:1.5;">
                Input live match conditions — venue, teams, current score, overs — and get an AI-predicted final total in seconds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="neon-card">
            <div style="font-size:2rem; margin-bottom:0.8rem;">📊</div>
            <div class="neon-card-title">Analytics Dashboard</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; font-size:0.95rem; line-height:1.5;">
                Explore match data with interactive Plotly charts — venue comparisons, top players, team performance trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="neon-card">
            <div style="font-size:2rem; margin-bottom:0.8rem;">⚔️</div>
            <div class="neon-card-title">Head-to-Head</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; font-size:0.95rem; line-height:1.5;">
                Pit any two IPL teams against each other. Explore historical battles, win rates, and venue dominance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How It Works ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">How The Model Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="neon-card">
        <div style="display:flex; gap:2rem; flex-wrap:wrap; align-items:center;">
            <div style="flex:1; min-width:200px;">
                <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; line-height:1.8; font-size:1rem;">
                    The prediction engine uses a <span style="color:#00e5ff; font-weight:600;">Deep Neural Network</span>
                    trained on historical IPL ball-by-ball data from 2008–2017.<br><br>
                    It encodes team names, venues, and player identities as learned embeddings,
                    then combines them with live match state (runs, wickets, overs) to project the final score.
                    <br><br>
                    Mean Absolute Error on test data: <span style="color:#00e5ff; font-weight:700;">~14.5 runs</span>
                </div>
            </div>
            <div style="flex:1; min-width:200px; text-align:center;">
                <div style="font-family:'Orbitron',monospace; font-size:0.75rem; color:#4a6fa5; line-height:2.5; letter-spacing:0.05em;">
                    VENUE + TEAMS + PLAYERS<br>
                    ↓<br>
                    LABEL ENCODING<br>
                    ↓<br>
                    MINMAX SCALING<br>
                    ↓<br>
                    NEURAL NETWORK (9→...→1)<br>
                    ↓<br>
                    <span style="color:#00e5ff;">PREDICTED TOTAL</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0;">
        <div style="font-family:'Rajdhani',sans-serif; color:#6b8aad; font-size:1rem; letter-spacing:0.1em; text-transform:uppercase;">
            → Select a page from the sidebar to get started ←
        </div>
    </div>
    """, unsafe_allow_html=True)
