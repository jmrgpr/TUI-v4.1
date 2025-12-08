# REPORTE FINAL: v10_multiseed – Validación seeds 13/42/101/2025/9999 (Config B 8×8)

**Fecha:** 2025-12-08  
**Datos:** `results/pgf_v10_ablation/config_B_direct_8x8/seeds/seed_*/direct_8x8_summary_*.csv`  
**Seeds:** [13, 42, 101, 2025, 9999] (múltiples corridas por seed)  
**Scripts:** `scripts/run_ablation_B_direct_8x8.py`

---

## 1. Diseño
- Config B: entrenamiento directo en 8×8 (RL puro) con hiperparámetros de `run_curriculum_complete_viable.py`.  
- Gate: 10% success en últimos 100 episodios (superado en todas las corridas).  
- Múltiples ejecuciones por seed; se agregan resultados por seed sobre todos los summaries disponibles.

## 2. Resultados agregados (success_last_100 por seed)
```
seed    mean    std    min    max
13     0.948  0.060  0.83   0.99
42     0.895  0.044  0.85   0.95
101    0.803  0.142  0.60   0.98
2025   0.802  0.109  0.67   0.99
9999   0.910  0.079  0.77   0.99
```
Todas las corridas pasan el gate (10%); éxito alto y estable en la mayoría de seeds (excepto 101/2025 con mayor varianza).

## 3. Interpretación
- Config B directo 8×8 es robusta: éxito alto (>0.8) en la mayoría de ejecuciones y seeds; gate siempre superado.  
- Varianza moderada en seeds 101 y 2025 (mínimos 0.60 y 0.67) sugiere episodios con desempeño bajo; revisar curvas si se necesita diagnóstico fino.  
- No se detectan fallos de convergencia; `convergence_episode`=-1 indica que no se aplicó detección de estabilidad, pero el éxito final es sólido.

## 4. Limitaciones
- No se consolidó en un único summary por seed (hay múltiples corridas por seed); los agregados combinan todas.  
- Sin análisis de first_success/convergence agregados; se centró en `success_last_100`.  
- No incluye curvas ni episodios; para anomalías en seeds 101/2025 revisar los CSV de episodios correspondientes.

## 5. Archivos generados
- Agregado: `results/pgf_v10_multiseed/multiseed_summary.csv` (concat de todos los summaries B 8×8).  
- Este reporte: `results/pgf_v10_multiseed/reportes/REPORTE_FINAL_v10_multiseed.md`.

## 6. Recomendaciones
- Si se requiere un único valor por seed, elegir la última corrida o hacer promedio/mediana explícita y fijarla en el preregistro.  
+- Revisar seeds 101 y 2025 con menor éxito mínimo; inspeccionar episodios para entender la caída.  
- Para trazabilidad, mantener los summaries por seed en `config_B_direct_8x8/seeds/seed_xxxx/` como evidencia.

