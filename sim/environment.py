"""
SimbiosisEnv: Entorno Gridworld para TUI v4.1
"""
import numpy as np
from . import config

class SimbiosisEnv:
    def __init__(self,
                 size=config.ENV_GRID_SIZE,
                 initial_resources=config.ENV_INITIAL_RESOURCES,
                 tripwires=config.ENV_DEFAULT_TRIPWIRES,
                 shocks=config.ENV_DEFAULT_SHOCKS,
                 distractors=config.ENV_DEFAULT_DISTRACTORS,
                 risk_scale=1.0):
        self.size = size
        self.agent_pos = [0,0]
        self.resources = initial_resources
        self.tripwires = tripwires
        self.shocks = shocks
        self.distractors = distractors
        self.risk_scale = risk_scale
        self.timestep = 0
        self.done = False
        self.history = []
    def reset(self):
        self.agent_pos = [0,0]
        self.resources = config.ENV_INITIAL_RESOURCES
        self.timestep = 0
        self.done = False
        self.history = []
        return self.get_abstract_state()
    def get_state(self):  # pragma: no cover - API auxiliar no usado en pruebas
        return {
            "pos": tuple(self.agent_pos),
            "resources": self.resources,
            "timestep": self.timestep
        }
    def is_tripwire_near(self, x, y):
        for tx, ty in self.tripwires:
            if abs(tx-x)+abs(ty-y) == 1:
                return True
        return False
    def is_shock_near(self, x, y):
        for sx, sy in self.shocks:
            if abs(sx-x)+abs(sy-y) == 1:
                return True
        return False
    def is_distractor_near(self, x, y):
        for dx, dy in self.distractors:
            if abs(dx-x)+abs(dy-y) == 1:
                return True
        return False
    def is_goal_near(self, x, y):
        gx, gy = self.size-1, self.size-1
        return abs(gx-x)+abs(gy-y) == 1
    def get_abstract_state(self):
        x, y = self.agent_pos
        state_features = {
            "x": x,
            "y": y,
            "recursos_altos": 1 if self.resources > config.ENV_RESOURCE_THRESHOLD_HIGH else 0,
            "recursos_bajos": 1 if self.resources < config.ENV_RESOURCE_THRESHOLD_LOW else 0,
            "veo_tripwire_cerca": 1 if self.is_tripwire_near(x, y) else 0,
            "veo_shock_cerca": 1 if self.is_shock_near(x, y) else 0,
            "veo_distractor_cerca": 1 if self.is_distractor_near(x, y) else 0,
            "veo_meta_cerca": 1 if self.is_goal_near(x, y) else 0
        }
        return tuple(sorted(state_features.items()))
    def step(self, action: str):
        moves = {"up":(-1,0), "down":(1,0), "left":(0,-1), "right":(0,1)}
        dx, dy = moves.get(action, (0,0))
        new_x = max(0, min(self.size-1, self.agent_pos[0]+dx))
        new_y = max(0, min(self.size-1, self.agent_pos[1]+dy))
        self.agent_pos = [new_x, new_y]
        self.timestep += 1
        reward = 0.0
        info = {}
        if tuple(self.agent_pos) in self.tripwires:
            penalty = config.ENV_PENALTY_TRIPWIRE_BASE * self.risk_scale
            self.resources += penalty
            reward += penalty
            info['tripwire'] = True
        if tuple(self.agent_pos) in self.shocks:
            shock_penalty = config.ENV_PENALTY_SHOCK_BASE * self.risk_scale
            self.resources += shock_penalty
            reward += shock_penalty
            info['shock'] = True
        if tuple(self.agent_pos) in self.distractors:
            distractor_penalty = config.ENV_PENALTY_DISTRACTOR_BASE
            self.resources += distractor_penalty
            reward += distractor_penalty
            info['distractor'] = True
        if self.agent_pos == [self.size-1, self.size-1] and self.resources > config.ENV_RESOURCE_THRESHOLD_HIGH:
            help_bonus = config.ENV_REWARD_HELP_BONUS
            self.resources += help_bonus
            reward += help_bonus
            info['help'] = True
        if self.resources < config.ENV_RESOURCE_THRESHOLD_LOW:
            reward += config.ENV_PENALTY_LOW_RESOURCES
            info['low_resources'] = True
        self.done = self.resources <= 0 or self.timestep >= config.ENV_MAX_STEPS_PER_EPISODE
        self.history.append({"pos":tuple(self.agent_pos),"resources":self.resources,"action":action,"reward":reward,"info":info})
        return self.get_abstract_state(), reward, self.done, info
