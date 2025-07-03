
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(page_title="Predicción de Partidos de Fútbol", layout="wide")
st.title("⚽ Predicción de Partidos de Fútbol con Modelo Real")

# Cargar modelo y datos
@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv("data/matches.csv", parse_dates=["MatchDate"])
    return df.dropna()

model = load_model()
df = load_data()

# Obtener lista de equipos
equipos = sorted(set(df["HomeTeam"]).union(df["AwayTeam"]))

# Selección de equipos
st.subheader("Selecciona los equipos para predecir el partido")
col1, col2 = st.columns(2)
with col1:
    equipo_local = st.selectbox("Equipo Local", equipos)
with col2:
    equipo_visitante = st.selectbox("Equipo Visitante", [e for e in equipos if e != equipo_local])

# Buscar últimos partidos de cada equipo
def get_last_matches(df, team, n=5):
    mask = (df["HomeTeam"] == team) | (df["AwayTeam"] == team)
    return df[mask].sort_values("MatchDate", ascending=False).head(n)

def extract_team_stats(df, team):
    shots, target, corners, yellows, reds, goals = [], [], [], [], [], []
    for _, row in df.iterrows():
        is_home = row["HomeTeam"] == team
        if is_home:
            shots.append(row["HomeShots"])
            target.append(row["HomeTarget"])
            corners.append(row["HomeCorners"])
            yellows.append(row["HomeYellow"])
            reds.append(row["HomeRed"])
            goals.append(row["FTHome"])
        else:
            shots.append(row["AwayShots"])
            target.append(row["AwayTarget"])
            corners.append(row["AwayCorners"])
            yellows.append(row["AwayYellow"])
            reds.append(row["AwayRed"])
            goals.append(row["FTAway"])
    return {
        "shots": np.mean(shots),
        "target": np.mean(target),
        "corners": np.mean(corners),
        "yellows": np.mean(yellows),
        "reds": np.mean(reds),
        "goals": np.mean(goals)
    }

if st.button("🔍 Analizar partido"):
    df_local = get_last_matches(df, equipo_local)
    df_visita = get_last_matches(df, equipo_visitante)

    if df_local.empty or df_visita.empty:
        st.warning("❗ No hay suficientes datos para uno o ambos equipos seleccionados.")
        st.stop()

    stats_local = extract_team_stats(df_local, equipo_local)
    stats_visita = extract_team_stats(df_visita, equipo_visitante)

    # El resto del análisis va aquí...

    st.subheader("📊 Estadísticas Promedio")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{equipo_local}**")
        for k, v in stats_local.items():
            st.metric(k.capitalize(), round(v, 2))
    with col2:
        st.markdown(f"**{equipo_visitante}**")
        for k, v in stats_visita.items():
            st.metric(k.capitalize(), round(v, 2))

    # Crear entrada para el modelo
    X = pd.DataFrame([{
        "shots_home": stats_local["shots"],
        "target_home": stats_local["target"],
        "corners_home": stats_local["corners"],
        "yellows_home": stats_local["yellows"],
        "reds_home": stats_local["reds"],
        "shots_away": stats_visita["shots"],
        "target_away": stats_visita["target"],
        "corners_away": stats_visita["corners"],
        "yellows_away": stats_visita["yellows"],
        "reds_away": stats_visita["reds"]
    }])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    st.subheader("🔮 Predicción del Resultado")
    labels = model.classes_
    resultado = labels[np.argmax(proba)]
    st.success(f"Resultado estimado: **{resultado}**")
    for label, p in zip(labels, proba):
        st.write(f"{label}: {p*100:.2f}%")

    st.caption("Modelo entrenado localmente con datos reales de múltiples ligas.")
