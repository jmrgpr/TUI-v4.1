# Experimento 1: Validación Grid 4x4 - PGF v4

## Objetivo

Confirmar la hipótesis de "dilución espacial" midiendo el rendimiento de PGF v3 en un entorno de complejidad intermedia (grid 4x4).

## Hipótesis

**H0 (Hipótesis Nula):** El ratio de desempeño PGF/Control en 4x4 no difiere significativamente de los extremos (3x3: 105%, 5x5: 39%).

**H1 (Hipótesis Alternativa):** El ratio de desempeño en 4x4 se sitúa en el rango intermedio 60-75%, confirmando una degradación lineal de la señal PGF con la complejidad espacial.

## Diseño Experimental

### Configuración del Entorno
- **Grid size:** 4x4 (16 celdas)
- **Risk scale:** 1.5 (riesgo moderado, igual que v3)
- **PGF mix:** 0.2 (igual que v3)
- **Episodes:** 500 por semilla
- **Semillas:** 3 independientes (42, 123, 456)

### Agentes a Evaluar
1. **Agente Control:** Sin PGF, maximización pura de recompensa
2. **Agente Simbiosis:** Con PGF v3 completo (bonos + señal teórica)

### Métricas Primarias
1. **Recompensa media:** μ_R ± σ_R
2. **Coeficiente de variación:** CV = σ/μ
3. **Ratio de desempeño:** R_simbiosis / R_control
4. **PGF_Bruto_Avg:** Señal PGF promedio

### Métricas Secundarias
1. **Reproducibilidad multi-semilla:** CV del ratio entre semillas
2. **Convergencia:** Análisis de últimos 100 episodios
3. **Estabilidad:** Comparación de varianza entre agentes

## Protocolo de Ejecución

### Paso 1: Preparación
```bash
cd C:\Proyectos\TUI-v4.1
```

### Paso 2: Ejecución por semilla

**Semilla 42:**
```bash
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --grid_size 4 --risk_scale 1.5 --pgf_mix 0.2 --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed42
```

**Semilla 123:**
```bash
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 123 --grid_size 4 --risk_scale 1.5 --pgf_mix 0.2 --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed123
```

**Semilla 456:**
```bash
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 456 --grid_size 4 --risk_scale 1.5 --pgf_mix 0.2 --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed456
```

### Paso 3: Análisis Estadístico

Ejecutar script de análisis multi-semilla (a crear):
```bash
python results/pgf_v4/analisis/analyze_multiseed_grid4x4.py
```

## Criterios de Éxito

### Éxito Total
- Ratio de desempeño entre 60-75%
- CV multi-semilla < 5%
- Diferencia estadísticamente significativa vs 3x3 y 5x5 (p < 0.05)

### Éxito Parcial
- Ratio fuera del rango pero con tendencia clara
- CV < 10%
- Datos reproducibles y consistentes

### Fracaso
- Ratio no diferenciable de 3x3 o 5x5
- CV > 15%
- Alta variabilidad entre semillas

## Resultados Esperados

### Archivos Generados (por semilla)
- `exp1_grid4x4_seed{N}.json` - Configuración y resumen
- `exp1_grid4x4_seed{N}_episodes.csv` - Datos por episodio

### Análisis Multi-Semilla
- `multiseed_summary_grid4x4.csv` - Estadísticas agregadas
- `tabla_comparativa_grid4x4.csv` - Comparación con 3x3 y 5x5
- Figuras: barras, boxplots, evolución temporal

## Tiempo Estimado

- Ejecución por semilla: ~5-10 minutos
- Total 3 semillas: ~30 minutos
- Análisis: ~15 minutos
- **Total:** ~45 minutos

## Notas y Precauciones

1. **Verificar entorno Python:** Confirmar que todas las dependencias están instaladas
2. **Espacio en disco:** ~10 MB por experimento
3. **Comparabilidad:** Mantener todos los hiperparámetros iguales a v3 excepto grid_size
4. **Documentación:** Registrar cualquier anomalía o comportamiento inesperado

## Próximos Pasos Post-Experimento

1. Si ratio está en 60-75%: ✅ Hipótesis confirmada → Pasar a Experimento 2 (entrenamiento extendido)
2. Si ratio > 75%: Investigar por qué 4x4 es "más fácil" de lo esperado
3. Si ratio < 60%: Investigar si hay problemas de convergencia o configuración

---

**Responsable:** Jose M Rivera Garcia  
**Fecha:** 2 de diciembre de 2025  
**Estado:** LISTO PARA EJECUCIÓN
