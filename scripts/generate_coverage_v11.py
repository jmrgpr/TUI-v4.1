#!/usr/bin/env python3
"""Genera tabla de coverage por agente para resultados v11.

Salida: results/v11/data/coverage_by_agent.csv y .md
"""
from pathlib import Path
import pandas as pd

repo = Path(__file__).resolve().parents[1]
root = repo / 'results' / 'v11'
data_dir = root / 'data'
arch_dir = root / 'archived'
data_dir.mkdir(parents=True, exist_ok=True)

def agent_from_file(f):
    # Try to infer agent from path segments (common layout) or from CSV header
    parts = [p.lower() for p in f.parts]
    for a in ('control','dqn_control','simbiosis','tui','a2c'):
        if a in parts:
            return a
    # fallback: try reading csv and look for agent/Agente column
    try:
        df = pd.read_csv(f, nrows=5)
        for col in df.columns:
            if col.lower() in ('agent','agente'):
                return df[col].iloc[0]
    except Exception:
        return 'unknown'
    return 'unknown'

def collect(files):
    rows = []
    for f in files:
        agent = agent_from_file(f)
        stem = f.stem
        # grid tag
        grid = None
        for p in f.parts:
            if p.startswith('grid'):
                grid = p
                break
        # seed try parse
        seed = None
        for tok in stem.split('_'):
            if tok.startswith('seed'):
                try:
                    seed = int(tok.replace('seed',''))
                except:
                    seed = None
        rows.append({'file':str(f), 'agent':agent, 'grid': grid, 'seed': seed})
    return pd.DataFrame(rows)

# active files (exclude archived)
active_files = [p for p in root.rglob('*_episodes.csv') if arch_dir not in p.parents]
archived_files = [p for p in arch_dir.rglob('*_episodes.csv')] if arch_dir.exists() else []

df_active = collect(active_files)
df_arch = collect(archived_files)

agents = sorted(set(df_active['agent'].unique()).union(df_arch['agent'].unique()))
out_rows = []
for a in agents:
    a_active = df_active[df_active['agent']==a]
    a_arch = df_arch[df_arch['agent']==a]
    files_active = len(a_active)
    files_arch = len(a_arch)
    seeds_active = a_active['seed'].dropna().unique().tolist()
    seeds_arch = a_arch['seed'].dropna().unique().tolist()
    grids_active = sorted([g for g in a_active['grid'].dropna().unique().tolist()])
    out_rows.append({'agent':a,'files_active':files_active,'files_archived':files_arch,'unique_seeds_active':len(seeds_active),'unique_seeds_archived':len(seeds_arch),'grids_active':'|'.join(grids_active)})

out_df = pd.DataFrame(out_rows)
out_csv = data_dir / 'coverage_by_agent.csv'
out_md = data_dir / 'coverage_by_agent.md'
out_df.to_csv(out_csv, index=False)

with open(out_md,'w',encoding='utf-8') as f:
    f.write('# Coverage por agente — v11\n\n')
    f.write('Tabla de archivos activos/archivados, seeds y grids por agente.\n\n')
    f.write(out_df.to_string(index=False))

print('Wrote', out_csv, out_md)
