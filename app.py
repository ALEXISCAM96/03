import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide", page_title="Predicción de Partidos de Fútbol")

st.title("⚽ Predicción Avanzada de Partidos de Fútbol (Sin API)")

# Simulador de datos recientes para un equipo
def generar_estadisticas_equipo(nombre):
    return {
        "nombre": nombre,
        "goles_prom": round(np.random.uniform(0.8, 2.5), 2),
        "goles_contra": round(np.random.uniform(0.6, 2.0), 2),
        "remates": int(np.random.uniform(8, 18)),
        "remates_puerta": int(np.random.uniform(3, 9)),
        "corners": int(np.random.uniform(3, 10)),
        "tarjetas": int(np.random.uniform(1, 4)),
        "posesion": round(np.random.uniform(45, 60), 1),
        "forma": np.random.choice(["Alta", "Media", "Baja"])
    }

# Simula lista de jugadores con goles
def generar_jugadores(equipo):
    jugadores = []
    for i in range(1, 12):
        tiros = np.random.randint(1, 5)
        goles = np.random.binomial(tiros, 0.25)
        jugadores.append({
            "nombre": f"Jugador {i} ({equipo})",
            "tiros": tiros,
            "goles": goles,
            "probabilidad_gol": round(min(1.0, 0.15 + goles * 0.1), 2)
        })
    return jugadores

# Simula enfrentamientos previos
def simulacion_enfrentamientos_directos():
    return {
        "victorias_local": random.randint(2, 6),
        "victorias_visita": random.randint(1, 5),
        "empates": random.randint(0, 3),
        "promedio_goles_total": round(random.uniform(1.8, 3.5), 2)
    }

# Mapa de calor simulado
def generar_mapa_calor(equipo):
    zonas = ['Izquierda', 'Centro', 'Derecha', 'Área', 'Defensa']
    intensidad = np.random.randint(10, 50, size=len(zonas))
    fig = go.Figure(go.Barpolar(
        r=intensidad,
        theta=zonas,
        width=[15]*len(zonas),
        marker_color='crimson',
        marker_line_color="black",
        marker_line_width=1,
        opacity=0.75
    ))
    fig.update_layout(title=f"Mapa de calor simulado - {equipo}")
    return fig

# Predicción de resultado
def predecir_resultado(equipo1, equipo2):
    dif_goles = equipo1["goles_prom"] - equipo2["goles_contra"]
    dif_contra = equipo2["goles_prom"] - equipo1["goles_contra"]
    gol1 = max(0.2, round((equipo1["goles_prom"] + dif_goles + equipo1["forma"].count("Alta") * 0.2), 2))
    gol2 = max(0.2, round((equipo2["goles_prom"] + dif_contra + equipo2["forma"].count("Alta") * 0.2), 2))
    return gol1, gol2

# Entrada de usuario
col1, col2 = st.columns(2)
with col1:
    equipo_local = st.text_input("Equipo Local", "Barcelona")
with col2:
    equipo_visitante = st.text_input("Equipo Visitante", "Real Madrid")

if st.button("🔍 Analizar Partido"):
    stats_local = generar_estadisticas_equipo(equipo_local)
    stats_visita = generar_estadisticas_equipo(equipo_visitante)
    enfrentamientos = simulacion_enfrentamientos_directos()
    jugadores_local = generar_jugadores(equipo_local)
    jugadores_visita = generar_jugadores(equipo_visitante)

    st.subheader("📊 Estadísticas Simuladas")
    col1, col2 = st.columns(2)
    col1.metric("Goles Promedio", stats_local["goles_prom"])
    col1.metric("Remates", stats_local["remates"])
    col1.metric("Remates a Puerta", stats_local["remates_puerta"])
    col1.metric("Corners", stats_local["corners"])
    col1.metric("Tarjetas", stats_local["tarjetas"])
    col1.metric("Posesión", f"{stats_local['posesion']}%")
    col1.metric("Forma", stats_local["forma"])

    col2.metric("Goles Promedio", stats_visita["goles_prom"])
    col2.metric("Remates", stats_visita["remates"])
    col2.metric("Remates a Puerta", stats_visita["remates_puerta"])
    col2.metric("Corners", stats_visita["corners"])
    col2.metric("Tarjetas", stats_visita["tarjetas"])
    col2.metric("Posesión", f"{stats_visita['posesion']}%")
    col2.metric("Forma", stats_visita["forma"])

    st.subheader("🤝 Enfrentamientos Directos")
    st.write(f"Victorias {equipo_local}: {enfrentamientos['victorias_local']}")
    st.write(f"Victorias {equipo_visitante}: {enfrentamientos['victorias_visita']}")
    st.write(f"Empates: {enfrentamientos['empates']}")
    st.write(f"Goles Promedio por Partido: {enfrentamientos['promedio_goles_total']}")

    st.subheader("🔮 Predicción de Resultado")
    gol1, gol2 = predecir_resultado(stats_local, stats_visita)
    st.write(f"Resultado estimado: **{equipo_local} {gol1} - {gol2} {equipo_visitante}**")

    if gol1 > gol2:
        ganador = equipo_local
    elif gol2 > gol1:
        ganador = equipo_visitante
    else:
        ganador = "Empate"
    st.success(f"Predicción: {ganador}")

    st.subheader("⚽ Goleadores Probables")
    top_goleadores = sorted(jugadores_local + jugadores_visita, key=lambda x: -x["probabilidad_gol"])[:5]
    df_goleadores = pd.DataFrame(top_goleadores)
    st.table(df_goleadores[["nombre", "tiros", "goles", "probabilidad_gol"]])

    st.subheader("🔥 Mapas de Calor Simulados")
    col1, col2 = st.columns(2)
    col1.plotly_chart(generar_mapa_calor(equipo_local))
    col2.plotly_chart(generar_mapa_calor(equipo_visitante))

    st.subheader("💡 Apuestas Combinadas Recomendadas")
    jugador_top = df_goleadores.iloc[0]["nombre"]
    st.write(f"✅ **{jugador_top} marca + gana {ganador}**")
    st.caption("Basado en simulación de rendimiento reciente y forma general.")
