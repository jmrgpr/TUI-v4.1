# Experimento 3: Análisis de la Curva Goldilocks (PGF v6)

**Fecha análisis**: 2025-12-03 09:04:57  
**Datos analizados**: 25 configuraciones (24 robustos)  
**Outliers detectados**: 1

---

## 1. Resumen de Datos

### Configuraciones Ejecutadas
- **Densidades probadas**: [0.05, 0.1, 0.2, 0.3, 0.4]
- **Seeds por densidad**: [42, 123, 456, 789, 101112]
- **Episodios por agente**: 300 PGF + 300 Control

### Estadísticas Generales (Robustos)

| Densidad | N | Ratio medio | Std | D_eff medio |
|----------|---|-------------|-----|-------------|
| 0.05 | 5 | 99.82% | 4.16 | 0.245 |
| 0.1 | 5 | 95.79% | 13.57 | 0.449 |
| 0.2 | 5 | 98.93% | 10.23 | 0.851 |
| 0.3 | 5 | 100.72% | 4.25 | 1.244 |
| 0.4 | 4 | 103.07% | 3.01 | 1.643 |

---

## 2. Comparación de Modelos

| Modelo | Ecuación | AIC | BIC | RSS |
|--------|----------|-----|-----|-----|
| Constant | `ratio = 99.52` | 100.49 | 101.67 | 1453.44 |
| Linear | `ratio = 3.26D + 96.74` | 101.41 | 103.76 | 1389.42 |
| Quadratic | `ratio = 2.43D² + -1.30D + 98.25` | 103.29 | 106.82 | 1382.66 |
| Logarithmic | `ratio = 100.24 + 1.96log(D)` | 101.76 | 104.12 | 1410.29 |
| Exponential | `ratio = 96.76exp(0.03D)` | 101.40 | 103.76 | 1389.12 |

**Mejor modelo (menor AIC)**: **Constant**

---

## 3. Verificación de Criterios Goldilocks

**Criterios cumplidos**: 1/5

❌ **1. 1 Correlation**
   - Valor observado: `r=0.210, p=0.3249`
   - Umbral preregistrado: `|r|>0.5, p<0.01`

❌ **2. 2 Quadratic Wins**
   - Valor observado: `ΔAIC=1.88`
   - Umbral preregistrado: `ΔAIC<-4`

❌ **3. 3 Inverted Parabola**
   - Valor observado: `a=2.426, IC95%=[-8.6936882  16.72989529]`
   - Umbral preregistrado: `a<0, IC95%<0`

❌ **4. 4 Maximum Range**
   - Valor observado: `D*=0.268`
   - Umbral preregistrado: `0.7≤D*≤1.5`

✅ **5. 5 Peak Ratio**
   - Valor observado: `ratio(D*)=98.08%`
   - Umbral preregistrado: `>95%`


---

## 4. Veredicto Final

### ❌ HIPÓTESIS GOLDILOCKS NO CONFIRMADA

La hipótesis H1 NO es soportada por los datos. La relación ratio(D) no sigue parábola invertida.

**Recomendación**: Explorar formas funcionales alternativas o paper metodológico
