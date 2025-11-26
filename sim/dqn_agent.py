"""
dqn_agent.py — Agente DQN para Simbiosis RL / DQN Agent for Symbiosis RL

Integración directa con prototipo_rl_simbiosis.py para el experimento A/B (Q-learning vs DQN+PGF).
Direct integration with prototipo_rl_simbiosis.py for A/B experiment (Q-learning vs DQN+PGF).

Uso / Usage:
    python dqn_agent.py --state_dim 8 --action_dim 4

Ejemplo de uso / Example:
    >>> agent = DQNAgent(state_dim=8, action_dim=4)
    >>> agent.save_policy('policy.json')
    >>> agent.load_policy('policy.json')
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# Red neuronal simple para DQN / Simple neural network for DQN

class DQNNet(nn.Module):
<<<<<<< HEAD
    def __init__(self, input_dim, output_dim, hidden_dim=64, dropout=0.0):
        super(DQNNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout) if dropout > 0 else None
=======
    def __init__(self, input_dim, output_dim, hidden_dim=64):
        super(DQNNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)  # Capa oculta / Hidden layer
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)  # Salida / Output layer
>>>>>>> f89d18b (Estado estable: DQN robusto, seguridad mejorada, cobertura 99%, listo para refactorización de configuración y arquitectura)
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        if self.dropout:
            x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        if self.dropout:
            x = self.dropout(x)
        return self.fc3(x)

class DQNAgent:
    """
    Agente DQN con experiencia replay y aprendizaje por PGF.
    DQN agent with experience replay and PGF learning.
    """
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.95, epsilon=0.2, epsilon_decay=0.995, epsilon_end=0.01, batch_size=32, memory_size=10000, target_update_freq=100, hidden_dim=64):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_end = epsilon_end
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQNNet(state_dim, action_dim, hidden_dim=hidden_dim).to(self.device)
        # Target network para estabilidad (DQN clásico)
        self.target_model = DQNNet(state_dim, action_dim, hidden_dim=hidden_dim).to(self.device)
        # Inicializar target igual que modelo principal
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        # Contador y frecuencia de actualización de target
        self._learn_steps = 0
        self.target_update_freq = target_update_freq
    def act(self, state):
        # Acción epsilon-greedy / Epsilon-greedy action
        if random.random() < self.epsilon:
            action = random.randrange(self.action_dim)
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            action = int(torch.argmax(q_values).item())
        # Decaimiento de epsilon
        if self.epsilon > self.epsilon_end:
            self.epsilon *= self.epsilon_decay
            if self.epsilon < self.epsilon_end:
                self.epsilon = self.epsilon_end
        return action
    def remember(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=np.float32)
        next_state = np.array(next_state, dtype=np.float32)
        self.memory.append((state, action, reward, next_state, done))
    def learn(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(np.stack(states)).to(self.device)
        actions = torch.LongTensor(np.array(actions)).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(np.array(rewards)).to(self.device)
        next_states = torch.FloatTensor(np.stack(next_states)).to(self.device)
        dones = torch.FloatTensor(np.array(dones)).to(self.device)
        q_values = self.model(states).gather(1, actions).squeeze()
        # Usar la target network para calcular next_q y estabilizar el objetivo
        with torch.no_grad():
            next_q = self.target_model(next_states).max(1)[0]
        target = rewards + self.gamma * next_q * (1 - dones)
        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        # Actualizar contador y, si procede, copiar pesos al target
        self._learn_steps += 1
        if self._learn_steps % self.target_update_freq == 0:
            self.target_model.load_state_dict(self.model.state_dict())
    def save(self, filename):
        torch.save(self.model.state_dict(), filename)
    def load(self, filename):
        self.model.load_state_dict(torch.load(filename, map_location=self.device))
