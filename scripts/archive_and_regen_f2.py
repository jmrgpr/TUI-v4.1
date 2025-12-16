#!/usr/bin/env python3
"""Archiva archivos marcados en `results/v11/f2_final_checks.csv` y regenera resúmenes.

Uso: ejecutar desde la raíz del repo: `python scripts/archive_and_regen_f2.py`
"""
import csv
import shutil
import subprocess
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    checks_csv = repo_root / 'results' / 'v11' / 'f2_final_checks.csv'
    archived_root = repo_root / 'results' / 'v11' / 'archived'
    archived_root.mkdir(parents=True, exist_ok=True)

    if not checks_csv.exists():
        print(f'No existe {checks_csv}. Ejecuta primero `scripts/final_checks_f2.py`.')
        return 1

    files_to_move = set()
    with checks_csv.open('r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                low_n = row.get('low_n', '').strip().lower() in ('true', '1', 'yes')
                outlier = row.get('outlier', '').strip().lower() in ('true', '1', 'yes')
            except Exception:
                low_n = False
                outlier = False
            if low_n or outlier:
                files_to_move.add(row['file'])

    moved = []
    for f in sorted(files_to_move):
        # Normalize slashes and build absolute path
        rel = f.replace('\\', '/').lstrip('./')
        src = repo_root / rel
        if not src.exists():
            print(f'AVISO: archivo no encontrado, se omite: {src}')
            continue

        # Try to place under archived/<path_after_results_v11>
        parts = rel.split('/')
        dest_sub = None
        try:
            idx = parts.index('results')
            # Expect parts like results/v11/...
            if len(parts) > idx + 2 and parts[idx+1] == 'v11':
                dest_sub = Path(*parts[idx+2:])
        except ValueError:
            dest_sub = None

        if dest_sub is None:
            dest = archived_root / src.name
        else:
            dest = archived_root / dest_sub

        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(src), str(dest))
            moved.append((str(src), str(dest)))
            print(f'Movido: {src} -> {dest}')
        except Exception as e:
            print(f'ERROR moviendo {src} -> {dest}: {e}')

    # Save log of moved files
    log_path = archived_root / 'moved_files_log.csv'
    if moved:
        with log_path.open('w', encoding='utf-8', newline='') as lf:
            w = csv.writer(lf)
            w.writerow(['src', 'dest'])
            for s, d in moved:
                w.writerow([s, d])
        print(f'Log guardado en {log_path}')
    else:
        print('No se movió ningún archivo.')

    # Regenerar resúmenes: final checks, episodic metrics, analisis estadistico
    scripts = [
        repo_root / 'scripts' / 'final_checks_f2.py',
        repo_root / 'scripts' / 'episodic_metrics_v11.py',
        repo_root / 'scripts' / 'analisis_estadistico_v11.py',
    ]

    for s in scripts:
        if not s.exists():
            print(f'Ignorado (no existe el script): {s}')
            continue
        print(f'Ejecutando: python {s}')
        res = subprocess.run(['python', str(s)], cwd=str(repo_root))
        if res.returncode != 0:
            print(f'ERROR: el script {s} devolvió código {res.returncode}')

    print('Proceso completado.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
