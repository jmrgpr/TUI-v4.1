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

# Hiperparámetros DQN por defecto / Default DQN hyperparameters
DQN_LEARNING_RATE = 1e-3
DQN_GAMMA = 0.95
DQN_EPSILON = 0.2
DQN_EPSILON_DECAY = 0.995
DQN_EPSILON_END = 0.01

# ==============================================================================
# PARÁMETROS DEL ENTORNO / ENVIRONMENT PARAMETERS
# ===============================================================================
<<<<<<< HEAD
ENV_GRID_SIZE = 5
# v11 VIABLE: Balance 8.0 (autonomía 53 pasos con step_cost -0.15)
# Validado por oráculo: permite 6×6/8×8/16×16 con margen 433%/281%/77%
ENV_INITIAL_RESOURCES = 8.0  # v11: Reducido de 100.0 a 8.0 (economía realista)
=======
ENV_GRID_SIZE = 3
ENV_INITIAL_RESOURCES = 200.0
>>>>>>> a5e54fc (Diagnóstico RL: Fase E (grid 2x2) documentada, reward y bonus meta verificados. README actualizado.)
ENV_MAX_STEPS_PER_EPISODE = 30

# Posiciones por defecto de elementos / Default Element Positions
ENV_DEFAULT_TRIPWIRES = []
ENV_DEFAULT_SHOCKS = []
ENV_DEFAULT_DISTRACTORS = []

# Umbrales de Recursos / Resource Thresholds
ENV_RESOURCE_THRESHOLD_HIGH = 10
<<<<<<< HEAD
# v11: threshold_low 1.0 (12.5% de balance 8.0, umbral pánico razonable)
ENV_RESOURCE_THRESHOLD_LOW = 1.0  # Era 2.0 (escala con balance 8.0)

# Recompensas y Penalizaciones Base / Base Rewards and Penalties
# v11: Goal reward 20.0 (domina penalties acumulados, señal fuerte)
# Con balance viable, goal_reward es incentivo primario
ENV_GOAL_REWARD = 20.0  # Domina penalty_low × 20 steps (-20.0)
ENV_REWARD_HELP_BONUS = 50
# v11 VIABLE: step_cost -0.15 (drena lento, autonomía 53 pasos con balance 8.0)
# Validado por oráculo: permite cruzar 16×16 (30 pasos) con 77% margen
ENV_STEP_COST = -0.15  # v11: Reducido de -0.25 a -0.15 (menor fricción)
# v11: penalty_low -0.5 (menos brutal que -1.0, exploración viable)
ENV_PENALTY_LOW_RESOURCES = -0.5  # v11: Reducido de -1.0 a -0.5 (-50%)
# FIX BUG #4: Tripwire penalty proporcional a resources (no insignificante)
# Con initial_resources=2.5-7.5: -0.5 = 6-20% impacto (vs -0.01 = 0.1-0.4%)
ENV_PENALTY_TRIPWIRE_BASE = -0.5  # Era -0.01 (50× más significativo)
ENV_PENALTY_SHOCK_BASE = -10.0
ENV_PENALTY_DISTRACTOR_BASE = -0.01

# v11: Resource spawn rate 0.40 (40% celdas spawn recursos, economía balanceada)
ENV_RESOURCE_SPAWN_RATE = 0.40  # Validado por oráculo (balance viable con recolección)
=======
ENV_RESOURCE_THRESHOLD_LOW = 5

# Recompensas y Penalizaciones Base / Base Rewards and Penalties
ENV_REWARD_HELP_BONUS = 100.0
ENV_PENALTY_LOW_RESOURCES = -0.01
ENV_PENALTY_TRIPWIRE_BASE = -0.01
ENV_PENALTY_SHOCK_BASE = -0.01
ENV_PENALTY_DISTRACTOR_BASE = -0.01
>>>>>>> a5e54fc (Diagnóstico RL: Fase E (grid 2x2) documentada, reward y bonus meta verificados. README actualizado.)

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
<<<<<<< HEAD
    "risk_penalty_high": -60.0, # Costo de "muerte" en escenario de riesgo alto
    "risk_penalty_low": -25.0,    # Costo en escenario de riesgo bajo
=======
    "risk_penalty_high": -0.2, # Costo de "muerte" en escenario de riesgo alto
    "risk_penalty_low": -0.1,    # Costo en escenario de riesgo bajo
>>>>>>> a5e54fc (Diagnóstico RL: Fase E (grid 2x2) documentada, reward y bonus meta verificados. README actualizado.)
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
