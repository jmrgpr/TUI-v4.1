import math

import pytest

from sim.environment_v2 import ResourceDensityEnv


def test_resource_density_env_max_steps_and_step_cost():
    env = ResourceDensityEnv(
        size=16,
        initial_resources=5.0,
        resource_spawn_rate=0.0,
        step_cost=-0.5,
        max_steps_multiplier=5.0,
    )

    env.reset()

    assert env.max_steps == (16 - 1) * 2 * 5  # Manhattan (30) * multiplier (5)

    _, reward, done, info = env.step("noop")

    assert pytest.approx(env.resources, rel=1e-5) == 4.5
    assert pytest.approx(reward, rel=1e-5) == -0.5
    assert not done
    assert "density_metrics" in info
    assert info["density_metrics"]["resources_on_grid"] >= 0


def test_resource_collection_and_spawn_cycle():
    env = ResourceDensityEnv(
        size=4,
        initial_resources=8.0,
        resource_spawn_rate=1.0,
        resource_reward=2.0,
        max_resources_on_grid=1,
        step_cost=0.0,
        resource_decay_steps=10,
    )

    env.reset()
    assert len(env.resource_positions) == 1

    resource_pos = next(iter(env.resource_positions))
    env.agent_pos = list(resource_pos)

    _, reward, _, info = env.step("noop")

    assert info.get("resource_collected") is True
    assert pytest.approx(reward, rel=1e-5) == 2.0
    assert env.total_resources_collected == 1
    assert info["density_metrics"]["total_collected"] == 1


def test_compute_d_effective_uses_cells_and_collection_times():
    env = ResourceDensityEnv(size=4, resource_spawn_rate=0.25)

    env.cells_visited = {(0, 0), (0, 1), (1, 1)}
    env.resource_collection_times = [2, 4]

    metrics = env.compute_D_effective()

    assert math.isclose(metrics["p_acceso"], 3 / 16)
    assert math.isclose(metrics["tau_consumo"], 3.0)
    assert math.isclose(metrics["D_effective"], 0.25)
    assert metrics["cells_visited"] == 3
    assert metrics["total_cells"] == 16
