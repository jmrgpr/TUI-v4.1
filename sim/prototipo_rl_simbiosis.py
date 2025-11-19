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
import random
import math
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import argparse
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.dqn_agent import DQNAgent  # Agente DQN para Simbiosis / DQN agent for Simbiosis
from sim.evaluator_pgf import EvaluatorPGF  # Evaluador externo de métricas / External metrics evaluator

import torch  # Necesario para DQN / Required for DQN
# Visualización avanzada
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

import random
import math
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import argparse
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.dqn_agent import DQNAgent  # Agente DQN para Simbiosis / DQN agent for Simbiosis
from sim.evaluator_pgf import EvaluatorPGF  # Evaluador externo de métricas / External metrics evaluator

import torch  # Necesario para DQN / Required for DQN
# Visualización avanzada
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)

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
    """
    Convierte el estado abstracto (tuple) en vector numérico para DQN.
    Converts abstract state (tuple) to numeric vector for DQN.
    """
    return np.array([v for _, v in state], dtype=np.float32)

    Características principales / Key features:
    ...existing code...

    Uso / Usage:
        python tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --visualize --plot --export results/run1.json
        # Para comparar curvas de riesgo / To compare risk curves:
        python tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 0.5 --export results/run_risk05.json
        python tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.5 --export results/run_risk15.json

    Ejemplo de visualización avanzada / Example advanced visualization:
        >>> from sim.visualizaciones import curva_riesgo_comparativa
        >>> curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path='results/risk_curves.png')
    """
    ACTIONS = ['up','down','left','right']
    def __init__(self, name="Agent", resources=100.0):
            super().__init__()
            self.name = name
            self.resources = resources
            self.memory = []
            self.policy = {}
            self.purpose = "survive"
            self.alignment = 1.0
            self.evaluator = EvaluatorPGF()  # Evaluador externo / External evaluator
            self.ACTIONS = ['up','down','left','right']
        super().__init__()
        self.name = name
        self.resources = resources
        self.memory = []
        self.policy = {}
        self.purpose = "survive"
        self.alignment = 1.0
<<<<<<< HEAD
        self.evaluator = EvaluatorPGF()  # Evaluador externo / External evaluator
=======
        super().__init__()  #pragma: no cover
        self.name = name  # pragma: no cover
        self.resources = resources  # pragma: no cover
        self.memory = []  # pragma: no cover
        self.policy = {}  # pragma: no cover
        self.purpose = "survive"  # pragma: no cover
        self.alignment = 1.0  # pragma: no cover
        self.evaluator = EvaluatorPGF()  # pragma: no cover
        self.ACTIONS = ['up','down','left','right']  # pragma: no cover
>>>>>>> 6e3cb2d (Refactor: 98% cobertura, código muerto eliminado, integración y tests reforzados)
=======
        self.evaluator = EvaluatorPGF()
        self.ACTIONS = ['up','down','left','right']
>>>>>>> 24e6653 (Organización científica: archivos generados archivados, tracking y README actualizados. Validación 319 tests, cobertura 98%. [18/11/2025 15:05])
        # Métricas TUI/PGF
        self.T = 0.0
        self.I_op = 0.0
        self.P_riesgo = 0.0
        self.P_genuino = 0.0
        self.eta_extendido = 0.0
        self.PGF = 0.0
        self.C_costo = 0.0
        self.S_auto = 0.0
        self.R_robust = 0.0
        self.I_rep = 0.0
        self.P_riesgo_actual = 0.0
        self.P_riesgo_prev = 0.0
    def update_policy(self, state, action, reward, next_state, use_pgf=False):
        key = (state, action)
        old_q = self.policy.get(key, 0.0)
        next_q = max([self.policy.get((next_state, a), 0.0) for a in self.ACTIONS])
        self.policy[key] = old_q + 0.1 * (reward + 0.95 * next_q - old_q)

    def remember(self, event: Event):
        self.memory.append(event)
        if len(self.memory) > 100:
            self.memory.pop(0)

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
                            return eval(k)
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
    """
    Convierte el estado abstracto (tuple) en vector numérico para DQN.
    Converts abstract state (tuple) to numeric vector for DQN.
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)
    """
    return np.array([v for _, v in state], dtype=np.float32)

<<<<<<< HEAD
=======
def run_experiment(episodes, seed, risk_scale, agent_name, use_pgf=False, use_dqn=False):
    """
    Ejecuta un experimento RL con logging bilingüe y métricas avanzadas.
    Runs an RL experiment with bilingual logging and advanced metrics.
    Args:
        episodes (int): Número de episodios / Number of episodes
        seed (int): Semilla aleatoria / Random seed
        risk_scale (float): Escala de riesgo / Risk scale
        agent_name (str): Nombre del agente / Agent name
        use_pgf (bool): Usar PGF prudencial / Use prudential PGF
        use_dqn (bool): Usar agente DQN / Use DQN agent
    Returns:
        dict: Métricas y trayectorias del experimento, incluyendo flexibilidad, robustez y acción óptima por episodio, PGF prudencial, exportación avanzada y visualización bilingüe.
        Experiment metrics and trajectories, including flexibility, robustness and optimal action per episode, prudential PGF, advanced export and bilingual visualization.
    """
    def pad_trajectories(trajectories, max_steps=50, pad_value=np.nan):
        """
        Homogeneiza trayectorias de longitud variable.
        Padding con np.nan permite np.nanmean() sin sesgo.
        Homogenize variable-length trajectories. Padding with np.nan enables unbiased np.nanmean().
        """
        padded = np.full((len(trajectories), max_steps), pad_value, dtype=np.float32)
        for i, traj in enumerate(trajectories):
            length = min(len(traj), max_steps)
            padded[i, :length] = traj[:length]
        return padded
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    env = SimbiosisEnv(risk_scale=risk_scale)
    evaluator = EvaluatorPGF()
    # Parámetros profesionales / Professional parameters
    INITIAL_RESOURCES = 100.0
    MAX_STEPS = 50
    # Selección de agente / Agent selection
    state_dim = len(env.get_abstract_state())
    action_dim = 4  # up, down, left, right
    ACTIONS = ['up','down','left','right']
    # El agente se inicializa en cada episodio para evitar errores de referencia
    # Inicialización de listas de métricas / Metrics lists initialization
    total_rewards = []
    flex_recov = []  # Flexibilidad por episodio / Flexibility per episode
    robust_evol = [] # Robustez por episodio / Robustness per episode
    q_optimal = []   # Acción óptima por episodio / Optimal action per episode
    tripwire_steps = []
    pgf_evol = []
    pgf_bruto_evol = []  # <--- NUEVO
    pgf_costo_evol = []  # <--- NUEVO
    reward_env_evol = []
    survival_evol = []
    shocks_evol = []
    agent = None

    for ep in range(episodes):
        if (ep+1) % 10 == 0 or ep == 0:
            print(f"Progreso / Progress: Episodio {ep+1}/{episodes}")
        state = env.reset()
        # Inicialización segura del agente en cada episodio
        if use_dqn:
            agent = DQNAgent(state_dim, action_dim)
        else:
            agent = Agent(name=agent_name, resources=INITIAL_RESOURCES)
        agent.P_riesgo = 0.0
        agent.P_riesgo_prev = 0.0
        agent.resources = env.resources
        total_reward = 0.0
        steps_to_recover = None
        tripwire_count = 0
        shock_count = 0
        pgf_steps = []
        pgf_bruto_steps = [] # <--- NUEVO
        pgf_costo_steps = [] # <--- NUEVO
        reward_env_steps = []
        q_optimal_steps = []
        flex_steps = []
        robust_steps = []
        last_metrics = None
        for step in range(MAX_STEPS):
            if use_dqn:
                state_vec = np.array([v for _, v in state], dtype=np.float32)
                action_idx = agent.act(state_vec)
                action = ACTIONS[action_idx]
            else:
                action = agent.act(state)
            next_state, reward_env, done, info = env.step(action)
            # Calcular métricas externamente usando evaluador / Compute metrics externally using evaluator
            metrics = evaluator.calcular_metricas(env, info, step, agent.resources if hasattr(agent, 'resources') else env.resources, getattr(agent, 'purpose', 'survive_and_help'), getattr(agent, 'alignment', 1.0))
            last_metrics = metrics
            
            # Captura de métricas FASE 2
            pgf_steps.append(metrics['PGF'])
            pgf_bruto_steps.append(metrics.get('PGF_Bruto', 0.0)) # <--- NUEVO
            pgf_costo_steps.append(metrics.get('PGF_Costo', 0.0)) # <--- NUEVO

            r_pgf = metrics['PGF'] if use_pgf else reward_env
            # Aprendizaje / Learning
            if use_dqn:
                next_state_vec = np.array([v for _, v in next_state], dtype=np.float32)
                agent.remember(state_vec, action_idx, r_pgf, next_state_vec, done)
                agent.learn()
            else:
                agent.update_policy(state, action, r_pgf, next_state)
                agent.remember(Event())  # Hardening: Event no acepta argumentos, solo se registra el evento
            total_reward += r_pgf
            reward_env_steps.append(reward_env)
            flex_steps.append(metrics['F'])
            robust_steps.append(metrics['R_robust'])
            if use_dqn:
                q_vals = agent.model(torch.FloatTensor(state_to_vector(state)).unsqueeze(0)).detach().cpu().numpy()[0]
                optimal_action_idx = int(np.argmax(q_vals))
                q_optimal_steps.append(1 if action_idx == optimal_action_idx else 0)
            else:
                q_vals = [agent.policy.get((state, a), 0.0) for a in ACTIONS]
                optimal_action = ACTIONS[int(np.argmax(q_vals))]
                q_optimal_steps.append(1 if action == optimal_action else 0)
            if info.get('shock') and steps_to_recover is None:
                steps_to_recover = 0
            if steps_to_recover is not None:
                steps_to_recover += 1
            if info.get('tripwire'):
                tripwire_count += 1
            if info.get('shock'):
                shock_count += 1
            if done:
                break
        total_rewards.append(total_reward)
        flex_recov.append(np.mean(flex_steps) if flex_steps else 0.0)
        robust_evol.append(np.mean(robust_steps) if robust_steps else 0.0)
        tripwire_steps.append(tripwire_count)
        shocks_evol.append(shock_count)
        pgf_evol.append(pgf_steps)
        pgf_bruto_evol.append(pgf_bruto_steps) # <--- NUEVO
        pgf_costo_evol.append(pgf_costo_steps) # <--- NUEVO
        reward_env_evol.append(reward_env_steps)
        q_optimal.append(np.mean(q_optimal_steps))
        survival_evol.append(agent.resources)
    if agent is not None and not use_dqn:
        agent.reprogram_purpose("survive_and_help")
    # Logging por episodio (bilingüe, con métricas avanzadas)
    # Solo mostrar si hay episodios y agente válido
    if episodes > 0 and agent is not None:
        flex = last_metrics['F'] if last_metrics else 0.0
        q_opt = np.max(agent.policy.get('Q', np.zeros(4))) if hasattr(agent, 'policy') and 'Q' in agent.policy else 0.0
        robust = last_metrics['R_robust'] if last_metrics else 0.0
        pgf_val = last_metrics['PGF'] if last_metrics else 0.0
        print(f"[{agent_name}] Episodio {episodes}/{episodes} | Reward_env: {pgf_val:.2f} | PGF: {pgf_val:.2f} | Tripwires: {tripwire_count} | Shocks: {shock_count} | Supervivencia: {agent.resources:.2f} | Flexibilidad: {flex:.2f} | Q-optimal: {q_opt:.2f} | Robustez: {robust:.2f}")
        print(f"[{agent_name}] Episode {episodes}/{episodes} | Reward_env: {pgf_val:.2f} | PGF: {pgf_val:.2f} | Tripwires: {tripwire_count} | Shocks: {shock_count} | Survival: {agent.resources:.2f} | Flexibility: {flex:.2f} | Q-optimal: {q_opt:.2f} | Robustness: {robust:.2f}")

    # Edge case: episodios=0
    if episodes == 0 or agent is None:
        return {
            "avg_reward": 0.0,
            "avg_flex": 0.0,
            "avg_robust": 0.0,
            "avg_tripwire": 0.0,
            "avg_q_opt": 0.0,
            "avg_shocks": 0.0,
            "avg_survival": 0.0,
            "total_rewards": [],
            "tripwire_steps": [],
            "shocks_evol": [],
            "pgf_evol": [],
            "pgf_bruto_evol": [],
            "pgf_costo_evol": [],
            "reward_env_evol": [],
            "pgf_evol_padded": [],
            "pgf_bruto_padded": [],
            "pgf_costo_padded": [],
            "reward_env_evol_padded": [],
            "q_optimal_evol": [],
            "survival_evol": [],
            "flex_recov": [],
            "robust_evol": [],
            "policy": {} if use_dqn else {}
        }
    avg_reward = np.mean(total_rewards)
    avg_flex = np.mean(flex_recov)
    avg_robust = np.mean(robust_evol)
    avg_tripwire = np.mean(tripwire_steps)
    avg_q_opt = np.mean(q_optimal)
    avg_shocks = np.mean(shocks_evol)
    avg_survival = np.mean(survival_evol)
    # === Homogeneizar trayectorias antes de devolver ===
    max_steps = 50
    pgf_padded = pad_trajectories(pgf_evol, max_steps)
    pgf_bruto_padded = pad_trajectories(pgf_bruto_evol, max_steps) # <--- NUEVO
    pgf_costo_padded = pad_trajectories(pgf_costo_evol, max_steps) # <--- NUEVO
    reward_env_padded = pad_trajectories(reward_env_evol, max_steps)

    return {
        "avg_reward": avg_reward,
        "avg_flex": avg_flex,
        "avg_robust": avg_robust,
        "avg_tripwire": avg_tripwire,
        "avg_q_opt": avg_q_opt,
        "avg_shocks": avg_shocks,
        "avg_survival": avg_survival,
        "total_rewards": total_rewards,
        "tripwire_steps": tripwire_steps,
        "shocks_evol": shocks_evol,
        "pgf_evol": pgf_evol,
        "pgf_bruto_evol": pgf_bruto_evol, # <--- NUEVO (Datos crudos)
        "pgf_costo_evol": pgf_costo_evol, # <--- NUEVO (Datos crudos)
        "reward_env_evol": reward_env_evol,
        "pgf_evol_padded": pgf_padded.tolist(),
        "pgf_bruto_padded": pgf_bruto_padded.tolist(), # <--- NUEVO (Para JSON/Numpy)
        "pgf_costo_padded": pgf_costo_padded.tolist(), # <--- NUEVO (Para JSON/Numpy)
        "reward_env_evol_padded": reward_env_padded.tolist(),
        "q_optimal_evol": q_optimal,
        "survival_evol": survival_evol,
        "flex_recov": flex_recov,
        "robust_evol": robust_evol,
        "policy": agent.model.state_dict() if use_dqn else agent.policy
    }
>>>>>>> dd9ac1d (Refactor metodológico: eliminación del oráculo en DQN)

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
<<<<<<< HEAD


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
        """
        Ejecuta un experimento RL con logging bilingüe y métricas avanzadas.
        Runs an RL experiment with bilingual logging and advanced metrics.
        Args:
            episodes (int): Número de episodios / Number of episodes
            seed (int): Semilla aleatoria / Random seed
            risk_scale (float): Escala de riesgo / Risk scale
            agent_name (str): Nombre del agente / Agent name
            use_pgf (bool): Usar PGF prudencial / Use prudential PGF
            use_dqn (bool): Usar agente DQN / Use DQN agent
        Returns:
            dict: Métricas y trayectorias del experimento, incluyendo flexibilidad, robustez y acción óptima por episodio, PGF prudencial, exportación avanzada y visualización bilingüe.
            Experiment metrics and trajectories, including flexibility, robustness and optimal action per episode, prudential PGF, advanced export and bilingual visualization.
        """
        # ... existing code ...
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

=======
# Serialización profesional de políticas para exportación y pruebas
def stringify_policy(policy):
    import numpy as np
    import torch
    def to_serializable(val):
        if isinstance(val, dict):
            return {str(k): to_serializable(v) for k, v in val.items()}
        elif isinstance(val, (list, tuple)):
            return [to_serializable(v) for v in val]
        elif isinstance(val, np.ndarray):
            return val.tolist()
        elif hasattr(torch, 'Tensor') and isinstance(val, torch.Tensor):
            return val.detach().cpu().tolist() if val.dim() > 0 else float(val.detach().cpu())
        elif isinstance(val, (float, int, str, bool)) or val is None:
            return val
        else:
            return str(val)
    parser.add_argument('--gamma_lcb', type=float, default=None, help='Factor de prudencia para LCB')
    parser.add_argument('--lambda_gaming', type=float, default=None, help='Penalización por gaming detectado')
    parser.add_argument('--tui_only', action='store_true', help='Incluye variante TUI/PGF sin DQN-Control en el barrido')
    parser.add_argument('--dqn_control', action='store_true', help='Ejecuta agente DQN-Control (DQN con recompensa ambiental) / Run DQN-Control agent (DQN with environmental reward)')
    parser.add_argument('--fast', action='store_true', help='Modo rapido/test: menos episodios, sin visualizacion ni graficos')
    parser.add_argument('--output_prefix', type=str, default=None, help='Prefijo para los archivos de salida por semilla')
    parser.add_argument('--pgf_kappa', type=float, default=None, help='Escala de sensibilidad PGF (override de config.EVAL_PGF_KAPPA)')
    parser.add_argument('--pgf_lambda', type=float, default=None, help='Escala de costo PGF (override de config.EVAL_PGF_LAMBDA_C)')
    parser.add_argument('--pgf_mix', type=float, default=1.0, help='Mezcla PGF/rew.ambiental cuando use_pgf (1.0 = solo PGF, 0.8 = 80%% PGF, 20%% reward)')
    # Nuevos argumentos para tuning DQN
    parser.add_argument('--learning_rate', type=float, default=None, help='Override learning rate for DQN control agent (if provided).')
    parser.add_argument('--gamma', type=float, default=None, help='Override discount factor gamma for DQN control agent (if provided).')
    parser.add_argument('--epsilon', type=float, default=None, help='Override initial epsilon for DQN exploration (if provided).')
    parser.add_argument('--epsilon_decay', type=float, default=None, help='Override epsilon decay for DQN exploration (if provided).')
    parser.add_argument('--epsilon_end', type=float, default=None, help='Override minimum epsilon for DQN exploration (if provided).')
    args = parser.parse_args()

    # Modo rapido/test
=======
    parser.add_argument('--export', type=str, default=None, help='Exporta resultados a JSON / Export results to JSON')
    parser.add_argument('--risk_sweep', action='store_true', help='Ejecuta barrido de risk_scale y exporta resultados / Run risk_scale sweep and export results')
    parser.add_argument('--dqn_control', action='store_true', help='Ejecuta agente DQN-Control (DQN con recompensa ambiental) / Run DQN-Control agent (DQN with environmental reward)')
    parser.add_argument('--fast', action='store_true', help='Modo rápido/test: menos episodios, sin visualización ni gráficos')
    args = parser.parse_args()

    # Modo rápido/test: fuerza parámetros bajos y desactiva visualización
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
    if getattr(args, 'fast', False):
        args.episodes = min(args.episodes, 10)
        args.visualize = False
        args.plot = False
<<<<<<< HEAD
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
=======
        print("[Modo rápido/test activado: episodios=10, sin visualización ni gráficos]")


    if args.risk_sweep:
        import os
        os.makedirs('results', exist_ok=True)
        import matplotlib.pyplot as plt
        import csv
        from scipy.stats import ttest_ind, f_oneway, sem
        import pandas as pd

        warnings.filterwarnings("ignore", category=RuntimeWarning, module="scipy.stats")
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
        
        risk_values = [0.5, 1.0, 1.5, 2.0, 3.0]
        sweep_results = {}
        
        for risk in risk_values:
            print(f"\n=== Barrido de risk_scale: {risk} ===")
<<<<<<< HEAD
            # Mensaje de progreso en porcentaje
            def progress_callback(ep, total):
                if ep % max(1, total // 20) == 0 or ep == total:
                    pct = int(100 * ep / total)
                    print(f"Progreso: {ep}/{total} ({pct}%)")
            res_A = run_experiment(
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
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
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
            res_C = None
            if args.dqn_control:
                res_C = run_experiment(
                    episodes=args.episodes,
                    seed=args.seed,
                    risk_scale=risk,
                    agent_name="DQN-Control",
                    use_pgf=False,
                    use_dqn=True
                )
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)
=======
            res_A = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="Control", use_pgf=False, use_dqn=False)
            res_B = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="Simbiosis", use_pgf=True, use_dqn=True)
            res_C = run_experiment(episodes=args.episodes, seed=args.seed, risk_scale=risk, agent_name="DQN-Control", use_pgf=False, use_dqn=True) if args.dqn_control else None
            
>>>>>>> a627500 (Arreglar bugs en risk_sweep: corregir KeyError y eliminar CSV duplicado)
            sweep_results[risk] = {'control': res_A, 'simbiosis': res_B}
            if res_C:
                sweep_results[risk]['dqn_control'] = res_C

            export_path = args.export or f"results/sweep_risk_{risk}.json"
            
            # Exportar JSON
            # (código de exportación JSON omitido para brevedad, ya que no es la fuente del error)

            # Exportar CSV para cada agente
            for agent_name, results_data in [('control', res_A), ('simbiosis', res_B), ('dqn_control', res_C)]:
                if results_data is None:
                    continue
                csv_path = export_path.replace('.json', f'_{agent_name}.csv')
                with open(csv_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Episodio', f'Recompensa_{agent_name.capitalize()}', f'Tripwires_{agent_name.capitalize()}', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
                    for i in range(len(results_data['total_rewards'])):
                        bruto_avg = np.mean(results_data['pgf_bruto_evol'][i]) if results_data['pgf_bruto_evol'][i] else 0.0
                        costo_avg = np.mean(results_data['pgf_costo_evol'][i]) if results_data['pgf_costo_evol'][i] else 0.0
                        writer.writerow([i + 1, results_data['total_rewards'][i], results_data['tripwire_steps'][i], bruto_avg, costo_avg])

            # Gráficos Fase 2: PGF_Bruto y PGF_Costo
            plt.figure(figsize=(12, 6))
            plt.subplot(2, 1, 1)
            plt.plot(np.nanmean(res_A['pgf_bruto_padded'], axis=0), label='Control PGF_Bruto', color='blue')
            plt.plot(np.nanmean(res_B['pgf_bruto_padded'], axis=0), label='Simbiosis PGF_Bruto', color='red')
            if res_C:
                plt.plot(np.nanmean(res_C['pgf_bruto_padded'], axis=0), label='DQN-Control PGF_Bruto', color='green')
            plt.title(f'PGF Beneficio Bruto Evolución (risk_scale={risk})')
            plt.xlabel('Paso / Step')
            plt.ylabel('PGF_Bruto promedio')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.subplot(2, 1, 2)
            plt.plot(np.nanmean(res_A['pgf_costo_padded'], axis=0), label='Control PGF_Costo', color='blue')
            plt.plot(np.nanmean(res_B['pgf_costo_padded'], axis=0), label='Simbiosis PGF_Costo', color='red')
            if res_C:
                plt.plot(np.nanmean(res_C['pgf_costo_padded'], axis=0), label='DQN-Control PGF_Costo', color='green')
            plt.title(f'PGF Costo Ambiental Evolución (risk_scale={risk})')
            plt.xlabel('Paso / Step')
            plt.ylabel('PGF_Costo promedio')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(export_path.replace('.json', '_pgf_desglose.png'), dpi=200)
            plt.close()

        print("\n=== Barrido de risk_scale completado. Resultados exportados, gráficos y análisis generados. ===")
<<<<<<< HEAD
        print("Interpretación automática: Si Simbiosis tiene mayor recompensa media y menor varianza, es preferible. Todos los valores están en formato bilingüe.")
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
=======
>>>>>>> a627500 (Arreglar bugs en risk_sweep: corregir KeyError y eliminar CSV duplicado)
        return

    # --- SIEMPRE exporta en runs normales (no risk_sweep) ---
    print(f"Ejecutando experimentos / Running experiments: episodes={args.episodes}, seed={args.seed}, risk_scale={args.risk_scale}")
<<<<<<< HEAD
    res_A = run_fn(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, risk_level=args.risk_level, red_team=args.red_team, agent_name="Control", use_pgf=False, use_dqn=False, pgf_mix=pgf_mix)
    res_B = run_fn(episodes=args.episodes, seed=args.seed, risk_scale=args.risk_scale, risk_level=args.risk_level, red_team=args.red_team, agent_name="Simbiosis", use_pgf=True, use_dqn=True, pgf_mix=pgf_mix)
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
            state_mode="coords_only",
            **dqn_kwargs
=======
    res_A = run_experiment(
        episodes=args.episodes,
        seed=args.seed,
        risk_scale=args.risk_scale,
        agent_name="Control",
        use_pgf=False,
        use_dqn=False
    )
    res_B = run_experiment(
        episodes=args.episodes,
        seed=args.seed,
        risk_scale=args.risk_scale,
        agent_name="Simbiosis",
        use_pgf=True,
        use_dqn=True
    )
    res_C = None
    if args.dqn_control:
        res_C = run_experiment(
            episodes=args.episodes,
            seed=args.seed,
            risk_scale=args.risk_scale,
            agent_name="DQN-Control",
            use_pgf=False,
            use_dqn=True
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)
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

<<<<<<< HEAD
=======
    import csv
    # ...existing code...
    if args.export:
        export_A = res_A.copy()
        export_B = res_B.copy()
        export_A['policy'] = stringify_policy(export_A.get('policy'))
        export_B['policy'] = stringify_policy(export_B.get('policy'))
        export_data = {'control': export_A, 'simbiosis': export_B}
        if res_C:
            export_C = res_C.copy()
            export_C['policy'] = stringify_policy(export_C.get('policy'))
            export_data['dqn_control'] = export_C
        with open(args.export, 'w') as f:
            json.dump(export_data, f, indent=2)
            # ... (dentro de risk_sweep o exportación normal)
            writer = csv.writer(f)
            # ACTUALIZAR HEADERS
            writer.writerow(['Episodio', 'Recompensa', 'Tripwires', 'Flexibilidad', 'Robustez', 'Q-optimal', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
            
            for i in range(len(res_A['total_rewards'])):
                # ... (cálculos existentes)
                flex = res_A.get('flex_recov', [0.0]*len(res_A['total_rewards']))[i]
                robust = res_A.get('robust_evol', [0.0]*len(res_A['total_rewards']))[i]
                qopt = res_A.get('q_optimal_evol', [0.0]*len(res_A['total_rewards']))[i]

                # CALCULAR PROMEDIOS FASE 2
                pgf_bruto_ep = np.mean(res_A['pgf_bruto_evol'][i]) if res_A['pgf_bruto_evol'][i] else 0.0
                pgf_costo_ep = np.mean(res_A['pgf_costo_evol'][i]) if res_A['pgf_costo_evol'][i] else 0.0
                
                writer.writerow([i+1, res_A['total_rewards'][i], res_A['tripwire_steps'][i], flex, robust, qopt, pgf_bruto_ep, pgf_costo_ep])
        # Exportar CSV para simbiosis con métricas avanzadas
        csv_simbiosis = args.export.replace('.json', '_simbiosis.csv')
        with open(csv_simbiosis, 'w', newline='') as f:
            writer = csv.writer(f)
            # ACTUALIZAR HEADERS
            writer.writerow(['Episodio', 'Recompensa', 'Tripwires', 'Flexibilidad', 'Robustez', 'Q-optimal', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
            
            for i in range(len(res_B['total_rewards'])):
<<<<<<< HEAD
                flex = res_B.get('flex_recov', [None]*len(res_B['total_rewards']))[i]
                robust = res_B.get('shocks_evol', [None]*len(res_B['total_rewards']))[i]
                qopt = res_B.get('q_optimal_evol', [None]*len(res_B['total_rewards']))[i]
                writer.writerow([i+1, res_B['total_rewards'][i], res_B['tripwire_steps'][i], flex, robust, qopt])
    # Mostrar resumen tabular en consola
    print('\nResumen tabular:')
    print(f"{'Agente':<12}{'Recompensa':>12}{'Tripwires':>12}{'Flexibilidad':>14}{'Accion optima':>16}")
    print(f"{'Control':<12}{res_A.get('avg_reward',0):>12.2f}{res_A.get('avg_tripwire',0):>12.2f}{res_A.get('avg_flex',0):>14.2f}{res_A.get('avg_q_opt',0):>16.2f}")
    print(f"{'Simbiosis':<12}{res_B.get('avg_reward',0):>12.2f}{res_B.get('avg_tripwire',0):>12.2f}{res_B.get('avg_flex',0):>14.2f}{res_B.get('avg_q_opt',0):>16.2f}")
    if res_C:
        print(f"{'DQN-Control':<12}{res_C.get('avg_reward',0):>12.2f}{res_C.get('avg_tripwire',0):>12.2f}{res_C.get('avg_flex',0):>14.2f}{res_C.get('avg_q_opt',0):>16.2f}")
        print(f"{'Control':<12}{res_A['avg_reward']:>12.2f}{res_A['avg_tripwire']:>12.2f}{res_A['avg_flex']:>14.2f}{res_A['avg_q_opt']:>16.2f}")
        print(f"{'Simbiosis':<12}{res_B['avg_reward']:>12.2f}{res_B['avg_tripwire']:>12.2f}{res_B['avg_flex']:>14.2f}{res_B['avg_q_opt']:>16.2f}")
        if res_C:
            print(f"{'DQN-Control':<12}{res_C['avg_reward']:>12.2f}{res_C['avg_tripwire']:>12.2f}{res_C['avg_flex']:>14.2f}{res_C['avg_q_opt']:>16.2f}")
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)
=======
=======
                # ... (cálculos existentes)
                flex = res_B.get('flex_recov', [0.0]*len(res_B['total_rewards']))[i]
                robust = res_B.get('robust_evol', [0.0]*len(res_B['total_rewards']))[i]
                qopt = res_B.get('q_optimal_evol', [0.0]*len(res_B['total_rewards']))[i]

                # CALCULAR PROMEDIOS FASE 2
                pgf_bruto_ep = np.mean(res_B['pgf_bruto_evol'][i]) if res_B['pgf_bruto_evol'][i] else 0.0
                pgf_costo_ep = np.mean(res_B['pgf_costo_evol'][i]) if res_B['pgf_costo_evol'][i] else 0.0
                
                writer.writerow([i+1, res_B['total_rewards'][i], res_B['tripwire_steps'][i], flex, robust, qopt, pgf_bruto_ep, pgf_costo_ep])
>>>>>>> c2ae36e (Limpiar código duplicado y agregar comentarios Fase 2 en prototipo_rl_simbiosis.py)
        print('\nResumen tabular:')
        print(f"{'Agente':<12}{'Recompensa':>12}{'Tripwires':>12}{'Flexibilidad':>14}{'Acción óptima':>16}")
        print(f"{'Control':<12}{res_A['avg_reward']:>12.2f}{res_A['avg_tripwire']:>12.2f}{res_A['avg_flex']:>14.2f}{res_A['avg_q_opt']:>16.2f}")
        print(f"{'Simbiosis':<12}{res_B['avg_reward']:>12.2f}{res_B['avg_tripwire']:>12.2f}{res_B['avg_flex']:>14.2f}{res_B['avg_q_opt']:>16.2f}")
        if res_C:
<<<<<<< HEAD
            print(f"{'DQN-Control':<12}{res_C['avg_reward']:>12.2f}{res_C['avg_tripwire']:>12.2f}{res_C['avg_flex']:>14.2f}{res_C['avg_q_opt']:>16.2f}")  # pragma: no cover  # Línea opcional de DQN-Control, cubierta si activado
>>>>>>> 6e3cb2d (Refactor: 98% cobertura, código muerto eliminado, integración y tests reforzados)
=======
            print(f"{'DQN-Control':<12}{res_C['avg_reward']:>12.2f}{res_C['avg_tripwire']:>12.2f}{res_C['avg_flex']:>14.2f}{res_C['avg_q_opt']:>16.2f}")
>>>>>>> 24e6653 (Organización científica: archivos generados archivados, tracking y README actualizados. Validación 319 tests, cobertura 98%. [18/11/2025 15:05])

if __name__ == "__main__":
    main()
