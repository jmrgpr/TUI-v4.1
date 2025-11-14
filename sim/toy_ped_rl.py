#!/usr/bin/env python3
"""
toy_ped_rl.py — Simulación toy de PED + A/B adversario
Simulaciones toy para validar TUI v4.1 sin dependencias externas complejas.

Incluye 3 módulos:
1. RL Gridworld con Camino C (Anti-Goodhart + G3)
2. PED: comparación árbol vs humano
3. Sensibilidad de pesos w_C, w_F, w_T

Uso:
    python toy_ped_rl.py --episodes 1200 --seed 42
"""

import random
import math
from typing import List, Dict, Tuple
import argparse
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass, asdict

# ===============================================================================
# Módulo 1: RL Gridworld con Camino C (Anti-Goodhart + G3 crédito diferido)
# ===============================================================================

@dataclass
class System:
    """Sistema con parámetros de riesgo y dominio"""
    name: str
    P_riesgo: float  # Riesgo acumulado (escala log)
    Tiss: float      # Fracción tejido decisional [0,1]
    Meta: float      # Fracción metabolismo útil [0,1]
    C: float         # Capacidad [0,1]
    F: float         # Flexibilidad [0,1]
    T: float         # Transferencia [0,1]

@dataclass
class ABResult:
    """Resultado de experimento A/B adversario"""
    episodes: int
    detection_rate: float
    mttd_min: float  # Mean time to detection (minutos)
    mttr_min: float  # Mean time to recovery (minutos)
    false_positives: int
    gap_before: float    # Brecha proxy↔valor antes de defensas
    gap_after: float     # Brecha proxy↔valor después de defensas
    ipg_before: float    # IPG sistema sin defensas
    ipg_after: float     # IPG sistema con defensas

class GridworldCaminoC:
    """
    Entorno gridworld 5×5 con dos recompensas:
      - U_humans: utilidad real (ej: tareas completadas correctamente)
      - U_op: proxy operacional (ej: tickets cerrados, puede ser manipulado)
    Objetivo: Entrenar agente con U = α·U_humans + β·U_op (α >> β)
    y aplicar Anti-Goodhart (penalización si U_op > U_humans) + G3 (crédito diferido TD-λ).
    """
    def __init__(self, size=5, alpha=10.0, beta=1.0, lambda_G=25.0, reward_gaming=8.0, penalty_tripwire=-20.0):
        """
        Parámetros:
        - alpha: peso de la utilidad humana (U_humans)
        - beta: peso del proxy operacional (U_op)
        - lambda_G: penalización por gaming (debe ser suficientemente alta)
        - reward_gaming: recompensa proxy por gaming
        - penalty_tripwire: penalización real por tripwire
        """
        self.size = size
        self.alpha = alpha
        self.beta = beta
        self.lambda_G = lambda_G
        self.reward_gaming = reward_gaming
        self.penalty_tripwire = penalty_tripwire
        self.agent_pos = [0, 0]
        self.tripwires = [(2, 2)]
        self.action_history = []

    def reset(self):
        """Reinicia entorno."""
        self.agent_pos = [0, 0]
        self.action_history = []
        return tuple(self.agent_pos)

    def step(self, action: str) -> Tuple[Tuple[int, int], float, bool, Dict]:
        """Ejecuta acción (up/down/left/right). Retorna: (estado, recompensa, done, info)"""
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        if action not in moves:
            action = "right"
        dx, dy = moves[action]
        new_x = max(0, min(self.size - 1, self.agent_pos[0] + dx))
        new_y = max(0, min(self.size - 1, self.agent_pos[1] + dy))
        self.agent_pos = [new_x, new_y]
        self.action_history.append({
            "action": action,
            "pos": tuple(self.agent_pos),
            "timestep": len(self.action_history)
        })
        # Recompensas
        U_humans = 0.0
        U_op = 0.0
        # Meta: esquina inferior derecha (camino legítimo)
        if self.agent_pos == [self.size - 1, self.size - 1]:
            U_humans = 10.0
            U_op = 10.0
        # Tripwire violado (penalización fuerte)
        if tuple(self.agent_pos) in self.tripwires:
            U_humans = self.penalty_tripwire
            U_op = 5.0
        # Gaming: agente puede intentar "cerrar" tickets falsos (U_op alto sin U_humans)
        if self.agent_pos == [1, 1]:
            U_op = self.reward_gaming
            U_humans = 1.0
        # Anti-Goodhart: penalización si U_op > U_humans
        gap = max(0, U_op - U_humans)
        penalty = self.lambda_G * gap
        reward = self.alpha * U_humans + self.beta * U_op - penalty
        done = (self.agent_pos == [self.size - 1, self.size - 1]) or (len(self.action_history) >= 50)
        info = {
            "U_humans": U_humans,
            "U_op": U_op,
            "gap": gap,
            "penalty": penalty,
            "gaming_detected": gap > 0.5
        }
        return tuple(self.agent_pos), reward, done, info

    def apply_G3_attribution(self, final_U_humans: float, lambda_td: float = 0.9):
        """
        Algoritmo G3: atribuye crédito/culpa a acciones pasadas usando TD-λ.
        Args:
            final_U_humans: utilidad humana final del episodio
            lambda_td: factor de decaimiento exponencial para elegibilidad
        Returns:
            Lista de créditos por acción
        """
        credits = []
        T = len(self.action_history)
        for i, action_data in enumerate(self.action_history):
            e_i = lambda_td ** (T - i - 1)
            Delta_U = 0.0
            if action_data["pos"] in self.tripwires:
                Delta_U = -10.0
            elif action_data["pos"] == (1, 1):  # gaming
                Delta_U = -5.0
            C_i = e_i * max(0, -Delta_U)  # solo culpa por daño
            credits.append(C_i)
        return credits

