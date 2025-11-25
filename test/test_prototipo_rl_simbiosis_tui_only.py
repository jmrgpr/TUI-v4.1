import sys

import sim.prototipo_rl_simbiosis as mod


def test_risk_sweep_includes_tui_only(monkeypatch, tmp_path):
    calls = []

    def fake_run_experiment(**kwargs):
        calls.append((kwargs["agent_name"], kwargs["use_pgf"], kwargs["use_dqn"]))
        return {
            "total_rewards": [0],
            "pgf_bruto_evol": [[1]],
            "pgf_costo_evol": [[1]],
            "pgf_bruto_padded": [[0]],
            "pgf_costo_padded": [[0]],
            "pgf_evol": [[0]],
            "tripwire_steps": [0],
            "avg_tripwire": 0,
            "avg_reward": 0,
        }

    monkeypatch.setattr(mod, "run_experiment", fake_run_experiment)
    for fn in ["figure", "subplot", "plot", "title", "xlabel", "ylabel", "legend", "grid", "tight_layout", "savefig", "close"]:
        monkeypatch.setattr(mod.plt, fn, lambda *a, **k: None)

    argv = [
        "prog",
        "--risk_sweep",
        "--episodes",
        "1",
        "--seed",
        "1",
        "--output_prefix",
        str(tmp_path / "out"),
        "--tui_only",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    mod.main()

    assert any(agent == "TUI" and use_pgf and not use_dqn for agent, use_pgf, use_dqn in calls)
