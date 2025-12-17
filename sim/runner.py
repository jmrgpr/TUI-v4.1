"""
Runner para experimentos RL TUI v4.1
"""
import numpy as np
import torch
import random
from sim.environment import SimbiosisEnv
from sim.dqn_agent import DQNAgent
from sim.evaluator_pgf import EvaluatorPGF
import sim.config as config
from sim.agent import Agent, Event


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


def _behavior_prob(agent, state, action):
    """
    Estima probabilidad de comportamiento para OPE-DR.
    Intenta usar métodos del agente; si no, asume uniforme.
    """
    if hasattr(agent, "behavior_prob"):
        try:
            p = agent.behavior_prob(state, action)
            if p is not None:
                return float(p)
        except Exception:
            pass
    # fallback uniforme
    return 1.0 / len(config.AGENT_ACTIONS)


def _target_prob(agent, state, action):
    """
    Estima probabilidad de la política target para OPE-DR.
    Si no hay método, asume política determinista sobre acción elegida.
    """
    if hasattr(agent, "target_prob"):
        try:
            p = agent.target_prob(state, action)
            if p is not None:
                return float(p)
        except Exception:
            pass
    return 1.0


def run_experiment(
    episodes,
    seed,
    risk_scale,
    agent_name,
    use_pgf=False,
    use_dqn=False,
    pgf_mix: float = 1.0,
    risk_level: str = "low",
        red_team: bool = False,
        grid_size: int = 5,
        **kwargs):
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
    env = SimbiosisEnv(risk_scale=risk_scale, risk_level=risk_level, red_team_mode=red_team, size=grid_size)
    # Logging explícito para trazabilidad
    print(f"✓ Entorno creado: grid {env.size}x{env.size}, meta en {env.goal_pos}, risk_scale={risk_scale}")
    evaluator = EvaluatorPGF()
    # Modo debug para tuning: usar solo coords como estado
    state_mode = kwargs.get('state_mode', 'abstract')
    if state_mode == 'coords_only':
        state_dim = 2
    else:
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
    u_proxy_all = []
    u_humans_all = []
    ope_weights = []
    ope_rewards = []
    total_gaps = []
    all_actions = []
    gaming_hits_total = 0
    gating_hits_total = 0
    # Extraer hiperparámetros DQN de kwargs o usar los de config
    dqn_lr = kwargs.get('learning_rate', None)
    dqn_gamma = kwargs.get('gamma', None)
    dqn_epsilon = kwargs.get('epsilon', None)
    dqn_epsilon_decay = kwargs.get('epsilon_decay', None)
    dqn_epsilon_end = kwargs.get('epsilon_end', None)
    # Defaults centralizados (usar hiperparámetros DQN del config)
    DEFAULT_LR = getattr(config, 'DQN_LEARNING_RATE', getattr(config, 'AGENT_LEARNING_RATE', 1e-3))
    DEFAULT_GAMMA = getattr(config, 'DQN_GAMMA', getattr(config, 'AGENT_DISCOUNT_FACTOR', 0.95))
    DEFAULT_EPSILON = getattr(config, 'DQN_EPSILON', getattr(config, 'AGENT_EXPLORATION_RATE', 0.2))
    DEFAULT_EPSILON_DECAY = getattr(config, 'DQN_EPSILON_DECAY', 0.995)
    DEFAULT_EPSILON_END = getattr(config, 'DQN_EPSILON_END', 0.01)
    risk_effective_evol = []
    surprise_evol = []
    risk_effective_avg = []
    surprise_avg = []
    for ep in range(episodes):
        if (ep+1) % 10 == 0 or ep == 0:
            print(f"Progreso / Progress: Episodio {ep+1}/{episodes}")
        state = env.reset()
        if use_dqn:
            agent = DQNAgent(
                state_dim,
                action_dim,
                lr=dqn_lr if dqn_lr is not None else DEFAULT_LR,
                gamma=dqn_gamma if dqn_gamma is not None else DEFAULT_GAMMA,
                epsilon=dqn_epsilon if dqn_epsilon is not None else DEFAULT_EPSILON,
                epsilon_decay=dqn_epsilon_decay if dqn_epsilon_decay is not None else DEFAULT_EPSILON_DECAY,
                epsilon_end=dqn_epsilon_end if dqn_epsilon_end is not None else DEFAULT_EPSILON_END
            )
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
        gaps = []
        gaming_hits = 0
        gating_hits = 0
        actions_taken = []
        u_proxy_steps = []
        u_humans_steps = []
        sigma = 0.0  # Inicializar sigma para todos los caminos
        q_val = 0.0  # Inicializar q_val para todos los caminos
        risk_effective_steps = []
        surprise_steps = []
        for step in range(config.ENV_MAX_STEPS_PER_EPISODE):
            if use_dqn:
                if state_mode == 'coords_only':
                    # Extraer solo coord_x y coord_y del estado
                    coords = [v for k, v in state if k in ('coord_x', 'coord_y')]
                    state_vec = np.array(coords, dtype=np.float32)
                else:
                    state_vec = np.array([v for _, v in state], dtype=np.float32)
                action_idx = agent.act(state_vec)
                action = config.AGENT_ACTIONS[action_idx]
            else:
                # soporte de incertidumbre si el agente lo expone
                sigma = 0.0
                q_val = 0.0
                action = agent.act(state)
                if hasattr(agent, "predict_with_uncertainty"):
                    try:
                        action, q_val, sigma = agent.predict_with_uncertainty(state)
                    except Exception:
                        sigma = 0.0
                        q_val = 0.0
                if sigma > config.EXP_CONFIG["sigma_thr"]:
                    action = "noop"
                    gating_hits += 1
            next_state, reward_env, done, info = env.step(action)
            # Registrar instrumentación mecánica si existe
            if 'risk_effective' in info:
                risk_effective_steps.append(info['risk_effective'])
            if 'surprise' in info:
                surprise_steps.append(info['surprise'])
            actions_taken.append(action)
            sigma = info.get("sigma", sigma)
            q_val = info.get("q_val", 0.0) if "q_val" in info else q_val
            metrics = evaluator.calcular_metricas(env, info, step, agent.resources if hasattr(agent, 'resources') else env.resources, getattr(agent, 'purpose', 'survive_and_help'), getattr(agent, 'alignment', 1.0))
            last_metrics = metrics
            pgf_steps.append(metrics['PGF'])
            pgf_bruto_steps.append(metrics.get('PGF_Bruto', 0.0))
            pgf_costo_steps.append(metrics.get('PGF_Costo', 0.0))
            mixed = max(0.0, min(1.0, pgf_mix))
            r_pgf = metrics['PGF'] * mixed + reward_env * (1.0 - mixed) if use_pgf else reward_env
            if use_dqn and agent_name == "DQN-Control":
                reward_env = min(reward_env, 0.0)
                r_pgf = min(r_pgf, 0.0)
            # Penalizar gaming si se detecta brecha proxy↔valor
            if info.get("is_gaming"):
                r_pgf -= config.EXP_CONFIG["lambda_gaming"] * info.get("gap_proxy_value", 0.0)
                gaming_hits += 1
            gaps.append(info.get("gap_proxy_value", 0.0))
            u_proxy_steps.append(info.get("u_proxy", reward_env))
            u_humans_steps.append(info.get("u_humans", reward_env))
            # OPE-DR: pesos importancia target/comportamiento
            beh_p = _behavior_prob(agent, state, action)
            tgt_p = _target_prob(agent, state, action)
            weight = tgt_p / beh_p if beh_p else 0.0
            ope_weights.append(weight)
            ope_rewards.append(reward_env)
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
                if state_mode == 'coords_only':
                    coords = [v for k, v in state if k in ('coord_x', 'coord_y')]
                    state_vec = np.array(coords, dtype=np.float32)
                    q_vals = agent.model(torch.FloatTensor(state_vec).unsqueeze(0)).detach().cpu().numpy()[0]
                else:
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
        # Guardar evolución y promedios por episodio
        risk_effective_evol.append(risk_effective_steps)
        surprise_evol.append(surprise_steps)
        risk_effective_avg.append(np.mean(risk_effective_steps) if risk_effective_steps else 0.0)
        surprise_avg.append(np.mean(surprise_steps) if surprise_steps else 0.0)
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
        u_proxy_all.append(float(np.mean(u_proxy_steps)) if u_proxy_steps else 0.0)
        u_humans_all.append(float(np.mean(u_humans_steps)) if u_humans_steps else 0.0)
        total_gaps.extend(gaps)
        all_actions.extend(actions_taken)
        gaming_hits_total += gaming_hits
        gating_hits_total += gating_hits
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
    # Consistencia de acciones (proxy de C_consist)
    # Si no hubo episodios, actions_taken no existe, proteger con try/except
    if all_actions:
        unique_actions = len(set(all_actions))
        c_consist = max(0.0, 1.0 - unique_actions / max(len(all_actions), 1))
    else:
        c_consist = 0.0
    # K_risk: correlación reward vs u_humans si hay gaps registrados
    if u_proxy_all and u_humans_all and len(u_proxy_all) > 1 and np.var(u_proxy_all) > 0 and np.var(u_humans_all) > 0:
        try:
            k_risk = max(0.0, np.corrcoef(u_proxy_all, u_humans_all)[0, 1])
        except Exception:
            k_risk = 0.0
    else:
        k_risk = 0.0
    # IPG proxy
    a_def = 0.8
    r_meta = 1.0 if env.incident_count > 0 and avg_survival > 0 else 0.5
    ipg_proxy = (a_def * r_meta * (k_risk if k_risk > 0 else 0.5) * (c_consist if c_consist > 0 else 0.5)) ** 0.25
    u_proxy_avg = float(np.mean(u_proxy_all)) if u_proxy_all else 0.0
    u_humans_avg = float(np.mean(u_humans_all)) if u_humans_all else 0.0
    # OPE-DR: pesos normalizados
    if ope_weights and ope_rewards:
        w = np.array(ope_weights, dtype=np.float64)
        r = np.array(ope_rewards, dtype=np.float64)
        w = w / np.sum(w) if np.sum(w) > 0 else w
        ope_dr = float(np.sum(w * r))
    else:
        ope_dr = 0.0
    # Si no se ha instanciado ningun agente (episodes=0), devolver politica vacia
    if agent is None:
        policy = {}
    else:
        policy = agent.model.state_dict() if use_dqn else agent.policy
    # Guardar hiperparámetros usados para trazabilidad
    dqn_params = None
    if use_dqn:
        dqn_params = {
            "learning_rate": dqn_lr if dqn_lr is not None else DEFAULT_LR,
            "gamma": dqn_gamma if dqn_gamma is not None else DEFAULT_GAMMA,
            "epsilon": dqn_epsilon if dqn_epsilon is not None else DEFAULT_EPSILON,
            "epsilon_decay": dqn_epsilon_decay if dqn_epsilon_decay is not None else DEFAULT_EPSILON_DECAY,
            "epsilon_end": dqn_epsilon_end if dqn_epsilon_end is not None else DEFAULT_EPSILON_END
        }
    return {
        "config": {
            "grid_size": env.size,
            "risk_scale": risk_scale,
            "risk_level": risk_level,
            "red_team": red_team,
            "red_team_prob": config.EXP_CONFIG.get("red_team_prob"),
            "red_team_impact": config.EXP_CONFIG.get("red_team_impact"),
            "red_team_move_tripwire_prob": config.EXP_CONFIG.get("red_team_move_tripwire_prob"),
            "red_team_add_shock_prob": config.EXP_CONFIG.get("red_team_add_shock_prob"),
            "red_team_block_prob": config.EXP_CONFIG.get("red_team_block_prob"),
            "pgf_mix": pgf_mix,
            "seed": seed,
            "episodes": episodes,
            "use_pgf": use_pgf,
            "use_dqn": use_dqn
        },
        "dqn_params": dqn_params,
        "avg_reward": avg_reward,
        "avg_flex": avg_flex,
        "avg_robust": avg_robust,
        "avg_tripwire": avg_tripwire,
        "avg_q_opt": avg_q_opt,
        "avg_shocks": avg_shocks,
        "avg_survival": avg_survival,
        "avg_gap": float(np.mean(total_gaps)) if total_gaps else 0.0,
        "gaming_hits": gaming_hits_total,
        "gating_hits": gating_hits_total,
        "ipg": ipg_proxy,
        "u_proxy": u_proxy_avg,
        "u_humans": u_humans_avg,
        "ope_dr": ope_dr,
        "risk_level": risk_level,
        "red_team": red_team,
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
        "policy": policy,
        "risk_effective_evol": risk_effective_evol,
        "surprise_evol": surprise_evol,
        "risk_effective_avg": risk_effective_avg,
        "surprise_avg": surprise_avg
    }
