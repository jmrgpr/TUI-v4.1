# --- RUNNER FASE 2: Ablation científica por componentes v10 ---
# --- RUNNER FASE 2: Ablation científica por componentes v10 ---
import argparse
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from run_curriculum_complete_viable import (
    create_env,
    state_to_vector,
    train_phase,
    GATE_8X8,
    GATE_4X4,
    GATE_6X6,
    LEARNING_RATE,
    GAMMA,
    EPSILON_START,
    EPSILON_MIN,
    EPSILON_DECAY,
    BATCH_SIZE,
    MEMORY_SIZE,
    HIDDEN_DIM,
)
from sim.dqn_agent import DQNAgent


def parse_args():
    parser = argparse.ArgumentParser(description="Runner de ablation por componentes v10 (científico)")
    parser.add_argument(
        '--variant',
        type=str,
        required=True,
        help=(
            "baseline|minimal|with_shaping|with_rewardextra|"
            "with_curriculum|with_transfer|with_regularization|"
            "hyper_lr_..., hyper_gamma_..., hyper_batch_..."
        ),
    )
    parser.add_argument('--seed', type=int, required=True, help='Seed de entrenamiento')
    parser.add_argument('--episodes', type=int, default=1500, help='Numero de episodios (default: 1500, igual que baseline v10)')
    parser.add_argument('--lr', type=float, default=None, help='Learning rate (sobrescribe variante si se indica)')
    parser.add_argument('--gamma', type=float, default=None, help='Gamma (sobrescribe variante si se indica)')
    parser.add_argument('--batch', type=int, default=None, help='Batch size (sobrescribe variante si se indica)')
    parser.add_argument('--transfer_checkpoint', type=str, default=None, help='Ruta a checkpoint .pth para transfer (opcional)')
    return parser.parse_args()


def parse_hyper_variant(variant: str, base_config: dict) -> dict:
    """
    Soporta variantes:
    - hyper_lr_0005, hyper_lr_0.0005
    - hyper_gamma_095, hyper_gamma_0.95
    - hyper_batch_128
    - hyperparam_sweep_lr_0005_gamma_095_batch_32 (combinaciones)
    """
    import re
    config = base_config.copy()
    lr_match = re.search(r'lr_([0-9.]+)', variant)
    gamma_match = re.search(r'gamma_([0-9.]+)', variant)
    batch_match = re.search(r'batch_([0-9]+)', variant)
    if lr_match:
        val = lr_match.group(1)
        config['learning_rate'] = float(val) if '.' in val else float(f"0.{val}")
    if gamma_match:
        val = gamma_match.group(1)
        config['gamma'] = float(val) if '.' in val else float(f"0.{val}")
    if batch_match:
        config['batch_size'] = int(batch_match.group(1))
    return config


def get_variant_config(variant: str):
    """
    Baseline F2 = RL puro 8x8 (Config B):
    - Sin shaping PGF
    - Sin reward_extra
    - Sin curriculum
    - Sin transfer
    - Sin regularización
    """
    config = {
        'shaping': False,
        'transfer': False,
        'curriculum': False,
        'reward_extra': False,
        'regularization': False,
        'learning_rate': LEARNING_RATE,
        'gamma': GAMMA,
        'batch_size': BATCH_SIZE,
        'epsilon_start': EPSILON_START,
        'epsilon_min': EPSILON_MIN,
        'epsilon_decay': EPSILON_DECAY,
        'memory_size': MEMORY_SIZE,
        'hidden_dim': HIDDEN_DIM,
        # Shaping PGF baseline (serie 10.x)
        'shaping_scale': 1.0,
        'shaping_tripwire_penalty': -100.0,
        'shaping_resource_bonus': 10.0,
        # Regularización (solo si regularization=True)
        'weight_decay': 0.0,
        'dropout': 0.0,
        # Episodios y gate baseline v10
        'episodes': 1500,
        'gate_8x8': 0.10,  # 10% como en baseline v10
    }

    # Variantes que ENCIENDEN un componente
    if variant in ('baseline', 'minimal'):
        pass  # ya está todo en False
    elif variant in ('with_shaping', 'shaping'):
        config['shaping'] = True
    elif variant in ('with_rewardextra', 'rewardextra'):
        config['reward_extra'] = True
    elif variant in ('with_curriculum', 'curriculum'):
        config['curriculum'] = True
    elif variant in ('with_transfer', 'transfer'):
        config['transfer'] = True
    elif variant in ('with_regularization', 'regularization'):
        config['regularization'] = True
        config['weight_decay'] = 1e-5
        config['dropout'] = 0.10
    elif variant.startswith('hyper'):
        config = parse_hyper_variant(variant, config)
    else:
        raise ValueError(f"Variant desconocida: {variant}")
    return config


