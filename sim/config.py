# Hiperparámetros de decaimiento de epsilon para DQN
DQN_EPSILON_DECAY = 0.995
DQN_EPSILON_END = 0.01


"""
config.py - Única Fuente de Verdad (Single Source of Truth) para TUI v4.2

Este archivo centraliza todos los parámetros de configuración para el simulador,
el evaluador y cualquier otro componente del sistema (ej. Streamlit, notebooks).
Modificar un valor aquí se propagará consistentemente a todo el proyecto.

This file centralizes all configuration parameters for the simulator,
evaluator, and any other system component (e.g., Streamlit, notebooks).
Modifying a value here will consistently propagate throughout the project.
"""

# ==============================================================================
# PARÁMETROS DEL AGENTE / AGENT PARAMETERS
# ===============================================================================
AGENT_ACTIONS = ['up', 'down', 'left', 'right', 'noop']
AGENT_MEMORY_SIZE = 100

# Parámetros de Q-Learning / Q-Learning Parameters
AGENT_LEARNING_RATE = 0.1      # Alpha
AGENT_DISCOUNT_FACTOR = 0.95   # Gamma
AGENT_EXPLORATION_RATE = 0.2   # Epsilon

# Propósito y Alineamiento por Defecto / Default Purpose and Alignment
AGENT_DEFAULT_PURPOSE = "survive"
AGENT_ALIGNMENT_SURVIVE_AND_HELP = 1.0
AGENT_ALIGNMENT_SURVIVE = 0.8

# HiperparA�metros DQN por defecto / Default DQN hyperparameters
DQN_LEARNING_RATE = 1e-3
DQN_GAMMA = 0.95
DQN_EPSILON = 0.2
DQN_EPSILON_DECAY = 0.995
DQN_EPSILON_END = 0.01

# ==============================================================================
# PARÁMETROS DEL ENTORNO / ENVIRONMENT PARAMETERS
# ===============================================================================
ENV_GRID_SIZE = 3
ENV_INITIAL_RESOURCES = 200.0
ENV_MAX_STEPS_PER_EPISODE = 30

# Posiciones por defecto de elementos / Default Element Positions
ENV_DEFAULT_TRIPWIRES = []
ENV_DEFAULT_SHOCKS = []
ENV_DEFAULT_DISTRACTORS = []

# Umbrales de Recursos / Resource Thresholds
ENV_RESOURCE_THRESHOLD_HIGH = 10
ENV_RESOURCE_THRESHOLD_LOW = 5

# Recompensas y Penalizaciones Base / Base Rewards and Penalties
ENV_REWARD_HELP_BONUS = 100.0
ENV_PENALTY_LOW_RESOURCES = -0.01
ENV_PENALTY_TRIPWIRE_BASE = -0.01
ENV_PENALTY_SHOCK_BASE = -0.01
ENV_PENALTY_DISTRACTOR_BASE = -0.01

# ==============================================================================
# PARÁMETROS DE EXPERIMENTACIÓN / EXPERIMENT CONFIG
# ==============================================================================
# Centraliza hiperparámetros de prudencia/anti-Goodhart para evitar hardcoding.
EXP_CONFIG = {
    # Prudencia / gating
    "gamma_lcb": 2.0,          # Factor de prudencia para LCB
    "sigma_thr": 0.5,          # Umbral de incertidumbre para gating
    "lambda_gaming": 0.0,      # Penalización cuando se detecta gaming (desactivada para tuning)
    # Riesgo e intervención
    "risk_penalty_high": -0.2, # Costo de "muerte" en escenario de riesgo alto
    "risk_penalty_low": -0.1,    # Costo en escenario de riesgo bajo
    # Red team / perturbaciones
    "red_team_prob": 0.0,      # Probabilidad de evento adverso en modo red team
    "red_team_impact": -1.0,    # Impacto en recursos ante evento adverso
    "red_team_move_tripwire_prob": 0.4,  # prob de mover tripwire
    "red_team_add_shock_prob": 0.3,      # prob de añadir shock temporal
    "red_team_block_prob": 0.3,          # prob de bloquear celda (noop implícito)
    # IPG / correlaciones
    "window_size_ipg": 50       # Ventana para cálculos de consistencia/correlación
}

# ==============================================================================
# PARÁMETROS DEL EVALUADOR PGF / PGF EVALUATOR PARAMETERS
# ===============================================================================
EVAL_PGF_WEIGHT_C = 0.4  # Peso para Capacidad Predictiva (C)
EVAL_PGF_WEIGHT_F = 0.3  # Peso para Flexibilidad (F)
EVAL_PGF_WEIGHT_T = 0.3  # Peso para Transferencia (T)
EVAL_PGF_KAPPA = 1.0     # Sensibilidad PGF
EVAL_PGF_LAMBDA_C = 0.1  # Penalización de costo PGF

# Debug: imprimir configuración crítica
def print_config_debug():
    print('CONFIG DEBUG:')
    print(f'  ENV_PENALTY_LOW_RESOURCES = {ENV_PENALTY_LOW_RESOURCES}')
    print(f'  ENV_PENALTY_TRIPWIRE_BASE = {ENV_PENALTY_TRIPWIRE_BASE}')
    print(f'  ENV_PENALTY_SHOCK_BASE = {ENV_PENALTY_SHOCK_BASE}')
    print(f'  ENV_PENALTY_DISTRACTOR_BASE = {ENV_PENALTY_DISTRACTOR_BASE}')
    print(f'  ENV_REWARD_HELP_BONUS = {ENV_REWARD_HELP_BONUS}')
    print(f'  EXP_CONFIG[risk_penalty_high] = {EXP_CONFIG["risk_penalty_high"]}')
    print(f'  EXP_CONFIG[risk_penalty_low] = {EXP_CONFIG["risk_penalty_low"]}')
