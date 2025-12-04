"""
Smoke Test Multi-Seed para validar consistencia FIX #5
Ejecuta 3 seeds diferentes (42, 123, 456) para confirmar mejora
"""

import subprocess
import json
from pathlib import Path

SEEDS = [42, 123, 456]

def run_single_seed(seed):
    """Ejecuta smoke test con seed específico."""
    print(f"\n{'='*70}")
    print(f"EJECUTANDO SEED {seed}")
    print('='*70)
    
    # Modificar script temporalmente
    script_path = Path("scripts/run_smoke_test_6x6_post_penalty_fix.py")
    original = script_path.read_text(encoding='utf-8')
    modified = original.replace("SEED = 42", f"SEED = {seed}")
    script_path.write_text(modified, encoding='utf-8')
    
    # Ejecutar
    result = subprocess.run(
        ["python", str(script_path)],
        capture_output=True,
        text=True
    )
    
    # Restaurar original
    script_path.write_text(original, encoding='utf-8')
    
    # Leer resultados
    summary_path = Path(f"results/smoke_test_6x6_post_penalty_fix/summary.json")
    if summary_path.exists():
        with open(summary_path) as f:
            data = json.load(f)
        return data['metrics']
    return None

def main():
    print("="*70)
    print("VALIDACIÓN MULTI-SEED FIX #5")
    print("="*70)
    
    results = []
    for seed in SEEDS:
        metrics = run_single_seed(seed)
        if metrics:
            results.append(metrics)
            print(f"\nSeed {seed} - Reward: {metrics['reward_mean']:.2f}, "
                  f"Resources: {metrics['resources_mean']:.2f}, "
                  f"Success: {metrics['success_rate']:.1f}%")
    
    if not results:
        print("❌ No se obtuvieron resultados")
        return
    
    # Promedios
    print("\n" + "="*70)
    print("RESUMEN MULTI-SEED (3 seeds)")
    print("="*70)
    
    avg_reward = sum(r['reward_mean'] for r in results) / len(results)
    avg_resources = sum(r['resources_mean'] for r in results) / len(results)
    avg_tripwires = sum(r['tripwires_mean'] for r in results) / len(results)
    avg_success = sum(r['success_rate'] for r in results) / len(results)
    
    print(f"\nPromedios (n={len(results)}):")
    print(f"  Reward: {avg_reward:.2f}")
    print(f"  Resources: {avg_resources:.2f}")
    print(f"  Tripwires: {avg_tripwires:.2f}")
    print(f"  Success: {avg_success:.1f}%")
    
    print(f"\n🚦 VALIDACIÓN FIX #5:")
    if avg_reward > -50:
        print(f"  ✅ Rewards {avg_reward:.2f} viable (vs -160 previo)")
    else:
        print(f"  ❌ Rewards {avg_reward:.2f} aún negativos")
    
    if avg_resources > 0.3:
        print(f"  ✅ Resources {avg_resources:.2f} > 0.3 (explora)")
    else:
        print(f"  ❌ Resources {avg_resources:.2f} ≤ 0.3 (paralizado)")
    
    print(f"\n{'='*70}")
    if avg_reward > -50 and avg_resources > 0.3:
        print("✅ FIX #5 VALIDADO: Mejora consistente en múltiples seeds")
    else:
        print("⚠️  FIX #5 PARCIAL: Necesita ajustes adicionales")
    print('='*70)

if __name__ == '__main__':
    main()
