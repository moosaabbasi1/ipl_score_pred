"""
pages/predictor.py  —  Page 2: Live Score Predictor
"""
import streamlit as st
from utils import load_data, get_unique_values, predict_score


def show():
    df   = load_data()
    uniq = get_unique_values(df)

    st.markdown("""
    <div style="padding: 1.5rem 0 1rem 0;">
        <div class="neon-title" style="font-size:2rem;">🎯 Score Predictor</div>
        <div class="neon-subtitle" style="font-size:0.85rem; margin-top:0.4rem;">
            Enter live match conditions · Get AI-predicted final total
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Form ──────────────────────────────────────────────────────────────
    with st.form("prediction_form"):

        st.markdown('<div class="section-header">Match Setup</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            venue = st.selectbox("🏟️ Venue", uniq["venues"], index=0)
        with col2:
            bat_team = st.selectbox("🏏 Batting Team", uniq["teams"], index=0)
        with col3:
            bowl_team_options = [t for t in uniq["teams"] if t != bat_team]
            bowl_team = st.selectbox("🎳 Bowling Team", bowl_team_options, index=0)

        st.markdown('<div class="section-header">Players</div>', unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        with col4:
            batsman = st.selectbox("🏏 Current Batsman (Striker)", uniq["batsmen"], index=0)
        with col5:
            bowler = st.selectbox("🎳 Current Bowler", uniq["bowlers"], index=0)

        st.markdown('<div class="section-header">Current Match State</div>', unsafe_allow_html=True)
        col6, col7, col8, col9 = st.columns(4)
        with col6:
            runs = st.number_input("🏃 Runs Scored", min_value=0, max_value=300, value=80, step=1)
        with col7:
            wickets = st.number_input("💀 Wickets Fallen", min_value=0, max_value=9, value=2, step=1)
        with col8:
            overs = st.number_input("⏱️ Overs Bowled", min_value=0.0, max_value=19.5, value=10.0, step=0.1, format="%.1f")
        with col9:
            striker_runs = st.number_input("🏏 Striker's Runs", min_value=0, max_value=200, value=30, step=1,
                                           help="Individual runs scored by the current striker batsman")

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn = st.columns([1, 2, 1])
        with col_btn[1]:
            submitted = st.form_submit_button("⚡ PREDICT FINAL SCORE", use_container_width=True)

    # ── Result ────────────────────────────────────────────────────────────
    if submitted:
        if bat_team == bowl_team:
            st.markdown('<div class="warning-badge">⚠️ Batting and bowling teams must be different!</div>',
                        unsafe_allow_html=True)
            return

        with st.spinner("Running neural network inference..."):
            result = predict_score(
                bat_team=bat_team,
                bowl_team=bowl_team,
                venue=venue,
                batsman=batsman,
                bowler=bowler,
                runs=runs,
                wickets=wickets,
                overs=overs,
                striker_runs=striker_runs,
            )

        if result:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown('<div class="section-header">Prediction Result</div>', unsafe_allow_html=True)

            # Main score display
            remaining_runs = max(0, result["predicted"] - runs)
            remaining_overs = round(max(0, 20 - overs), 1)
            crr = round(runs / overs, 2) if overs > 0 else 0
            rrr = round(remaining_runs / remaining_overs, 2) if remaining_overs > 0 else 0

            st.markdown(f"""
            <div class="score-result">
                <div style="font-family:'Rajdhani',sans-serif; color:#6b8aad; font-size:0.85rem;
                            letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.5rem;">
                    Predicted Final Score
                </div>
                <div class="score-number">{result['predicted']}</div>
                <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; font-size:1rem; margin-top:0.5rem;">
                    Range: {result['low']} – {result['high']} runs
                </div>
                <div style="margin-top:1rem; display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
                    <span class="badge">±15 run accuracy</span>
                    <span class="badge">MAE: 14.5 runs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Secondary metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("🏃 Runs Still Needed", f"{remaining_runs}")
            with col_m2:
                st.metric("⏱️ Overs Remaining", f"{remaining_overs}")
            with col_m3:
                st.metric("📈 Current Run Rate", f"{crr:.2f}")
            with col_m4:
                st.metric("⚡ Req. Run Rate", f"{rrr:.2f}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Match summary card
            st.markdown(f"""
            <div class="neon-card">
                <div class="neon-card-title">Match Summary</div>
                <div class="stat-row">
                    <span class="stat-label">Venue</span>
                    <span class="stat-value">{venue}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Batting</span>
                    <span class="stat-value">{bat_team}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Bowling</span>
                    <span class="stat-value">{bowl_team}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Current Score</span>
                    <span class="stat-value">{runs}/{wickets} in {overs} overs</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Striker ({batsman})</span>
                    <span class="stat-value">{striker_runs} runs</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Bowler</span>
                    <span class="stat-value">{bowler}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="warning-badge">
                ⚠️ Model not loaded. Make sure <code>ipl_score_model.keras</code> is in the <code>model/</code> folder
                and TensorFlow is installed (<code>pip install tensorflow</code>).
            </div>
            """, unsafe_allow_html=True)

    else:
        # Placeholder hint
        st.markdown("""
        <div style="text-align:center; padding:3rem 0; opacity:0.4;">
            <div style="font-size:3rem;">🏏</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; letter-spacing:0.1em;
                        text-transform:uppercase; color:#4a6fa5; margin-top:0.5rem;">
                Fill in the form above and hit Predict
            </div>
        </div>
        """, unsafe_allow_html=True)
