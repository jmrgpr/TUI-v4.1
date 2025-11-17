# CHANGELOG

## [2025-11-17] Refactor Metodológico - Eliminación del Oráculo en DQN (3:19 PM)
- Eliminado el método `calcular_metricas` interno del agente DQN para evitar bias metodológico (oráculo) y asegurar pureza en experimentos RL.
- Externalizado el cálculo de métricas PGF a `EvaluatorPGF` independiente, garantizando que el agente reciba recompensas como valores negros.
- Actualizados todos los tests dependientes para usar el evaluador externo en lugar del método interno del agente.
- Agregado nuevo test `test_pgf_logic_independence` que valida la separación de lógica PGF del agente.
- Cobertura de tests mantenida en 97% (ligera disminución por eliminación de código interno).
- Fecha y hora de documentación: 3:19 PM, 11-17-2025.

## [2025-11-17] Mejora de Cobertura de Tests a 95%
- Agregados tests para cubrir líneas faltantes en `sim/gui_streamlit.py` (except en seed, validación de parámetros, comparación histórica).
- Agregados tests para cubrir el bloque `if __name__ == "__main__"` en `sim/toy_ped_rl_excel.py` usando runpy.
- Agregados tests para cubrir branches en `sim/prototipo_rl_simbiosis.py` (logging condicional, barrido de risk_scale, DQN control).
- Cobertura global mejorada de 92% a 95%, con módulos principales en 96-99%.
- Fecha y hora de documentación: 11-17-2025.

## [2025-11-13] Proveniencia y estructura de datos
- Se agrega el archivo `Cacería de sistemas inteligencia riesgo.txt` con documentación detallada de fuentes, estructura y referencias del dataset principal.
- Se actualiza el `README.md` para citar el nuevo archivo y resaltar la transparencia y trazabilidad de los datos.

## [2025-11-13] Mejoras en simuladores
- Correcciones y mejoras en los módulos de simulación (Aprendizaje Simbiótico, PED en sistemas reales, Sensibilidad de Pesos).
- Scripts y datos listos para publicación y revisión científica.


Para detalles de versiones anteriores, consulte el historial de commits en GitHub.

## [2025-11-17] Limpieza y profesionalización de resultados experimentales
- Se movieron los archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raíz a la carpeta `results/` para mejorar la trazabilidad y limpieza del workspace.
- Se eliminó el archivo temporal vacío `test_export_empty.json`.
Motivo: Estos archivos estaban en la raíz por prácticas de desarrollo y pruebas rápidas. Ahora, siguiendo la estructura profesional, se centralizan en `results/`.