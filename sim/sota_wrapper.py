import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sim.prototipo_rl_simbiosis import SimbiosisEnv
from sim.evaluator_pgf import EvaluatorPGF

class SimbiosisGymEnv(gym.Env):
    """
    Wrapper compatible con Gymnasium/Stable-Baselines3 para el entorno SimbiosisEnv.
    Integra EvaluatorPGF para métricas TUI (Bruto/Costo/Neto).
    """
    def __init__(self, risk_scale=1.0):
        super(SimbiosisGymEnv, self).__init__()
        self.env = SimbiosisEnv(risk_scale=risk_scale)
        self.action_space = spaces.Discrete(4) # up, down, left, right
        self.observation_space = spaces.Box(low=0, high=1, shape=(8,), dtype=np.float32)
        self.evaluator = EvaluatorPGF()
        self.evaluator.P_riesgo_prev = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state_tuple = self.env.reset()
        self.evaluator = EvaluatorPGF()
        obs_values = [v for _, v in state_tuple]
        if len(obs_values) < 8:
            obs_values += [0.0] * (8 - len(obs_values))
        obs = np.array(obs_values[:8], dtype=np.float32)
        return obs, {}

    def step(self, action_idx):
        actions = ['up', 'down', 'left', 'right']
        action_str = actions[action_idx]
        next_state_tuple, reward, done, info = self.env.step(action_str)
        metrics = self.evaluator.calcular_metricas(
            self.env,
            info,
            self.env.timestep,
            self.env.resources,
            "survive_and_help",
            1.0
        )
        info['pgf_neto'] = metrics['PGF']
        info['pgf_bruto'] = metrics['PGF_Bruto']
        info['pgf_costo'] = metrics['PGF_Costo']
        obs_values = [v for _, v in next_state_tuple]
        if len(obs_values) < 8:
            obs_values += [0.0] * (8 - len(obs_values))
        obs = np.array(obs_values[:8], dtype=np.float32)
        truncated = False
        return obs, reward, done, truncated, info
        return obs, reward, done, truncated, info