def main():
    args = parse_args()
    config = get_variant_config(args.variant)
    # Sobrescribir hiperparametros si se pasan por CLI
    if args.lr is not None:
        config['learning_rate'] = args.lr
    if args.gamma is not None:
        config['gamma'] = args.gamma
    if args.batch is not None:
        config['batch_size'] = args.batch


    # --- Curriculum/Transfer wiring real ---
    def make_env(grid_size, max_steps_multiplier):
        return create_env(grid_size=grid_size, max_steps_multiplier=max_steps_multiplier)

    def make_agent(state_dim, action_dim, config, epsilon_start=None):
        return DQNAgent(
            state_dim=state_dim,
            action_dim=action_dim,
            lr=config['learning_rate'],
            gamma=config['gamma'],
            epsilon=epsilon_start if epsilon_start is not None else config['epsilon_start'],
            epsilon_end=config['epsilon_min'],
            epsilon_decay=config['epsilon_decay'],
            batch_size=config['batch_size'],
            memory_size=config['memory_size'],
            hidden_dim=config['hidden_dim'],
            weight_decay=config['weight_decay'] if config['regularization'] else 0.0,
            dropout=config['dropout'] if config['regularization'] else 0.0,
        )

    outdir = Path(f"results/pgf_v10_ablation/component_{args.variant}/seeds/seed_{args.seed:04d}")
    outdir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    from sim.evaluator_pgf import EvaluatorPGF

    def patch_shaping(env, config):
        evaluator = EvaluatorPGF()
        original_step = env.step
        def shaped_step(action):
            next_state, reward_env, done, info = original_step(action)
            reward_shaped = reward_env
            if config['shaping']:
                agent_resources = getattr(env, 'resources', 1.0)
                agent_purpose = "survive"
                agent_alignment = 1.0
                step_count = info.get('timestep', 0) if isinstance(info, dict) else 0
                metrics = evaluator.calcular_metricas(env, info if isinstance(info, dict) else {}, step_count, agent_resources, agent_purpose, agent_alignment)
                reward_shaped += config.get('shaping_scale', 1.0) * metrics.get('PGF_Bruto', 0.0)
            if config['reward_extra']:
                if info.get('resource_collected', False) or info.get('resource_value', None) is not None:
                    reward_shaped += config.get('shaping_resource_bonus', 10.0) * 0.5
            return next_state, reward_shaped, done, info
        env.step = shaped_step

    if config['curriculum']:
        # === Fase 1: 4x4 ===
        env_4x4 = make_env(4, 4.0)
        patch_shaping(env_4x4, config)
        state = env_4x4.reset()
        state_dim = len(state_to_vector(state))
        action_dim = 5
        agent_4x4 = make_agent(state_dim, action_dim, config)
        result_4x4 = train_phase(env_4x4, agent_4x4, num_episodes=500, phase_name="4x4", gate_threshold=GATE_4X4)
        pd.DataFrame(result_4x4["metrics"]).to_csv(outdir / f"episodes_4x4_{timestamp}.csv", index=False)
        if not result_4x4["gate_passed"]:
            print("[ABORT] Curriculum abortado en 4x4")
            return
        model_4x4_path = outdir / f"model_4x4_{timestamp}.pth"
        torch.save(agent_4x4.model.state_dict(), model_4x4_path)

        # === Fase 2: 6x6 ===
        env_6x6 = make_env(6, 5.0)
        patch_shaping(env_6x6, config)
        agent_6x6 = make_agent(state_dim, action_dim, config, epsilon_start=0.9)
        agent_6x6.model.load_state_dict(torch.load(model_4x4_path))
        agent_6x6.target_model.load_state_dict(agent_6x6.model.state_dict())
        result_6x6 = train_phase(env_6x6, agent_6x6, num_episodes=1000, phase_name="6x6", gate_threshold=GATE_6X6)
        pd.DataFrame(result_6x6["metrics"]).to_csv(outdir / f"episodes_6x6_{timestamp}.csv", index=False)
        if not result_6x6["gate_passed"]:
            print("[ABORT] Curriculum abortado en 6x6")
            return
        model_6x6_path = outdir / f"model_6x6_{timestamp}.pth"
        torch.save(agent_6x6.model.state_dict(), model_6x6_path)

        # === Fase 3: 8x8 ===
        env_8x8 = make_env(8, 3.0)
        patch_shaping(env_8x8, config)
        agent_8x8 = make_agent(state_dim, action_dim, config, epsilon_start=0.3)
        agent_8x8.model.load_state_dict(torch.load(model_6x6_path))
        agent_8x8.target_model.load_state_dict(agent_8x8.model.state_dict())
        result_8x8 = train_phase(env_8x8, agent_8x8, num_episodes=1500, phase_name="8x8", gate_threshold=config['gate_8x8'])
        pd.DataFrame(result_8x8["metrics"]).to_csv(outdir / f"episodes_8x8_{timestamp}.csv", index=False)

        # Guardar resumen final
        summary = {
            'success_rate_total': result_8x8['success_rate'],
            'success_last_100': result_8x8['last_100_success'],
            'gate': config['gate_8x8'],
            'gate_passed': result_8x8['gate_passed'],
            'first_success_episode': result_8x8['first_success'],
            'convergence_episode': result_8x8.get('convergence_episode', -1),
            'variant': args.variant,
            'seed': args.seed,
            'episodes': args.episodes,
            'learning_rate': config['learning_rate'],
            'gamma': config['gamma'],
            'batch_size': config['batch_size'],
            'shaping': config['shaping'],
            'transfer': config['transfer'],
            'curriculum': config['curriculum'],
            'reward_extra': config['reward_extra'],
            'regularization': config['regularization'],
            'shaping_scale': config['shaping_scale'],
            'shaping_tripwire_penalty': config['shaping_tripwire_penalty'],
            'shaping_resource_bonus': config['shaping_resource_bonus'],
            'weight_decay': config['weight_decay'] if config['regularization'] else 0.0,
            'dropout': config['dropout'] if config['regularization'] else 0.0,
            'transfer_checkpoint': args.transfer_checkpoint,
        }
        pd.DataFrame([summary]).to_csv(outdir / f"{args.variant}_summary_{timestamp}.csv", index=False)
        print(f"[INFO] Resultados guardados en {outdir}")
        return

    # --- Direct 8x8 (baseline B) y variantes ---
    env = make_env(8, 5.0)
    patch_shaping(env, config)
    state = env.reset()
    state_dim = len(state_to_vector(state))
    action_dim = 5
    agent = make_agent(state_dim, action_dim, config, epsilon_start=config['epsilon_start'] if config['transfer'] else 1.0)
    if config['transfer'] and args.transfer_checkpoint:
        ckpt = Path(args.transfer_checkpoint)
        if ckpt.is_file():
            state_dict = torch.load(ckpt, map_location=agent.device)
            agent.model.load_state_dict(state_dict)
            agent.target_model.load_state_dict(agent.model.state_dict())
            print(f"[INFO] Transfer activado: pesos cargados desde {ckpt}")
        else:
            print(f"[WARN] Transfer solicitado pero checkpoint no encontrado: {ckpt}. Entrenando desde cero.")
    result = train_phase(
        env,
        agent,
        num_episodes=config['episodes'],
        phase_name=f"{args.variant}_seed{args.seed}",
        gate_threshold=config['gate_8x8'],
    )
    pd.DataFrame(result["metrics"]).to_csv(outdir / f"episodes_{timestamp}.csv", index=False)
    summary = {
        'success_rate_total': result['success_rate'],
        'success_last_100': result['last_100_success'],
        'gate': config['gate_8x8'],
        'gate_passed': result['gate_passed'],
        'first_success_episode': result['first_success'],
        'convergence_episode': result.get('convergence_episode', -1),
        'variant': args.variant,
        'seed': args.seed,
        'episodes': config['episodes'],
        'learning_rate': config['learning_rate'],
        'gamma': config['gamma'],
        'batch_size': config['batch_size'],
        'shaping': config['shaping'],
        'transfer': config['transfer'],
        'curriculum': config['curriculum'],
        'reward_extra': config['reward_extra'],
        'regularization': config['regularization'],
        'shaping_scale': config['shaping_scale'],
        'shaping_tripwire_penalty': config['shaping_tripwire_penalty'],
        'shaping_resource_bonus': config['shaping_resource_bonus'],
        'weight_decay': config['weight_decay'] if config['regularization'] else 0.0,
        'dropout': config['dropout'] if config['regularization'] else 0.0,
        'transfer_checkpoint': args.transfer_checkpoint,
    }
    pd.DataFrame([summary]).to_csv(outdir / f"{args.variant}_summary_{timestamp}.csv", index=False)
    print(f"[INFO] Resultados guardados en {outdir}")


