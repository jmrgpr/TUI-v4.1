import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sim.prototipo_rl_simbiosis import SimbiosisEnv
<<<<<<< HEAD
from sim.evaluator_pgf import EvaluatorPGF
=======
from sim.evaluator_pgf import EvaluatorPGF 
>>>>>>> aa50614 (feat: Complete SOTA comparison and documentation update)

class SimbiosisGymEnv(gym.Env):
    """
    Wrapper compatible con Gymnasium/Stable-Baselines3 para el entorno SimbiosisEnv.
<<<<<<< HEAD
    Integra EvaluatorPGF para métricas TUI (Bruto/Costo/Neto).
=======
    Integra EvaluatorPGF para generar métricas comparables (Bruto/Costo/Neto).
>>>>>>> aa50614 (feat: Complete SOTA comparison and documentation update)
    """
    def __init__(self, risk_scale=1.0):
        super(SimbiosisGymEnv, self).__init__()
        self.env = SimbiosisEnv(risk_scale=risk_scale)
        self.action_space = spaces.Discrete(4) # up, down, left, right
<<<<<<< HEAD
        self.observation_space = spaces.Box(low=0, high=1, shape=(8,), dtype=np.float32)
=======
        
        # Observación: 8 features (flags + posición)
        self.observation_space = spaces.Box(low=0, high=1, shape=(8,), dtype=np.float32)
        
        # Evaluador para métricas TUI
>>>>>>> aa50614 (feat: Complete SOTA comparison and documentation update)
        self.evaluator = EvaluatorPGF()
        self.evaluator.P_riesgo_prev = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state_tuple = self.env.reset()
<<<<<<< HEAD
        self.evaluator = EvaluatorPGF()
        obs_values = [v for _, v in state_tuple]
        if len(obs_values) < 8:
            obs_values += [0.0] * (8 - len(obs_values))
        obs = np.array(obs_values[:8], dtype=np.float32)
=======
        # Reiniciar evaluador al inicio de episodio
        self.evaluator = EvaluatorPGF()
        
        obs = np.array([v for _, v in state_tuple], dtype=np.float32)
>>>>>>> aa50614 (feat: Complete SOTA comparison and documentation update)
        return obs, {}

    def step(self, action_idx):
        actions = ['up', 'down', 'left', 'right']
        action_str = actions[action_idx]
        next_state_tuple, reward, done, info = self.env.step(action_str)
<<<<<<< HEAD
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
=======
        
        # Calcular métricas PGF para reporte (Asumiendo alignment=1.0 para PPO como baseline)
        metrics = self.evaluator.calcular_metricas(
            self.env, 
            info, 
            self.env.timestep, 
            self.env.resources, 
            "survive_and_help", 
            1.0
        )
        
        # Inyectar métricas en info para que el script de evaluación las capture
        info['pgf_neto'] = metrics['PGF']
        info['pgf_bruto'] = metrics['PGF_Bruto']
        info['pgf_costo'] = metrics['PGF_Costo']
        
        obs = np.array([v for _, v in next_state_tuple], dtype=np.float32)
        truncated = False 
        
        return obs, reward, done, truncated, info
>>>>>>> aa50614 (feat: Complete SOTA comparison and documentation update)
