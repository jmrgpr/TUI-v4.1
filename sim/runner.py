"""
Runner para experimentos RL TUI v4.1
"""
import numpy as np
import torch
import random
from .environment import SimbiosisEnv
from sim.dqn_agent import DQNAgent
from sim.evaluator_pgf import EvaluatorPGF
from . import config
from .agent import Agent, Event


def state_to_vector(state):  # pragma: no cover - helper redundante cubierto en otros tests
    """Convierte el estado en un vector de floats para DQNAgent, extrayendo solo los valores numericos."""
    if isinstance(state, dict):
        return np.array(list(state.values()), dtype=np.float32)
    elif isinstance(state, (list, tuple)):
        # Si es una lista/tupla de pares (clave, valor), extraer solo los valores
        if all(isinstance(x, (list, tuple)) and len(x) == 2 for x in state):
            return np.array([float(x[1]) for x in state], dtype=np.float32)
        else:
            return np.array([float(x) for x in state], dtype=np.float32)
    else:
        # Fallback: si el estado es escalar
        return np.array([float(state)], dtype=np.float32)


def run_experiment(episodes, seed, risk_scale, agent_name, use_pgf=False, use_dqn=False, pgf_mix: float = 1.0):
    def pad_trajectories(trajectories, max_steps=config.ENV_MAX_STEPS_PER_EPISODE, pad_value=np.nan):
        padded = np.full((len(trajectories), max_steps), pad_value, dtype=np.float32)
        for i, traj in enumerate(trajectories):
            length = min(len(traj), max_steps)
            padded[i, :length] = traj[:length]
        return padded
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():  # pragma: no cover - dependencia de GPU
        torch.cuda.manual_seed_all(seed)  # pragma: no cover
        torch.backends.cudnn.deterministic = True  # pragma: no cover
        torch.backends.cudnn.benchmark = False  # pragma: no cover
    env = SimbiosisEnv(risk_scale=risk_scale)
    evaluator = EvaluatorPGF()
    state_dim = len(env.get_abstract_state())
    action_dim = len(config.AGENT_ACTIONS)
    total_rewards = []
    flex_recov = []
    robust_evol = []
    q_optimal = []
    tripwire_steps = []
    pgf_evol = []
    pgf_bruto_evol = []
    pgf_costo_evol = []
    reward_env_evol = []
    survival_evol = []
    shocks_evol = []
    agent = None
    for ep in range(episodes):
        if (ep+1) % 10 == 0 or ep == 0:
            print(f"Progreso / Progress: Episodio {ep+1}/{episodes}")
        state = env.reset()
        if use_dqn:
            agent = DQNAgent(state_dim, action_dim)
        else:
            agent = Agent(name=agent_name, resources=config.ENV_INITIAL_RESOURCES)
        agent.P_riesgo = 0.0
        agent.P_riesgo_prev = 0.0
        agent.resources = env.resources
        total_reward = 0.0
        steps_to_recover = None
        tripwire_count = 0
        shock_count = 0
        pgf_steps = []
        pgf_bruto_steps = []
        pgf_costo_steps = []
        reward_env_steps = []
        q_optimal_steps = []
        flex_steps = []
        robust_steps = []
        last_metrics = None
        for step in range(config.ENV_MAX_STEPS_PER_EPISODE):
            if use_dqn:
                state_vec = np.array([v for _, v in state], dtype=np.float32)
                action_idx = agent.act(state_vec)
                action = config.AGENT_ACTIONS[action_idx]
            else:
                action = agent.act(state)
            next_state, reward_env, done, info = env.step(action)
            metrics = evaluator.calcular_metricas(env, info, step, agent.resources if hasattr(agent, 'resources') else env.resources, getattr(agent, 'purpose', 'survive_and_help'), getattr(agent, 'alignment', 1.0))
            last_metrics = metrics
            pgf_steps.append(metrics['PGF'])
            pgf_bruto_steps.append(metrics.get('PGF_Bruto', 0.0))
            pgf_costo_steps.append(metrics.get('PGF_Costo', 0.0))
            mixed = max(0.0, min(1.0, pgf_mix))
            r_pgf = metrics['PGF'] * mixed + reward_env * (1.0 - mixed) if use_pgf else reward_env
            if use_dqn:
                next_state_vec = np.array([v for _, v in next_state], dtype=np.float32)
                agent.remember(state_vec, action_idx, r_pgf, next_state_vec, done)
                agent.learn()
            else:
                agent.update_policy(state, action, r_pgf, next_state)
                agent.remember(Event())
            total_reward += r_pgf
            reward_env_steps.append(reward_env)
            flex_steps.append(metrics['F'])
            robust_steps.append(metrics['R_robust'])
            if use_dqn:
                q_vals = agent.model(torch.FloatTensor(state_to_vector(state)).unsqueeze(0)).detach().cpu().numpy()[0]
                optimal_action_idx = int(np.argmax(q_vals))
                q_optimal_steps.append(1 if action_idx == optimal_action_idx else 0)
            else:
                q_vals = [agent.policy.get((state, a), 0.0) for a in config.AGENT_ACTIONS]
                optimal_action = config.AGENT_ACTIONS[int(np.argmax(q_vals))]
                q_optimal_steps.append(1 if action == optimal_action else 0)
            if info.get('shock') and steps_to_recover is None:
                steps_to_recover = 0
            if steps_to_recover is not None:
                steps_to_recover += 1
            if info.get('tripwire'):
                tripwire_count += 1
            if info.get('shock'):
                shock_count += 1
            if done:
                break
        total_rewards.append(total_reward)
        flex_recov.append(np.mean(flex_steps) if flex_steps else 0.0)
        robust_evol.append(np.mean(robust_steps) if robust_steps else 0.0)
        tripwire_steps.append(tripwire_count)
        shocks_evol.append(shock_count)
        pgf_evol.append(pgf_steps)
        pgf_bruto_evol.append(pgf_bruto_steps)
        pgf_costo_evol.append(pgf_costo_steps)
        reward_env_evol.append(reward_env_steps)
        q_optimal.append(np.mean(q_optimal_steps))
        survival_evol.append(agent.resources)
    if agent is not None and not use_dqn:
        agent.reprogram_purpose("survive_and_help")

    # Manejo robusto de promedios para el caso de 0 episodios
    avg_reward = np.mean(total_rewards) if total_rewards else 0.0
    avg_flex = np.mean(flex_recov) if flex_recov else 0.0
    avg_robust = np.mean(robust_evol) if robust_evol else 0.0
    avg_tripwire = np.mean(tripwire_steps) if tripwire_steps else 0.0
    avg_q_opt = np.mean(q_optimal) if q_optimal else 0.0
    avg_shocks = np.mean(shocks_evol) if shocks_evol else 0.0
    avg_survival = np.mean(survival_evol) if survival_evol else 0.0

    max_steps = config.ENV_MAX_STEPS_PER_EPISODE
    pgf_padded = pad_trajectories(pgf_evol, max_steps)
    pgf_bruto_padded = pad_trajectories(pgf_bruto_evol, max_steps)
    pgf_costo_padded = pad_trajectories(pgf_costo_evol, max_steps)
    reward_env_padded = pad_trajectories(reward_env_evol, max_steps)
    # Si no se ha instanciado ningun agente (episodes=0), devolver politica vacia
    if agent is None:
        policy = {}
    else:
        policy = agent.model.state_dict() if use_dqn else agent.policy
    return {
        "avg_reward": avg_reward,
        "avg_flex": avg_flex,
        "avg_robust": avg_robust,
        "avg_tripwire": avg_tripwire,
        "avg_q_opt": avg_q_opt,
        "avg_shocks": avg_shocks,
        "avg_survival": avg_survival,
        "total_rewards": total_rewards,
        "tripwire_steps": tripwire_steps,
        "shocks_evol": shocks_evol,
        "pgf_evol": pgf_evol,
        "pgf_bruto_evol": pgf_bruto_evol,
        "pgf_costo_evol": pgf_costo_evol,
        "reward_env_evol": reward_env_evol,
        "pgf_evol_padded": pgf_padded.tolist(),
        "pgf_bruto_padded": pgf_bruto_padded.tolist(),
        "pgf_costo_padded": pgf_costo_padded.tolist(),
        "reward_env_evol_padded": reward_env_padded.tolist(),
        "q_optimal_evol": q_optimal,
        "survival_evol": survival_evol,
        "flex_recov": flex_recov,
        "robust_evol": robust_evol,
        "policy": policy
    }
