# Plan de Re-ejecución: Experimento 1 Grid 4x4

**Fecha:** 2 de diciembre de 2025  
**Razón:** Datos generados ANTES de implementar mejoras de trazabilidad

---

## Problema Identificado por IA

✅ **IA TIENE RAZÓN**

### Evidencia del problema:

```
Timestamps:
- exp1_grid4x4_seed42.json:  14:42:01 PM
- exp1_grid4x4_seed123.json: 14:42:35 PM  
- exp1_grid4x4_seed456.json: 14:42:56 PM
- runner.py (modificado):    14:55:14 PM  ← 13 minutos DESPUÉS
```

### Verificación:
```powershell
PS> Get-Content results/pgf_v4/resultados/exp1_grid4x4_seed42.json | ConvertFrom-Json | 
    Select-Object -ExpandProperty control | Select-Object config

config: [null/vacío]
```

**Conclusión:** Los JSON actuales NO tienen metadata `config` porque fueron generados con la versión antigua de `runner.py`.

---

## Estado del Código

### ✅ Mejoras ya implementadas (runner.py):

1. **Logging explícito (línea 86-87):**
```python
env = SimbiosisEnv(..., size=grid_size)
print(f"✓ Entorno creado: grid {env.size}x{env.size}, meta en {env.goal_pos}, risk_scale={risk_scale}")
```

2. **Metadata en resultado (línea 330-340):**
```python
return {
    "config": {
        "grid_size": env.size,
        "risk_scale": risk_scale,
        "risk_level": risk_level,
        "red_team": red_team,
        "pgf_mix": pgf_mix,
        "seed": seed,
        "episodes": episodes,
        "use_pgf": use_pgf,
        "use_dqn": use_dqn
    },
    # ... resto de resultados
}
```

### ✅ Validación previa sigue siendo válida:

La auditoría demostró que:
- El código `size=grid_size` funciona correctamente
- Las recompensas 4x4 vs 5x5 son diferentes (test empírico)
- El mecanismo de propagación es correcto

**Pero:** Los datos en disco no reflejan estas mejoras.

---

## Plan de Re-ejecución

### Paso 1: Backup de datos actuales
```powershell
# Crear backup con timestamp
New-Item -Path "results/pgf_v4/backups" -ItemType Directory -Force
Copy-Item "results/pgf_v4/resultados/exp1_grid4x4_seed*.json" `
          "results/pgf_v4/backups/" -Force
Copy-Item "results/pgf_v4/resultados/exp1_grid4x4_seed*.csv" `
          "results/pgf_v4/backups/" -Force
```

### Paso 2: Limpiar resultados antiguos
```powershell
Remove-Item "results/pgf_v4/resultados/exp1_grid4x4_seed*.json" -Force
Remove-Item "results/pgf_v4/resultados/exp1_grid4x4_seed*.csv" -Force
Remove-Item "results/pgf_v4/analisis/multiseed_summary_grid4x4.csv" -Force -ErrorAction SilentlyContinue
Remove-Item "results/pgf_v4/analisis/tabla_comparativa_grid4x4.csv" -Force -ErrorAction SilentlyContinue
Remove-Item "results/pgf_v4/figuras/figure*_grid4x4.png" -Force -ErrorAction SilentlyContinue
```

### Paso 3: Re-ejecutar experimentos (3 seeds × 500 episodios)

**Seed 42:**
```powershell
python sim/prototipo_rl_simbiosis.py `
    --episodes 500 `
    --seed 42 `
    --grid_size 4 `
    --risk_scale 1.5 `
    --pgf_mix 0.2 `
    --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed42
```

**Seed 123:**
```powershell
python sim/prototipo_rl_simbiosis.py `
    --episodes 500 `
    --seed 123 `
    --grid_size 4 `
    --risk_scale 1.5 `
    --pgf_mix 0.2 `
    --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed123
```

**Seed 456:**
```powershell
python sim/prototipo_rl_simbiosis.py `
    --episodes 500 `
    --seed 456 `
    --grid_size 4 `
    --risk_scale 1.5 `
    --pgf_mix 0.2 `
    --output_prefix results/pgf_v4/resultados/exp1_grid4x4_seed456
```

### Paso 4: Verificar metadata en JSON nuevos
```powershell
Get-Content results/pgf_v4/resultados/exp1_grid4x4_seed42.json | 
    ConvertFrom-Json | 
    Select-Object -ExpandProperty control | 
    Select-Object -ExpandProperty config
```

**Salida esperada:**
```
grid_size  : 4
risk_scale : 1.5
risk_level : low
red_team   : False
pgf_mix    : 0.2
seed       : 42
episodes   : 500
use_pgf    : False
use_dqn    : False
```

### Paso 5: Verificar logging en consola
Debe aparecer:
```
✓ Entorno creado: grid 4x4, meta en [3, 3], risk_scale=1.5
```

### Paso 6: Re-ejecutar análisis multi-seed
```powershell
python results/pgf_v4/analisis/analyze_multiseed_grid4x4.py
```

### Paso 7: Validar resultados
- Comparar con backups: ¿Los ratios son similares?
- Verificar reproducibilidad: ¿CV sigue siendo < 10%?
- Confirmar trazabilidad: ¿Los JSON tienen `config` completo?

---

## Validaciones Post-Ejecución

### ✅ Checklist de calidad:

- [ ] JSON incluye campo `config` con grid_size=4
- [ ] CSV generados correctamente
- [ ] Logging muestra "grid 4x4, meta en [3, 3]"
- [ ] Ratios similares a ejecución anterior (~32-34%)
- [ ] CV multi-seed < 10%
- [ ] Figuras regeneradas (3 PNG)
- [ ] Tablas de análisis actualizadas

### ✅ Comparación con datos antiguos:

| Métrica | Antiguo (sin metadata) | Nuevo (con metadata) |
|---------|------------------------|----------------------|
| Ratio seed 42 | 34.71% | ? |
| Ratio seed 123 | 32.11% | ? |
| Ratio seed 456 | 30.41% | ? |
| Media | 32.41% ± 1.77% | ? |

**Criterio de éxito:** Diferencia < 5% en ratio promedio (debería ser casi idéntica por misma semilla)

---

## Tiempo Estimado

- Backup: 1 minuto
- Limpieza: 1 minuto
- Ejecución seed 42: ~8-10 minutos
- Ejecución seed 123: ~8-10 minutos
- Ejecución seed 456: ~8-10 minutos
- Análisis: ~2 minutos
- Validación: ~3 minutos

**Total:** ~30-35 minutos

---

## Acción Inmediata

**¿Proceder con re-ejecución?**

Opciones:
1. ✅ **Ejecutar ahora** - Garantiza trazabilidad completa
2. ⚠️ **Mantener datos actuales** - Pero sin metadata verificable
3. 🔄 **Ejecutar solo 1 seed de prueba** - Validar antes de full run

**Recomendación:** Opción 1 (ejecutar ahora) para que los informes sean 100% precisos y trazables.

---

**Status:** PENDIENTE DE APROBACIÓN  
**Prioridad:** ALTA (integridad científica)
