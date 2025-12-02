# Protocolo de Consolidación y Normalización de Resultados Experimentales (Completo)

Este documento fusiona el protocolo general y el específico de Experimento 2, asegurando que no se pierda información relevante.

---

## Protocolo General

Fecha: 25/11/2025
Autor: Jose M Rivera Garcia

## Objetivo
Garantizar que los datos experimentales de TUI-v4.1 y SOTA sean comparables, completos y aptos para análisis y revisión por pares.

---

## 1. Exportación de metadatos completos en SOTA
**Acción:** Modificar el pipeline de exportación de resultados para los agentes SOTA (`ppo`, `a2c`, `dqn`) para incluir:
- `seed`
- `risk_level`
- `red_team`
- (Opcional: episodios por seed)
**Justificación:** Permite agrupaciones y comparaciones directas por semilla y riesgo, igual que los agentes TUI/control/dqn_control/simbiosis.

---

## 2. Inclusión de métricas faltantes
**Acción:** Actualizar el pipeline para que exporte las métricas `robustez` y `flexibilidad` en los CSV de resultados.
**Justificación:** Estas métricas son relevantes para la evaluación científica y deben estar presentes en el dataset final.

---

## 3. Normalización de la columna `seed`
**Acción:** Asegurar que la columna `seed` tenga siempre el mismo tipo de dato (entero o string, nunca NaN) en todos los CSV antes de consolidar.
- Usar pandas: `df['seed'] = df['seed'].fillna(-1).astype(int)` o similar.
**Justificación:** Evita advertencias (`DtypeWarning`) y problemas de agrupación/filtrado.

---

## 4. Reconsolidación del archivo master
**Acción:** Unir todos los CSV (TUI, control, dqn_control, simbiosis, SOTA) en un único archivo master, asegurando que todas las columnas relevantes estén presentes y normalizadas.
- Validar que no haya NaN en columnas clave.
- Verificar que los tipos de datos sean consistentes.
**Justificación:** Permite análisis robustos y comparaciones directas entre todos los agentes y configuraciones.

---

## 5. Validación final
**Acción:**
- Realizar agrupaciones y comparaciones por agente, riesgo y semilla.
- Ejecutar scripts de análisis y visualización para comprobar la usabilidad del dataset.
- Documentar cualquier advertencia, error o anomalía detectada.
**Justificación:** Garantiza que el dataset cumple los requisitos para revisión por pares y análisis científico.

---

## 6. Documentación y trazabilidad
**Acción:**
- Registrar cada paso del proceso en `experiment_log.txt` y en el informe comparativo.
- Guardar versiones intermedias de los CSV y del master para auditoría.
- Incluir este protocolo en la documentación del repositorio.
**Justificación:** Facilita la revisión, auditoría y reproducibilidad del proceso.

---

## Ejemplo de código para normalización y consolidación (Python/pandas)
```python
import pandas as pd
from glob import glob
import os
# 1. Cargar todos los CSV relevantes, incluyendo subcarpetas y excluyendo agregados
csv_files = [f for f in glob('results/**/*.csv', recursive=True) if 'sota_all_global_summary.csv' not in f]
frames = []
for file in csv_files:
    df = pd.read_csv(file)
    # 2. Normalizar seed (no inventar valores, dejar NaN si falta)
    if 'seed' in df.columns:
        df['seed'] = df['seed'].astype(str)
    else:
        df['seed'] = None
    # 3. Añadir columnas faltantes si no existen
    for col in ['risk_level', 'red_team', 'robustez', 'flexibilidad']:
        if col not in df.columns:
            df[col] = None
    # 4. Añadir columna source_file para trazabilidad
    df['source_file'] = os.path.basename(file)
    frames.append(df)
# 5. Concatenar y guardar master
master = pd.concat(frames, ignore_index=True)
master.to_csv('results/master_results.csv', index=False, encoding='utf-8')
```

---

## Checklist para revisión por pares (objetivos a cumplir)
- [ ] Metadatos completos en SOTA (seed, risk_level, red_team, episodios por seed)
- [ ] Métricas robustez y flexibilidad presentes en todos los CSV
- [ ] Columna seed normalizada (sin NaN ni tipos mixtos)
- [ ] Archivo master consolidado y validado
- [ ] Documentación y trazabilidad completa

---

## Notas y advertencias importantes
- Actualmente, los CSV de SOTA son resúmenes por riesgo y agente, sin episodios, seed, risk_level ni red_team. Para comparabilidad real, es necesario reexportar los resultados SOTA con esos metadatos o analizarlos aparte como resúmenes.
- Las métricas robustez y flexibilidad siguen vacías en los CSV actuales; deben exportarse desde los scripts antes de reconsolidar.
- Excluir archivos agregados como `sota_all_global_summary.csv` para evitar filas espurias.
- No inventar valores de seed ausentes; dejar NaN o string vacío y documentar.
- Este protocolo debe acompañar cualquier entrega de resultados para garantizar transparencia y reproducibilidad. Actualiza el checklist conforme se vayan cumpliendo los objetivos.

---

## Protocolo específico Experimento 2

Protocolo actualizado, advertencias, objetivos pendientes y ejemplo de script para consolidar resultados de Experimento 2.
