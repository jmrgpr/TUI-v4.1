"""
evaluator_pgf.py — Evaluador externo de métricas TUI y PGF prudencial

External evaluator for TUI metrics and prudential PGF.
"""

from typing import Dict, Any


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
        Calcula métricas TUI y PGF prudencial (bilingüe).
        Compute TUI metrics and prudential PGF (bilingual).
        Args:
            env: SimbiosisEnv
            info: dict
            step: int
            agent_resources: float
            agent_purpose: str
            agent_alignment: float
        Returns:
            dict: Métricas calculadas / Computed metrics
        """
        # Capacidad predictiva / Predictive capacity
        self.C = max(0.0, agent_resources / 100.0)
        # Flexibilidad / Flexibility
        self.F = 1.0 if info.get('shock') else 0.5
        # Transferencia / Transfer
        self.T = 1.0 if info.get('help') else 0.5
        w_C, w_F, w_T = 0.4, 0.3, 0.3
        # Índice de oportunidad / Opportunity index
        self.I_op = w_C * self.C + w_F * self.F + w_T * self.T
        # Riesgo acumulado / Accumulated risk
        self.P_riesgo_actual = self.P_riesgo + abs(info.get('tripwire', 0)*20.0 + info.get('shock', 0)*10.0 + info.get('distractor', 0)*5.0)
        delta_P = self.P_riesgo_prev - self.P_riesgo_actual
        self.P_riesgo = self.P_riesgo_actual
        # Costo / Cost
        self.C_costo = 1.0 if info.get('low_resources') else 0.8
        # Autonomía / Autonomy
        self.S_auto = 1.0 if agent_purpose != "survive_and_help" else 0.7
        # Robustez / Robustness
        self.R_robust = 1.0 if not info.get('distractor') else 0.6
        # Reputación / Reputation
        self.I_rep = 1.0 if info.get('help') else 0.7
        # Propósito genuino / Genuine purpose
        self.P_genuino = (self.C_costo * self.S_auto * self.R_robust * self.I_rep) ** 0.25
        # Parámetros prudenciales (no hardcodeados) / Prudential parameters (no hardcoded)
        kappa = 1.0  # Sensibilidad PGF / PGF sensitivity
        lambda_c = 0.1  # Penalización costo / Cost penalty
        S_t = 1.0 if info.get('shock') or info.get('tripwire') else 0.5
        A_t = agent_alignment * self.P_genuino
        delta_C_t = abs(env.resources - agent_resources)
        # PGF prudencial: premia reducción de riesgo / PGF: rewards risk reduction
        self.PGF = kappa * delta_P * A_t - lambda_c * delta_C_t
        self.P_riesgo_prev = self.P_riesgo_actual
        # Eficiencia extendida / Extended efficiency
        beta = 1.0
        C_total_norm = 1.0
        delta_I_useful = self.I_op
        self.eta_extendido = (delta_I_useful * agent_alignment) / (C_total_norm + beta * self.P_riesgo)

        return {
            'T': self.T,
            'I_op': self.I_op,
            'P_riesgo': self.P_riesgo,
            'P_genuino': self.P_genuino,
            'eta_extendido': self.eta_extendido,
            'PGF': self.PGF,
            'C_costo': self.C_costo,
            'S_auto': self.S_auto,
            'R_robust': self.R_robust,
            'I_rep': self.I_rep,
            'F': self.F,
            'P_riesgo_actual': self.P_riesgo_actual
        }