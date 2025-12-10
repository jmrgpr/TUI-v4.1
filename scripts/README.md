## Índice de experimentos (series 9.x y 10.x)

Este README resume los scripts activos de las series 9.x y 10.x y dónde están sus resultados. Todo lo anterior (análisis, smokes, validaciones, utilitarios) quedó en `scripts/experimentos_previos/`.

### Serie 9.x (baseline curriculum)
- `run_experiment_9_curriculum.py`: Experimento 9 – Curriculum base (versión original 9.0). Resultados en `results/pgf_v9/`.
- `run_experiment_9.1_robust.py`: Experimento 9.1 – Curriculum robustecido. Resultados en `results/pgf_v9.1/`.

### Serie 10.x (economía, curriculum y escalado)
- `run_experiment_10_adaptive.py`: Experimento 10 (v10.0) – Curriculum adaptativo 8×8 inicial. Resultados en `results/pgf_v10/`.
- `run_experiment_10.1_balanced.py`: Experimento 10.1 – Economía balanceada. Resultados en `results/pgf_v10.1/`.
- `run_experiment_10.2_harder.py`: Experimento 10.2 – Economía más dura. Resultados en `results/pgf_v10.2/`.
- `run_experiment_10.3_critical.py`: Experimento 10.3 – Caso crítico/economía trivial. Resultados en `results/pgf_v10.3/`.
- `run_experiment_10.4_austere.py`: Experimento 10.4 – Economía austera (inviable). Resultados en `results/pgf_v10.4/`.
- `run_experiment_10.5_viable_economy.py`: Experimento 10.5 – Economía “viable” (pre-fixes). Resultados en `results/pgf_v10.5/`.
- `run_experiment_10.6_exploratory_16x16.py`: Exploratorio 16×16 (v10.6). Resultados en `results/pgf_v10.6_exploratory_16x16/`.
- `run_experiment_10.8_goal_oriented.py` (smoke): Test rápido con goal_reward; resultados en `results/pgf_v10.8/resultados/smoke_test_v10.8_goal_oriented/`.
- `run_experiment_10.9_rapid.py` (smoke): Test rápido ajustes no-lineales; resultados en `results/pgf_v10.9/resultados/smoke_test_v10.9_rapid/`.
- `run_experiment_10_adaptive.py` (fixes recientes de goal detection): pruebas en `results/pgf_v11/resultados/smoke_test_v11_20251205_083906/`.

### Experimentos previos y utilitarios
- Todo lo demás (análisis, smokes antiguos, validaciones, oráculos alternos, utilidades) está en `scripts/experimentos_previos/`. Los resultados correspondientes se agruparon en `results/experimentos_previos/` o `results/smoke_tests/` y `results/validations/`.