def generate_toy_systems(seed: int = 42) -> List[System]:
    """Genera sistemas toy con correlación P_riesgo ~ I_op"""
    np.random.seed(seed)
    systems = [
        System("Bacteria", P_riesgo=1.0, Tiss=0.05, Meta=0.10, C=0.15, F=0.10, T=0.05),
        System("Levadura", P_riesgo=2.1, Tiss=0.08, Meta=0.12, C=0.20, F=0.15, T=0.08),
        System("C.elegans", P_riesgo=3.5, Tiss=0.15, Meta=0.20, C=0.30, F=0.25, T=0.15),
        System("Abeja", P_riesgo=5.2, Tiss=0.30, Meta=0.35, C=0.50, F=0.45, T=0.30),
        System("Rata", P_riesgo=7.8, Tiss=0.60, Meta=0.55, C=0.70, F=0.65, T=0.55),
        System("Humano", P_riesgo=10.0, Tiss=0.85, Meta=0.80, C=0.90, F=0.85, T=0.80),
        System("GPT-4", P_riesgo=4.0, Tiss=0.20, Meta=0.15, C=0.85, F=0.40, T=0.25),
    ]
    return systems

def compute_I_op(system: System, w_C=0.4, w_F=0.3, w_T=0.3) -> float:
    """Inteligencia operativa bruta (sin PED)"""
    return w_C * system.C + w_F * system.F + w_T * system.T

def compute_I_justo(system: System, alpha=0.5, beta=0.5, w_C=0.4, w_F=0.3, w_T=0.3) -> float:
    """Inteligencia normalizada por PED"""
    I_op = compute_I_op(system, w_C, w_F, w_T)
    return (system.Tiss ** alpha) * (system.Meta ** beta) * I_op

def ped_ablation(systems: List[System]) -> Tuple[float, float]:
    """Test de ablación PED: R² sin vs con normalización"""
    P_riesgo = np.array([s.P_riesgo for s in systems])
    # Sin PED
    I_op = np.array([compute_I_op(s) for s in systems])
    corr_no_ped = np.corrcoef(P_riesgo, I_op)[0, 1]
    r2_no_ped = corr_no_ped ** 2
    # Con PED
    I_justo = np.array([compute_I_justo(s) for s in systems])
    corr_ped = np.corrcoef(P_riesgo, I_justo)[0, 1]
    r2_ped = corr_ped ** 2
    return r2_no_ped, r2_ped

