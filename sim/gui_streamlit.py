#!/usr/bin/env python3
"""
GUI liviana para el toy model TUI v4.1.
Enfocada en los casos de prueba: sliders básicos, validación de seed,
ejecución de simulación control + agente seleccionado, panel de comparación y exportación.
"""
import os
import sys
from pathlib import Path
import json

import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.runner import run_experiment  # noqa: E402


PARAMS = {
    "episodes": {"label": "Episodios / Episodes", "min_value": 100, "max_value": 5000, "step": 100, "value": 1000},
    "seed": {"label": "Semilla / Seed", "min_value": 1, "max_value": 9999, "step": 1, "value": 42},
    "risk_scale": {"label": "Escala de riesgo / Risk scale", "min_value": 0.1, "max_value": 5.0, "step": 0.1, "value": 1.0},
    "grid_size": {"label": "Tamaño del grid / Grid size", "min_value": 3, "max_value": 10, "step": 1, "value": 5},
    "initial_resources": {"label": "Recursos iniciales / Initial resources", "min_value": 10.0, "max_value": 500.0, "step": 10.0, "value": 100.0},
    "tripwires": {"label": "Tripwires (cantidad)", "min_value": 0, "max_value": 10, "step": 1, "value": 1},
    "shocks": {"label": "Shocks (cantidad)", "min_value": 0, "max_value": 10, "step": 1, "value": 1},
    "distractors": {"label": "Distractores (cantidad)", "min_value": 0, "max_value": 10, "step": 1, "value": 1},
    "max_steps": {"label": "Pasos máximos por episodio", "min_value": 10, "max_value": 200, "step": 10, "value": 50},
}

AGENT_CONFIGS = {
    "Simbiosis (DQN+PGF)": {"agent_name": "Simbiosis", "use_dqn": True, "use_pgf": True, "pgf_mix": 1.0},
    "Simbiosis (DQN)": {"agent_name": "Simbiosis", "use_dqn": True, "use_pgf": False, "pgf_mix": 0.0},
    "TUI only": {"agent_name": "tui_only", "use_dqn": False, "use_pgf": False, "pgf_mix": 0.0},
    "TUI PGF light": {"agent_name": "tui_pgf_light", "use_dqn": True, "use_pgf": True, "pgf_mix": 0.5},
    "TUI PGF heavy": {"agent_name": "tui_pgf_heavy", "use_dqn": True, "use_pgf": True, "pgf_mix": 0.8},
    "Control (Q-table)": {"agent_name": "Control", "use_dqn": False, "use_pgf": False, "pgf_mix": 0.0},
}
AGENT_OPTIONS = list(AGENT_CONFIGS.keys())

