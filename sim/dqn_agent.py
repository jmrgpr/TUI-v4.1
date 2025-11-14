"""
dqn_agent.py — Agente DQN para Simbiosis RL / DQN Agent for Symbiosis RL

Integración directa con prototipo_rl_simbiosis.py para el experimento A/B (Q-learning vs DQN+PGF).
Direct integration with prototipo_rl_simbiosis.py for A/B experiment (Q-learning vs DQN+PGF).

Uso: El script principal permite comparar ambos agentes y guardar sus políticas usando flags CLI.
Usage: The main script allows comparison of both agents and saving their policies using CLI flags.

"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# Red neuronal simple para DQN / Simple neural network for DQN
class DQNNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQNNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)  # Capa oculta / Hidden layer
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_dim)  # Salida / Output layer
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def calcular_metricas(self, env, info, step):
        """
        Calcula métricas TUI y PGF prudencial (bilingüe).
        Compute TUI metrics and prudential PGF (bilingual).
        Args:
            env: SimbiosisEnv
            info: dict
            step: int
        """
        self.C = max(0.0, env.resources / 100.0)
        self.F = 1.0 if info.get('shock') else 0.5
        self.T = 1.0 if info.get('help') else 0.5
        w_C, w_F, w_T = 0.4, 0.3, 0.3
        self.I_op = w_C * self.C + w_F * self.F + w_T * self.T
        # Guardar riesgo previo / Store previous risk
        if not hasattr(self, 'P_riesgo_prev'):
            self.P_riesgo_prev = 0.0
        self.P_riesgo_actual = getattr(self, 'P_riesgo', 0.0) + abs(info.get('tripwire', 0)*20.0 + info.get('shock', 0)*10.0 + info.get('distractor', 0)*5.0)
        delta_P = self.P_riesgo_prev - self.P_riesgo_actual
        self.P_riesgo = self.P_riesgo_actual
        self.C_costo = 1.0 if info.get('low_resources') else 0.8
        self.S_auto = 1.0 if getattr(self, 'purpose', 'survive_and_help') != "survive_and_help" else 0.7
        self.R_robust = 1.0 if not info.get('distractor') else 0.6
        self.I_rep = 1.0 if info.get('help') else 0.7
        self.P_genuino = (self.C_costo * self.S_auto * self.R_robust * self.I_rep) ** 0.25
        # Parámetros prudenciales (no hardcodeados) / Prudential parameters (no hardcoded)
        kappa = 1.0  # Sensibilidad PGF / PGF sensitivity
        lambda_c = 0.1  # Penalización costo / Cost penalty
        S_t = 1.0 if info.get('shock') or info.get('tripwire') else 0.5
        A_t = getattr(self, 'alignment', 1.0) * self.P_genuino
        delta_C_t = abs(env.resources - getattr(self, 'resources', 100.0))
        # PGF prudencial: premia reducción de riesgo / PGF: rewards risk reduction
        self.PGF = kappa * delta_P * A_t - lambda_c * delta_C_t
        self.P_riesgo_prev = self.P_riesgo_actual
        beta = 1.0
        C_total_norm = 1.0
        delta_I_useful = self.I_op
        self.eta_extendido = (delta_I_useful * getattr(self, 'alignment', 1.0)) / (C_total_norm + beta * self.P_riesgo)
    """
    Agente DQN con experiencia replay y aprendizaje por PGF.
    DQN agent with experience replay and PGF learning.
    """
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.95, epsilon=0.2, batch_size=32, memory_size=10000):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQNNet(state_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
    def act(self, state):
        # Acción epsilon-greedy / Epsilon-greedy action
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state)
        return int(torch.argmax(q_values).item())
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    def learn(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        import numpy as np
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(np.array(actions)).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(np.array(rewards)).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(np.array(dones)).to(self.device)
        q_values = self.model(states).gather(1, actions).squeeze()
        with torch.no_grad():
            next_q = self.model(next_states).max(1)[0]
        target = rewards + self.gamma * next_q * (1 - dones)
        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    def save(self, filename):
        torch.save(self.model.state_dict(), filename)
    def load(self, filename):
        self.model.load_state_dict(torch.load(filename, map_location=self.device))
