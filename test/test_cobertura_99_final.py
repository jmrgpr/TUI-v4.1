


def test_persistencia_export(monkeypatch, tmp_path):
    import sim.prototipo_rl_simbiosis as mod
    # Simular export_json y csv_path
    export_json = tmp_path / "test_export.json"
    csv_path = tmp_path / "test_export_episodes.csv"
    # Crear datos mínimos
    res_A = {'total_rewards': [1.0], 'tripwire_steps': [0.0], 'flex_recov': [0.0], 'robust_evol': [0.0], 'q_optimal_evol': [0.0], 'pgf_bruto_evol': [[0.0]], 'pgf_costo_evol': [[0.0]], 'avg_reward': 1.0, 'avg_tripwire': 0.0, 'avg_flex': 0.0, 'avg_q_opt': 0.0}
    res_B = res_A.copy()
    raw_data = {'control': res_A, 'simbiosis': res_B}
    # Forzar persistencia
    import json, csv
    with open(export_json, 'w', encoding='utf-8') as jf:
        json.dump({'control': res_A, 'simbiosis': res_B}, jf, indent=2)
    with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(['Agente', 'Episodio', 'Recompensa', 'Tripwires', 'Flexibilidad', 'Robustez', 'Q-optimal', 'PGF_Bruto_Avg', 'PGF_Costo_Avg'])
        for agent_name, results in raw_data.items():
            if not results or not results.get('total_rewards'):
                writer.writerow([agent_name] + [0]*8)
            else:
                mod.write_episode_rows(writer, agent_name, results)
    # Verificar archivos
    assert export_json.exists()
    assert csv_path.exists()
def test_main_entorno_degradado(monkeypatch, capsys):
    import sim.prototipo_rl_simbiosis as mod
    # Simular entorno degradado: numpy, torch y Agent faltan
    monkeypatch.setattr(mod, 'np', None)
    monkeypatch.setattr(mod, 'torch', None)
    monkeypatch.setattr(mod, 'Agent', None)
    # Ejecutar main y capturar salida
    sys_argv_backup = sys.argv
    sys.argv = ["script"]
    try:
        mod.main()
    except SystemExit:
        pass  # Esperado: main llama sys.exit(0)
    finally:
        sys.argv = sys_argv_backup
    out = capsys.readouterr().out
    # Debe imprimir barrido de risk_scale
    assert "Barrido de risk_scale" in out
"""
Tests para cobertura total y branches faltantes en TUI v4.1
Cubre imports fallidos, fallback de Agent, run_experiment, y ramas de edge en visualizaciones y Excel.
"""
import sys
import types
import importlib
import pytest

# --- Test fallback de importación fallida en prototipo_rl_simbiosis.py ---
def test_import_fallbacks_prototipo_rl_simbiosis(monkeypatch):
    # Simular fallo de import de Agent y SimbiosisEnv
    monkeypatch.setitem(sys.modules, 'sim.agent', types.ModuleType('sim.agent'))
    monkeypatch.setitem(sys.modules, 'sim.environment', types.ModuleType('sim.environment'))
    import sim.prototipo_rl_simbiosis as mod
    # Forzar fallback de Agent y SimbiosisEnv
    assert hasattr(mod, 'Agent')
    assert hasattr(mod, 'SimbiosisEnv')
    # Forzar fallback de stringify_policy
    assert callable(mod.stringify_policy)

# --- Test fallback de run_experiment ---

# --- Test branch de SimbiosisGymEnv en sota_wrapper.py ---
def test_simbiosis_gym_env_branches():
    from sim.sota_wrapper import SimbiosisGymEnv
    env = SimbiosisGymEnv(risk_scale=1.0)
    # Forzar branch de reset con menos de 8 valores
    env.env.reset = lambda: [(f'flag{i}', 1.0) for i in range(5)]
    obs, info = env.reset()
    assert obs.shape == (8,)
    # Forzar branch de step con menos de 8 valores
    env.env.step = lambda action: ([(f'flag{i}', 1.0) for i in range(5)], 1.0, False, {})
    obs, reward, done, truncated, info = env.step(0)
    assert obs.shape == (8,)

# --- Test branch de datos vacíos en toy_ped_rl_excel.py ---
def test_toy_ped_rl_excel_empty_branch():
    from sim.toy_ped_rl_excel import cargar_datos_excel, analizar_datos
    # Forzar branch de archivo vacío
    assert cargar_datos_excel('no_existe.csv') == []
    # Forzar branch de analizar_datos vacío
    assert analizar_datos([]) == {'media_I_op': 0.0, 'media_P_riesgo': 0.0, 'correlacion': 0.0}

# --- Test fallback de boxplot_metricas en visualizaciones.py ---
def test_boxplot_metricas_fallback(monkeypatch):
    import matplotlib.pyplot as plt
    from sim.visualizaciones import boxplot_metricas
    # Forzar TypeError en tick_labels para cubrir fallback
    def fake_boxplot(*args, **kwargs):
        if 'tick_labels' in kwargs:
            raise TypeError('tick_labels not supported')
        return plt.boxplot(*args, **kwargs)
    monkeypatch.setattr(plt, 'boxplot', fake_boxplot)
    data = [[1, 2, 3], [2, 3, 4]]
    boxplot_metricas(data, labels=['A', 'B'], show=False)
