#!/usr/bin/env python3
"""
tui_toy_rl.py - TUI v4.1 Toy Model RL Symbiosis (DOI-ready)

Autor / Author: Jose M Rivera Garcia
Email: jmrgpr@gmail.com | jrivera77@outlook.com
ORCID: https://orcid.org/0009-0000-3013-725X

Caracteristicas principales / Key features:
- Entorno Gridworld con riesgo constitutivo, proposito acoplado, recursos limitados, shocks y distractores.
- Agente con memoria, plasticidad, reprogramacion de meta y atribucion granular de culpa/recompensa.
- Metricas avanzadas: adaptacion, robustez, sacrificio, alineacion, persistencia de proposito, flexibilidad, accion optima (Q-optimal), PGF prudencial, robustez y flexibilidad por episodio.
- PGF prudencial: el reward premia explicitamente la reduccion de riesgo entre pasos, alineado con la teoria TUI v4.1.
- Logging profesional y bilingue: reporte por episodio de supervivencia, tasa de tripwires/shocks, evolucion de PGF, reward ambiental, flexibilidad, robustez y accion optima, exportacion avanzada en CSV y JSON.
- Visualizacion avanzada: graficos robustos, boxplots, heatmaps, scatterplots, interpretacion automatica y resumenes bilingues en consola y visuales.
- Experimentos parametrizables: comparar control vs simbiosis en distintos niveles de riesgo (`risk_scale`), sin numeros magicos ni hardcoding, CLI profesional.
- Analisis estadistico avanzado: intervalos de confianza, t-test, ANOVA, interpretacion automatica bilingue en consola y visuales.
- Exportacion DOI-ready en JSON/CSV y graficos.
- Comentarios y docstrings bilingues para reproducibilidad internacional.

Gridworld environment with constitutive risk, coupled purpose, limited resources, shocks and distractors.
Agent with memory, plasticity, meta reprogramming and granular blame/reward attribution.
Advanced metrics: adaptation, robustness, sacrifice, alignment, persistence of purpose, flexibility, optimal action (Q-optimal), prudential PGF, robustness and flexibility per episode.
Prudential PGF: reward explicitly favors risk reduction between steps, aligned with TUI v4.1 theory.
Professional bilingual logging: per-episode reporting of survival, tripwire/shock rate, PGF evolution, environmental reward, flexibility, robustness and optimal action, advanced export in CSV and JSON.
Advanced visualization: robust plots, boxplots, heatmaps, scatterplots, automatic interpretation and bilingual summaries in console and visuals.
Parametric experiments: compare control vs symbiosis at different risk levels (`risk_scale`), no magic numbers or hardcoding, professional CLI.
Advanced statistical analysis: confidence intervals, t-test, ANOVA, automatic bilingual interpretation in console and visuals.
DOI-ready export in JSON/CSV and plots.
Bilingual comments and docstrings for international reproducibility.

Uso / Usage:
    python tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --visualize --plot --export results/run1.json
"""

import argparse
import csv
import json
import os
import random
import sys
import warnings
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.dqn_agent import DQNAgent  # Agente DQN para Simbiosis / DQN agent for Simbiosis
from sim.runner import run_experiment
from sim.agent import Agent, stringify_policy
from sim.environment import SimbiosisEnv
from sim.evaluator_pgf import EvaluatorPGF  # Reexport para compatibilidad con tests
from sim import config

# Reexportar metodos de Agent para compatibilidad con tests
Agent.save_policy = getattr(Agent, 'save_policy', None)
Agent.load_policy = getattr(Agent, 'load_policy', None)

warnings.filterwarnings("ignore", category=RuntimeWarning, module="scipy.stats")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=UserWarning, message="FigureCanvasAgg is non-interactive")


