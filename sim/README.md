# README — Módulo sim

## Descripción
Este módulo contiene los componentes principales del simulador TUI v4.1, incluyendo el runner, la lógica de agentes, y las interfaces gráficas (GUI).

## GUIs disponibles
- `gui_streamlit.py`: GUI minimalista para pruebas y cobertura.
- `gui_streamlit_cli.py`: Centro de control experimental avanzado, permite ejecutar scripts reales y toy model.

## Área de mejoras y revisión científica (GUI CLI)

### Contexto
El nuevo centro de control experimental (`gui_streamlit_cli.py`) permite ejecutar cualquier script científico desde la GUI, pasando parámetros editables y reproducibles. Sin embargo, para lograr una sincronización total y evitar hardcoding de defaults, se recomienda lo siguiente:

### Mejora recomendada: Sincronización automática de parámetros
- **Añadir un bloque `EXPERIMENT_SPEC`** al inicio de cada script experimental (por ejemplo, `run_ablation_quick.py`, `run_search_pgf.py`).
- Este bloque debe definir los parámetros, tipos y valores por defecto que la GUI debe mostrar y permitir editar.
- Ejemplo:

```python
EXPERIMENT_SPEC = {
    "params": {
        "test_mode": {"type": "bool", "default": False, "label": "Modo test rápido", "flag": "--test"},
        "episodes": {"type": "int", "default": 200, "label": "Episodios", "flag": "--episodes"},
        # Añade más parámetros según el script
    }
}
```

- Si el script no tiene `EXPERIMENT_SPEC`, la GUI intentará extraer los parámetros de `argparse`.
- Así se garantiza que los valores por defecto y los parámetros estén siempre sincronizados entre la GUI y los scripts, evitando duplicación y errores.

### Justificación científica
- **Reproducibilidad:** Los experimentos pueden ser configurados y ejecutados de forma transparente y trazable.
- **Extensibilidad:** Añadir nuevos parámetros o scripts solo requiere modificar el bloque `EXPERIMENT_SPEC`.
- **Evita hardcoding:** Los valores por defecto viven en un solo lugar (el script), no en la GUI.
- **Control total:** El usuario puede modificar cualquier parámetro relevante desde la interfaz, sin perder robustez ni compatibilidad.

### Protocolo de revisión
- En cada revisión científica, verifica que los scripts tengan el bloque `EXPERIMENT_SPEC` actualizado.
- Si se añaden nuevos parámetros, actualiza el bloque y prueba la GUI para asegurar que los inputs aparecen correctamente.
- Documenta cualquier cambio relevante en este README para trazabilidad.

---

¿Dudas o sugerencias? Añade aquí tus comentarios para futuras revisiones.
