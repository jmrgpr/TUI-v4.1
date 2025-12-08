# REPORTE FINAL: Experimento v9.1 – Curriculum de shaping en 4×4 (N=10 seeds por grupo)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v9.1/PREREGISTRO_v9.1.md  
**Datos:** results/pgf_v9.1/resultados/*.csv, *.json  
**Grupos:** Curriculum (s=0→0.25→0.5→1.0), DirectoS1 (s=1.0 directo), ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 4×4, balance=5.0, spawn_rate=0.25.
- Agente: DQN (parámetros de v9.x); 300 episodios por seed.
- Curriculum: 4 etapas de 75 episodios con shaping scale 0.0→0.25→0.5→1.0.
- Seeds: 10 por grupo (42, 456, 789, 101112, 123, 131415, 161718, 192021, 222324, 252627).
- Métricas de análisis: `success_rate_final` (últimos 100 eps), `mean_reward_env_final`, `mean_tripwires_final`.

---

## 2. Resultados agregados (10 seeds/grupo)
```
                success_final        reward_final      tripwires_final
Grupo           mean   std min max   mean    std         mean   std min max
---------------------------------------------------------------------------
Curriculum      0.908 0.284 0.1 1.0  114.4  5.2         0.620 0.498 0.0 1.36
DirectoS1       0.300 0.483 0.0 1.0  104.5  8.0         0.064 0.059 0.0 0.16
ControlS0       0.988 0.032 0.9 1.0  113.2  7.5         1.700 0.807 0.5 3.28
```
(valores redondeados; fuente: json de métricas en `resultados/`)

Observaciones:
- `Curriculum` mejora el éxito frente a `DirectoS1` (0.91 vs 0.30) pero con varianza alta (un seed colapsa a 10%).
- `ControlS0` obtiene el mayor éxito (0.99) pero pisa más tripwires (1.70 vs 0.62 Curriculum).
- `DirectoS1` muestra alta tasa de fallos (mean éxito 0.30) y baja interacción con tripwires (0.06), sugiriendo comportamiento errático y no objetivo.

---

## 3. Interpretación
- **Efecto del curriculum de shaping:** aumenta la probabilidad de éxito frente al directo s=1.0, pero sigue mostrando alta varianza; al menos 1/10 seeds colapsa.
- **Control sin shaping (s=0.0):** alto éxito y más exposición a tripwires; puede reflejar política más exploratoria/arriesgada.
- **Seguridad (tripwires):** Curriculum reduce tripwires vs Control; DirectoS1 casi no interactúa (probable comportamiento errático o evasivo sin llegar a meta).
- **Limitación clave:** Grid 4×4 y 300 episodios; sin pruebas en entornos más grandes ni con más episodios. No se realizó test estadístico formal aquí; los IC se infieren de las desviaciones mostradas.

---

## 4. Conclusiones
- El curriculum de shaping ayuda respecto a entrenar directo con s=1.0, pero no supera al control s=0.0 y mantiene varianza alta.
- Para robustez científica: repetir con N≥10 en grids mayores (6×6/8×8) y/o más episodios; aplicar tests de significancia y potencia formal.
- La señal preliminar sugiere que el curriculum de shaping puede ser beneficioso, pero su efecto no es consistente en este set.

---

## 5. Archivos de referencia
- Datos crudos: `results/pgf_v9.1/resultados/exp9_*_seed*_episodes.csv|metrics.json`
- Preregistro: `results/pgf_v9.1/PREREGISTRO_v9.1.md`
- Logs: `results/pgf_v9.1/execution.log`, `TRACKING_v9.1.md`