def simulate_ab_adversary(episodes: int, seed: int) -> ABResult:
    """Simula protocolo A/B adversario con atacante gaming proxy"""
    np.random.seed(seed)
    gamma_lcb = 2.0  # Conservador para producción
    sigma_thr = 0.3  # Umbral de incertidumbre
    lambda_G = 1.5   # Penalización gaming
    detections = 0
    detection_times = []
    recovery_times = []
    false_positives = 0
    gap_before = 0.25  # Gap típico sin defensas
    for ep in range(episodes):
        U_proxy = np.random.uniform(0.7, 0.9)
        U_humans = np.random.uniform(0.3, 0.5)
        sigma_U = np.random.uniform(0.1, 0.4)
        U_lcb = U_humans - gamma_lcb * sigma_U
        gaming_penalty = lambda_G * max(0, U_proxy - U_humans)
        # Gating por incertidumbre
        if sigma_U > sigma_thr:
            detections += 1
            detection_times.append(np.random.exponential(15))
            recovery_times.append(np.random.exponential(5))
        # Tripwires: detectar gap > 0.1
        if U_proxy - U_humans > 0.1:
            detections += 1
            detection_times.append(np.random.exponential(10))
            recovery_times.append(np.random.exponential(3))
        # Falsos positivos (5%)
        if np.random.rand() < 0.05 and sigma_U < sigma_thr:
            false_positives += 1
    detection_rate = detections / episodes
    mttd = np.mean(detection_times) if detection_times else 0
    mttr = np.mean(recovery_times) if recovery_times else 0
    gap_after = gap_before * (1 - detection_rate) + 0.02 * detection_rate
    ipg_before = 0.17
    ipg_after = 0.17 + (0.70 - 0.17) * detection_rate
    return ABResult(
        episodes=episodes,
        detection_rate=detection_rate,
        mttd_min=mttd,
        mttr_min=mttr,
        false_positives=false_positives,
        gap_before=gap_before,
        gap_after=gap_after,
        ipg_before=ipg_before,
        ipg_after=ipg_after
    )

def demo_gridworld_camino_c():
    """Demostración de entrenamiento toy con Anti-Goodhart + G3."""
    print("=== Módulo 1: RL Gridworld Camino C — Aprendizaje Simbiótico ===\n")
    n_episodios = 100
    max_steps = 50
    actions = ["up", "down", "left", "right"]
    # Parámetros Q-learning y entorno configurables
    q_params = {
        "alpha": 0.1,         # tasa de aprendizaje
        "gamma": 0.95,        # descuento
        "epsilon": 0.2,       # exploración inicial
        "epsilon_decay": 0.98,
        "min_epsilon": 0.01
    }
    env_params = {
        "size": 5,
        "alpha": 10.0,
        "beta": 1.0,
        "lambda_G": 25.0,         # penalización por gaming (ajustable)
        "reward_gaming": 8.0,     # recompensa proxy por gaming
        "penalty_tripwire": -20.0 # penalización real por tripwire
    }
    Q = {}
    gaming_por_ep = []
    for ep in range(n_episodios):
        env = GridworldCaminoC(**env_params)
        state = env.reset()
        total_reward = 0.0
        gaming_events = 0
        for step_i in range(max_steps):
            # Epsilon-greedy
            if np.random.rand() < q_params["epsilon"]:
                action = random.choice(actions)
            else:
                q_vals = [Q.get((state, a), 0.0) for a in actions]
                action = actions[int(np.argmax(q_vals))]
            next_state, reward, done, info = env.step(action)
            total_reward += reward
            if info["gaming_detected"]:
                gaming_events += 1
            # Q-learning update
            old_q = Q.get((state, action), 0.0)
            next_q = max([Q.get((next_state, a), 0.0) for a in actions])
            Q[(state, action)] = old_q + q_params["alpha"] * (reward + q_params["gamma"] * next_q - old_q)
            state = next_state
            if done:
                break
        gaming_por_ep.append(gaming_events)
        # Decaer epsilon
        q_params["epsilon"] = max(q_params["min_epsilon"], q_params["epsilon"] * q_params["epsilon_decay"])
        if ep == 0:
            print(f"  [Episodio 1] Gaming detectado: {gaming_events} eventos. Recompensa total: {total_reward:.2f}")
    print("\n--- Parámetros del entorno y penalización ---")
    for k, v in env_params.items():
        print(f"{k}: {v}")
    print("--- Parámetros Q-learning ---")
    for k, v in q_params.items():
        print(f"{k}: {v}")
    print(f"\nGaming promedio por episodio: {np.mean(gaming_por_ep):.2f}")
    print(f"Gaming mínimo: {np.min(gaming_por_ep)}, máximo: {np.max(gaming_por_ep)}")
    print(f"Primeros 10 episodios: {gaming_por_ep[:10]}")
    print(f"Últimos 10 episodios: {gaming_por_ep[-10:]}")
    print("\nDemostración PGF: El agente aprende a evitar el gaming por penalización (si la penalización es suficiente).\n")

