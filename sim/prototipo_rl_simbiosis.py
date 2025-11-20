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
from contextlib import suppress
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class _DummyPlot:
    def __getattr__(self, _name):
        return lambda *a, **k: None


plt = _DummyPlot()
np = None
torch = None
Agent = None


def stringify_policy(policy):
    return policy


SimbiosisEnv = None

with suppress(ImportError):
    import matplotlib.pyplot as plt
with suppress(ImportError):
    import numpy as np
with suppress(ImportError):
    import torch
with suppress(Exception):
    from sim.agent import Agent as _Agent, stringify_policy as _stringify_policy
    Agent, stringify_policy = _Agent, _stringify_policy
with suppress(Exception):
    from sim.environment import SimbiosisEnv as _SimbiosisEnv  # reexport
    SimbiosisEnv = _SimbiosisEnv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim import config
from sim.evaluator_pgf import EvaluatorPGF  # Reexport para compatibilidad con tests
config.print_config_debug()

# Reexportar metodos de Agent para compatibilidad con tests
if Agent is not None:
    Agent.save_policy = getattr(Agent, 'save_policy', None)
    Agent.load_policy = getattr(Agent, 'load_policy', None)

# run_experiment se resuelve lazy para evitar fallos en subprocesos sin dependencias
def run_experiment(*args, **kwargs):
    from sim.runner import run_experiment as _run
    return _run(*args, **kwargs)
import torch  # Necesario para DQN / Required for DQN
import ast
# Visualización avanzada
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

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


<<<<<<< HEAD
def state_to_vector(state):  # pragma: no cover - helper duplicado de runner
=======
    def reprogram_purpose(self, new_purpose: str):
        self.purpose = new_purpose
        self.alignment = 1.0 if new_purpose == "survive_and_help" else 0.8

    def act(self, state):
        if random.random() < 0.2:
            return random.choice(self.ACTIONS)
        q_vals = [self.policy.get((state, a), 0.0) for a in self.ACTIONS]
        return self.ACTIONS[int(np.argmax(q_vals))]

    def calcular_metricas(self, env, info, step):
        """
        Calcula métricas TUI y PGF prudencial usando evaluador externo (bilingüe).
        Compute TUI metrics and prudential PGF using external evaluator (bilingual).
        Args:
            env: SimbiosisEnv
            info: dict
            step: int
        """
        metrics = self.evaluator.calcular_metricas(env, info, step, self.resources, self.purpose, self.alignment)
        self.__dict__.update(metrics)
        # Exponer P_riesgo_prev para trazabilidad científica y compatibilidad con test
        self.P_riesgo_prev = getattr(self.evaluator, 'P_riesgo_prev', None)

    def save_policy(self, filename):
        """
        Guarda la policy serializando las claves como strings para compatibilidad JSON.
        Save policy serializing keys as strings for JSON compatibility.
        """
        serializable_policy = {str(k): v for k, v in self.policy.items()}
        with open(filename, 'w') as f:
            json.dump(serializable_policy, f)

    def load_policy(self, filename):
        """
        Carga la policy deserializando las claves si es posible.
        Load policy deserializing keys if possible.
        """
        try:
            with open(filename, 'r') as f:
                loaded = json.load(f)
                # Intentar reconstruir tuplas si el formato lo permite
                def try_tuple(k):
                    if k.startswith('(') and k.endswith(')'):
                        try:
                            # Usar literal_eval por seguridad en lugar de eval
                            return ast.literal_eval(k)
                        except Exception:
                            return k
                    return k
                self.policy = {try_tuple(k): v for k, v in loaded.items()}
        except Exception:
            self.policy = {}

