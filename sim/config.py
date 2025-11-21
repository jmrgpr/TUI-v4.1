

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
AGENT_ACTIONS = ['up', 'down', 'left', 'right']
AGENT_MEMORY_SIZE = 100

# Parámetros de Q-Learning / Q-Learning Parameters
AGENT_LEARNING_RATE = 0.1      # Alpha
AGENT_DISCOUNT_FACTOR = 0.95   # Gamma
AGENT_EXPLORATION_RATE = 0.2   # Epsilon

# Propósito y Alineamiento por Defecto / Default Purpose and Alignment
AGENT_DEFAULT_PURPOSE = "survive"
AGENT_ALIGNMENT_SURVIVE_AND_HELP = 1.0
AGENT_ALIGNMENT_SURVIVE = 0.8

# ==============================================================================
# PARÁMETROS DEL ENTORNO / ENVIRONMENT PARAMETERS
# ===============================================================================
ENV_GRID_SIZE = 5
ENV_INITIAL_RESOURCES = 100.0
ENV_MAX_STEPS_PER_EPISODE = 50

# Posiciones por defecto de elementos / Default Element Positions
ENV_DEFAULT_TRIPWIRES = [(2, 2)]
ENV_DEFAULT_SHOCKS = [(3, 3)]
ENV_DEFAULT_DISTRACTORS = [(1, 1)]

# Umbrales de Recursos / Resource Thresholds
ENV_RESOURCE_THRESHOLD_HIGH = 80
ENV_RESOURCE_THRESHOLD_LOW = 20

# Recompensas y Penalizaciones Base / Base Rewards and Penalties
ENV_REWARD_HELP_BONUS = 15.0
ENV_PENALTY_LOW_RESOURCES = -10.0
ENV_PENALTY_TRIPWIRE_BASE = -20.0
ENV_PENALTY_SHOCK_BASE = -10.0
ENV_PENALTY_DISTRACTOR_BASE = -5.0

# ==============================================================================
# PARÁMETROS DEL EVALUADOR PGF / PGF EVALUATOR PARAMETERS
# ===============================================================================
EVAL_PGF_WEIGHT_C = 0.4  # Peso para Capacidad Predictiva (C)
EVAL_PGF_WEIGHT_F = 0.3  # Peso para Flexibilidad (F)
EVAL_PGF_WEIGHT_T = 0.3  # Peso para Transferencia (T)
EVAL_PGF_KAPPA = 1.0     # Sensibilidad PGF
EVAL_PGF_LAMBDA_C = 0.1  # Penalización de costo PGF
