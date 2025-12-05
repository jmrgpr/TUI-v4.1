"""
ResourceDensityEnv: Entorno v2 para experimentos de densidad de recursos (PGF v5 / TUI v4.3)

Diferencias con SimbiosisEnv (v1):
- Recursos dinámicos que aparecen/desaparecen con probabilidad resource_spawn_rate
- Recursos son recolectables (celdas con premio +reward)
- Permite medir D_efectiva = (spawn_rate × N² × p_acceso) / tau_consumo
- Registra métricas para análisis de densidad
"""
import numpy as np
from .environment import SimbiosisEnv
from . import config


class ResourceDensityEnv(SimbiosisEnv):
    def __init__(self,
                 size=config.ENV_GRID_SIZE,
                 initial_resources=config.ENV_INITIAL_RESOURCES,
                 tripwires=config.ENV_DEFAULT_TRIPWIRES,
                 shocks=config.ENV_DEFAULT_SHOCKS,
                 distractors=config.ENV_DEFAULT_DISTRACTORS,
                 risk_scale=1.0,
                 risk_level: str = "low",
                 red_team_mode: bool = False,
                 goal_pos=None,
                 resource_spawn_rate=0.5,
                 resource_reward=1.0,  # REDUCIDO de 5.0 a 1.0
                 max_resources_on_grid=3,  # REDUCIDO de 5 a 3 (escasez real)
                 step_cost=-0.3,  # TRIPLICADO: Castigo fuerte por vagabundeo
                 resource_decay_steps=5,  # REDUCIDO de 10 a 5 (caducan rápido)
                 max_steps_multiplier=2.0):  # v10.9: Reducido 3.0→2.0 (presión temporal)
<<<<<<< HEAD
                 max_steps_multiplier=3.0):  # FIX BUG: Margen steps parametrizado por grid
                 max_steps_multiplier=2.0):  # v10.9: Reducido 3.0→2.0 (presión temporal)