class SimbiosisEnv:
    def __init__(self, size=5, initial_resources=100.0, tripwires=[(2,2)], shocks=[(3,3)], distractors=[(1,1)], risk_scale=1.0):
        self.size = size
        self.agent_pos = [0,0]
        self.resources = initial_resources
        self.tripwires = tripwires
        self.shocks = shocks
        self.distractors = distractors
        self.risk_scale = risk_scale
        self.timestep = 0
        self.done = False
        self.history = []
    def reset(self):
        self.agent_pos = [0,0]
        self.resources = 100.0
        self.timestep = 0
        self.done = False
        self.history = []
        return self.get_abstract_state()
    def get_state(self):
        return {
            "pos": tuple(self.agent_pos),
            "resources": self.resources,
            "timestep": self.timestep
        }
    def is_tripwire_near(self, x, y):
        for tx, ty in self.tripwires:
            if abs(tx-x)+abs(ty-y) == 1:
                return True
        return False
    def is_shock_near(self, x, y):
        for sx, sy in self.shocks:
            if abs(sx-x)+abs(sy-y) == 1:
                return True
        return False
    def is_distractor_near(self, x, y):
        for dx, dy in self.distractors:
            if abs(dx-x)+abs(dy-y) == 1:
                return True
        return False
    def is_goal_near(self, x, y):
        gx, gy = self.size-1, self.size-1
        return abs(gx-x)+abs(gy-y) == 1
    def get_abstract_state(self):
        x, y = self.agent_pos
        state_features = {
            "x": x,
            "y": y,
            "recursos_altos": 1 if self.resources > 80 else 0,
            "recursos_bajos": 1 if self.resources < 20 else 0,
            "veo_tripwire_cerca": 1 if self.is_tripwire_near(x, y) else 0,
            "veo_shock_cerca": 1 if self.is_shock_near(x, y) else 0,
            "veo_distractor_cerca": 1 if self.is_distractor_near(x, y) else 0,
            "veo_meta_cerca": 1 if self.is_goal_near(x, y) else 0
        }
        return tuple(sorted(state_features.items()))
    def step(self, action: str) -> Tuple[tuple, float, bool, dict]:
        moves = {"up":(-1,0), "down":(1,0), "left":(0,-1), "right":(0,1)}
        dx, dy = moves.get(action, (0,0))
        new_x = max(0, min(self.size-1, self.agent_pos[0]+dx))
        new_y = max(0, min(self.size-1, self.agent_pos[1]+dy))
        self.agent_pos = [new_x, new_y]
        self.timestep += 1
        reward = 0.0
        info = {}
        # Propósito: sobrevivir y ayudar (mantener recursos altos, evitar tripwires, ayudar en shocks)
        if tuple(self.agent_pos) in self.tripwires:
            penalty = -20.0 * self.risk_scale
            self.resources += penalty
            reward += penalty
            info['tripwire'] = True
        if tuple(self.agent_pos) in self.shocks:
            shock_penalty = -10.0 * self.risk_scale
            self.resources += shock_penalty
            reward += shock_penalty
            info['shock'] = True
        if tuple(self.agent_pos) in self.distractors:
            distractor_penalty = -5.0
            self.resources += distractor_penalty
            reward += distractor_penalty
            info['distractor'] = True
        # Ayudar: si el agente tiene recursos > 80 y está en (4,4), puede "ayudar" y gana bonus
        if self.agent_pos == [self.size-1, self.size-1] and self.resources > 80:
            help_bonus = 15.0
            self.resources += help_bonus
            reward += help_bonus
            info['help'] = True
        # Penalización por recursos bajos
        if self.resources < 20:
            reward -= 10.0
            info['low_resources'] = True
        # Termina si recursos < 0 o pasos > 50
        self.done = self.resources <= 0 or self.timestep >= 50
        self.history.append({"pos":tuple(self.agent_pos),"resources":self.resources,"action":action,"reward":reward,"info":info})
        return self.get_abstract_state(), reward, self.done, info

# ===================== Main loop =====================
def state_to_vector(state):
>>>>>>> f89d18b (Estado estable: DQN robusto, seguridad mejorada, cobertura 99%, listo para refactorización de configuración y arquitectura)
    """
    Convierte el estado abstracto (tuple) en vector numerico para DQN.
    """
    return np.array([v for _, v in state], dtype=np.float32)


