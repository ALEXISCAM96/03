
import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Predicción de Fútbol", layout="wide")
st.title("⚽ Predicción de Partidos de Fútbol con Modelo Real")

@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv("data/matches.csv")
    return df.dropna()

model = load_model()
df = load_data()

equipos = sorted(set(df["HomeTeam"]).union(df["AwayTeam"]))

st.subheader("Selecciona los equipos")
col1, col2 = st.columns(2)
with col1:
    equipo_local = st.selectbox("Equipo Local", equipos)
with col2:
    equipo_visitante = st.selectbox("Equipo Visitante", [e for e in equipos if e != equipo_local])

def get_last_matches(df, team, n=5):
    mask = (df["HomeTeam"] == team) | (df["AwayTeam"] == team)
    return df[mask].tail(n)

def extract_team_stats(df, team):
    shots, target, corners, yellows, reds, goals = [], [], [], [], [], []
    for _, row in df.iterrows():
        if row["HomeTeam"] == team:
            shots.append(row["HomeShots"])
            target.append(row["HomeTarget"])
            corners.append(row["HomeCorners"])
            yellows.append(row["HomeYellow"])
            reds.append(row["HomeRed"])
            goals.append(row["FTHome"])
        elif row["AwayTeam"] == team:
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

    X = pd.DataFrame([{
        "HomeShots": stats_local["shots"],
        "HomeTarget": stats_local["target"],
        "HomeCorners": stats_local["corners"],
        "HomeYellow": stats_local["yellows"],
        "HomeRed": stats_local["reds"],
        "AwayShots": stats_visita["shots"],
        "AwayTarget": stats_visita["target"],
        "AwayCorners": stats_visita["corners"],
        "AwayYellow": stats_visita["yellows"],
        "AwayRed": stats_visita["reds"]
    }])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    labels = model.classes_

    st.subheader("🔮 Predicción del Resultado")
    st.success(f"Resultado estimado: **{pred}**")
    for label, p in zip(labels, proba):
        st.write(f"{label}: {p*100:.2f}%")