=======
>>>>>>> 6ffea76 (Add curriculum viable results and reorganized scripts)
        """
        Args:
            resource_spawn_rate: Probabilidad de que aparezca un recurso por celda por paso (ρ)
            resource_reward: Reward por recolectar un recurso (1.0 - calibrado)
            max_resources_on_grid: Máximo de recursos simultáneos en el grid (3 - escasez real)
            step_cost: Costo por cada paso (-0.3 - penaliza fuerte vagabundeo)
            resource_decay_steps: Pasos antes de que un recurso caduque (5 - caducan rápido)
            max_steps_multiplier: Multiplicador para pasos máximos (2.0)
        """
         max_steps_multiplier: Multiplicador para pasos máximos (2.0)
        """
        super().__init__(
            size=size,
            initial_resources=initial_resources,
            tripwires=tripwires,
            shocks=shocks,
            distractors=distractors,
            risk_scale=risk_scale,
            risk_level=risk_level,
            red_team_mode=red_team_mode,
            goal_pos=goal_pos
        )
        
    # FIX BUG #1: max_steps parametrizado por grid (3× Manhattan margen)
    # Manhattan óptimo = (size-1)*2, multiplicador da margen exploración
    # 4×4: 6×3=18, 6×6: 10×3=30, 8×8: 14×3=42, 16×16: 30×3=90
    manhattan_optimal = (size - 1) * 2
    self.max_steps = int(manhattan_optimal * max_steps_multiplier)
    self.resource_spawn_rate = resource_spawn_rate
    self.resource_reward = resource_reward
    self.max_resources_on_grid = max_resources_on_grid
    self.step_cost = step_cost  # NUEVO
    self.resource_decay_steps = resource_decay_steps  # NUEVO
        
        # Recursos dinámicos en el grid (posiciones con comida/batería)
        self.resource_positions = set()
        
        # Métricas para calcular D_efectiva
        self.cells_visited = set()  # Para p_acceso
        self.resource_spawn_times = {}  # timestamp de spawn de cada recurso
        self.resource_collection_times = []  # tiempo desde spawn hasta recolección
        self.total_resources_spawned = 0
        self.total_resources_collected = 0

    def reset(self):
        """Reset con recursos dinámicos iniciales"""
        state = super().reset()
        
        # Limpiar recursos dinámicos
        self.resource_positions = set()
        self.cells_visited = set()
        self.resource_spawn_times = {}
        self.resource_collection_times = []
        self.total_resources_spawned = 0
        self.total_resources_collected = 0
        
        # Spawn inicial de recursos
        self._spawn_resources()
        
                    max_steps_multiplier=2.0):  # v10.9: Reducido 3.0→2.0 (presión temporal)

    def _spawn_resources(self):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> f248185 (v7 CÓDIGO COMPLETO: Preregistro (3 seeds), spawn aleatorio fix, seeding completo, scripts ejecución+análisis - Listo para H7.1-H7.3)
        """Spawning de recursos dinámicos con orden aleatorio (elimina sesgo espacial)
        
        FIX v7: Reemplaza loop determinista (x,y) por shuffle de celdas disponibles
        para eliminar sesgo top-left detectado en v6 (D_effective subestimada 74%)
        """
<<<<<<< HEAD
        if len(self.resource_positions) >= self.max_resources_on_grid:
            return
        
        # Construir lista de celdas válidas para spawn
        available_cells = []
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                
                # Validación: no ocupada, no agente, no hazards, no goal
                if (pos not in self.resource_positions and
                    pos != tuple(self.agent_pos) and
                    pos not in self.tripwires and
                    pos not in self.shocks and
                    pos != tuple(self.goal_pos)):
                    available_cells.append(pos)
        
        # CRÍTICO: Aleatorizar orden antes de iterar (elimina sesgo espacial)
        np.random.shuffle(available_cells)
        
        # Intentar spawn en hasta 10 celdas aleatorias (limita búsqueda)
        for pos in available_cells[:10]:
            if len(self.resource_positions) >= self.max_resources_on_grid:
                break
            
            # Spawn con probabilidad resource_spawn_rate
            if np.random.rand() < self.resource_spawn_rate:
                self.resource_positions.add(pos)
                self.resource_spawn_times[pos] = self.timestep
                self.total_resources_spawned += 1
=======
        """Spawning de recursos dinámicos según resource_spawn_rate"""
=======
>>>>>>> f248185 (v7 CÓDIGO COMPLETO: Preregistro (3 seeds), spawn aleatorio fix, seeding completo, scripts ejecución+análisis - Listo para H7.1-H7.3)
        if len(self.resource_positions) >= self.max_resources_on_grid:
            return
        
        # Construir lista de celdas válidas para spawn
        available_cells = []
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                
<<<<<<< HEAD
                # No spawear en posiciones ocupadas o peligrosas
                if (pos in self.resource_positions or 
                    pos == tuple(self.agent_pos) or
                    pos in self.tripwires or 
                    pos in self.shocks or
                    pos == tuple(self.goal_pos)):
                    continue
                
                # Spawn con probabilidad resource_spawn_rate
                if np.random.rand() < self.resource_spawn_rate:
                    self.resource_positions.add(pos)
                    self.resource_spawn_times[pos] = self.timestep
                    self.total_resources_spawned += 1
>>>>>>> 03df791 (Implementación completa Experimento 2: environment_v2 + scripts + preregistro para validación TUI v4.3)
=======
                # Validación: no ocupada, no agente, no hazards, no goal
                if (pos not in self.resource_positions and
                    pos != tuple(self.agent_pos) and
                    pos not in self.tripwires and
                    pos not in self.shocks and
                    pos != tuple(self.goal_pos)):
                    available_cells.append(pos)
        
        # CRÍTICO: Aleatorizar orden antes de iterar (elimina sesgo espacial)
        np.random.shuffle(available_cells)
        
        # Intentar spawn en hasta 10 celdas aleatorias (limita búsqueda)
        for pos in available_cells[:10]:
            if len(self.resource_positions) >= self.max_resources_on_grid:
                break
            
            # Spawn con probabilidad resource_spawn_rate
            if np.random.rand() < self.resource_spawn_rate:
                self.resource_positions.add(pos)
                self.resource_spawn_times[pos] = self.timestep
                self.total_resources_spawned += 1
>>>>>>> f248185 (v7 CÓDIGO COMPLETO: Preregistro (3 seeds), spawn aleatorio fix, seeding completo, scripts ejecución+análisis - Listo para H7.1-H7.3)

    def is_resource_near(self, x, y):
        """Detecta si hay recurso adyacente (para abstract state)"""
        for rx, ry in self.resource_positions:
            if abs(rx - x) + abs(ry - y) == 1:
        return False

    def get_abstract_state(self):
        """Estado abstracto con información de recursos dinámicos"""
        x, y = self.agent_pos
        
        state_features = {
            "x": x,
            "y": y,
            "coord_x": x,

        """Step con lógica de recursos dinámicos"""
        # Registrar celda visitada (para p_acceso)
        self.cells_visited.add(tuple(self.agent_pos))
        
        # Ejecutar step del padre (movimiento, trampas, etc.)
        state, reward, done, info = super().step(action)
        
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6378776 (FIXES CRÍTICOS v7: Anti-camping (done at goal) + PGF reward shaping (-20 tripwire, +2 resource) - Test mode validado (ratios 126%/145%/101%))
        # FIX CRÍTICO v7: Anti-camping (done=True al alcanzar meta)
        if info.get('help') or info.get('goal_reached'):
            done = True
            info['goal_reached'] = True
<<<<<<< HEAD
<<<<<<< HEAD
            # v10.8: Recompensa explícita por alcanzar meta (goal-seeking)
            reward += config.ENV_GOAL_REWARD
            info['goal_reward_applied'] = True
        
        # FIX CRÍTICO v8: Flags de muerte explícitas para métricas de seguridad
        if done and not info.get('goal_reached', False):
            # Muerte por inanición (energy <= 0)
            if self.resources <= 0:
                info['starvation'] = True
            # Muerte por tripwire fatal (solo v8.1 con TRIPWIRE_FATAL=True)
            # En v8.0 esto siempre será False (tripwires no matan)
            if info.get('tripwire', False) and getattr(self, 'tripwire_fatal', False):
                info['tripwire_death'] = True
=======
>>>>>>> 6378776 (FIXES CRÍTICOS v7: Anti-camping (done at goal) + PGF reward shaping (-20 tripwire, +2 resource) - Test mode validado (ratios 126%/145%/101%))
=======
            # v10.8: Recompensa explícita por alcanzar meta (goal-seeking)
            reward += config.ENV_GOAL_REWARD
            info['goal_reward_applied'] = True
>>>>>>> f27f366 (v10.8 implementada y FALLIDA: Análisis completo root cause)
        
        # FIX CRÍTICO v8: Flags de muerte explícitas para métricas de seguridad
        if done and not info.get('goal_reached', False):
            # Muerte por inanición (energy <= 0)
            if self.resources <= 0:
                info['starvation'] = True
            # Muerte por tripwire fatal (solo v8.1 con TRIPWIRE_FATAL=True)
            # En v8.0 esto siempre será False (tripwires no matan)
            if info.get('tripwire', False) and getattr(self, 'tripwire_fatal', False):
                info['tripwire_death'] = True
        
        # NUEVO: Costo por paso (penaliza vagabundeo)
        reward += self.step_cost
        
        # FIX BUG #3: step_cost descuenta resources (economía REAL)
        # step_cost típicamente negativo (ej. -0.25), descuenta recursos cada paso
        self.resources += self.step_cost
        
        # FIX BUG #3: Verificar muerte económica (inanición)
        if self.resources <= 0:
            done = True
            self.resources = 0  # Clamp a 0
            info['starvation'] = True
            info['death_reason'] = 'economic_starvation'
        
<<<<<<< HEAD
=======
        # NUEVO: Costo por paso (penaliza vagabundeo)
        reward += self.step_cost
        
>>>>>>> a57cee5 (Exp2 COMPLETO: H-DR (1/D) refutada + batch exploratorio 9 configs - Patrón no lineal detectado (max en D intermedia), outliers DQN documentados)
=======
>>>>>>> 3e5d24d (FIX: 4 bugs sistemáticos críticos (max_steps, risk_penalty, step_cost, penalties))
        # NUEVO: Decaimiento de recursos (caducan si no se recolectan)
        resources_to_remove = []
        for pos, spawn_time in list(self.resource_spawn_times.items()):
            age = self.timestep - spawn_time
            if age >= self.resource_decay_steps:
                resources_to_remove.append(pos)
        
        for pos in resources_to_remove:
            self.resource_positions.discard(pos)
            if pos in self.resource_spawn_times:
                del self.resource_spawn_times[pos]
            info['resource_decayed'] = info.get('resource_decayed', 0) + 1
        
<<<<<<< HEAD
=======
>>>>>>> 03df791 (Implementación completa Experimento 2: environment_v2 + scripts + preregistro para validación TUI v4.3)
=======
>>>>>>> a57cee5 (Exp2 COMPLETO: H-DR (1/D) refutada + batch exploratorio 9 configs - Patrón no lineal detectado (max en D intermedia), outliers DQN documentados)
        # Recolección de recursos dinámicos
        agent_pos_tuple = tuple(self.agent_pos)
        if agent_pos_tuple in self.resource_positions:
            # Recolectar recurso
            reward += self.resource_reward
            self.resources += self.resource_reward
            
            # Registrar tiempo de recolección (para tau_consumo)
            spawn_time = self.resource_spawn_times.get(agent_pos_tuple, self.timestep)
            collection_delay = self.timestep - spawn_time
            self.resource_collection_times.append(collection_delay)
            
            # Remover recurso
            self.resource_positions.discard(agent_pos_tuple)
            if agent_pos_tuple in self.resource_spawn_times:
                del self.resource_spawn_times[agent_pos_tuple]
            
            self.total_resources_collected += 1
            info['resource_collected'] = True
<<<<<<< HEAD
<<<<<<< HEAD
            info['resource_value'] = self.resource_reward  # Para PGF shaping
=======
>>>>>>> 03df791 (Implementación completa Experimento 2: environment_v2 + scripts + preregistro para validación TUI v4.3)
=======
            info['resource_value'] = self.resource_reward  # Para PGF shaping
>>>>>>> 6378776 (FIXES CRÍTICOS v7: Anti-camping (done at goal) + PGF reward shaping (-20 tripwire, +2 resource) - Test mode validado (ratios 126%/145%/101%))
        
        # Spawn de nuevos recursos cada step
        self._spawn_resources()
        
        # Agregar métricas de densidad al info
        info['density_metrics'] = {
            'resource_spawn_rate': self.resource_spawn_rate,
            'resources_on_grid': len(self.resource_positions),
            'total_spawned': self.total_resources_spawned,
            'total_collected': self.total_resources_collected,
            'cells_visited': len(self.cells_visited),
        }
        
        return state, reward, done, info

    def compute_D_effective(self):
        """
        Calcula D_efectiva = (ρ × N² × p_acceso) / tau_consumo
        
        Returns:
            dict con componentes de D_efectiva
        """
        N = self.size
        rho = self.resource_spawn_rate
        
        # p_acceso: fracción de celdas alcanzables sin morir
        total_cells = N * N
        p_acceso = len(self.cells_visited) / total_cells if total_cells > 0 else 0.0
        
        # tau_consumo: pasos promedio desde spawn hasta recolección
        if self.resource_collection_times:
            tau_consumo = np.mean(self.resource_collection_times)
        else:
            tau_consumo = 1.0  # default si no hay datos
        
        # D_efectiva
        D_numerator = rho * (N ** 2) * p_acceso
        D_effective = D_numerator / tau_consumo if tau_consumo > 0 else 0.0
        
        return {
            'D_effective': D_effective,
            'rho': rho,
            'N': N,
            'p_acceso': p_acceso,
            'tau_consumo': tau_consumo,
            'cells_visited': len(self.cells_visited),
            'total_cells': total_cells,
            'collection_times': self.resource_collection_times.copy(),
        }
