#!/usr/bin/env python3
"""
GUI interactiva para el simulador TUI v4.1 (toy model)
------------------------------------------------------
Controla parámetros, ejecuta simulaciones, visualiza métricas y exporta resultados.
Enfocada en comparabilidad: siempre corre Control y un agente seleccionado
entre Simbiosis (DQN+PGF) y variantes TUI (only / PGF light / PGF heavy).
"""
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.runner import run_experiment  # noqa: E402
from sim.gui_utils import plot_heatmap, plot_dashboard, scientific_report  # noqa: E402

# Parámetros de entrada
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
}

# Configuración de agentes (alineado con ablations)
AGENT_CONFIGS = {
    "Simbiosis (DQN+PGF)": {"agent_name": "Simbiosis", "use_dqn": True, "use_pgf": True, "pgf_mix": 1.0},
    "TUI only": {"agent_name": "tui_only", "use_dqn": False, "use_pgf": False, "pgf_mix": 0.0},
    "TUI PGF light": {"agent_name": "tui_pgf_light", "use_dqn": True, "use_pgf": True, "pgf_mix": 0.5},
    "TUI PGF heavy": {"agent_name": "tui_pgf_heavy", "use_dqn": True, "use_pgf": True, "pgf_mix": 0.8},
}

AGENT_OPTIONS = ["Simbiosis (DQN+PGF)", "TUI only", "TUI PGF light", "TUI PGF heavy"]


def main():  # pragma: no cover
    st.title("Simulador TUI v4.1 — Toy Model RL Symbiosis")
    st.sidebar.title("Parámetros")
    # Botón reset
    if st.sidebar.button("Reset to default"):
        for k, cfg in PARAMS.items():
            st.session_state[k] = cfg["value"]
    # Sliders
    episodes = st.sidebar.slider(**PARAMS["episodes"], value=st.session_state.get("episodes", PARAMS["episodes"]["value"]))
    seed = st.sidebar.slider(**PARAMS["seed"], value=st.session_state.get("seed", PARAMS["seed"]["value"]))
    risk_scale = st.sidebar.slider(**PARAMS["risk_scale"], value=st.session_state.get("risk_scale", PARAMS["risk_scale"]["value"]))
    grid_size = st.sidebar.slider(**PARAMS["grid_size"], value=st.session_state.get("grid_size", PARAMS["grid_size"]["value"]))
    initial_resources = st.sidebar.slider(**PARAMS["initial_resources"], value=st.session_state.get("initial_resources", PARAMS["initial_resources"]["value"]))
    tripwires = st.sidebar.slider(**PARAMS["tripwires"], value=st.session_state.get("tripwires", PARAMS["tripwires"]["value"]))
    shocks = st.sidebar.slider(**PARAMS["shocks"], value=st.session_state.get("shocks", PARAMS["shocks"]["value"]))
    distractors = st.sidebar.slider(**PARAMS["distractors"], value=st.session_state.get("distractors", PARAMS["distractors"]["value"]))
    max_steps = st.sidebar.slider(**PARAMS["max_steps"], value=st.session_state.get("max_steps", PARAMS["max_steps"]["value"]))
    agent_choice = st.sidebar.selectbox("Tipo de agente / Agent type", AGENT_OPTIONS, help="Se compara siempre contra Control (Q-table).")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Documentación TUI:**")
    st.sidebar.markdown("[Teoría Unificada de la Inteligencia v4.1](./TUI/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md)")

    if "runs" not in st.session_state:
        st.session_state["runs"] = []

    st.markdown(
        "Controla parámetros, ejecuta simulaciones y compara Control vs el agente seleccionado. "
        "Útil para mostrar prudencia PGF vs DQN en los mismos riesgos."
    )

    if st.button("Ejecutar simulación / Run simulation"):
        cfg = AGENT_CONFIGS[agent_choice]
        # Control baseline
        st.info("Simulando agente Control (Q-table)...")
        control = run_experiment(
            episodes=episodes,
            seed=seed,
            risk_scale=risk_scale,
            agent_name="Control",
            use_pgf=False,
            use_dqn=False,
            pgf_mix=0.0,
        )
        # Agente seleccionado
        st.info(f"Simulando agente {cfg['agent_name']}...")
        selected = run_experiment(
            episodes=episodes,
            seed=seed,
            risk_scale=risk_scale,
            agent_name=cfg["agent_name"],
            use_pgf=cfg["use_pgf"],
            use_dqn=cfg["use_dqn"],
            pgf_mix=cfg["pgf_mix"],
        )
        st.session_state["runs"].append(
            {
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
                    agent=agent_choice,
                ),
                "control": control,
                "selected": selected,
            }
        )
        st.success("Simulación completada y registrada.")

    if len(st.session_state["runs"]) >= 1:
        st.subheader("Corridas registradas")
        st.write(f"Total runs: {len(st.session_state['runs'])}")
        last = st.session_state["runs"][-1]
        st.write("Última configuración:", last["params"])
        st.write("Métricas Control:", {k: v for k, v in last["control"].items() if not isinstance(v, (list, dict))})
        st.write("Métricas agente seleccionado:", {k: v for k, v in last["selected"].items() if not isinstance(v, (list, dict))})

    if len(st.session_state["runs"]) >= 2:
        st.subheader("Comparación de corridas")
        idx_a = st.selectbox("Run A", options=list(range(len(st.session_state["runs"]))), format_func=lambda i: f"Run {i+1}")
        idx_b = st.selectbox("Run B", options=list(range(len(st.session_state["runs"]))), index=len(st.session_state["runs"]) - 1, format_func=lambda i: f"Run {i+1}")
        run_a = st.session_state["runs"][idx_a]
        run_b = st.session_state["runs"][idx_b]
        st.write("Params A:", run_a["params"])
        st.write("Params B:", run_b["params"])

    if st.session_state["runs"]:
        st.subheader("Exportar historial")
        if st.button("Exportar a JSON (session_runs.json)"):
            import json

            export = []
            for r in st.session_state["runs"]:
                export.append(r)
            Path("session_runs.json").write_text(json.dumps(export, indent=2), encoding="utf-8")
            st.success("Historial exportado en session_runs.json")


if __name__ == "__main__":  # pragma: no cover
    main()
