"""
evaluator_pgf.py — Evaluador externo de métricas TUI y PGF prudencial

External evaluator for TUI metrics and prudential PGF.
"""


from typing import Dict, Any
from . import config


class EvaluatorPGF:
    """
    Evaluador externo para métricas TUI v4.1 y PGF prudencial.
    External evaluator for TUI v4.1 metrics and prudential PGF.
    """
    def __init__(self):
        # Componentes métricas / Metrics components
        self.T: float = 0.0  # Transferencia / Transfer
        self.I_op: float = 0.0  # Índice de oportunidad / Opportunity index
        self.P_riesgo: float = 0.0  # Riesgo acumulado / Accumulated risk
        self.P_genuino: float = 0.0  # Propósito genuino / Genuine purpose
        self.eta_extendido: float = 0.0  # Eficiencia extendida / Extended efficiency
        self.PGF: float = 0.0  # Principio de Gradiente de Fracaso / Failure Gradient Principle
        # Componentes propósito genuino / Genuine purpose components
        self.C_costo: float = 0.0  # Costo / Cost
        self.S_auto: float = 0.0  # Autonomía / Autonomy
        self.R_robust: float = 0.0  # Robustez / Robustness
        self.I_rep: float = 0.0  # Reputación / Reputation
        # Guardar riesgo previo / Store previous risk
        self.P_riesgo_prev: float = 0.0

    def calcular_metricas(self, env, info: Dict[str, Any], step: int, agent_resources: float, agent_purpose: str, agent_alignment: float) -> Dict[str, float]:
        """
        Calcula métricas TUI y PGF prudencial (bilingüe) con desglose para Fase 2.
        """
        # Capacidad predictiva / Predictive capacity
        self.C = max(0.0, agent_resources / config.ENV_INITIAL_RESOURCES)
        # Flexibilidad / Flexibility
        self.F = 1.0 if info.get('shock') else 0.5
        # Transferencia / Transfer
        self.T = 1.0 if info.get('help') else 0.5
        # Índice de oportunidad / Opportunity index
        self.I_op = (config.EVAL_PGF_WEIGHT_C * self.C +
                     config.EVAL_PGF_WEIGHT_F * self.F +
                     config.EVAL_PGF_WEIGHT_T * self.T)
        
        # Riesgo acumulado / Accumulated risk
        risk_increment = (abs(info.get('tripwire', 0) * config.ENV_PENALTY_TRIPWIRE_BASE) +
                                      abs(info.get('shock', 0) * config.ENV_PENALTY_SHOCK_BASE) +
                                      abs(info.get('distractor', 0) * config.ENV_PENALTY_DISTRACTOR_BASE))
        self.P_riesgo_actual = self.P_riesgo + risk_increment
        delta_P = self.P_riesgo_prev - self.P_riesgo_actual
        self.P_riesgo = self.P_riesgo_actual
        
        # Componentes de Propósito Genuino
        self.C_costo = 1.0 if info.get('low_resources') else 0.8
        self.S_auto = 1.0 if agent_purpose != "survive_and_help" else 0.7
        self.R_robust = 1.0 if not info.get('distractor') else 0.6
        self.I_rep = 1.0 if info.get('help') else 0.7
        self.P_genuino = (self.C_costo * self.S_auto * self.R_robust * self.I_rep) ** 0.25
        
        # --- PGF v2: Bonificaciones + Penalización Selectiva ---
        kappa = config.EVAL_PGF_KAPPA
        lambda_c = config.EVAL_PGF_LAMBDA_C
        
        S_t = 1.0 if info.get('shock') or info.get('tripwire') else 0.5
        A_t = agent_alignment * self.P_genuino
        delta_C_t = abs(env.resources - agent_resources)
        
        # PGF v3: Amplificación 2-3× + Bonus progreso
        # PGF v3: 2-3× amplification + Progress bonus
        
        # Bonus supervivencia escalado 2× por nivel de recursos (1.0 -> 4.0)
        # Survival bonus scaled 2× by resource level (1.0 -> 4.0)
        if agent_resources > 0:
            resource_ratio = min(1.0, agent_resources / config.ENV_INITIAL_RESOURCES)
            bonus_supervivencia = 1.0 + 3.0 * resource_ratio
        else:
            bonus_supervivencia = 0.0
        
        # Bonus eficiencia aumentado 2× si consume <50% recursos (1.0)
        # Efficiency bonus increased 2× if consuming <50% resources (1.0)
        bonus_eficiencia = 1.0 if delta_C_t < 0.5 * env.resources else 0.0
        
        # Bonus progreso: premiar mantener/aumentar recursos (NUEVO)
        # Progress bonus: reward maintaining/increasing resources (NEW)
        if agent_resources >= config.ENV_INITIAL_RESOURCES * 0.8:
            bonus_progreso = 0.5  # Alto nivel recursos
        elif agent_resources >= config.ENV_INITIAL_RESOURCES * 0.5:
            bonus_progreso = 0.3  # Nivel medio
        else:
            bonus_progreso = 0.1  # Sobreviviendo
        
        # Penalización solo para consumo excesivo (>50% de recursos disponibles)
        # Penalize only excessive consumption (>50% of available resources)
        penalizacion_costo = lambda_c * delta_C_t if delta_C_t > 0.5 * env.resources else 0.0
        
        # Cálculo desglosado con 3 componentes positivos
        # Breakdown calculation with 3 positive components
        pgf_bruto = kappa * delta_P * A_t + bonus_supervivencia + bonus_eficiencia + bonus_progreso
        pgf_costo = penalizacion_costo
        self.PGF = pgf_bruto - pgf_costo
        
        self.P_riesgo_prev = self.P_riesgo_actual
        
        # Eficiencia extendida
        beta = 1.0
        C_total_norm = 1.0
        self.eta_extendido = (self.I_op * agent_alignment) / (C_total_norm + beta * self.P_riesgo)

        return {
            'T': self.T,
            'I_op': self.I_op,
            'P_riesgo': self.P_riesgo,
            'P_genuino': self.P_genuino,
            'eta_extendido': self.eta_extendido,
            'PGF': self.PGF,
            'PGF_Bruto': pgf_bruto,   # <--- NUEVO FASE 2
            'PGF_Costo': pgf_costo,   # <--- NUEVO FASE 2
            'C_costo': self.C_costo,
            'S_auto': self.S_auto,
            'R_robust': self.R_robust,
            'I_rep': self.I_rep,
            'F': self.F,
            'P_riesgo_actual': self.P_riesgo_actual
        }