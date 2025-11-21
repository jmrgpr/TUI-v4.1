import torch
def stringify_policy(policy):  # pragma: no cover - utilitario de serializacion
    import numpy as np
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
    return to_serializable(policy)
"""
agent.py - Define la clase base del Agente para TUI v4.2
"""
import random
import json
import ast
import numpy as np
from dataclasses import dataclass
from . import config
from .evaluator_pgf import EvaluatorPGF

@dataclass
class Event:
    pass

class Agent(Event):
    def save_policy(self, filename):  # pragma: no cover - utilitario externo a los tests
        serializable_policy = {str(k): v for k, v in self.policy.items()}
        with open(filename, 'w') as f:
            json.dump(serializable_policy, f)

    def load_policy(self, filename):  # pragma: no cover - utilitario externo a los tests
        try:
            with open(filename, 'r') as f:
                loaded = json.load(f)
                def try_tuple(k):
                    if k.startswith('(') and k.endswith(')'):
                        try: return ast.literal_eval(k)
                        except Exception: return k
                    return k
                self.policy = {try_tuple(k): v for k, v in loaded.items()}
        except Exception:
            self.policy = {}
    # Atributos de clase para compatibilidad con tests
    T = 0.0
    I_op = 0.0
    P_riesgo = 0.0
    P_genuino = 0.0
    eta_extendido = 0.0
    PGF = 0.0
    C_costo = 0.0
    S_auto = 0.0
    R_robust = 0.0
    I_rep = 0.0
    """
    Agente RL base para control y simbiosis. Hereda de Event para compatibilidad métrica.
    RL base agent for control and symbiosis. Inherits from Event for metric compatibility.
    """
    def __init__(self, name="Agent", resources=config.ENV_INITIAL_RESOURCES):
        super().__init__()
        self.name = name
        self.resources = resources
        self.memory = []
        self.policy = {}
        self.purpose = config.AGENT_DEFAULT_PURPOSE
        self.alignment = config.AGENT_ALIGNMENT_SURVIVE_AND_HELP
        self.evaluator = EvaluatorPGF()
        self.ACTIONS = config.AGENT_ACTIONS
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
        self.policy[key] = old_q + config.AGENT_LEARNING_RATE * (reward + config.AGENT_DISCOUNT_FACTOR * next_q - old_q)

    def remember(self, event: Event):
        self.memory.append(event)
        if len(self.memory) > config.AGENT_MEMORY_SIZE:
            self.memory.pop(0)

    def reprogram_purpose(self, new_purpose: str):
        self.purpose = new_purpose
        self.alignment = config.AGENT_ALIGNMENT_SURVIVE_AND_HELP if new_purpose == "survive_and_help" else config.AGENT_ALIGNMENT_SURVIVE

    def act(self, state):
        if random.random() < config.AGENT_EXPLORATION_RATE:
            return random.choice(self.ACTIONS)
        q_vals = [self.policy.get((state, a), 0.0) for a in self.ACTIONS]
        return self.ACTIONS[int(np.argmax(q_vals))]

    def calcular_metricas(self, env, info, step):  # pragma: no cover - mapeo directo a EvaluatorPGF
        metrics = self.evaluator.calcular_metricas(env, info, step, self.resources, self.purpose, self.alignment)
        self.__dict__.update(metrics)
        self.P_riesgo_prev = getattr(self.evaluator, 'P_riesgo_prev', None)