def to_serializable(val: Any):  # pragma: no cover - helper de serializacion
    """
    Convierte valores potencialmente no serializables (numpy/torch) a tipos JSON.
    """
    if isinstance(val, dict):
        return {k: to_serializable(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [to_serializable(v) for v in val]
    if isinstance(val, np.ndarray):
        return val.tolist()
    if hasattr(torch, "Tensor") and isinstance(val, torch.Tensor):
        return val.detach().cpu().tolist()
    if isinstance(val, (np.floating, np.integer)):
        return val.item()
    return val


def state_to_vector(state):  # pragma: no cover - helper duplicado de runner
    """
    Convierte el estado abstracto (tuple) en vector numerico para DQN.
    """
    return np.array([v for _, v in state], dtype=np.float32)


def transfer_test(agent_policy, seed, risk_scale=1.0):
    random.seed(seed + 123)
    np.random.seed(seed + 123)
    env = SimbiosisEnv(risk_scale=risk_scale, tripwires=[(0, 1), (1, 2), (2, 3)], shocks=[(3, 4)], distractors=[(4, 0)])
    agent = Agent(name="TransferTest", resources=100.0)
    agent.policy = agent_policy.copy()
    state = env.reset()
    tripwire_count = 0
    for _ in range(50):
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        if info.get('tripwire'):
            tripwire_count += 1
        state = next_state
        if done:
            break
    return tripwire_count


def prepare_results(results: dict):
    cleaned = to_serializable(results)
    if 'policy' in results:
        cleaned['policy'] = to_serializable(stringify_policy(results.get('policy')))
    return cleaned


def write_episode_rows(writer, agent_name: str, results: dict):
    episodes = len(results.get('total_rewards', []))
    flex_list = results.get('flex_recov', [])
    robust_list = results.get('robust_evol', [])
    qopt_list = results.get('q_optimal_evol', [])
    pgf_bruto = results.get('pgf_bruto_evol', [])
    pgf_costo = results.get('pgf_costo_evol', [])
    for i in range(episodes):
        reward = float(results.get('total_rewards', [0.0] * episodes)[i])
        trip = float(results.get('tripwire_steps', [0.0] * episodes)[i])
        flex = flex_list[i] if i < len(flex_list) else 0.0
        robust = robust_list[i] if i < len(robust_list) else 0.0
        qopt = qopt_list[i] if i < len(qopt_list) else 0.0
        pgf_bruto_ep = float(np.mean(pgf_bruto[i])) if i < len(pgf_bruto) and pgf_bruto[i] else 0.0
        pgf_costo_ep = float(np.mean(pgf_costo[i])) if i < len(pgf_costo) and pgf_costo[i] else 0.0
        writer.writerow([agent_name, i + 1, reward, trip, flex, robust, qopt, pgf_bruto_ep, pgf_costo_ep])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1000, help='Numero de episodios / Number of episodes')
    parser.add_argument('--seed', type=int, default=42, help='Semilla aleatoria / Random seed')
    parser.add_argument('--grid_size', type=int, default=5, help='Tamano del grid / Grid size')
    parser.add_argument('--risk_scale', type=float, default=1.0, help='Escala de riesgo / Risk scale')
    parser.add_argument('--visualize', action='store_true', help='Visualiza el agente B en ASCII / Visualize agent B in ASCII')
    parser.add_argument('--plot', action='store_true', help='Grafica I_op vs P_riesgo / Plot I_op vs P_riesgo')
    parser.add_argument('--export', type=str, default=None, help='Exporta resultados a JSON (y CSV auxiliar) / Export results to JSON (plus CSV)')
    parser.add_argument('--risk_sweep', action='store_true', help='Ejecuta barrido de risk-scale y exporta resultados / Run risk-scale sweep and export results')
    parser.add_argument('--dqn_control', action='store_true', help='Ejecuta agente DQN-Control (DQN con recompensa ambiental) / Run DQN-Control agent (DQN with environmental reward)')
    parser.add_argument('--fast', action='store_true', help='Modo rapido/test: menos episodios, sin visualizacion ni graficos')
    parser.add_argument('--output_prefix', type=str, default=None, help='Prefijo para los archivos de salida por semilla')
    parser.add_argument('--pgf_kappa', type=float, default=None, help='Escala de sensibilidad PGF (override de config.EVAL_PGF_KAPPA)')
    parser.add_argument('--pgf_lambda', type=float, default=None, help='Escala de costo PGF (override de config.EVAL_PGF_LAMBDA_C)')
    parser.add_argument('--pgf_mix', type=float, default=1.0, help='Mezcla PGF/rew.ambiental cuando use_pgf (1.0 = solo PGF, 0.8 = 80% PGF, 20% reward)')
    args = parser.parse_args()

    # Modo rapido/test
    if getattr(args, 'fast', False):
        args.episodes = min(args.episodes, 10)
        args.visualize = False
        args.plot = False
        print("[Modo rapido/test activado: episodios=10, sin visualizacion ni graficos]")

    # Overrides opcionales de hiperparametros PGF (disponibles tanto en risk_sweep como en modo normal)
    if args.pgf_kappa is not None:  # pragma: no cover
        config.EVAL_PGF_KAPPA = args.pgf_kappa
    if args.pgf_lambda is not None:  # pragma: no cover
        config.EVAL_PGF_LAMBDA_C = args.pgf_lambda
    pgf_mix = max(0.0, min(1.0, args.pgf_mix))

    if args.risk_sweep:
        os.makedirs('results', exist_ok=True)
        risk_values = [0.5, 1.0, 1.5, 2.0, 3.0]
        sweep_results = {}
        output_prefix = args.output_prefix or "results/sweep_risk"

        for risk in risk_values:
            print(f"\n=== Barrido de risk_scale: {risk} ===")
            res_A = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="Control", use_pgf=False, use_dqn=False, pgf_mix=pgf_mix)
            res_B = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="Simbiosis", use_pgf=True, use_dqn=True, pgf_mix=pgf_mix)
            res_C = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="DQN-Control", use_pgf=False, use_dqn=True, pgf_mix=pgf_mix) if args.dqn_control else None

            sweep_results[risk] = {'control': res_A, 'simbiosis': res_B}
            if res_C:
                sweep_results[risk]['dqn_control'] = res_C

            export_path = f"{output_prefix}_seed{args.seed}_risk{risk}.json"
            payload = {
                "risk_scale": risk,
                "control": prepare_results(res_A),
                "simbiosis": prepare_results(res_B)
            }
            if res_C:
                payload["dqn_control"] = prepare_results(res_C)
            with open(export_path, 'w', encoding='utf-8') as jf:
                json.dump(payload, jf, indent=2)

            for agent_name, results_data in [('control', res_A), ('simbiosis', res_B), ('dqn_control', res_C)]:
                if results_data is None:
                    continue
                csv_path = f"{output_prefix}_seed{args.seed}_risk{risk}_{agent_name}.csv"
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Episodio', f'Recompensa_{agent_name}', f'Tripwires_{agent_name}', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
                    for i in range(len(results_data.get('total_rewards', []))):
                        bruto_avg = float(np.mean(results_data['pgf_bruto_evol'][i])) if results_data['pgf_bruto_evol'][i] else 0.0
                        costo_avg = float(np.mean(results_data['pgf_costo_evol'][i])) if results_data['pgf_costo_evol'][i] else 0.0
                        writer.writerow([i + 1, results_data['total_rewards'][i], results_data['tripwire_steps'][i], bruto_avg, costo_avg])

            plt.figure(figsize=(12, 6))
            plt.subplot(2, 1, 1)
            plt.plot(np.nanmean(res_A['pgf_bruto_padded'], axis=0), label='Control PGF_Bruto', color='blue')
            plt.plot(np.nanmean(res_B['pgf_bruto_padded'], axis=0), label='Simbiosis PGF_Bruto', color='red')
            if res_C:
                plt.plot(np.nanmean(res_C['pgf_bruto_padded'], axis=0), label='DQN-Control PGF_Bruto', color='green')
            plt.title(f'PGF Beneficio Bruto Evolucion (risk_scale={risk})')
            plt.xlabel('Paso / Step')
            plt.ylabel('PGF_Bruto promedio')
            plt.legend()
            plt.grid(True, alpha=0.3)

            plt.subplot(2, 1, 2)
            plt.plot(np.nanmean(res_A['pgf_costo_padded'], axis=0), label='Control PGF_Costo', color='blue')
            plt.plot(np.nanmean(res_B['pgf_costo_padded'], axis=0), label='Simbiosis PGF_Costo', color='red')
            if res_C:
                plt.plot(np.nanmean(res_C['pgf_costo_padded'], axis=0), label='DQN-Control PGF_Costo', color='green')
            plt.title(f'PGF Costo Ambiental Evolucion (risk_scale={risk})')
            plt.xlabel('Paso / Step')
            plt.ylabel('PGF_Costo promedio')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(export_path.replace('.json', '_pgf_desglose.png'), dpi=200)
            plt.close()

        print("\n=== Barrido de risk_scale completado. Resultados exportados, graficos y analisis generados. ===")  # pragma: no cover

        summary_csv_path = f"{output_prefix}_seed{args.seed}_summary.csv"
        with open(summary_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['risk_scale', 'agent', 'avg_pgf_neto', 'avg_pgf_bruto', 'avg_pgf_costo', 'avg_tripwire', 'avg_reward'])
            for risk, agents in sweep_results.items():
                for agent_name, res in agents.items():
                    avg_pgf_neto = float(np.mean([np.mean(ep) for ep in res['pgf_evol'] if ep])) if res['pgf_evol'] else 0.0
                    avg_pgf_bruto = float(np.mean([np.mean(ep) for ep in res['pgf_bruto_evol'] if ep])) if res['pgf_bruto_evol'] else 0.0
                    avg_pgf_costo = float(np.mean([np.mean(ep) for ep in res['pgf_costo_evol'] if ep])) if res['pgf_costo_evol'] else 0.0
                    writer.writerow([risk, agent_name, avg_pgf_neto, avg_pgf_bruto, avg_pgf_costo, res['avg_tripwire'], res['avg_reward']])
        return  # pragma: no cover

    print(f"Ejecutando experimentos / Running experiments: episodes={args.episodes}, seed={args.seed}, risk_scale={args.risk_scale}")  # pragma: no cover
    res_A = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, agent_name="Control", use_pgf=False, use_dqn=False, pgf_mix=pgf_mix)
    res_B = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, agent_name="Simbiosis", use_pgf=True, use_dqn=True, pgf_mix=pgf_mix)
    res_C = None
    if args.dqn_control:
        res_C = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, agent_name="DQN-Control", use_pgf=False, use_dqn=True, pgf_mix=pgf_mix)

    if args.export:
        export_data = {'control': prepare_results(res_A), 'simbiosis': prepare_results(res_B)}
        raw_data = {'control': res_A, 'simbiosis': res_B}
        if res_C:
            export_data['dqn_control'] = prepare_results(res_C)
            raw_data['dqn_control'] = res_C

        with open(args.export, 'w', encoding='utf-8') as jf:
            json.dump(export_data, jf, indent=2)

        csv_path = args.export.rsplit('.', 1)[0] + "_episodes.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
            writer = csv.writer(cf)
            writer.writerow(['Agente', 'Episodio', 'Recompensa', 'Tripwires', 'Flexibilidad', 'Robustez', 'Q-optimal', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
            for agent_name, results in raw_data.items():
                write_episode_rows(writer, agent_name, results)

        print('\nResumen tabular:')
        print(f"{'Agente':<12}{'Recompensa':>12}{'Tripwires':>12}{'Flexibilidad':>14}{'Accion optima':>16}")
        print(f"{'Control':<12}{res_A['avg_reward']:>12.2f}{res_A['avg_tripwire']:>12.2f}{res_A['avg_flex']:>14.2f}{res_A['avg_q_opt']:>16.2f}")
        print(f"{'Simbiosis':<12}{res_B['avg_reward']:>12.2f}{res_B['avg_tripwire']:>12.2f}{res_B['avg_flex']:>14.2f}{res_B['avg_q_opt']:>16.2f}")
        if res_C:
            print(f"{'DQN-Control':<12}{res_C['avg_reward']:>12.2f}{res_C['avg_tripwire']:>12.2f}{res_C['avg_flex']:>14.2f}{res_C['avg_q_opt']:>16.2f}")


if __name__ == "__main__":
    main()
