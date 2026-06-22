"""
utils.py - Core utilities: data loading, preprocessing, model inference
"""
import os
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "ipl_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "ipl_score_model.keras")

# Categorical columns (same order as notebook)
CAT_COLS = ['bat_team', 'bowl_team', 'venue', 'batsman', 'bowler']
FEATURE_COLS = ['bat_team', 'bowl_team', 'venue', 'runs', 'wickets', 'overs', 'striker', 'batsman', 'bowler']

# ── CSS loader ─────────────────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(BASE_DIR, "assets", "theme.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


@st.cache_data(show_spinner=False)
def get_unique_values(df: pd.DataFrame) -> dict:
    """Return sorted unique values for all dropdown columns."""
    return {
        "venues":   sorted(df["venue"].unique().tolist()),
        "teams":    sorted(df["bat_team"].unique().tolist()),
        "batsmen":  sorted(df["batsman"].unique().tolist()),
        "bowlers":  sorted(df["bowler"].unique().tolist()),
    }


@st.cache_data(show_spinner=False)
def get_summary_stats(df: pd.DataFrame) -> dict:
    return {
        "total_matches": df["match_id"].nunique() if "match_id" in df.columns else len(df) // 100,
        "total_teams":   df["bat_team"].nunique(),
        "total_venues":  df["venue"].nunique(),
        "total_batsmen": df["batsman"].nunique(),
        "total_bowlers": df["bowler"].nunique(),
        "max_score":     int(df["runs"].max()),
        "avg_score":     round(df.groupby(["bat_team", "venue"])["runs"].max().mean(), 1) if "runs" in df.columns else 0,
    }


# ── Preprocessing ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_encoders_and_scaler():
    """
    Replicates the notebook's preprocessing exactly:
      1. LabelEncode each cat_col on the full dataset
      2. Build feature matrix X
      3. train_test_split (random_state=42, test_size=0.3)
      4. Fit MinMaxScaler on X_train only
    Returns (label_encoders dict, scaler)
    """
    df = pd.read_csv(DATA_PATH)

    label_encoders = {}
    df_enc = df.copy()
    for col in CAT_COLS:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df_enc[col])
        label_encoders[col] = le

    X = df_enc[FEATURE_COLS].values
    y = df_enc["total"].values if "total" in df_enc.columns else np.zeros(len(df_enc))

    X_train, _, _, _ = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = MinMaxScaler()
    scaler.fit(X_train)

    return label_encoders, scaler


# ── Model ──────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"❌ Could not load model: {e}")
        return None


# ── Prediction ─────────────────────────────────────────────────────────────
def predict_score(
    bat_team: str,
    bowl_team: str,
    venue: str,
    batsman: str,
    bowler: str,
    runs: int,
    wickets: int,
    overs: float,
    striker_runs: int,
) -> dict | None:
    """
    Encode inputs, scale, predict. Returns dict with predicted total and range.
    Feature order: bat_team, bowl_team, venue, runs, wickets, overs, striker, batsman, bowler
    """
    model = load_model()
    if model is None:
        return None

    label_encoders, scaler = build_encoders_and_scaler()

    try:
        enc_bat   = label_encoders["bat_team"].transform([bat_team])[0]
        enc_bowl  = label_encoders["bowl_team"].transform([bowl_team])[0]
        enc_venue = label_encoders["venue"].transform([venue])[0]
        enc_bat_p = label_encoders["batsman"].transform([batsman])[0]
        enc_bowler= label_encoders["bowler"].transform([bowler])[0]
    except ValueError as e:
        st.error(f"Encoding error (unseen label): {e}")
        return None

    features = np.array([[
        enc_bat, enc_bowl, enc_venue,
        runs, wickets, overs,
        striker_runs,
        enc_bat_p, enc_bowler
    ]], dtype=np.float32)

    features_scaled = scaler.transform(features)
    prediction = float(model.predict(features_scaled, verbose=0)[0][0])
    prediction = max(runs, round(prediction))   # can't predict less than current

    return {
        "predicted": prediction,
        "low":  max(runs, prediction - 15),
        "high": prediction + 15,
    }


# ── Analytics helpers ──────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def top_batsmen(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("batsman")["striker"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
        .rename(columns={"batsman": "Batsman", "striker": "Total Runs"})
    )


@st.cache_data(show_spinner=False)
def top_bowlers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("bowler")["wickets"]
        .max()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
        .rename(columns={"bowler": "Bowler", "wickets": "Max Wickets"})
    )


@st.cache_data(show_spinner=False)
def venue_match_counts(df: pd.DataFrame) -> pd.DataFrame:
    col = "match_id" if "match_id" in df.columns else df.columns[0]
    return (
        df.groupby("venue")[col]
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"venue": "Venue", col: "Matches"})
    )


@st.cache_data(show_spinner=False)
def team_batting_stats(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("bat_team")
        .agg(
            Avg_Runs=("runs", "mean"),
            Max_Runs=("runs", "max"),
            Matches=("bat_team", "count"),
        )
        .round(1)
        .sort_values("Avg_Runs", ascending=False)
        .reset_index()
        .rename(columns={"bat_team": "Team"})
    )


@st.cache_data(show_spinner=False)
def head_to_head(df: pd.DataFrame, team_a: str, team_b: str) -> pd.DataFrame:
    mask = (
        ((df["bat_team"] == team_a) & (df["bowl_team"] == team_b)) |
        ((df["bat_team"] == team_b) & (df["bowl_team"] == team_a))
    )
    return df[mask].copy()