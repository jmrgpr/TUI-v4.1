# TRACKING_v4.2

## Estado actual (18/11/2025)


**Nota importante:**
Las carpetas `scripts/experimentos_previos/` y `test/smoke_test/` han sido excluidas del repositorio en línea (.gitignore) para evitar problemas de espacio, conflictos y bloqueos en rebases y fusiones. Permanecen localmente para trazabilidad y reproducibilidad, pero no se subirán a GitHub ni generarán conflictos futuros.
- Auditoría científica completa: todos los tests pasan (316/316), cobertura 98% en sim/prototipo_rl_simbiosis.py.
- Documentación y tracking actualizados para reflejar la validación y reproducibilidad.

- **Actualización Fase 2 (18/11/2025)**: Aplicados parches de Gemini para desglose PGF (Bruto, Costo). Evaluator actualizado para retornar PGF_Bruto/PGF_Costo. Simulador captura evolución, padding y exporta en CSVs/gráficos. Prueba risk_sweep ejecutada con 10 episodios, métricas no cero confirmadas. Commit realizado. Listo para experimentos "Tensión de Riesgo".

## Próximos pasos
- Ejecutar risk_sweep completo con 1000 episodios por agente.
- Generar gráficos obligatorios para Fase 2.
- Validar resultados experimentales y preparar reporte científico.
- Mantener cobertura ≥98% en futuras ramas.

## Auditoría
- Última validación: pytest --cov=sim.prototipo_rl_simbiosis --cov-report=term-missing
- Última exportación: python sim/prototipo_rl_simbiosis.py --episodes 10 --seed 42 --risk_scale 1.0 --export results/test_run_fase2.json
- Prueba Fase 2: python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 10

## Historial de cambios
- 18/11/2025: Refactorización, instrumentación Fase 2, cobertura 98%, documentación actualizada.
- 18/11/2025: Parches Fase 2 aplicados, commit realizado, prueba risk_sweep validada.
