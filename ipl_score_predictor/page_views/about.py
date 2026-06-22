"""
pages/about.py  —  Page 5: About & Model Info
"""
import streamlit as st


def show():
    st.markdown("""
    <div style="padding: 1.5rem 0 1rem 0;">
        <div class="neon-title" style="font-size:2rem;">ℹ️ About & Model Info</div>
        <div class="neon-subtitle" style="font-size:0.85rem; margin-top:0.4rem;">
            Architecture · Training · How it works
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Project Overview ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">Project Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="neon-card">
        <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; line-height:1.9; font-size:1rem;">
            This app predicts the <span style="color:#00e5ff; font-weight:600;">final score</span>
            of an IPL first innings using a deep neural network trained on ball-by-ball match data
            from <span style="color:#00e5ff;">2008 – 2017</span>.
            <br><br>
            Given the current match state — batting team, bowling team, venue, striker, bowler,
            runs scored, wickets fallen, and overs completed — the model projects what the
            batting team will finish on.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Dataset ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Dataset</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="neon-card">
            <div class="neon-card-title">Data Source</div>
            <div class="stat-row">
                <span class="stat-label">File</span>
                <span class="stat-value">ipl_data.csv</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Years</span>
                <span class="stat-value">2008 – 2017</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Matches</span>
                <span class="stat-value">~617</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Teams</span>
                <span class="stat-value">14</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Venues</span>
                <span class="stat-value">35</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Batsmen</span>
                <span class="stat-value">411</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Bowlers</span>
                <span class="stat-value">329</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="neon-card">
            <div class="neon-card-title">Features Used</div>
            <div class="stat-row">
                <span class="stat-label">bat_team</span>
                <span class="stat-value">Batting team (encoded)</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">bowl_team</span>
                <span class="stat-value">Bowling team (encoded)</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">venue</span>
                <span class="stat-value">Match venue (encoded)</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">runs</span>
                <span class="stat-value">Runs scored so far</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">wickets</span>
                <span class="stat-value">Wickets fallen</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">overs</span>
                <span class="stat-value">Overs completed</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">striker</span>
                <span class="stat-value">Striker's current runs</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">batsman</span>
                <span class="stat-value">Striker identity (encoded)</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">bowler</span>
                <span class="stat-value">Bowler identity (encoded)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Model Architecture ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Model Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="neon-card">
        <div style="display:flex; gap:2rem; flex-wrap:wrap;">
            <div style="flex:1; min-width:200px;">
                <div class="neon-card-title" style="margin-bottom:1rem;">Neural Network</div>
                <div class="stat-row">
                    <span class="stat-label">Type</span>
                    <span class="stat-value">Dense (Fully Connected)</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Input Shape</span>
                    <span class="stat-value">(None, 9)</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Output</span>
                    <span class="stat-value">1 neuron (predicted score)</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Activation</span>
                    <span class="stat-value">ReLU (hidden), Linear (output)</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Loss</span>
                    <span class="stat-value">Huber Loss</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Optimizer</span>
                    <span class="stat-value">Adam</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Format</span>
                    <span class="stat-value">ipl_score_model.keras</span>
                </div>
            </div>
            <div style="flex:1; min-width:200px; padding-left:1rem; border-left:1px solid rgba(0,229,255,0.15);">
                <div class="neon-card-title" style="margin-bottom:1rem;">Preprocessing Pipeline</div>
                <div class="stat-row">
                    <span class="stat-label">Categorical</span>
                    <span class="stat-value">LabelEncoder (per column)</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Numeric</span>
                    <span class="stat-value">MinMaxScaler</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Train Split</span>
                    <span class="stat-value">70% train / 30% test</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Random State</span>
                    <span class="stat-value">42</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Scaler Fit On</span>
                    <span class="stat-value">X_train only</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Performance ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Model Performance</div>', unsafe_allow_html=True)
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("📉 Mean Absolute Error", "~14.5 runs")
    with col_p2:
        st.metric("🎯 Typical Range", "±15 runs")
    with col_p3:
        st.metric("📊 Test Size", "30% of dataset")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="neon-card">
        <div class="neon-card-title">Interpretation</div>
        <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; line-height:1.9; font-size:1rem;">
            A MAE of ~14.5 runs means the model is typically within <span style="color:#00e5ff;">14–15 runs</span>
            of the actual final score. For example, if the real total was 165, the model
            would predict somewhere between 150–180 in most cases.
            <br><br>
            Predictions are most reliable when at least <span style="color:#00e5ff;">6–10 overs</span>
            have been bowled, giving the model enough match-state context to project forward.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Setup Guide ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Setup Guide</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="neon-card">
        <div class="neon-card-title" style="margin-bottom:1rem;">How to Run This App</div>
        <div style="font-family:'Rajdhani',sans-serif; color:#8ab4d4; font-size:1rem; line-height:2;">
            <span style="color:#00e5ff; font-weight:700;">1.</span> Place <code style="color:#00e5ff;">ipl_data.csv</code> in the <code style="color:#00e5ff;">data/</code> folder<br>
            <span style="color:#00e5ff; font-weight:700;">2.</span> Place <code style="color:#00e5ff;">ipl_score_model.keras</code> in the <code style="color:#00e5ff;">model/</code> folder<br>
            <span style="color:#00e5ff; font-weight:700;">3.</span> Install dependencies: <code style="color:#00e5ff;">pip install -r requirements.txt</code><br>
            <span style="color:#00e5ff; font-weight:700;">4.</span> Launch: <code style="color:#00e5ff;">streamlit run app.py</code><br>
            <span style="color:#00e5ff; font-weight:700;">5.</span> Open <code style="color:#00e5ff;">http://localhost:8501</code> in your browser
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:2rem 0; opacity:0.4;">
        <div style="font-family:'Orbitron',monospace; font-size:0.7rem; letter-spacing:0.2em;
                    color:#4a6fa5; text-transform:uppercase;">
            IPL Score Predictor · Built with Streamlit & TensorFlow · Data: 2008–2017
        </div>
    </div>
    """, unsafe_allow_html=True)