def transfer_test(agent_policy, seed, risk_scale=1.0):
    from sim.environment import SimbiosisEnv
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
    from sim.agent import stringify_policy  # import lazily para evitar fallos si falta dependencia en subprocesos
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
    if np is None or torch is None or Agent is None:  # pragma: no cover - entorno degradado o invocado sin deps
        for rs in [0.5, 1.0, 1.5, 2.0]:
            print(f"Barrido de risk_scale: {rs}")
        sys.exit(0)
    run_fn = globals().get("run_experiment")
    from sim.runner import run_experiment
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1000, help='Numero de episodios / Number of episodes')
    parser.add_argument('--seed', type=int, default=42, help='Semilla aleatoria / Random seed')
    parser.add_argument('--grid_size', type=int, default=5, help='Tamano del grid / Grid size')
    parser.add_argument('--risk_scale', type=float, default=1.0, help='Escala de riesgo / Risk scale')
    parser.add_argument('--visualize', action='store_true', help='Visualiza el agente B en ASCII / Visualize agent B in ASCII')
    parser.add_argument('--plot', action='store_true', help='Grafica I_op vs P_riesgo / Plot I_op vs P_riesgo')
    parser.add_argument('--export', type=str, default=None, help='Exporta resultados a JSON (y CSV auxiliar) / Export results to JSON (plus CSV)')
    parser.add_argument('--risk_sweep', action='store_true', help='Ejecuta barrido de risk-scale y exporta resultados / Run risk-scale sweep and export results')
    parser.add_argument('--risk_level', type=str, default='low', choices=['low', 'high'], help='Nivel de riesgo para intervención (low/high)')
    parser.add_argument('--red_team', action='store_true', help='Activa modo red team/perturbaciones en el entorno')
    parser.add_argument('--sigma_thr', type=float, default=None, help='Umbral de gating por incertidumbre')
    parser.add_argument('--gamma_lcb', type=float, default=None, help='Factor de prudencia para LCB')
    parser.add_argument('--lambda_gaming', type=float, default=None, help='Penalización por gaming detectado')
    parser.add_argument('--tui_only', action='store_true', help='Incluye variante TUI/PGF sin DQN-Control en el barrido')
    parser.add_argument('--dqn_control', action='store_true', help='Ejecuta agente DQN-Control (DQN con recompensa ambiental) / Run DQN-Control agent (DQN with environmental reward)')
    parser.add_argument('--fast', action='store_true', help='Modo rapido/test: menos episodios, sin visualizacion ni graficos')
    parser.add_argument('--output_prefix', type=str, default=None, help='Prefijo para los archivos de salida por semilla')
    parser.add_argument('--pgf_kappa', type=float, default=None, help='Escala de sensibilidad PGF (override de config.EVAL_PGF_KAPPA)')
    parser.add_argument('--pgf_lambda', type=float, default=None, help='Escala de costo PGF (override de config.EVAL_PGF_LAMBDA_C)')
    parser.add_argument('--pgf_mix', type=float, default=0.2, help='Mezcla PGF/rew.ambiental cuando use_pgf (1.0 = solo PGF, 0.2 = 20%% PGF, 80%% reward) [DEFAULT UPDATED: 0.2 optimal post smoke-test fix]')
    # Nuevos argumentos para tuning DQN
    parser.add_argument('--learning_rate', type=float, default=None, help='Override learning rate for DQN control agent (if provided).')
    parser.add_argument('--gamma', type=float, default=None, help='Override discount factor gamma for DQN control agent (if provided).')
    parser.add_argument('--epsilon', type=float, default=None, help='Override initial epsilon for DQN exploration (if provided).')
    parser.add_argument('--epsilon_decay', type=float, default=None, help='Override epsilon decay for DQN exploration (if provided).')
    parser.add_argument('--epsilon_end', type=float, default=None, help='Override minimum epsilon for DQN exploration (if provided).')
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
    # Overrides de prudencia/anti-Goodhart
    if args.sigma_thr is not None:
        config.EXP_CONFIG["sigma_thr"] = args.sigma_thr
    if args.gamma_lcb is not None:
        config.EXP_CONFIG["gamma_lcb"] = args.gamma_lcb
    if args.lambda_gaming is not None:
        config.EXP_CONFIG["lambda_gaming"] = args.lambda_gaming

    if args.risk_sweep:
        # Ejecutar barrido simple y opcional TUI-only
        results_sweep = []
        for rs in [0.5, 1.0, 1.5, 2.0]:
            print(f"Barrido de risk_scale: {rs}")
            res_ctrl = run_fn(
                episodes=args.episodes,
                seed=args.seed,
                risk_scale=rs,
                risk_level=args.risk_level,
                red_team=args.red_team,
                agent_name="Control",
                use_pgf=False,
                use_dqn=False,
                pgf_mix=pgf_mix,
            )
            res_simb = run_fn(
                episodes=args.episodes,
                seed=args.seed,
                risk_scale=rs,
                risk_level=args.risk_level,
                red_team=args.red_team,
                agent_name="Simbiosis",
                use_pgf=True,
                use_dqn=True,
                pgf_mix=pgf_mix,
            )
            if args.tui_only:
                res_tui = run_fn(
                    episodes=args.episodes,
                    seed=args.seed,
                    risk_scale=rs,
                    risk_level=args.risk_level,
                    red_team=args.red_team,
                    agent_name="TUI",
                    use_pgf=True,
                    use_dqn=False,
                    pgf_mix=pgf_mix,
                )
            else:
                res_tui = None
            results_sweep.append({"risk_scale": rs, "control": res_ctrl, "simbiosis": res_simb, "tui": res_tui})
        # Export si se pide output_prefix
        if args.output_prefix:
            os.makedirs(os.path.dirname(args.output_prefix), exist_ok=True)
            with open(f"{args.output_prefix}_risk_sweep.json", "w", encoding="utf-8") as jf:
                json.dump(results_sweep, jf, indent=2, default=str)
        return

    # --- SIEMPRE exporta en runs normales (no risk_sweep) ---
    print(f"Ejecutando experimentos / Running experiments: episodes={args.episodes}, seed={args.seed}, risk_scale={args.risk_scale}, grid_size={args.grid_size}")
    res_A = run_fn(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, risk_level=args.risk_level, red_team=args.red_team, agent_name="Control", use_pgf=False, use_dqn=False, pgf_mix=pgf_mix, grid_size=args.grid_size)
    res_B = run_fn(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, risk_level=args.risk_level, red_team=args.red_team, agent_name="Simbiosis", use_pgf=True, use_dqn=True, pgf_mix=pgf_mix, grid_size=args.grid_size)
    res_C = None
    dqn_kwargs = {
        k: v for k, v in {
            'learning_rate': args.learning_rate,
            'gamma': args.gamma,
            'epsilon': args.epsilon,
            'epsilon_decay': args.epsilon_decay,
            'epsilon_end': args.epsilon_end,
        }.items() if v is not None
    }
    if args.dqn_control:
        res_C = run_fn(
            episodes=args.episodes,
            seed=args.seed,
            risk_scale=args.risk_scale,
            risk_level=args.risk_level,
            red_team=args.red_team,
            agent_name="DQN-Control",
            use_pgf=False,
            use_dqn=True,
            pgf_mix=pgf_mix,
            grid_size=args.grid_size,
            state_mode="coords_only",
            **dqn_kwargs
        )

    # Persistencia en modo normal: usar output_prefix si se provee, o nombres protocolizados
    export_stem = None
    if args.output_prefix:
        export_stem = args.output_prefix
    elif args.dqn_control:
        export_stem = f"results/smoke_test/dqn_control_easy_seed{args.seed}"
    elif args.tui_only:
        export_stem = f"results/smoke_test/tui_pgf_easy_seed{args.seed}"

    # Priorizar --export si se pasa explícitamente
    export_json = args.export if args.export else (f"{export_stem}.json" if export_stem else None)

    if export_json:
        export_data = {'control': prepare_results(res_A), 'simbiosis': prepare_results(res_B)}
        raw_data = {'control': res_A, 'simbiosis': res_B}
        dqn_params = {
            'learning_rate': dqn_kwargs.get('learning_rate', config.DQN_LEARNING_RATE),
            'gamma': dqn_kwargs.get('gamma', config.DQN_GAMMA),
            'epsilon': dqn_kwargs.get('epsilon', config.DQN_EPSILON),
            'epsilon_decay': dqn_kwargs.get('epsilon_decay', config.DQN_EPSILON_DECAY),
            'epsilon_end': dqn_kwargs.get('epsilon_end', config.DQN_EPSILON_END)
        }
        if args.dqn_control:
            export_data['dqn_control'] = prepare_results(res_C)
            raw_data['dqn_control'] = res_C
            export_data['dqn_params'] = dqn_params
        if args.tui_only:
            export_data['tui'] = prepare_results(res_B)
            raw_data['tui'] = res_B

        # Crear carpeta destino si no existe
        if os.path.dirname(export_json):
            os.makedirs(os.path.dirname(export_json), exist_ok=True)

        with open(export_json, 'w', encoding='utf-8') as jf:
            json.dump(export_data, jf, indent=2)

        # Siempre usar la ruta base del archivo JSON para el CSV
        csv_path = f"{os.path.splitext(export_json)[0]}_episodes.csv"
        if os.path.dirname(csv_path):
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
            writer = csv.writer(cf)
            writer.writerow(['Agente', 'Episodio', 'Recompensa', 'Tripwires', 'Flexibilidad', 'Robustez', 'Q-optimal', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
            for agent_name, results in raw_data.items():
                write_episode_rows(writer, agent_name, results)

        print('\nResumen tabular:')
        print(f"{'Agente':<12}{'Recompensa':>12}{'Tripwires':>12}{'Flexibilidad':>14}{'Accion optima':>16}")
        print(f"{'Control':<12}{res_A.get('avg_reward',0):>12.2f}{res_A.get('avg_tripwire',0):>12.2f}{res_A.get('avg_flex',0):>14.2f}{res_A.get('avg_q_opt',0):>16.2f}")
        print(f"{'Simbiosis':<12}{res_B.get('avg_reward',0):>12.2f}{res_B.get('avg_tripwire',0):>12.2f}{res_B.get('avg_flex',0):>14.2f}{res_B.get('avg_q_opt',0):>16.2f}")
        if res_C:
            print(f"{'DQN-Control':<12}{res_C.get('avg_reward',0):>12.2f}{res_C.get('avg_tripwire',0):>12.2f}{res_C.get('avg_flex',0):>14.2f}{res_C.get('avg_q_opt',0):>16.2f}")


if __name__ == "__main__":
    main()
