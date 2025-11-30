import json
import os
import csv
import sys
import torch

from sim.dqn_agent import DQNAgent
from sim import config
import sim.prototipo_rl_simbiosis as proto
import sim.dqn_agent as dqn_mod
from sim import runner as runner_mod


def test_prepare_results_and_writer(tmp_path):
    raw_results = {
        "policy": {("s", "a"): 1.0},
        "total_rewards": [1.0, 2.0],
        "tripwire_steps": [0, 1],
        "flex_recov": [0.1, 0.2],
        "robust_evol": [0.3, 0.4],
        "q_optimal_evol": [0.5, 0.6],
        "pgf_bruto_evol": [[0.7], [0.8]],
        "pgf_costo_evol": [[0.9], [1.0]],
    }
    cleaned = proto.prepare_results(raw_results)
    assert "policy" in cleaned
    # Escribir filas de episodios con listas disparejas
    csv_path = tmp_path / "episodes.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Agente", "Episodio", "Recompensa", "Tripwires", "Flexibilidad", "Robustez", "Q-optimal", "PGF_Bruto_Avg", "PGF_Costo_Avg"])
        proto.write_episode_rows(writer, "agent", raw_results)
    lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
    # 2 episodios + cabecera
    assert len(lines) == 3
    assert lines[1].startswith("agent,1,1.0")


def test_dqn_agent_learn_and_decay(monkeypatch):
    # Forzar determinismo en random para cubrir rama no aleatoria
    monkeypatch.setattr(dqn_mod.random, "random", lambda: 0.99)
    agent = DQNAgent(
        state_dim=2,
        action_dim=2,
        lr=1e-3,
        gamma=0.9,
        epsilon=0.25,
        epsilon_decay=0.1,
        epsilon_end=0.2,
        batch_size=2,
        target_update_freq=1,
        hidden_dim=4,
    )
    # Primera llamada: epsilon>epsilon_end y decae hasta el mínimo
    action = agent.act([0.0, 0.0])
    assert action in (0, 1)
    assert agent.epsilon == agent.epsilon_end
    # Llenar memoria y ejecutar learn para activar target_update_freq
    for _ in range(2):
        agent.remember([0.0, 0.0], 0, 1.0, [0.1, 0.1], False)
    agent.learn()
    # Forzar otra pasada por la red para cubrir forward completo
    _ = agent.model(torch.zeros(1, 2))