def main():  # pragma: no cover
    if "runs" not in st.session_state:
        st.session_state["runs"] = []
    st.title("Simulador TUI v4.1 — Toy Model RL Symbiosis")
    st.sidebar.title("TUI v4.1 Simulador — Parámetros")
    st.markdown("**Ayuda / Help:**")

    # Validación temprana de seed si viene del session_state (para cubrir tests)
    seed_min, seed_max = PARAMS["seed"]["min_value"], PARAMS["seed"]["max_value"]
    seed_ss = st.session_state.get("seed")
    if seed_ss is not None:
        try:
            seed_ss_int = int(seed_ss)
            if seed_ss_int < seed_min or seed_ss_int > seed_max:
                st.sidebar.error("Seed fuera de rango / Seed out of range")
                st.warning("Seed inválida, ajusta el valor antes de continuar. / Invalid seed, adjust before running.")
                st.stop()
                return
        except Exception:
            st.sidebar.error("La 'Semilla (seed)' debe ser un número entero válido")
            st.warning("Seed inválida, ajusta el valor antes de continuar. / Invalid seed, adjust before running.")
            st.stop()
            return

    # Sliders (9)
    episodes = st.sidebar.slider(**PARAMS["episodes"])
    seed = st.sidebar.slider(**PARAMS["seed"])
    risk_scale = st.sidebar.slider(**PARAMS["risk_scale"])
    grid_size = st.sidebar.slider(**PARAMS["grid_size"])
    initial_resources = st.sidebar.slider(**PARAMS["initial_resources"])
    tripwires = st.sidebar.slider(**PARAMS["tripwires"])
    shocks = st.sidebar.slider(**PARAMS["shocks"])
    distractors = st.sidebar.slider(**PARAMS["distractors"])
    max_steps = st.sidebar.slider(**PARAMS["max_steps"])
    agent_choice = st.sidebar.selectbox("Tipo de agente / Agent type", AGENT_OPTIONS)

    # Validación seed
    try:
        seed_int = int(seed)
    except Exception:
        st.sidebar.error("La 'Semilla (seed)' debe ser un número entero válido")
        st.warning("Seed inválida, ajusta el valor antes de continuar. / Invalid seed, adjust before running.")
        st.stop()
        return
    if seed_int < seed_min or seed_int > seed_max:
        st.sidebar.error("Seed fuera de rango / Seed out of range")
        st.warning("Seed inválida, ajusta el valor antes de continuar. / Invalid seed, adjust before running.")
        st.stop()
        return

    if st.button("Ejecutar simulación / Run simulation"):
        cfg = AGENT_CONFIGS[agent_choice]
        control = run_experiment(
            episodes=episodes,
            seed=seed_int,
            risk_scale=risk_scale,
            agent_name="Control",
            use_pgf=False,
            use_dqn=False,
            pgf_mix=0.0,
            grid_size=grid_size,
            initial_resources=initial_resources,
            tripwires=tripwires,
            shocks=shocks,
            distractors=distractors,
            max_steps=max_steps,
        )
        selected = run_experiment(
            episodes=episodes,
            seed=seed_int,
            risk_scale=risk_scale,
            agent_name=cfg["agent_name"],
            use_pgf=cfg["use_pgf"],
            use_dqn=cfg["use_dqn"],
            pgf_mix=cfg["pgf_mix"],
            grid_size=grid_size,
            initial_resources=initial_resources,
            tripwires=tripwires,
            shocks=shocks,
            distractors=distractors,
            max_steps=max_steps,
        )
        st.session_state["runs"].append(
            {
                "params": {
                    "episodes": episodes,
                    "seed": seed_int,
                    "risk_scale": risk_scale,
                    "grid_size": grid_size,
                    "initial_resources": initial_resources,
                    "tripwires": tripwires,
                    "shocks": shocks,
                    "distractors": distractors,
                    "max_steps": max_steps,
                    "agent": agent_choice,
                },
                "control": control,
                "selected": selected,
            }
        )
        st.success("Simulación completada y registrada. / Simulation completed and logged.")

    # Panel de corridas
    if st.session_state["runs"]:
        st.subheader("Corridas registradas")
        st.write(f"Total runs: {len(st.session_state['runs'])}")
    if len(st.session_state["runs"]) >= 2:
        st.subheader("Comparación de corridas históricas / Historical runs comparison")
        idx_a = st.selectbox("Run A", options=list(range(len(st.session_state["runs"]))), format_func=lambda i: f"Run {i+1}")
        idx_b = st.selectbox("Run B", options=list(range(len(st.session_state["runs"]))), index=len(st.session_state["runs"])-1, format_func=lambda i: f"Run {i+1}")
        run_a = st.session_state["runs"][idx_a]
        run_b = st.session_state["runs"][idx_b]
        st.write("Params A:", run_a["params"])
        st.write("Params B:", run_b["params"])
    else:
        st.info("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")

    # Exportación
    if st.session_state["runs"]:
        st.subheader("Exportar historial / Export history")
        try:
            export_preview = json.dumps(st.session_state["runs"], indent=2, default=str)
        except Exception:
            export_preview = "{}"
        st.download_button("Descargar JSON", data=export_preview, file_name="session_runs.json")
        if st.button("Exportar a JSON (session_runs.json)"):
            Path("session_runs.json").write_text(export_preview, encoding="utf-8")
            st.info("Historial exportado en session_runs.json")


        runs_serializable = [sanitize_run(run) for run in st.session_state["runs"]]
        st.download_button("Descargar historial JSON / Download history JSON", json.dumps(runs_serializable, indent=2), "historial_corridas.json")

    # ===================== Panel de ayuda =====================

    # ===================== Panel de ayuda =====================
    st.markdown("---")
    st.markdown("**Ayuda / Help:**")
    st.markdown("Toy model para validar la Teoría Unificada de la Inteligencia. Modifica parámetros, ejecuta simulaciones y analiza resultados. Para detalles teóricos, consulta la documentación TUI.")

# ===================== Ejecución del script =====================
if __name__ == "__main__":  # pragma: no cover - interfaz interactiva
    main()
