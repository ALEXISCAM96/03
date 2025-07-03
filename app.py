
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Predicción de Partidos de Fútbol", layout="wide")
st.title("⚽ Predicción Avanzada de Partidos de Fútbol")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/matches_sample.csv", parse_dates=["MatchDate"])
    df = df.dropna()
    return df

df = load_data()

st.markdown("### Selecciona el Partido a Analizar")
equipos = sorted(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
equipo_local = st.selectbox("Equipo Local", equipos)
equipo_visitante = st.selectbox("Equipo Visitante", [e for e in equipos if e != equipo_local])

# Filtrado de últimos partidos para análisis
def get_last_matches(df, team, n=10):
    mask = (df['HomeTeam'] == team) | (df['AwayTeam'] == team)
    return df[mask].sort_values(by="MatchDate", ascending=False).head(n)

local_matches = get_last_matches(df, equipo_local)
visitante_matches = get_last_matches(df, equipo_visitante)

# Estadísticas promedio
def compute_team_stats(matches, team):
    goles = []
    remates = []
    tiros = []
    corners = []
    tarjetas = []
    for _, row in matches.iterrows():
        if row['HomeTeam'] == team:
            goles.append(row['FTHome'])
            remates.append(row['HomeShots'])
            tiros.append(row['HomeTarget'])
            corners.append(row['HomeCorners'])
            tarjetas.append(row['HomeYellow'] + row['HomeRed'])
        else:
            goles.append(row['FTAway'])
            remates.append(row['AwayShots'])
            tiros.append(row['AwayTarget'])
            corners.append(row['AwayCorners'])
            tarjetas.append(row['AwayYellow'] + row['AwayRed'])
    return {
        "Goles": np.mean(goles),
        "Remates": np.mean(remates),
        "Remates a puerta": np.mean(tiros),
        "Córners": np.mean(corners),
        "Tarjetas": np.mean(tarjetas)
    }

stats_local = compute_team_stats(local_matches, equipo_local)
stats_visitante = compute_team_stats(visitante_matches, equipo_visitante)

st.subheader("📊 Estadísticas Promedio Últimos 10 Partidos")
cols = st.columns(2)
for i, (team, stats) in enumerate([(equipo_local, stats_local), (equipo_visitante, stats_visitante)]):
    with cols[i]:
        st.markdown(f"**{team}**")
        for k, v in stats.items():
            st.metric(k, f"{v:.2f}")

# Predicción simple (puedes reemplazar por modelo real)
st.subheader("🔮 Predicción del Partido")
goles_local = stats_local["Goles"]
goles_visitante = stats_visitante["Goles"]
resultado = "Empate"
if goles_local > goles_visitante:
    resultado = f"Gana {equipo_local}"
elif goles_visitante > goles_local:
    resultado = f"Gana {equipo_visitante}"

st.markdown(f"**Resultado Estimado:** {resultado}")
st.markdown(f"**Goles esperados:** {equipo_local} {goles_local:.1f} - {goles_visitante:.1f} {equipo_visitante}")