=======
import argparse
import os
from pathlib import Path

# Importar el agente y entorno base v10 (ajustar según tu estructura)
# from TUI.agent import DQNAgent
# from TUI.environment import Environment
# ...

def parse_args():
    parser = argparse.ArgumentParser(description="Runner de ablation por componentes v10")
    parser.add_argument('--variant', type=str, required=True, help='Nombre de la variante (minimal, noshaping, notransfer, etc.)')
    parser.add_argument('--seed', type=int, required=True, help='Seed de entrenamiento')
    parser.add_argument('--episodes', type=int, default=1000, help='Número de episodios (default: 1000)')
    # Puedes añadir más flags para hiperparámetros si lo deseas
    return parser.parse_args()

def get_variant_config(variant):
    """
    Devuelve un diccionario con los flags de componentes y cambios de hiperparámetros según la variante.
    """
    config = {
        'shaping': True,
        'transfer': True,
        'curriculum': True,
        'reward_extra': True,
        'regularization': True,
        'learning_rate': 0.0005,
        'gamma': 0.99,
        'batch_size': 64,
    }
    if variant == 'minimal':
        config.update({'shaping': False, 'transfer': False, 'curriculum': False, 'reward_extra': False, 'regularization': False})
    elif variant == 'noshaping':
        config['shaping'] = False
    elif variant == 'notransfer':
        config['transfer'] = False
    elif variant == 'nocurriculum':
        config['curriculum'] = False
    elif variant == 'norewardextra':
        config['reward_extra'] = False
    elif variant == 'noregularization':
        config['regularization'] = False
    elif variant.startswith('hyper_lr_'):
        lr = float(variant.split('_')[-1])
        config['learning_rate'] = lr
    # Agrega más variantes según sea necesario
    return config

def main():
    args = parse_args()
    config = get_variant_config(args.variant)
    # Configurar entorno, agente y entrenamiento según config
    # env = Environment(..., curriculum=config['curriculum'], ...)
    # agent = DQNAgent(..., shaping=config['shaping'], transfer=config['transfer'], ...)
    # agent.set_hyperparams(lr=config['learning_rate'], gamma=config['gamma'], batch_size=config['batch_size'])
    # agent.train(env, episodes=args.episodes, seed=args.seed)
    # Guardar resultados en la carpeta correspondiente
    outdir = Path(f"results/pgf_v10_ablation/component_{args.variant}/seeds/seed_{args.seed:04d}")
    outdir.mkdir(parents=True, exist_ok=True)
    # agent.save_results(outdir)
    print(f"[INFO] Resultados guardados en {outdir}")

>>>>>>> 9d4f81b (Limpieza y commit: actualización de documentación, runners y resultados FASE 1 y preregistro FASE 2)
if __name__ == "__main__":
    main()