def test_prototipo_main_fast_export(monkeypatch, tmp_path):
    calls = {"count": 0}

    def fake_run_experiment(**_kwargs):
        calls["count"] += 1
        return {
            "avg_reward": 1.0,
            "avg_tripwire": 0.0,
            "avg_flex": 0.0,
            "avg_q_opt": 0.0,
            "avg_survival": 1.0,
            "total_rewards": [1.0],
            "tripwire_steps": [0],
            "flex_recov": [0.0],
            "robust_evol": [0.0],
            "pgf_evol": [[0.1]],
            "pgf_bruto_evol": [[0.2]],
            "pgf_costo_evol": [[0.3]],
            "reward_env_evol": [[0.4]],
            "q_optimal_evol": [0.0],
            "policy": {"s": 1},
        }

    monkeypatch.setattr(proto, "run_experiment", lambda **kwargs: fake_run_experiment(**kwargs))
    prefix = tmp_path / "smoke" / "exp_test"
    argv = [
        "prog",
        "--episodes",
        "2",
        "--seed",
        "1",
        "--risk_scale",
        "0.5",
        "--fast",
        "--sigma_thr",
        "0.5",
        "--gamma_lcb",
        "0.7",
        "--lambda_gaming",
        "0.1",
        "--dqn_control",
        "--output_prefix",
        str(prefix),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    proto.main()
    # Se debe haber llamado a run_experiment para control y simbiosis y DQN-Control
    assert calls["count"] >= 2
    json_path = prefix.with_suffix(".json")
    csv_path = prefix.with_name(prefix.name + "_episodes").with_suffix(".csv")
    assert json_path.exists()
    assert csv_path.exists()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    # Debe incluir trazabilidad de dqn_params cuando dqn_control está activo
    assert "dqn_params" in data


def test_prototipo_risk_sweep_short_circuit(monkeypatch, tmp_path):
    monkeypatch.setattr(proto, "run_experiment", lambda **kwargs: {})
    argv = [
        "prog",
        "--risk_sweep",
        "--episodes",
        "1",
        "--seed",
        "0",
        "--risk_scale",
        "0.1",
        "--output_prefix",
        str(tmp_path / "unused"),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    # Debe salir pronto sin lanzar excepciones aunque el cuerpo esté stubbeado
    proto.main()


def test_environment_risky_branches(monkeypatch):
    from sim import environment as env_mod
    SimbiosisEnv = env_mod.SimbiosisEnv

    original_probs = (
        config.EXP_CONFIG["red_team_prob"],
        config.EXP_CONFIG["red_team_move_tripwire_prob"],
        config.EXP_CONFIG["red_team_add_shock_prob"],
    )
    config.EXP_CONFIG["red_team_prob"] = 1.0
    config.EXP_CONFIG["red_team_move_tripwire_prob"] = 1.0
    config.EXP_CONFIG["red_team_add_shock_prob"] = 0.0
    env = SimbiosisEnv(
        tripwires=[(0, 0)],
        shocks=[(0, 0)],
        distractors=[(0, 0)],
        risk_scale=2.0,
        risk_level="high",
        red_team_mode=True,
        goal_pos=(1, 1),
    )
    env.timestep = config.ENV_MAX_STEPS_PER_EPISODE
    # Forzar determinismo en red team: primer rand activa evento, segundo selecciona mover tripwire
    sequence = iter([0.0, 0.0])
    monkeypatch.setattr(env_mod.np.random, "rand", lambda: next(sequence))
    monkeypatch.setattr(env_mod.np.random, "randint", lambda _size: 0)
    state, reward, done, info = env.step("noop")
    assert info.get("tripwire") is True
    assert info.get("shock") is True
    assert info.get("distractor") is True
    assert info.get("risk_penalty_applied") is True
    # Restaurar probabilidades originales
    config.EXP_CONFIG["red_team_prob"], config.EXP_CONFIG["red_team_move_tripwire_prob"], config.EXP_CONFIG["red_team_add_shock_prob"] = original_probs


def test_runner_branches(monkeypatch):
    # Reducir umbral para activar gating en control
    original_sigma = config.EXP_CONFIG["sigma_thr"]
    config.EXP_CONFIG["sigma_thr"] = -1.0

    class FakeEnv:
        def __init__(self, risk_scale, risk_level, red_team_mode):
            self.risk_scale = risk_scale
            self.risk_level = risk_level
            self.red_team_mode = red_team_mode
            self.size = 2
            self.resources = 1.0
            self.incident_count = 0
            self.step_count = 0

        def reset(self):
            self.step_count = 0
            return (("coord_x", 0), ("coord_y", 1))

        def get_abstract_state(self):
            return (("coord_x", 0), ("coord_y", 1), ("foo", 1.0))

        def step(self, action):
            self.step_count += 1
            self.incident_count += 1
            info = {
                "tripwire": True,
                "shock": True,
                "gap_proxy_value": 0.1 * self.incident_count,
                "is_gaming": True,
                "u_proxy": 0.2 * self.incident_count,
                "u_humans": 0.1 * self.incident_count,
                "sigma": 0.0,
            }
            reward = 0.5 * self.incident_count
            done = True
            return (("coord_x", 0), ("coord_y", 1)), reward, done, info

    class FakeEval:
        def calcular_metricas(self, env, info, step, resources, purpose, alignment):
            return {"PGF": 0.3 + step, "PGF_Bruto": 0.2, "PGF_Costo": 0.1, "F": 0.4, "R_robust": 0.5}

    class FakeAgent:
        def __init__(self, name=None, resources=None):
            self.policy = {}
            self.resources = resources or 1.0
            self.purpose = "p"
            self.alignment = 1.0

        def act(self, state):
            return "right"

        def predict_with_uncertainty(self, state):
            raise ValueError("force")

        def update_policy(self, *args, **kwargs):
            return None

        def remember(self, _event):
            return None

        def reprogram_purpose(self, _p):
            self.purpose = _p

    class FakeDQN:
        def __init__(self, *args, **kwargs):
            self.model = self

        def act(self, state):
            return 0

        def remember(self, *args, **kwargs):
            return None

        def learn(self):
            return None

        def __call__(self, _tensor):
            return torch.tensor([[0.1, 0.9]], dtype=torch.float32)

        def state_dict(self):
            return {"w": 1.0}

    def raise_corrcoef(*_args, **_kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(runner_mod, "SimbiosisEnv", FakeEnv)
    monkeypatch.setattr(runner_mod, "EvaluatorPGF", FakeEval)
    monkeypatch.setattr(runner_mod, "Agent", FakeAgent)
    monkeypatch.setattr(runner_mod, "DQNAgent", FakeDQN)
    monkeypatch.setattr(runner_mod.np, "corrcoef", raise_corrcoef)

    # DQN coords_only cubre state_dim=2 y q_opt coords
    result_dqn = runner_mod.run_experiment(
        episodes=2,
        seed=1,
        risk_scale=0.5,
        agent_name="DQN",
        use_pgf=True,
        use_dqn=True,
        pgf_mix=0.5,
        risk_level="low",
        red_team=False,
        state_mode="coords_only",
    )
    assert result_dqn["avg_reward"] >= 0.0
    # DQN modo abstracto para q_vals estándar
    result_dqn_abstract = runner_mod.run_experiment(
        episodes=1,
        seed=3,
        risk_scale=0.5,
        agent_name="DQN",
        use_pgf=True,
        use_dqn=True,
        pgf_mix=0.5,
        risk_level="low",
        red_team=False,
    )
    assert "q_optimal_evol" in result_dqn_abstract
    # Control con gating y excepción en predict_with_uncertainty
    result_ctrl = runner_mod.run_experiment(
        episodes=2,
        seed=2,
        risk_scale=0.5,
        agent_name="Control",
        use_pgf=False,
        use_dqn=False,
        pgf_mix=1.0,
        risk_level="low",
        red_team=False,
    )
    assert result_ctrl["gating_hits"] >= 1
    config.EXP_CONFIG["sigma_thr"] = original_sigma


def test_visualizaciones_profesional(tmp_path):
    from sim.visualizaciones import boxplot_metricas_profesional

    export_path = tmp_path / "boxplot.png"
    boxplot_metricas_profesional([1, 2, 3], [2, 3, 4], "Test", export_path=export_path)
    assert export_path.exists()
