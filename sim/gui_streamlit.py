"""
GUI interactiva para el simulador TUI v4.1 (toy model)
------------------------------------------------------
Permite controlar parámetros, ejecutar simulaciones, visualizar métricas y reportes, exportar resultados y acceder a documentación TUI.
Organización profesional, sin hardcoding ni números mágicos, bilingüe y extensible.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sim.prototipo_rl_simbiosis import run_experiment
from sim.gui_utils import plot_heatmap, plot_dashboard, scientific_report

# ===================== Configuración de parámetros =====================
# Valores por defecto y rangos profesionales
PARAMS = {
    "episodes": {"label": "Episodios / Episodes", "min_value": 100, "max_value": 5000, "step": 100, "value": 1000, "help": "Número total de episodios a simular. / Total episodes to simulate."},
    "seed": {"label": "Semilla / Seed", "min_value": 1, "max_value": 9999, "step": 1, "value": 42, "help": "Semilla aleatoria para reproducibilidad. / Random seed for reproducibility."},
    "risk_scale": {"label": "Escala de riesgo / Risk scale", "min_value": 0.1, "max_value": 5.0, "step": 0.1, "value": 1.0, "help": "Multiplicador de penalización por riesgo. / Risk penalty multiplier."},
    "grid_size": {"label": "Tamaño del grid / Grid size", "min_value": 3, "max_value": 10, "step": 1, "value": 5, "help": "Dimensión del entorno (NxN). / Environment size (NxN)."},
    "initial_resources": {"label": "Recursos iniciales / Initial resources", "min_value": 10.0, "max_value": 500.0, "step": 10.0, "value": 100.0, "help": "Cantidad de recursos al inicio. / Initial resources amount."},
    "tripwires": {"label": "Tripwires (cantidad) / Tripwires (count)", "min_value": 0, "max_value": 10, "step": 1, "value": 1, "help": "Número de tripwires en el entorno. / Number of tripwires in environment."},
    "shocks": {"label": "Shocks (cantidad) / Shocks (count)", "min_value": 0, "max_value": 10, "step": 1, "value": 1, "help": "Número de shocks en el entorno. / Number of shocks in environment."},
    "distractors": {"label": "Distractores (cantidad) / Distractors (count)", "min_value": 0, "max_value": 10, "step": 1, "value": 1, "help": "Número de distractores en el entorno. / Number of distractors in environment."},
    "max_steps": {"label": "Pasos máximos por episodio / Max steps per episode", "min_value": 10, "max_value": 200, "step": 10, "value": 50, "help": "Límite de pasos por episodio. / Step limit per episode."},
    "agent_type": {"label": "Tipo de agente / Agent type", "options": ["Control (Q-table)", "Simbiosis (DQN)"], "help": "Selecciona el tipo de agente a simular. / Select agent type."}
}

def main():
    # ===================== Sidebar: Parámetros =====================
    st.sidebar.title("TUI v4.1 Simulador — Parámetros")
    episodes = st.sidebar.slider(PARAMS["episodes"]["label"], min_value=PARAMS["episodes"]["min_value"], max_value=PARAMS["episodes"]["max_value"], step=PARAMS["episodes"]["step"], value=PARAMS["episodes"]["value"], help=PARAMS["episodes"]["help"])
    seed = st.sidebar.slider(PARAMS["seed"]["label"], min_value=PARAMS["seed"]["min_value"], max_value=PARAMS["seed"]["max_value"], step=PARAMS["seed"]["step"], value=PARAMS["seed"]["value"], help=PARAMS["seed"]["help"])
    risk_scale = st.sidebar.slider(PARAMS["risk_scale"]["label"], min_value=PARAMS["risk_scale"]["min_value"], max_value=PARAMS["risk_scale"]["max_value"], step=PARAMS["risk_scale"]["step"], value=PARAMS["risk_scale"]["value"], help=PARAMS["risk_scale"]["help"])
    grid_size = st.sidebar.slider(PARAMS["grid_size"]["label"], min_value=PARAMS["grid_size"]["min_value"], max_value=PARAMS["grid_size"]["max_value"], step=PARAMS["grid_size"]["step"], value=PARAMS["grid_size"]["value"], help=PARAMS["grid_size"]["help"])
    initial_resources = st.sidebar.slider(PARAMS["initial_resources"]["label"], min_value=PARAMS["initial_resources"]["min_value"], max_value=PARAMS["initial_resources"]["max_value"], step=PARAMS["initial_resources"]["step"], value=PARAMS["initial_resources"]["value"], help=PARAMS["initial_resources"]["help"])
    tripwires = st.sidebar.slider(PARAMS["tripwires"]["label"], min_value=PARAMS["tripwires"]["min_value"], max_value=PARAMS["tripwires"]["max_value"], step=PARAMS["tripwires"]["step"], value=PARAMS["tripwires"]["value"], help=PARAMS["tripwires"]["help"])
    shocks = st.sidebar.slider(PARAMS["shocks"]["label"], min_value=PARAMS["shocks"]["min_value"], max_value=PARAMS["shocks"]["max_value"], step=PARAMS["shocks"]["step"], value=PARAMS["shocks"]["value"], help=PARAMS["shocks"]["help"])
    distractors = st.sidebar.slider(PARAMS["distractors"]["label"], min_value=PARAMS["distractors"]["min_value"], max_value=PARAMS["distractors"]["max_value"], step=PARAMS["distractors"]["step"], value=PARAMS["distractors"]["value"], help=PARAMS["distractors"]["help"])
    max_steps = st.sidebar.slider(PARAMS["max_steps"]["label"], min_value=PARAMS["max_steps"]["min_value"], max_value=PARAMS["max_steps"]["max_value"], step=PARAMS["max_steps"]["step"], value=PARAMS["max_steps"]["value"], help=PARAMS["max_steps"]["help"])
    agent_type = st.sidebar.selectbox(PARAMS["agent_type"]["label"], PARAMS["agent_type"]["options"], help=PARAMS["agent_type"]["help"])

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Documentación TUI:**")
    st.sidebar.markdown("[Teoría Unificada de la Inteligencia v4.1](./TUI/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md)")

    # ===================== Registro de corridas en sesión =====================
    if "runs" not in st.session_state:
        st.session_state["runs"] = []

    st.title("Simulador TUI v4.1 — Toy Model RL Symbiosis")
    st.markdown("""
    Controla parámetros, ejecuta simulaciones, visualiza métricas y reportes científicos, exporta resultados y accede a la documentación TUI. Todo bilingüe y reproducible.

    **Nota:** Siempre se ejecuta y compara el agente Control (Q-table) con Simbiosis (DQN) para referencia científica. / **Note:** Control agent is always run and compared with Simbiosis for scientific reference.
    """)

    if st.button("Ejecutar simulación / Run simulation"):
        # Ejecutar Control
        st.info("Simulando agente Control (Q-table)... / Simulating Control agent...")
        results_control = run_experiment(
            episodes=episodes,
            seed=seed,
            risk_scale=risk_scale,
            agent_name="Control",
            use_pgf=False,
            use_dqn=False
        )
        # Ejecutar Simbiosis si corresponde
        if agent_type == "Simbiosis (DQN)":
            st.info("Simulando agente Simbiosis (DQN)... / Simulating Simbiosis agent...")
            results_simbiosis = run_experiment(
                episodes=episodes,
                seed=seed,
                risk_scale=risk_scale,
                agent_name="Simbiosis",
                use_pgf=True,
                use_dqn=True
            )
        else:
            results_simbiosis = None
        # Guardar corrida en registro
        st.session_state["runs"].append({
            "params": dict(
                episodes=episodes,
                seed=seed,
                risk_scale=risk_scale,
                grid_size=grid_size,
                initial_resources=initial_resources,
                tripwires=tripwires,
                shocks=shocks,
                distractors=distractors,
                max_steps=max_steps,
                agent_type=agent_type
            ),
            "control": results_control,
            "simbiosis": results_simbiosis
        })
        st.success("Simulación completada y registrada. / Simulation completed and logged.")

    # ===================== Selección y comparación de corridas históricas =====================
    if len(st.session_state["runs"]) > 1:
        st.subheader("Comparación de corridas históricas / Historical runs comparison")
        st.markdown("Selecciona dos corridas para comparar agentes y configuraciones. / Select two runs to compare agents and configurations.")
        idx_a = st.selectbox("Corrida A / Run A", options=list(range(len(st.session_state["runs"]))), format_func=lambda i: f"Run {i+1}")
        idx_b = st.selectbox("Corrida B / Run B", options=list(range(len(st.session_state["runs"]))), index=len(st.session_state["runs"])-1, format_func=lambda i: f"Run {i+1}")
        run_a = st.session_state["runs"][idx_a]
        run_b = st.session_state["runs"][idx_b]
        st.write("**Parámetros A / Parameters A:**", run_a["params"])
        st.write("**Parámetros B / Parameters B:**", run_b["params"])
        # Panel comparativo de métricas
        st.write("**Métricas principales / Main metrics:**")
        st.write({
            "Recompensa media Control A": run_a["control"]["avg_reward"],
            "Recompensa media Control B": run_b["control"]["avg_reward"],
            "Recompensa media Simbiosis A": run_a["simbiosis"]["avg_reward"] if run_a["simbiosis"] else None,
            "Recompensa media Simbiosis B": run_b["simbiosis"]["avg_reward"] if run_b["simbiosis"] else None,
            # ... puedes añadir más métricas aquí ...
        })
        # Panel de interpretación automática
        st.subheader("Interpretación automática / Automatic interpretation")
        interp = "Simbiosis supera a Control en PGF si la curva roja está por encima de la azul. / Simbiosis outperforms Control in PGF if the red curve is above the blue."
        interp += "\nMayor Q-optimal indica mejor alineación de política. / Higher Q-optimal indicates better policy alignment."
        st.info(interp)
    else:
        st.info("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")

    # ===================== Exportación del historial =====================
    if st.session_state["runs"]:  # Si hay al menos una run
        st.subheader("Exportar historial / Export history")
        import json
        st.download_button("Descargar historial JSON / Download history JSON", json.dumps(st.session_state["runs"], indent=2), "historial_corridas.json")

    # ===================== Panel de ayuda =====================

    # ===================== Panel de ayuda =====================
    st.markdown("---")
    st.markdown("**Ayuda / Help:**")
    st.markdown("Toy model para validar la Teoría Unificada de la Inteligencia. Modifica parámetros, ejecuta simulaciones y analiza resultados. Para detalles teóricos, consulta la documentación TUI.")

# ===================== Ejecución del script =====================
if __name__ == "__main__":
    main()
