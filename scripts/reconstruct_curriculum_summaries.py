#!/usr/bin/env python3
"""
Reconstruye curriculum_summary.csv desde phase CSVs individuales
Para seeds interrumpidas que no guardaron el summary final
"""

import pandas as pd
from pathlib import Path
import re

def extract_seed_from_path(path):
    """Extrae número de seed del path"""
    match = re.search(r'seed_(\d+)', str(path))
    return int(match.group(1)) if match else None

def reconstruct_summary_for_seed(seed_dir):
    """Reconstruye summary desde phase CSVs"""
    seed_num = extract_seed_from_path(seed_dir)
    if seed_num is None:
        return None
    
    # Buscar phase CSVs
    phase_files = {
        '4x4': list(seed_dir.glob('phase1_4x4_*.csv')),
        '6x6': list(seed_dir.glob('phase2_6x6_*.csv')),
        '8x8': list(seed_dir.glob('phase3_8x8_*.csv'))
    }
    
    results = []
    gates = {'4x4': 80.0, '6x6': 20.0, '8x8': 10.0}
    
    for phase_name, grid_size in [('4x4', 4), ('6x6', 6), ('8x8', 8)]:
        files = phase_files[phase_name]
        if not files:
            continue
            
        # Leer CSV
        df = pd.read_csv(files[0])
        
        # Calcular métricas
        total_episodes = len(df)
        success_rate_total = df['success'].mean()
        success_last_100 = df['success'].tail(100).mean()
        gate = gates[phase_name]
        gate_passed = (success_last_100 * 100) >= gate
        
        # First success
        first_success_idx = df[df['success'] == 1].index
        first_success_episode = first_success_idx[0] if len(first_success_idx) > 0 else None
        
        results.append({
            'seed': seed_num,
            'phase': phase_name,
            'grid_size': grid_size,
            'episodes': total_episodes,
            'success_rate_total': success_rate_total,
            'success_last_100': success_last_100,
            'gate': gate,
            'gate_passed': gate_passed,
            'first_success_episode': first_success_episode,
            'convergence_episode': -1  # No calculamos convergencia en reconstrucción
        })
    
    return results

def main():
    base_dir = Path('results/pgf_v10_multiseed/seeds')
    
    for seed_dir in sorted(base_dir.glob('seed_*')):
        seed_num = extract_seed_from_path(seed_dir)
        
        # Verificar si ya existe curriculum_summary
        existing_summaries = list(seed_dir.glob('curriculum_summary_*.csv'))
        
        if existing_summaries:
            # Verificar si está completo (debe tener 3 fases)
            df = pd.read_csv(existing_summaries[0])
            if len(df) == 3:
                print(f"✓ Seed {seed_num}: Summary completo ({len(df)} fases)")
                continue
            else:
                print(f"⚠ Seed {seed_num}: Summary incompleto ({len(df)}/3 fases) - reconstruyendo...")
        else:
            print(f"⚠ Seed {seed_num}: Sin summary - reconstruyendo...")
        
        # Reconstruir
        results = reconstruct_summary_for_seed(seed_dir)
        
        if results:
            df_new = pd.DataFrame(results)
            
            # Guardar con timestamp original si existe, o crear uno nuevo
            if existing_summaries:
                output_path = existing_summaries[0]
            else:
                # Usar timestamp de algún phase CSV
                phase_file = next(seed_dir.glob('phase*.csv'))
                timestamp = phase_file.stem.split('_')[-1]
                output_path = seed_dir / f'curriculum_summary_{timestamp}.csv'
            
            df_new.to_csv(output_path, index=False)
            print(f"  ✓ Reconstruido con {len(df_new)} fases → {output_path.name}")
            print(f"    4×4: {df_new[df_new['phase']=='4x4']['success_last_100'].values[0]:.2%}" if '4x4' in df_new['phase'].values else "")
            print(f"    6×6: {df_new[df_new['phase']=='6x6']['success_last_100'].values[0]:.2%}" if '6x6' in df_new['phase'].values else "")
            print(f"    8×8: {df_new[df_new['phase']=='8x8']['success_last_100'].values[0]:.2%}" if '8x8' in df_new['phase'].values else "")
        else:
            print(f"  ✗ No se pudo reconstruir (sin phase CSVs)")

if __name__ == '__main__':
    main()
