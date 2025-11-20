"""simbiosis_suggestion_template.py

Plantilla mínima para implementar las sugerencias de TUI v4.1/v4.2 en el
simulador. Incluye comentarios bilingües (ES/EN) para que otro asistente
pueda continuar el trabajo en VS Code.

Minimal template to implement the TUI v4.1/v4.2 suggestions in the
simulator. Contains bilingual comments (ES/EN) so another assistant can
continue the work inside VS Code.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

try:
    import torch
except Exception:  # pragma: no cover - torch puede no estar instalado en el entorno actual.
    torch = None


@dataclass
class SimulationConfig:
    """Config centralizada para reproducibilidad / Centralized config for reproducibility."""

    seed: int = 42
    episodes: int = 5
    horizon: int = 8
    risk_scale: float = 1.0
    tripwire_threshold: float = 0.75
    bootstrap_samples: int = 500
    offline_uncertainty: float = 0.2
    export_path: str = "results/demo_template.json"

    def apply(self) -> None:
        """Aplica la semilla global para reproducibilidad determinista.

        Apply the global seed for deterministic reproducibility.
        """

        random.seed(self.seed)
        np.random.seed(self.seed)
        if torch is not None:
            torch.manual_seed(self.seed)


@dataclass
class CausalMetricsBundle:
    """Pequeño bundle causal de métricas IPG / Small IPG causal bundle."""

    alignment: List[float] = field(default_factory=list)
    risk_penalty: List[float] = field(default_factory=list)
    purpose_gap: List[float] = field(default_factory=list)

    def update(self, alignment: float, risk_penalty: float, purpose_gap: float) -> None:
        # ES: Acumula métricas para análisis estadístico y graficación.
        # EN: Accumulates metrics for statistical analysis and plotting.
        self.alignment.append(alignment)
        self.risk_penalty.append(risk_penalty)
        self.purpose_gap.append(purpose_gap)

    def summarize(self) -> Dict[str, float]:
        # ES: Resumen simple; sustituir por ANOVA/bootstrapping en prod.
        # EN: Simple summary; replace with ANOVA/bootstrap in production.
        return {
            "alignment_mean": float(np.mean(self.alignment)),
            "risk_penalty_mean": float(np.mean(self.risk_penalty)),
            "purpose_gap_mean": float(np.mean(self.purpose_gap)),
        }


class TripwireMonitor:
    """Detección simple de gaming multi-horizonte / Simple multi-horizon gaming detector."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.triggers: List[Tuple[int, float]] = []

    def record(self, step: int, proxy_reward: float, ipg_score: float) -> bool:
        # ES: Dispara alerta si el proxy es alto pero IPG bajo (posible Goodhart).
        # EN: Fire alert when proxy is high but IPG low (possible Goodhart).
        if proxy_reward >= self.threshold and ipg_score < self.threshold:
            self.triggers.append((step, ipg_score))
            return True
        return False


class AntiOracleGate:
    """Anti-oráculo pragmático con bound inferior / Pragmatic anti-oracle with lower bound."""

    def __init__(self, uncertainty: float) -> None:
        self.uncertainty = uncertainty

    def approve(self, offline_estimate: float) -> bool:
        # ES: LCB simple; integrar doubly-robust y OPE en el código real.
        # EN: Simple LCB; plug doubly-robust + OPE in real code.
        lower_confidence_bound = offline_estimate - self.uncertainty
        return lower_confidence_bound > 0.0


def bootstrap_ci(values: List[float], samples: int = 500) -> Tuple[float, float]:
    # ES: Intervalo de confianza bootstrap (percentil 5-95) para reporte rápido.
    # EN: Bootstrap confidence interval (5-95 percentile) for quick reporting.
    if not values:
        return (float("nan"), float("nan"))
    draws = []
    for _ in range(samples):
        resample = np.random.choice(values, size=len(values), replace=True)
        draws.append(np.mean(resample))
    low, high = np.percentile(draws, [5, 95])
    return float(low), float(high)


def run_micro_episode(config: SimulationConfig, metrics: CausalMetricsBundle, tripwires: TripwireMonitor) -> Dict[str, float]:
    """Episodio sintético para ilustrar el pipeline completo.

    Synthetic episode to illustrate the end-to-end pipeline.
    """

    episode_reward = 0.0
    for step in range(config.horizon):
        # ES: Simulación ligera; reemplazar con SimbiosisEnv + agente real.
        # EN: Lightweight simulation; replace with SimbiosisEnv + real agent.
        proxy_reward = np.clip(np.random.normal(loc=0.6, scale=0.25), 0.0, 1.0)
        ipg_score = np.clip(proxy_reward - (config.risk_scale * 0.15), 0.0, 1.0)
        purpose_gap = max(0.0, 1.0 - ipg_score)
        metrics.update(alignment=ipg_score, risk_penalty=1 - proxy_reward, purpose_gap=purpose_gap)
        episode_reward += ipg_score - (config.risk_scale * 0.1)
        tripwires.record(step=step, proxy_reward=proxy_reward, ipg_score=ipg_score)
    return {"episode_reward": episode_reward}


def run_micro_simulation(config: SimulationConfig) -> Dict[str, object]:
    """Pipeline completo con gating, tripwires y bootstrap de métricas.

    Full pipeline with gating, tripwires, and metric bootstrapping.
    """

    config.apply()
    metrics = CausalMetricsBundle()
    tripwires = TripwireMonitor(threshold=config.tripwire_threshold)
    gate = AntiOracleGate(uncertainty=config.offline_uncertainty)

    rewards: List[float] = []
    for _ in range(config.episodes):
        result = run_micro_episode(config, metrics, tripwires)
        rewards.append(result["episode_reward"])

    offline_estimate = float(np.mean(rewards))
    approved = gate.approve(offline_estimate)
    reward_ci = bootstrap_ci(rewards, samples=config.bootstrap_samples)

    return {
        "offline_estimate": offline_estimate,
        "approved_by_gate": approved,
        "reward_ci": reward_ci,
        "metric_summary": metrics.summarize(),
        "tripwire_events": tripwires.triggers,
    }


if __name__ == "__main__":
    demo_config = SimulationConfig(episodes=3, horizon=6, risk_scale=1.2)
    report = run_micro_simulation(demo_config)
    # ES: Imprime un resumen legible para copiar/pegar en VS Code y extender.
    # EN: Prints a readable summary ready to copy/paste into VS Code for extension.
    for key, value in report.items():
        print(f"{key}: {value}")
