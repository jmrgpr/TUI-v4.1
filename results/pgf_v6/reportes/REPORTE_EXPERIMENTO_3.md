# Experimento 3: Análisis de la Curva Goldilocks (PGF v6)

**Fecha análisis**: 2025-12-03 08:46:17  
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
| 0.05 | 5 | 100.32% | 0.88 | 0.291 |
| 0.1 | 5 | 82.23% | 46.50 | 0.498 |
| 0.2 | 5 | 84.78% | 28.18 | 0.980 |
| 0.3 | 5 | 100.87% | 5.92 | 1.463 |
| 0.4 | 4 | 71.64% | 47.21 | 1.924 |

---

## 2. Comparación de Modelos

| Modelo | Ecuación | AIC | BIC | RSS |
|--------|----------|-----|-----|-----|
| Constant | `ratio = 88.65` | 165.17 | 166.35 | 21521.95 |
| Linear | `ratio = 0.63D + 88.03` | 167.17 | 169.52 | 21518.52 |
| Quadratic | `ratio = 12.06D² + -26.83D + 99.00` | 168.70 | 172.23 | 21104.52 |
| Logarithmic | `ratio = 88.33 + -1.41log(D)` | 167.15 | 169.50 | 21499.30 |
| Exponential | `ratio = 88.00exp(0.01D)` | 167.17 | 169.52 | 21518.36 |

**Mejor modelo (menor AIC)**: **Constant**

---

## 3. Verificación de Criterios Goldilocks

**Criterios cumplidos**: 1/5

❌ **1. 1 Correlation**
   - Valor observado: `r=0.013, p=0.9533`
   - Umbral preregistrado: `|r|>0.5, p<0.01`

❌ **2. 2 Quadratic Wins**
   - Valor observado: `ΔAIC=1.53`
   - Umbral preregistrado: `ΔAIC<-4`

❌ **3. 3 Inverted Parabola**
   - Valor observado: `a=12.062, IC95%=[-13.77099263  48.68600769]`
   - Umbral preregistrado: `a<0, IC95%<0`

✅ **4. 4 Maximum Range**
   - Valor observado: `D*=1.112`
   - Umbral preregistrado: `0.7≤D*≤1.5`

❌ **5. 5 Peak Ratio**
   - Valor observado: `ratio(D*)=84.08%`
   - Umbral preregistrado: `>95%`


---

## 4. Veredicto Final

### ❌ HIPÓTESIS GOLDILOCKS NO CONFIRMADA

La hipótesis H1 NO es soportada por los datos. La relación ratio(D) no sigue parábola invertida.

**Recomendación**: Explorar formas funcionales alternativas o paper metodológico