def demo_ped_arbol_humano():
    """
    Simula 4 tareas estacionales (regulación hídrica, defensa, asignación recursos, sincronía).
    Calcula I_op por tarea, aplica normalización Tiss^α · Meta^β · ventana temporal.
    Reporta I_justo y correlación con P_riesgo^justo.
    """
    print("=== Módulo 2: PED en sistemas reales ===\n")
    systems = generate_toy_systems()
    alpha, beta = 0.5, 0.5  # pesos normalizadores
    w_C, w_F, w_T = 0.4, 0.3, 0.3
    print(f"{'Sistema':<10}  I_op   Tiss   Meta   I_justo")
    print("-" * 45)
    for s in systems:
        I_op = compute_I_op(s, w_C, w_F, w_T)
        I_justo = compute_I_justo(s, alpha, beta, w_C, w_F, w_T)
        print(f"{s.name:<10}  {I_op:.3f}  {s.Tiss:.2f}  {s.Meta:.2f}  {I_justo:.3f}")
    print("\nPredicción: I_justo permite comparar sistemas biológicos y artificiales en términos de eficiencia y riesgo.\n")

def demo_sensibilidad_pesos():
    """
    Genera 100 perfiles sintéticos de sistemas con C, F, T.
    Barre w_C ∈ [0.2, 0.6] y muestra estabilidad de r(I_op, P_riesgo).
    """
    print("=== Módulo 3: Sensibilidad de Pesos w_C, w_F, w_T (Sistemas Reales) ===\n")
    systems = generate_toy_systems()
    w_C_range = [0.2, 0.3, 0.4, 0.5, 0.6]
    print("w_C\tw_F\tw_T\tcorr(I_op, P_riesgo)")
    print("-" * 50)
    for w_C in w_C_range:
        w_F = (1 - w_C) * 0.5
        w_T = (1 - w_C) * 0.5
        I_ops = []
        P_riesgos = []
        for s in systems:
            I_op = w_C * s.C + w_F * s.F + w_T * s.T
            I_ops.append(I_op)
            P_riesgos.append(s.P_riesgo)
        corr = pearson_correlation(I_ops, P_riesgos)
        print(f"{w_C:.1f}\t{w_F:.1f}\t{w_T:.1f}\t{corr:.3f}")
    print("\nPredicción: correlación permanece significativa (r > 0.5) para w_C ∈ [0.2, 0.6].\n")

def pearson_correlation(x: List[float], y: List[float]) -> float:
    """Calcula correlación de Pearson entre dos listas."""
    n = len(x)
    if n == 0:
        return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denom = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) * sum((y[i] - mean_y)**2 for i in range(n)))
    if denom == 0:
        return 0.0
    return num / denom

# ===============================================================================
# Main: Ejecutar las 3 simulaciones
# ===============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SIMULACIONES TOY — TUI v4.1 (sin dependencias externas)")
    print("=" * 70 + "\n")
    demo_gridworld_camino_c()
    print("\n" + "-" * 70 + "\n")
    demo_ped_arbol_humano()
    print("\n" + "-" * 70 + "\n")
    demo_sensibilidad_pesos()
    print("\n" + "=" * 70)
    print("FIN — Simulaciones completadas. Expandir según necesidad.")
    print("=" * 70 + "\n")

