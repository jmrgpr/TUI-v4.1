"""
Script para enriquecer los CSVs de Fase 3 con columnas PGF e I_op usando EvaluatorPGF.
"""
import sys
import os
import pandas as pd
from pathlib import Path
# Añadir la raíz del proyecto al sys.path para importar sim correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.evaluator_pgf import EvaluatorPGF

if len(sys.argv) < 3:
    print("Uso: python compute_pgf_offline_v10.py <input_csv> <output_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]

df = pd.read_csv(input_csv)

def enrich_row(row):
    evaluator = EvaluatorPGF()
    # Mapeo de columnas del CSV a parámetros del evaluador
    # resources → agent_resources
    agent_resources = row.get('resources', 0)
    # success → info['help']
    info = {
        'help': bool(row.get('success', 0)),
        'shock': False,
        'tripwire': False,
        'distractor': False,
        'low_resources': agent_resources < 2,  # ejemplo: umbral arbitrario
    }
    # Otros parámetros por defecto
    step = row.get('steps', 0)
    agent_purpose = 'survive_and_help'
    agent_alignment = 1.0
    # Simulación de entorno mínimo
    class DummyEnv:
        resources = agent_resources
    env = DummyEnv()
    metrics = evaluator.calcular_metricas(env, info, step, agent_resources, agent_purpose, agent_alignment)
    row['PGF'] = metrics['PGF']
    row['I_op'] = metrics['I_op']
    return row

df = df.apply(enrich_row, axis=1)
df.to_csv(output_csv, index=False)
print(f"Archivo enriquecido guardado en {output_csv}")
print(f"Archivo enriquecido guardado en {output_csv}")
