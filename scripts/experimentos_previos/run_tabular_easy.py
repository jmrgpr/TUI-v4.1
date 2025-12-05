# Baseline tabular RL en entorno easy (3x3)
# Ejecuta Q-learning tabular con estado (x,y) en el entorno benigno

import sim.config as config
from sim.environment import SimbiosisEnv
import numpy as np

# Configuración entorno easy
config.ENV_GRID_SIZE = 3
config.ENV_INITIAL_RESOURCES = 200.0
config.ENV_MAX_STEPS_PER_EPISODE = 30
config.ENV_DEFAULT_TRIPWIRES = []
config.ENV_DEFAULT_SHOCKS = []
config.ENV_DEFAULT_DISTRACTORS = []
config.ENV_RESOURCE_THRESHOLD_HIGH = 10
config.ENV_RESOURCE_THRESHOLD_LOW = 5
config.ENV_REWARD_HELP_BONUS = 100.0
config.ENV_PENALTY_LOW_RESOURCES = -0.01
config.ENV_PENALTY_TRIPWIRE_BASE = 0.0
config.ENV_PENALTY_SHOCK_BASE = 0.0
config.ENV_PENALTY_DISTRACTOR_BASE = 0.0
config.EXP_CONFIG["risk_penalty_high"] = -0.2
config.EXP_CONFIG["risk_penalty_low"] = -0.1
config.EXP_CONFIG["red_team_prob"] = 0.0
config.EXP_CONFIG["red_team_impact"] = 0.0

Q = np.zeros((3,3,4)) # 4 acciones: up, down, left, right
alpha = 0.5
gamma = 0.99
n_episodes = 500
rewards = []
actions = ['up','down','left','right']
goal = [2,2]

for ep in range(n_episodes):
    env = SimbiosisEnv(size=3, initial_resources=config.ENV_INITIAL_RESOURCES,
                       tripwires=[], shocks=[], distractors=[], risk_scale=0.5,
                       risk_level="low", red_team_mode=False, goal_pos=goal)
    state = tuple(env.agent_pos)
    total_r = 0.0
    for t in range(config.ENV_MAX_STEPS_PER_EPISODE):
        s = state
        a_idx = np.argmax(Q[s[0],s[1]]) if np.random.rand()>0.1 else np.random.randint(4)
        action = actions[a_idx]
        obs, reward, done, info = env.step(action)
        total_r += reward
        next_state = tuple(env.agent_pos)
        Q[s[0],s[1],a_idx] += alpha * (reward + gamma * np.max(Q[next_state[0],next_state[1]]) - Q[s[0],s[1],a_idx])
        state = next_state
        if done:
            break
    rewards.append(total_r)

print('Episodios:', n_episodes)
print('Reward media últimos 50:', np.mean(rewards[-50:]))
print('Reward media primeros 50:', np.mean(rewards[:50]))
print('Reward máxima:', np.max(rewards))
print('Reward mínima:', np.min(rewards))
print('Episodios con reward > 0:', np.sum(np.array(rewards)>0))
