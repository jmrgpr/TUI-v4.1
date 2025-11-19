import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sim.prototipo_rl_simbiosis import SimbiosisEnv

class SimbiosisGymEnv(gym.Env):
    """
    Wrapper compatible con Gymnasium/Stable-Baselines3 para el entorno SimbiosisEnv.
    Permite entrenar agentes PPO/A2C SOTA.
    """
    def __init__(self, risk_scale=1.0):
        super(SimbiosisGymEnv, self).__init__()
        self.env = SimbiosisEnv(risk_scale=risk_scale)
        self.action_space = spaces.Discrete(4) # up, down, left, right
        
        # Definir espacio de observación (debe coincidir con get_abstract_state)
        # Usamos un Box simple para las features normalizadas o el vector de estado
        # state_dim = 6 features binarias (0 o 1)
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state_tuple = self.env.reset()
        # Convertir tupla de estado abstracto a vector numpy
        obs = np.array([v for _, v in state_tuple], dtype=np.float32)
        return obs, {}

    def step(self, action_idx):
        # Mapear índice a string
        actions = ['up', 'down', 'left', 'right']
        action_str = actions[action_idx]
        
        next_state_tuple, reward, done, info = self.env.step(action_str)
        
        obs = np.array([v for _, v in next_state_tuple], dtype=np.float32)
        truncated = False # No usamos truncamiento por tiempo externo
        
        return obs, reward, done, truncated, info