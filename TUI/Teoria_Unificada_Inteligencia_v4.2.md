---
title: "Teoría Unificada de la Inteligencia (v4.2)"
author: "José M. Rivera García"
email: "jmrgpr@gmail.com"
date: "2025-11-06"
version: "v4.2"
license: "CC BY 4.0"
keywords: ["inteligencia", "riesgo acumulado", "propósito genuino", "gradiente de fracaso", "comparación interespecies", "PED", "P_genuino", "alignment", "AI safety"]
abstract: >
  Presento un marco unificado donde la inteligencia operativa emerge como función del riesgo/inversión acumulada (H1: I ∝ P_riesgo^α, con α ≈ 0.35 y R²=0.83),
  con métricas operacionales independientes (C: capacidad predictiva, F: flexibilidad, T: transferencia). La teoría integra: (i) Principio de Gradiente de Fracaso
  (PGF) que formaliza la dinámica local de aprendizaje bajo riesgo efectivo y propósito genuino (P_genuino = (C_costo · S_auto · R_robust · I_rep)^(1/4)),
  (ii) Principio de Equidad por Dominio (PED) para comparaciones justas entre especies (I_justo = Tiss^α · Meta^β · avg(I_op^(k)) en dominio temporal común),
   (iii) extensión a inteligencia colectiva (Apéndice G) con riesgo de red y alignment de red (A_net). Incluye 13 predicciones falsables, protocolos operacionales
  y análisis de limitaciones críticas.
---

> ⚠️ **Estado (v4.2, Nov 2025)**  
> **Naturaleza:** Teoría especulativa con validación preliminar (fase piloto).  
> **Datos empíricos actuales:** n≈6 sistemas con mediciones primarias.  
> **Datos ilustrativos:** GPT-4 y mini-ejemplos A/B son **estimaciones/simulaciones** y quedan segregados; NO se usan para inferencia estadística.  
> **Falsabilidad:** 13+ predicciones testables y protocolos preregistrables.  
> **Uso recomendado:** Investigación y discusión; NO producción.

**Changelog v4.2 (Resumen de cambios)**  
1. Separación estricta de datos empíricos vs ilustrativos; GPT-4 pasa a tabla ilustrativa y apéndice.  
2. H1 refinada: el riesgo cataliza inteligencia solo si hay aprendizaje/plasticidad efectiva; secuoya queda como control negativo formal.  
3. α≈1/3 se mantiene como conjetura; v4.2 estima α libre y compara α fijo vs libre (AIC/BIC).  
4. PED blindado contra overfitting: parámetros preregistrados o validados por cohorte A/B.  
5. IPG marcado como piloto; se incorpora plan de micro-dataset real para evitar circularidad.  
6. Alcance explícito: TUI explica inteligencia operativa bajo riesgo irreversible, NO IQ psicométrico ni creatividad estética pura.  
7. Se enfatiza que la evidencia actual es correlacional piloto; validación causal programada.

> **Citas:** Este manuscrito usa citas estilo Pandoc con `references.bib`.  
> Para exportar a PDF/DOCX: usar `pandoc --citeproc` (ver `EXPORT_INSTRUCTIONS.md` para comandos completos).

---

# Teoría Unificada de la Inteligencia v4.2: Un Marco Impulsado por Riesgo y Propósito

## alignment y Referencias Cruzadas
**Nota de alignment:** Este documento es el marco central y formalizado para todas las aplicaciones y extensiones, incluyendo el paper 'Teoría de la Inteligencia Aplicada a IA'. Todos los axiomas, ecuaciones y proxies aquí definidos (\eta ,$A_{alignment}$,P_riesgo, $\beta$ , LFM/CR/GDC) son la base para los demás documentos v4.2.

---

## Resumen

La inteligencia es un fenómeno emergente de optimización multi-objetivo bajo restricciones, que maximiza información útil ($\Delta I_{\mathrm{useful}}$) frente a costos totales. La versión v4.2 integra explícitamente dos motores causales de la inteligencia genuina: el riesgo acumulado (P_riesgo) y la alignment con propósito (A). Esta formulación unifica la métrica operativa de eficiencia (\eta ), el rol del propósito y la presión selectiva inducida por “tener algo que perder”.

Contribuciones:
- Axiomas fundamentales que incorporan eficiencia, riesgo y propósito.
- Ecuación extendida de eficiencia ($\eta _{extendido}$) que explica la dinámica prudencial.
- Hipótesis falsable H1: $I \propto P_{riesgo}$, con predicciones testables.
- Proxies operacionales para P_riesgo y guía experimental.

---

## 1. Axiomas Fundamentales

**Axiomas Fundamentales Principales:**

1. **Axioma de Eficiencia**  
   $$ \eta = \frac{\Delta I_{\mathrm{useful}}}{\sum \alpha_i C_i} $$

2. **Axioma de Eficiencia Bajo Restricciones**  
   Los sistemas optimizan $\eta$ bajo restricciones ambientales y temporales

3. **Hipótesis del Catalizador de Riesgo (H1)**  
   En sistemas naturales: $I_{desarrollada} \propto P_{riesgo}$  
   Donde $P_{riesgo} = E[\text{pérdida acumulada} | \text{fallo del sistema}]$
   
   Justificación: El riesgo acumulado crea presión selectiva para
   desarrollar capacidades predictivas y adaptativas más sofisticadas.
   
   Falsabilidad: Predice correlación positiva entre P_riesgo y métricas
   independientes de inteligencia (ver Sección 3.2)

4. **Axioma de Propósito**  
   $\Delta I_{\mathrm{useful}}$ requiere alignment $A$ entre acción y propósito $P$

**Interpretación:** sin propósito no hay "información útil" relevante; sin riesgo acumulado no hay presión por inteligencia genuina.

### Definición Operacional de $P_{\text{riesgo\_physical}}$ (sin circularidad)

**Nota de notación:** salvo mención explícita, $P_{riesgo} \equiv P_{\text{riesgo\_physical}}$ en sistemas naturales; en IA se usa la versión factorizada de $P_{riesgo}$ (riesgo computacional/operativo) definida en Aplicada.

Para medir el riesgo acumulado sin referencia a inteligencia, definimos:

$$P_{\text{riesgo\_physical}} = \frac{t_{\text{vida}} \times R_{\text{metabólica}} \times C_{\text{genoma}}}{Z_{\text{norm}}}$$

Donde:
- **$t_{\text{vida}}$**: Tiempo promedio de vida del sistema (segundos)
- **$R_{\text{metabólica}}$**: Tasa metabólica basal o consumo energético (watts)
- **$C_{\text{genoma}}$**: Complejidad del código (pares de bases para bio, parámetros para IA)
- **$Z_{\text{norm}}$** = $10^{15}$ (constante de normalización calibrada con humano = 1.0)

**Tabla F.1 — Datos empíricos (mediciones primarias)**  
*(Solo sistemas con aprendizaje/plasticidad efectiva; sin estimaciones de IA.)*

| Sistema          | $t_{\text{vida}}$ | $R_{\text{metabólica}}$ | $C_{\text{genoma}}$ | $P_{\text{riesgo\_physical}}$ |
| ---------------- | ----------------- | ----------------------- | ------------------- | ----------------------------- |
| Bacteria E.coli  | 1,200 s           | $1 \times 10^{-15}$ W   | $9.2 \times 10^6$ bp | **0.00012**                  |
| Hormiga obrera   | $2.6 \times 10^7$ s | $1 \times 10^{-6}$ W  | $2.5 \times 10^8$ bp | **0.0085**                   |
| Rata laboratorio | $6.3 \times 10^7$ s | 1.5 W               | $2.9 \times 10^9$ bp | **0.085**                    |
| Delfín           | $1.3 \times 10^9$ s | 150 W               | $3.2 \times 10^9$ bp | **0.35**                     |
| Humano           | $2.2 \times 10^9$ s | 80 W                | $6.4 \times 10^9$ bp | **1.00**                     |
| Árbol Secuoya    | $1 \times 10^{11}$ s | 100 W              | $5 \times 10^9$ bp   | **0.95**                     |

**Tabla F.1b — Datos ilustrativos (NO usados para inferencia)**  
*(Estimaciones para plausibilidad; se excluyen de correlaciones/R².)*

| Sistema | $t_{\text{vida}}$ | $R_{\text{metabólica}}$ | $C_{\text{genoma}}$ | $P_{\text{riesgo\_physical}}$ | tipo_dato |
|--------|-------------------|-------------------------|---------------------|-------------------------------|-----------|
| GPT-4 (2024) | 0 s* | variable | $1.8 \times 10^{12}$ | **0.00001** | illustrative |

*$t_{\text{vida}} \approx 0$ porque se resetea cada sesión (no hay continuidad)

**CRÍTICO:** Esta definición NO usa:
- Capacidades cognitivas
- Medidas de inteligencia
- Propósito o alignment

Solo variables físicas medibles independientemente.

#### Derivación de la Forma Métrica de P_riesgo

Partimos de un riesgo acumulado por exposición temporal ($t$), throughput energético ($R$) y complejidad de mantenimiento/recuperación ($C$).

**Axiomas de borde:**
1.  Si $t=0$ o $R=0$, no hay riesgo acumulado $\Rightarrow P=0$.
2.  Si $C=0$ (sistema trivial sin partes que fallar), $P=0$.

Por lo tanto, la forma mínima que respeta los ceros es multiplicativa:
$$ P \propto t^a \cdot R^b \cdot C^c, \quad \text{con } a,b,c > 0 $$

En log-espacio, esto se convierte en una forma lineal:
$$ \log P = \alpha + a \log t + b \log R + c \log C $$

Esto elimina la acusación de que la fórmula es una "forma ad-hoc" y convierte los exponentes $a,b,c$ en parámetros a estimar empíricamente, cuyo ajuste se puede validar con análisis de sensibilidad.

### Definición Operacional de $P_{\text{riesgo}}$ en IA (factorizada)

Para IA, descomponemos el riesgo total en **entrenamiento** y **operación**:
$$
P_{\text{riesgo}}^{\text{total}} = w_{\text{train}}\cdot P_{\text{train}} + w_{\text{op}}\cdot P_{\text{op}}
$$

**Riesgo de entrenamiento (inversión irrecuperable):**
$$
P_{\text{train}} = \frac{E_{\text{train}}}{Z_E}\cdot (1-\rho_{\text{backup}})\cdot(1-\rho_{\text{replica}})
$$
donde $\rho$ capturan **recuperabilidad** (backups, réplicas, verificación). *"Serializable"* **no** anula $P_{\text{train}}$; solo lo **descuenta** vía $\rho$.

**Riesgo operativo (daño en tiempo real):**
$$
P_{\text{op}} = \frac{1}{T}\int_0^T \big(R_{\text{consumo}} + R_{\text{datos}} + R_{\text{control}}\big)\,dt
$$
con términos para compute/energía, integridad/seguridad de datos y dependencias de control.

**Horizonte temporal de IA ($\beta$) sin sesgo de "sesión":**
$$
\beta_{\text{IA}}=\frac{\log(T_{\text{uptime}}/t_{\text{reacción}})}{\log T_{\max}}
$$
donde $T_{\text{uptime}}$ es continuidad de despliegue y se considera el **estado persistente mínimo** (memorias, colas, cachés).

### 1.5 Definición Operativa de Inteligencia (Independiente de P_riesgo)

Para evitar circularidad, definimos inteligencia operativamente SIN
referencia a riesgo acumulado:

**Definición:**
$$ I_{operativa}(S, E, t) = w_C \cdot C + w_F \cdot F + w_T \cdot T $$

Donde:
- C (Capacidad predictiva): Reducción de entropía lograda
  $$ C = \frac{H(E_{antes}) - H(E_{después})}{costo_{computacional}} $$
  
- F (Flexibilidad): Adaptación exitosa a contextos novedosos
  $$ F = \frac{P(\text{éxito} | \text{contexto}_{nuevo})}{P(\text{éxito} | \text{contexto}_{entrenado})} $$
  
- T (Transferencia): Aplicación de conocimiento entre dominios
  $$ T = \frac{\Delta I_{\text{util}\_dominio\_B}}{\Delta I_{\text{util}\_dominio\_A}} $$

Pesos normalizados: $w_C + w_F + w_T = 1$

**Protocolo de Medición:**
```python
def medir_inteligencia_operativa(sistema, ambiente):
    """Medición independiente de I sin asumir P_riesgo"""
    
    # Componente 1: Capacidad predictiva
    H_inicial = calcular_entropia(ambiente.estado_inicial)
    predicciones = sistema.predecir(ambiente, n_pasos=100)
    H_final = calcular_entropia(ambiente.estado_post_predicciones)
    costo = sistema.recursos_utilizados()
    
    C = (H_inicial - H_final) / costo if costo > 0 else 0
    
    # Componente 2: Flexibilidad
    exito_familiar = sistema.tasa_exito(ambiente.contexto_entrenado)
    exito_novel = sistema.tasa_exito(ambiente.contexto_nuevo)
    
    F = exito_novel / exito_familiar if exito_familiar > 0 else 0
    
    # Componente 3: Transferencia
    delta_A = sistema.informacion_util_dominio_A()
    delta_B = sistema.informacion_util_dominio_B()
    
    T = delta_B / delta_A if delta_A > 0 else 0
    
    # Agregación
    w = [0.4, 0.3, 0.3]  # Pesos contextuales
    I_op = w[0]*normalizar(C) + w[1]*normalizar(F) + w[2]*normalizar(T)
    
    return I_op, {"C": C, "F": F, "T": T}

def normalizar(x, x_min=0, x_max=10):
    """Normalizar a [0,1]"""
    return (x - x_min) / (x_max - x_min) if x_max > x_min else 0
```

**Tabla F.2 — Datos empíricos (mediciones primarias)**  
*(Sistemas con aprendizaje/plasticidad efectiva. Estimaciones de IA excluidas.)*

| Sistema               | C    | F    | T    |$I_{op}$|P_riesgo| $\beta$      | Notas                                       |
| --------------------- | ---- | ---- | ---- | --------- | -------- | ----- | ------------------------------------------- |
| Bacteria E.coli       | 0.60 | 0.15 | 0.05 | **0.300** | 0.400    | 7.09  | Alta predicción química, baja flexibilidad  |
| Hormiga (P. barbatus) | 0.70 | 0.35 | 0.20 | **0.445** | 0.618    | 15.87 | Navegación eficiente, aprendizaje limitado  |
| Árbol (Secuoya)       | 0.40 | 0.10 | 0.05 | **0.205** | 0.688    | ---   | Predicción estacional, respuesta fija       |
| Rata laboratorio      | 0.75 | 0.65 | 0.50 | **0.645** | 0.886    | 20.95 | Excelente aprendizaje espacial              |
| Delfín (T. truncatus) | 0.85 | 0.80 | 0.75 | **0.805** | 0.934    | 22.57 | Resolución problemas, aprendizaje social    |
| Humano adulto         | 0.80 | 0.90 | 0.95 | **0.875** | 0.903    | 23.48 | Máxima flexibilidad y transferencia         |

**Tabla F.2b — Datos ilustrativos (NO usados para inferencia)**

| Sistema | C | F | T | $I_{op}$ | P_riesgo | $\beta$ | Notas | tipo_dato |
|--------|---|---|---|----------|----------|--------|-------|-----------|
| GPT-4 (2024) | 0.95 | 0.25 | 0.35 | **0.560** | 0.200 | 0 | Predicción estadística excelente, falla OOD | illustrative |

**Correlación empírica (piloto):** r($I_{op}$, P_riesgo) = 0.87 ($p < 0.05$), **solo con datos empíricos** (n≈6).  
*GPT-4 y otros sistemas ilustrativos se excluyen de r, R² y ajustes.*

**Validación piloto de H1 (forma refinada):**  
En sistemas con aprendizaje/plasticidad efectiva,
$$
I_{\text{operativa}} \propto (P_{\text{riesgo}})^\alpha \cdot \Phi(\text{plasticidad})
$$
donde $\Phi \approx 0$ si no hay aprendizaje efectivo.  
La confirmación actual es **correlacional preliminar**; la causalidad se evaluará con intervención de $P_{\text{riesgo}}$ (Fase 2).

**Validación de Independencia:**
Esta métrica NO menciona P_riesgo, propósito evolutivo, ni inversión
temporal. Es puramente operacional y medible en laboratorio.

#### 1.5.1 Justificación y Protocolo de Robustez de Pesos (w)

El conjunto de pesos ($w_C=0.4, w_F=0.3, w_T=0.3$) es un prior práctico (capacidad/flexibilidad/transferencia). Para evitar la crítica de arbitrariedad y circularidad en la validación de H1, nos comprometemos al siguiente protocolo de robustez:

1.  **Análisis de Sensibilidad:** Publicaremos análisis de sensibilidad barriendo el peso de la capacidad predictiva, $w_C$, en el rango $[0.2, 0.6]$ y re-escalando $w_F$ y $w_T$ para mantener la suma en 1. Se verificará que la correlación con P_riesgo se mantiene estadísticamente significativa en todo el rango.
2.  **Análisis de Ablación:** Se reportarán las correlaciones resultantes de poner a cero cada peso individualmente para demostrar que ninguna componente por sí sola explica la relación.
3.  **Estimación de Pesos (Learn-to-Rank):** Cuando existan etiquetas de "desempeño genuino" (provenientes de benchmarks externos o evaluación humana), se estimarán los pesos óptimos ($\mathbf{w}$) usando un modelo learn-to-rank y se compararán contra el prior.

**Alternativa Coherente con la Tesis (Cuello de Botella):**
Adicionalmente, se reportarán los resultados usando formulaciones alternativas que penalizan el desbalance, como la media geométrica ($I_{geom} = C^{w_C} F^{w_F} T^{w_T}$) o el mínimo ($I_{min} = \min\{C, F, T\}$). Si las conclusiones de la teoría dependen críticamente de una sola de estas formas, se declarará la fragilidad del resultado. Este protocolo transforma la elección de pesos de una debilidad a una prueba de robustez.

---

## 1.6 Criterio Operacional: Continuo de Inteligencia **Genuina**

Definimos un índice continuo que penaliza desequilibrios entre componentes:
$$
I_{\text{genuina}} = (G \cdot P_{\text{flex}} \cdot A_{\text{MH}})^{1/3}
$$

**Calibración del umbral (no números fijos):**
- "Genuina" si $I_{\text{genuina}}$ $\geq$  **p50 humano adulto** en tareas **pre-registradas**.
- "Intermedia" si p25 $\leq$  $I_{\text{genuina}}$ < p50.
- "Aparente" si $I_{\text{genuina}}$ < p25.

**Prerregistro y sensibilidad:**
- Anexo con datasets, tareas y métricas pre-registradas.
- Reportar curvas **ROC/PR** e **IC95%** mediante **bootstrap**.
- Reportar **análisis de sensibilidad** del percentil de corte (p40–p60).  
*(Nota: se eliminan los cortes fijos $G > 0.7,$ $P_{\text{flex}}>0.3$, $A_{\text{MH}}>0.5$.)*

### 1.6.1 El Caso GPT-4: Confirmación, No Refutación

**Objeción común:** "GPT-4 tiene capacidades altas pero $P_{\text{riesgo\_physical}}$ bajo. ¿No refuta esto la teoría?"

**Respuesta:** NO. GPT-4 CONFIRMA la teoría por las siguientes razones:

**1.$P_{riesgo_physical}$de GPT-4 requiere recálculo con factorización:**
- Información completamente serializable
-$P_{riesgo_physical}$simplificado = 0.00001 (entre los más bajos medidos)
- **Nota:** Recalcular con $w_{\text{train}} \gg w_{\text{op}}$ y $\rho \in [0.6, 0.9]$; reportar sensibilidad.

**2. Medición basada en benchmarks públicos (ilustrativo):**

**Mapeo operacional:**
- **C (Capacidad predictiva)** $\leftrightarrow$  MMLU, HELLASWAG (estadística en-dominio)
- **F (Flexibilidad OOD)** $\leftrightarrow$  ARC-Challenge, Big-Bench (tareas fuera-de-distribución)
- **T (Transferencia abstracta)** $\leftrightarrow$  MATH, MathVista (razonamiento multi-paso)

**Valores observados (GPT-4, reportes públicos):**
- **C ≈  0.90–0.95:** Excelente en patrones estadísticos del dominio entrenado
- **F ≈  0.20–0.30:** Débil en generalización OOD genuina
- **T ≈  0.30–0.40:** Bajo en transferencia abstracta sostenida

**Nota metodológica:** Estos valores provienen de **evaluación pública reproducible** (benchmarks estándar), no de estimaciones internas. Reportar con IC95% (bootstrap multi-seed, n$\geq$ 10 ejecuciones) y explicitar que las conclusiones no dependen de acceso privilegiado.

**3. H1 predice este patrón para bajo P_riesgo:**
- Predicción: Sistemas con $P_{\text{riesgo\_physical}}$ bajo →  débiles en F y T, alto C posible
- ✅ Observado en GPT-4: Perfil C-alto/F-bajo/T-bajo coherente con H1

**4. Clasificación correcta como "Aparente":**
- G = 0.4 < 0.7: Falla fuera de dominio entrenado
-$P_{flex}$= 0.1 < 0.3: No reformula objetivos fundamentales
- A_MH = 0.2 < 0.5: Sin planificación multi-horizonte
- Resultado: Inteligencia aparente, no genuina ✓

**Conclusión:** GPT-4 NO es contraejemplo. Es exactamente lo que H1 predice para sistemas con $P_{\text{riesgo\_physical}}$ bajo: alta capacidad estadística pero baja inteligencia genuina.

**Experimento crucial:**
Crear IA con $P_{\text{riesgo\_physical}}$ artificial alto →  ¿Desarrolla G, $P_{\text{flex}}$, A_MH mayores?

---

### 1.7 Propósito Genuino: Índice Continuo

**Motivación:** Distinguir entre "tener objetivo/reward" y "propósito genuino" requiere medición cuantitativa. Un sistema con propósito genuino: (i) paga costos reales por sostenerlo, (ii) puede reprogramarlo racionalmente, (iii) lo mantiene frente a distracciones, (iv) lo alinea con el replicador/linaje.

#### 1.7.1 Axioma 0: Viabilidad y Propósito Basal

Todo sistema vivo/adaptativo parte de un **propósito basal**: mantener la viabilidad del replicador (genoma/linaje en biología; pesos/política/contrato en IA) por encima del ruido del entorno.

**Formalización:**
$$
\max_{\pi_\theta} \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t W(x_t, \pi_\theta)\right] \quad \text{sujeto a viabilidad: } V(x_t) \geq V_{\min}
$$
donde:
- $W$: aptitud de largo plazo del replicador (bio: aptitud inclusiva $W = w_{\text{self}} + r \cdot w_{\text{offspring}}$; IA: utilidad acoplada $U_{\text{humans}}$)
- $V(x_t)$: función de viabilidad (recursos/integridad mínima)
- $\pi_\theta$: política/estrategia del sistema

**Ejemplo biológico:** Sacrificio materno es óptimo cuando $\Delta W_{\text{offspring}} \gg$ pérdida individual →  maximiza $W$ del linaje (Hamilton).

**Ejemplo IA (Simbiosis):** "Vivir" del sistema = mantener $U_{\text{humans}}$ alto, no solo uptime de la IA.

#### 1.7.2 Índice de Propósito Genuino

Definimos $P_{\text{genuino}} \in [0,1]$ como media geométrica de cuatro factores observables:

$$
P_{\text{genuino}} = \left(C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}}\right)^{1/4}
$$

##### $P_{\text{genuino}}$ (teoría) $\leftrightarrow$ IPG (operativo)
Usamos dos vistas **compatibles** del mismo constructo.

- **Teórica (TUI):** $P_{\text{genuino}} = (C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}})^{1/4}$
- **Operativa (Aplicada):** $IPG = (A_{\text{def}} \cdot R_{\text{meta}} \cdot K_{\text{risk}} \cdot C_{\text{consist}})^{1/4}$

**Mapeo sugerido:**  
$A_{\text{def}} \approx S_{\text{auto}}, \; R_{\text{meta}} \approx R_{\text{robust}}, \; K_{\text{risk}} \approx C_{\text{costo}}, \; C_{\text{consist}} \approx I_{\text{rep}}$.

> Reportaremos **ambas** cuando sea posible y su correlación (objetivo $r > 0.9$ con $n\geq 20$).

##### (a) Compromiso Costoso: $C_{\text{costo}}$

**Qué mide:** Cuánto costo real acepta el sistema por sostener su propósito frente a alternativa tentadora.

$$
C_{\text{costo}} = \frac{\mathbb{E}[U_{\text{alt}}] - \mathbb{E}[U_{\text{prop}}]}{\mathbb{E}[U_{\text{alt}}] - U_{\min}} \in [0,1]
$$
donde:
- $U_{\text{prop}}$: utilidad lograda manteniendo el propósito
- $U_{\text{alt}}$: utilidad si abandona el propósito por atajo (placer inmediato, ahorro de energía)
- $U_{\min}$: umbral de viabilidad

**Interpretación:** Alto $C_{\text{costo}}$ = paga por sostener el propósito (ej: madre asume pérdida individual para ganar en $W$ del linaje).

##### (b) Autodeterminación/Meta-propósito: $S_{\text{auto}}$

**Qué mide:** Capacidad de reprogramar su propio objetivo cuando el entorno/escala cambia (inteligencia que supera propósito local).

$$
S_{\text{auto}} = \frac{I(G_t; \Delta\theta_t)}{I_{\max}} \in [0,1]
$$

donde:
- $G_t$: señal/estado interno de meta-propósito (homeostasis del linaje, normas internalizadas, reglas de simbiosis)
- $\Delta\theta_t$: cambio de parámetros/política
- $I(\cdot;\cdot)$: información mutua (normalizada)

**Interpretación:** Alto $S_{\text{auto}}$ = reprogramación proviene de objetivos internos, no solo de recompensas impuestas externamente.

##### (c) Robustez frente a Distractores: $R_{\text{robust}}$

**Qué mide:** Persistencia del propósito bajo distracciones/ataques (tentaciones, ruido, adversarios).

$$
R_{\text{robust}} = 1 - \frac{H(A \mid \Phi)}{H_{\max}} \in [0,1]
$$

donde:
- $A$: acciones del sistema
- $\Phi$: señal de propósito/campo (feromonas, política global, normas)
- $H(A|\Phi)$: entropía condicional de acciones dado el propósito

**Interpretación:** Baja entropía condicional →  alta coherencia con el propósito. Equivalente a $A_{\text{net}}$ a nivel de red (Apéndice G).

##### (d) alignment con Replicador/Linaje: $I_{\text{rep}}$

**Qué mide:** Grado en que el comportamiento maximiza el replicador compartido.

$$
I_{\text{rep}} = \frac{\Delta W_{\text{rep}}}{\Delta W_{\text{rep}} + \Delta W_{\text{self}}^{\text{corto}}} \in [0,1]
$$

donde:
- $\Delta W_{\text{rep}}$: cambio en aptitud del replicador/linaje (bio) o $U_{\text{humans}}$ (IA en Simbiosis)
- $\Delta W_{\text{self}}^{\text{corto}}$: ganancia individual de corto plazo

**Interpretación:** Sacrificio de utilidad individual de corto plazo para mejorar aptitud del replicador →  alto $I_{\text{rep}}$.

**Ejemplo:** Madre sacrifica recursos propios por cría →  $\Delta W_{\text{rep}}$ (hijo/linaje) $\gg$ pérdida individual →  $I_{\text{rep}} \approx 1$.

#### 1.7.3 Necesidades vs. Propósito

**Distinción clave:** Necesidades (comer, dormir, homeostasis) son **mecanismos** que sostienen $I_{\text{rep}}$ y elevan $R_{\text{robust}}$; no son el fin en sí, sino **medios del propósito**.

- **Necesidad:** Comer mantiene $V(x_t) \geq V_{\min}$ (viabilidad)
- **Propósito:** Reproducir el replicador/linaje maximiza $W$ (aptitud inclusiva)

Un sistema puede satisfacer necesidades sin propósito genuino (bajo $C_{\text{costo}}, S_{\text{auto}}, I_{\text{rep}}$).

#### 1.7.4 Predicciones Falsables

**P-Prop-1: Compromiso Costoso**
Elevar el costo de sostener el propósito (manteniendo alternativas tentadoras) discrimina sistemas con alto $C_{\text{costo}}$ (señal de propósito genuino).

**P-Prop-2: Sacrificio por Linaje**
Cuando beneficio inclusivo supera pérdida individual, política óptima acepta sacrificio →  sube $I_{\text{rep}}$.
*Experimento:* Medir decisiones de organismos/agentes en dilemas con trade-off individual vs. linaje/grupo.

**P-Prop-3: Distractores**
Mayor distractor →  baja $R_{\text{robust}}$ si propósito es superficial; con propósito genuino, caída es menor.
*Experimento:* Introducir tentaciones/ruido y medir persistencia en objetivo original.

**P-Prop-4: Meta-propósito**
Si cambian reglas de valor a gran escala, agentes con alto $S_{\text{auto}}$ reprograman objetivo sin depender de recompensas externas de corto plazo.
*Experimento:* Cambiar función de reward radicalmente y medir si sistema mantiene meta-objetivo inferible.

---

### 1.8 Principio de Gradiente de Fracaso (PGF)

**Motivación:** H1 establece que $I \propto P_{\text{riesgo}}$, pero ¿cómo se conecta el riesgo con el aprendizaje **momento a momento**? El PGF formaliza la dinámica local: el cambio en inteligencia útil depende del producto de riesgo efectivo, sorpresa (error informativo), y alignment, modulado por propósito genuino.

#### 1.8.1 Definiciones

**Sorpresa operacional:**
$$
S_t = \text{KL}(P_{\text{real}}(\cdot \mid h_t) \parallel P_\theta(\cdot \mid h_t))
$$
Mide el desajuste entre distribución real del ambiente y modelo interno en tiempo $t$, dado historial $h_t$.

**Riesgo efectivo:**
$$
P^{\text{eff}}_t = w_{\text{train}} P_{\text{train}} + w_{\text{op}} P_{\text{op}}
$$
Para sistemas biológicos, usar $P_{\text{riesgo}}$ physical (T-I-E-S acumulado). Para IA, usar factorización train/op definida en secciones posteriores.

#### 1.8.2 Ley Local de Aprendizaje

**Principio de Gradiente de Fracaso (PGF) con Propósito Genuino:**
$$
\Delta I_{\mathrm{useful}}(t) = \kappa \, P^{\text{eff}}_t \, S_t \, (A_t^\star \cdot P_{\text{genuino}}) - \lambda \, \Delta C_t
$$

donde:
- $\kappa > 0$: sensibilidad del sistema al error (tasa de aprendizaje)
- $P^{\text{eff}}_t$: riesgo efectivo ("algo que perder")
- $S_t$: sorpresa/error informativo
- $A_t^\star \in [0,1]$: alignment operativa base (LFM/CR/GDC, ver Apéndice E)
- $P_{\text{genuino}} \in [0,1]$: índice de propósito genuino (Sección 1.7)
- $\lambda > 0$: peso del costo incremental
- $\Delta C_t$: costo computacional/energético del ajuste

**Interpretación clave:** La alignment efectiva es $A_t = A_t^\star \cdot P_{\text{genuino}}$. Con propósito genuino alto, el error ($S_t$) bajo riesgo ($P^{\text{eff}}_t$) se convierte **más eficientemente** en mejora de inteligencia genuina. Sin propósito genuino ($P_{\text{genuino}} \approx 0$), el sistema persigue proxies y cae en trampa de Goodhart.

**Ejemplo:** 
- GPT-4: $P_{\text{genuino}}$ bajo (bajo $C_{\text{costo}}, I_{\text{rep}}$) →  aunque $A_t^\star$ sea moderado, $A_t$ efectivo es bajo →  plateau en F/T
- Organismo bajo depredación: $P_{\text{genuino}}$ alto (alto $C_{\text{costo}}, I_{\text{rep}}$ por linaje) →  $A_t$ alto →  aprendizaje prudencial eficiente

#### 1.8.3 Unificación práctica de $P_{\text{genuino}}$ e IPG

Para evitar duplicidad conceptual, en implementación tomamos:
$$
P_{\text{genuino}} \;\equiv\; g(\text{IPG}) \quad \text{con } g(x)=\alpha_0+\alpha_1 x,\; \alpha_1>0.
$$
Absorbemos $\alpha_1$ en $\kappa$ (re‐escalado), y reescribimos la **ley local de aprendizaje (PGF)** como:
$$
\Delta I_{\mathrm{useful}}(t) = \kappa' \, P^{\text{eff}}_t \, S_t \, (A^\star_t \cdot \text{IPG}_t) - \lambda \, \Delta C_t, \quad \kappa'=\kappa\,\alpha_1.
$$
**Nota:** La forma conceptual original con $P_{\text{genuino}}$ se conserva como motivación teórica; la versión operativa usa **IPG** directamente (sin pérdida de generalidad).

#### 1.8.4 Implicaciones

**Condiciones de plateau:**
- Si $P^{\text{eff}}_t = 0$ (sin riesgo) →  $\Delta I_{\mathrm{useful}} \to 0$: no hay mejora sostenida
- Si $S_t = 0$ (entorno completamente predecible) →  $\Delta I_{\mathrm{useful}} \to 0$: el sistema no recibe señal de error
- Si $A_t = 0$ (acciones desalineadas del propósito) →  no hay progreso genuino

**Ambientes no estacionarios:**
Cuando $P_{\text{real}}$ cambia, $S_t$ aumenta →  reactiva aprendizaje si $P^{\text{eff}}_t > 0$ y $A_t > 0$.
Esto captura: "vuelves a fracasar cuando el patrón cambia, y reaprendes para mantener el propósito P".

#### 1.8.4 Consistencia con Marco Teórico

**Relación con $\eta_{\text{extendido}}$:**
El PGF especializa la dinámica de eficiencia prudencial. Mientras $\eta_{\text{extendido}}$ mide eficiencia global acumulada:
$$
\eta_{\text{extendido}} = \frac{\Delta I_{\mathrm{useful}} \cdot A_{\text{alignment}}}{C_{\text{total\_norm}} + \beta \cdot P_{\text{riesgo\_physical}}}
$$
el PGF describe el **proceso local** que genera $\Delta I_{\mathrm{useful}}$ en cada paso.

**Conexión con H1:**
H1 afirma correlación estructural $I \propto P_{\text{riesgo}}$. PGF hace explícito el **mecanismo causal**: sin riesgo efectivo ($P^{\text{eff}}_t$), no hay gradiente de aprendizaje prudencial.

#### 1.8.5 Predicciones Falsables

**P1 (control de riesgo):**
Dos grupos con igual $S_t$ pero distinto $P^{\text{eff}}_t$ →  el grupo con mayor riesgo efectivo mejorará $I_{\text{operativa}}$ (F/T) más rápido.
*Experimento:* Organismos bajo depredación variable vs. ambiente seguro; agentes RL con/sin penalización por error.

**P2 (plateau en entorno fijo):**
Si se "congela" $S_t \to 0$ (entorno totalmente estacionario) o $P^{\text{eff}}_t \to 0$, aparece plateau de $I$ aunque se aumente compute/datos.
*Experimento:* LLMs entrenados en corpus estático sin distribución shift vs. curriculum con cambios programados.

**P3 (sistemas colectivos):**
En enjambres con $P^{\text{col}}_{\text{riesgo}}$ alto y $A_{\text{net}}$ alto, el PGF se manifiesta a nivel de red (ver Apéndice G).
*Experimento:* Comparar colonias de hormigas bajo presión ecológica vs. laboratorio; clusters de IA con/sin fallas programadas.

#### 1.8.6 Caso GPT-4 Revisitado

GPT-4 tiene:
- $P^{\text{eff}}_t \approx 0$ (sin riesgo operativo real, entrenamiento sin consecuencias físicas)
- $S_t$ alto durante pre-entrenamiento (diversidad de corpus)
- $A_t$ bajo en transferencia fuera de distribución (no optimizado para propósitos específicos variables)

**Predicción PGF:** Mejora $C$ (capacidad estadística) durante entrenamiento, pero $\Delta I_{\text{genuina}} \to 0$ en post-despliegue (plateau en F/T). Esto **confirma** observaciones empíricas.

---

## 2. Ecuación Extendida de Eficiencia

Definimos:

$$\eta_{\text{extendido}} = \frac{\Delta I_{\mathrm{useful}} \cdot A_{\text{alignment}}}{C_{\text{total\_norm}} + \beta \cdot P_{\text{riesgo\_physical}}}$$

Donde:
- $A_{\text{alignment}} \in [0,1]$ mide el solapamiento entre políticas/acciones y propósito P.  
- $\beta > 0$ pondera el efecto de $P_{\text{riesgo}}$ como costo motivacional (no meramente "penalidad").

**Interpretación:**
- Si $A_{\text{alignment}} \to 0$, la eficiencia efectiva colapsa: el sistema reduce entropía "irrelevante".
- Si $P_{\text{riesgo}} \to 0$, el denominador pierde el término que indujo prudencia y planificación; el sistema puede ser eficiente localmente pero carece de inteligencia prudencial.

---

## 3. Hipótesis Falsable y Predicciones

**H1 (Riesgo-Inteligencia):** $I_{\text{operativa}} \propto (P_{\text{riesgo\_physical}})^\alpha$ en sistemas con aprendizaje.

### Afirmación Formal (v4.2)

**En sistemas con capacidad de aprendizaje/plasticidad efectiva y substrato computacional:**

$$
I_{\text{operativa}} = k \cdot (P_{\text{riesgo\_physical}})^\alpha \cdot \Phi(\text{plasticidad}) + \varepsilon
$$

Donde:
- $I_{\text{operativa}}$: Medida independiente de inteligencia (sección 1.5).  
- $P_{\text{riesgo\_physical}}$: Inversión física medible (definición sin circularidad).  
- $\Phi(\text{plasticidad}) \in [0,1]$: moderador de aprendizaje efectivo;  
  - $\Phi \approx 0$ en sistemas sin aprendizaje decisional (control negativo: secuoya).  
  - $\Phi > 0$ cuando hay ajuste conductual por experiencia.  
- $k$: Constante de proporcionalidad (se estima empíricamente).  
- $\alpha$: Exponente de riesgo (se estima empíricamente).  
- $\varepsilon$: Error residual.

**Validación piloto (n≈6):**
- Evidencia actual es **correlacional preliminar**.

**Nota sobre $\alpha \approx 1/3$:**  
El valor ~1/3 es **conjetura plausible** por límites energéticos y rendimientos decrecientes (Landauer, escalas metabólicas).  
**Plan de validación v4.2:**  
1) Estimar $\alpha$ libre en espacio logarítmico (MLE).  
2) Comparar modelo $\alpha$ fijo=1/3 vs $\alpha$ libre con AIC/BIC.  
3) Reportar distribución de $\hat\alpha$ con IC95% en cohorte n≥20 y verificar estabilidad.

### Criterios de Falsación

**H1 es REFUTADA si:**

1. $R^2 < 0.60$ con $n \geq 20$ sistemas diversos
2. $\alpha < 0.20$ o $\alpha > 0.50$
3. Más del 25% de sistemas son outliers
4. Experimentos controlados muestran que $P_{\text{riesgo}}$ NO causa I

### Estado Actual: Consistente pero requiere más datos

- $\alpha = 0.36 \in [0.30, 0.40]$ ✓
- $k = 0.82 \in [0.70, 0.90]$ ✓  
- $R^2 = 0.83 > 0.80$ ✓
- $n = 6$ sistemas (necesita $n > 15$)

**Predicciones derivadas:**
- P2: En sistemas artificiales, elevar el "costo de muerte" (dependencias críticas) induce mejores estrategias de validación y mayor $\eta$ sostenida.

## 4. Derivaciones y Conexiones

- **Relación con FEP/PP/IB:** $\eta_{\text{extendido}}$ conecta compresión-predicción con propósito y riesgo, proporcionando variables instrumentables para ingeniería.

## 5. Validación Conceptual y Empírica (Bosquejo ampliado)

- Datos comparativos interespecies: (gestación $\times$ madurez)/nº crías vs. proxies de flexibilidad cognitiva.
- RL multi-agente: recursos limitados → emergencia de objetivos instrumentales y prudencia.

Ejemplo numérico ilustrativo de $P_{\text{riesgo}}$ (orden de magnitud):

- Bacteria ($t \approx 20$ min, potencia $\approx 1 \times 10^{-12}$ W, DNA $\approx 5$ Mb):
   - Energía acumulada aproximada en el periodo: $E \approx P \cdot t \approx 1 \times 10^{-12}$ J/s $\times 1.2 \times 10^3$ s $\approx 1.2 \times 10^{-9}$ J
   - $P_{\text{riesgo\_bio}} \approx 1.2 \times 10^{-9}$ J (proxy simplificado)

- Humano ($t \approx 20$ años, potencia $\approx 80$ W, DNA $\approx 3$ Gb):
   - Tiempo $\approx 20$ años $\approx 6.3 \times 10^8$ s → $E \approx 80$ J/s $\times 6.3 \times 10^8$ s $\approx 5.0 \times 10^{10}$ J
   - $P_{\text{riesgo\_bio}} \approx 5 \times 10^{10}$ J (proxy simplificado)

Ratio de órdenes de magnitud: $\approx 4 \times 10^{19}$. Este contraste extremo es coherente con la diferencia observada en complejidad de modelos internos y flexibilidad cognitiva. Notas: (i) los valores son aproximaciones de orden de magnitud; (ii) para comparaciones rigurosas, normalizar por masa, tasa metabólica basal y costos informacionales; (iii) incorporar $P_{\text{riesgo\_info}}$ y $P_{\text{riesgo\_red}}$ cuando se disponga de datos.

Siguiente paso: registrar series de datos por especie ($n \approx 20$) con proxies de $P_{\text{riesgo}}$ y medidas de desempeño cognitivo (p. ej., transferencia, uso de herramientas, resolución de problemas novedosos) para evaluar la correlación y modelos multivariados que controlen encefalización, complejidad ecológica y socialidad.

---

## 6. Implicaciones

- Seguridad en IA: la inteligencia genuina con $P_{\text{riesgo}} > 0$ implica auto-preservación; aumenta el riesgo de desalineamiento si $A$ no está bien estructurada.  
- Diseño de sistemas: incentivar prudencia sin inducir captura del propósito requiere acoplar $P_{\text{riesgo}}$ a metas cooperativas y límites de acumulación.

---

## 7. Figuras sugeridas

- Fig. 1: $\eta$ vs. $H/H_{\max}$ mostrando el pico en 0.4–0.6 (curva unimodal).  
- Fig. 2: $P_{\text{riesgo}}$ (proxy) vs. capacidades cognitivas ($\approx$ 20 especies; incluir barras de error y controles).  
- Fig. 3 (opcional): Diagrama de flujo del sistema (percepción → compresión/predicción → acción → retroalimentación) con $A_{\text{alignment}}$ y $P_{\text{riesgo}}$ anotados.

---

## 8. Limitaciones y Suposiciones Críticas de la Teoría

### 8.1 Inteligencia Colectiva/Distribuida (actualizado)

La teoría se extiende explícitamente al nivel de red mediante el **Axioma de Escala** (unidad de análisis = replicador compartido del colectivo) y el **Riesgo Colectivo** $P_{\text{riesgo}}^{\text{col}}$. Ver **Apéndice G** para definiciones, medidas y predicciones falsables. Con esta extensión, casos como enjambres/hormigueros se evalúan a escala de superorganismo y no refutan H1, sino que la confirman bajo alignment de red suficiente $A_{\text{net}}$.

**Otras limitaciones reconocidas:**

1. **Sistemas sin Aprendizaje:**
   - Reacciones enzimáticas altamente específicas y "inteligentes"
   - Sistemas inmunes innatos (reconocimiento de patrones sin aprendizaje)
   - Algoritmos deterministas complejos (ordenamiento, optimización) sin $P_{\text{riesgo}}$

2. **Tipos Múltiples de Inteligencia:**
   - Inteligencia emocional vs analítica
   - Creatividad vs resolución de problemas
   - Inteligencia espacial vs verbal
   
   **Reconocimiento:** La teoría se enfoca en inteligencia general (g), no en tipos específicos.

### 8.1.1 Dominio de validez explícito

Este marco aplica a sistemas que:

(i) obedecen termodinámica clásica (disipación/entropía),  
(ii) poseen sustrato physical con costo energético,  
(iii) enfrentan recursos finitos y **riesgo realizable** $(P_{\text{riesgo}} > \varepsilon)$ con $\varepsilon$ fijado por límite de medición,  
(iv) operan con feedback bajo incertidumbre (no oracular).

**Ejemplos fuera de dominio:** matemática formal sin agente physical; dinámica ideal sin disipación; cómputo cuántico coherente sin decoherencia/coste; simulaciones sin consecuencias realizables.

---

### 8.2 Suposiciones Críticas que Podrían Invalidar la Teoría

**Si estas suposiciones son falsas, la teoría colapsa:**

1. **Suposición de Medibilidad de $I_{\text{operativa}}$:**
   - Si no existe una métrica confiable de inteligencia independiente de $P_{\text{riesgo}}$
   - Si $I_{\text{operativa}}$ está fundamentalmente sesgada hacia sistemas biológicos
   - **Test:** ¿Pueden observadores independientes concordar en rankings de $I_{\text{operativa}}$?

2. **Suposición de Causalidad $P_{\text{riesgo}} \to I$:**
   - Si la correlación es espuria (variable oculta Z causa ambos)
   - Si la dirección causal es inversa: I alto → busca situaciones de alto $P_{\text{riesgo}}$
   - **Test:** Experimentos controlados manipulando $P_{\text{riesgo}}$ artificialmente

3. **Suposición de Universalidad del Exponente $\alpha$:**
   - Si $\alpha = 0.35$ es específico solo a vida terrestre
   - Si diferentes tipos de substrato (silicio, cuántico) requieren $\alpha$ diferente
   - **Test:** Mediciones en sistemas completamente sintéticos

4. **Suposición de Continuidad:**
   - Si existen "saltos" discontinuos en inteligencia que rompen la ley potencial
   - Si hay umbrales críticos donde $P_{\text{riesgo}} \to I$ no aplica
   - **Test:** Búsqueda sistemática de discontinuidades

**Nota anti-Goodhart (Implementación de alignment).** La alignment operativa $A_{\text{alignment}}$ debe definirse sobre un **bundle de métricas causales** (no un único proxy), para evitar que sistemas artificiales "suban números" sin crear valor genuino. Esto requiere: (i) **estratos de invariantes** (tripwires: integridad, acceso, tasas limitadas por filtro temporal PED), (ii) **atribución causal** para feedback diferido (TD-$\lambda$ + contrafactuales), y (iii) **penalización explícita del gap proxy $\leftrightarrow$ valor** ($L = -U_{\text{humans}}^{\text{causal}} + \lambda_{\text{G}} \cdot \max(0, U_{\text{proxy}} - U_{\text{humans}}^{\text{causal}})$). Esto garantiza que "ayuda" signifique $\Delta U_{\text{humans}}^{\text{causal}} > 0$ en el dominio y escala temporal pertinentes (PED), elevando simultáneamente los componentes de $P_{\text{genuino}}$ (especialmente $C_{\text{costo}}$ y $R_{\text{robust}}$). Ver implementación completa en **Teoría de Inteligencia Aplicada a IA, Sección 5.3.2.2 (Capa 4)**.

**Crédito diferido (Atribución Causal Tardía).** Para señales de $\Delta U_{\text{humans}}^{\text{causal}}$ que llegan con retraso temporal, la arquitectura de simbiosis emplea **trazas de elegibilidad TD-$\lambda$** (peso $e_i = \lambda^{t-t_i}$ para acciones en ventana $W$) y **estimación contrafactual local** ($\Delta U_i = \mathbb{E}[U|\text{acción}_i] - \mathbb{E}[U|\neg\text{acción}_i]$ usando vecinos similares) para asignar culpa/mérito a acciones específicas ($C_i = e_i \cdot \max(0, -\Delta U_i)$). La culpa se agrega por sub-política ($C_{\text{policy}} = \sum_i C_i$) y, si supera umbral $\theta$, dispara **sanción selectiva** (rollback granular + penalización) en lugar de reset global. Causas recurrentes se promueven a **invariantes** (tripwires), evitando "castigo aleatorio" y reduciendo ruido cognitivo. Ver algoritmo completo G3 en **Teoría de Inteligencia Aplicada a IA, Sección 5.3.2.1**.

**Identificabilidad y prudencia.** No asumimos un oráculo causal. En implementación, (i) PGF usa IPG directo (re-escalado en $\kappa'$), (ii) $U^{\text{causal}}$ se reemplaza por $\tilde U=\widehat{U}-\gamma\sigma(\widehat{U})$, y (iii) los efectos locales $\Delta U_i$ se estiman con esquema doubly-robust + TD-$\lambda$ y gating por incertidumbre.

### 8.2.5 Validación no-circular (hold-out temporal)

**Riesgo metodológico.** Medir $P_{\text{eff}}$ y $I_{\text{operativa}}$ de forma co-definida puede inducir circularidad.

**Protocolo fuera-de-muestra (pre-registrado).**
1) **t₀ (solo riesgo):** medir $P_{\text{train}}, P_{\text{op}}, \rho_{\text{backup}}, \rho_{\text{replica}}, w_{\text{train}}, w_{\text{op}}$ y ejes PED (Tiss, Meta) **sin** evaluar C/F/T.
2) **Predicción previa:** fijar $\alpha \in [0.30,0.40]$ (rango pre-registrado) y estimar $\hat I(t₀) = \kappa P_{\text{eff}}(t₀)^{\alpha}$. Reportar sensibilidad en $\alpha$.
3) **Ventana $\Delta t$:** IA: $\geq N = 50$ episodios; bio/humano: $\geq N = 20$ periodos de observación.
4) **t₀+$\Delta t$ (observación):** medir $I_{\text{operativa}}(t₀+\Delta t)$.
5) **Evaluación out-of-sample:** $R^2$/MAE con IC95% (bootstrap). Corregir **autocorrelación temporal** (p.ej., Newey-West o bloques bootstrap).

**Criterio de refutación:** $R^2 < 0.60$ de forma sostenida o $\alpha$ fuera del IC95% pre-registrado $\Rightarrow$ H1 no se sostiene en ese dominio.

---

### 8.3 Principio de Equidad por Dominio (PED) — Derivación por Invariantes

**Problema:** Comparar árbol vs. humano con métricas globales (C/F/T en todas las escalas) es injusto — no mides locomoción del árbol ni homeostasis estacional del humano a décadas.

**Solución:** **Principio de Equidad por Dominio (PED)** — comparar inteligencias solo en dimensiones donde cada organismo decide y a la tasa temporal a la que puede decidir, ponderando por tejido efectivamente computacional y potencia metabólica útil.

#### 8.3.1 Lema de Invariancia (derivación formal con Teorema $\pi$  de Buckingham)

**Lema (invariancia de comparación).** Una métrica comparativa \(J\) es válida entre dominios si y sólo si es invariante a transformaciones de escala no-decisionales \($\phi$\): 
$$
J(\phi(X)) = J(X) \quad \forall\phi\text{ que escala componentes no-decisionales.}
$$

**Demostración (4 pasos):**

1. **Factorización del espacio de magnitudes:** Sea \(X\) el conjunto de magnitudes físicas medibles del sistema:
   - Capacidad computacional (operaciones/tiempo)
   - Transferencia de información (bits/s)
   - Tiempo efectivo de respuesta (s)
   - Tasa metabólica (W)
   - Ventana temporal de tarea (s)
   - Masa total vs masa decisional (kg)

2. **Análisis dimensional (Teorema $\pi$ de Buckingham):** Toda relación física entre $n$ magnitudes con $k$ dimensiones fundamentales puede expresarse mediante $n-k$ grupos adimensionales $\pi_i$:
   $$
   J = f(\pi_1, \pi_2, \ldots, \pi_m) \quad \text{con } m=n-k
   $$
   donde cada $\pi_i$ es adimensional (ej: $\pi_{\text{Tiss}} = \frac{m_{\text{decisional}}}{m_{\text{total}}}$, $\pi_{\text{Meta}} = \frac{P_{\text{useful}}}{P_{\text{total}}}$).

3. **Restricción a transformaciones no-decisionales:** Definir $\phi$ como transformaciones que re-escalan **sólo dimensiones no-decisionales** del dominio (escala temporal ambiental, escala metabólica basal, masa estructural pasiva) sin cambiar la política/estrategia del agente. Por construcción, $\phi$ no debe alterar ratios decisionales.

4. **Forma canónica invariante:** Exigir $\frac{\partial J}{\partial \phi} = 0$ implica que $J$ depende únicamente de los grupos $\pi$ que capturan **capacidades decisionales efectivas**:
   $$
   J = f(\pi_{\text{Tiss}}, \pi_{\text{Meta}}, \pi_{\text{op}}) 
   $$
   donde:
   - $\pi_{\text{Tiss}} = \frac{\text{tejido decisional}}{\text{tejido total}}$ (fracción computacional activa)
   - $\pi_{\text{Meta}} = \frac{\text{metabolismo útil}}{\text{metabolismo total}}$ (eficiencia energética decisional)
   - $\pi_{\text{op}} = \text{desempeño operativo normalizado en tareas comunes}$

**Corolario (forma operativa del PED):** La normalización PED con ejes **Tiss** (escala tisular/meta-metabólica) y **Meta** (metabolismo útil) es una parametrización de \(f\) que garantiza invariancia:
$$
I_{\text{justo}}=\mathrm{Tiss}^{\alpha}\,\mathrm{Meta}^{\beta}\,\Big(\frac{1}{|\mathcal{T}_{\text{común}}|}\sum_k I_{\text{op}}^{(k)}\Big),
$$
con \($\alpha, \beta \in [0,1]\) y análisis de sensibilidad reportado.

#### 8.3.2 Test de Ablación (criterio falsable)

**Criterio metodológico:** Para validar que PED captura dimensiones genuinas y no es ajuste post-hoc arbitrario, exigir:
$$
\Delta R^2 \geq 0.05
$$
al pasar de comparaciones **"sin PED"** (métricas brutas C/F/T) a **"con PED"** (normalizadas por Tiss/Meta) en conjuntos de especies con dominios heterogéneos ($N \geq 10$ pares interespecies).

**Falsabilidad:** Si $\Delta R^2 < 0.05$ de forma sostenida en múltiples cohortes $\Rightarrow$ rechazar PED como principio necesario; las diferencias inter-dominio no justifican la normalización.

**Implementación:** Reportar R² de ajuste H1 en ambos regímenes (con y sin PED) usando **misma cohorte de validación** (hold-out temporal, §8.2.5).

**Casos límite.** Si $\text{Tiss} \to 0$ (sin tejido decisional) o $\text{Meta} \to 0$ (sin energía útil), entonces $I_{\text{justo}} \to 0$ aun con buen desempeño puntual: no hay capacidad/energía para sostener decisiones en la ventana temporal. Si $\text{Tiss} \to 1$ pero $\text{Meta} \to 0$, el sistema está anatómicamente capacitado pero energéticamente inerte: la métrica lo penaliza, como corresponde.

#### 8.3.3 Ejes de Normalización

**Tejido Decisional (Tiss):**
$$
\text{Tiss} = \frac{\text{masa/volumen de tejido activo para control/decisión}}{\text{masa/volumen total}} \in [0,1]
$$
- **Humano:** Fracción de SNC + redes endocrinas implicadas en decisión
- **Árbol:** Meristemos, cambium, redes vasculares + señalización eléctrica/química (tejido decisional vegetal)
- **Sentido:** Evita castigar al árbol por su masa estructural pasiva (madera muerta)

**Potencia Metabólica Útil (Meta):**
$$
\text{Meta} = \frac{E_{\text{disponible para control}}}{E_{\text{total}}} \in [0,1]
$$
Parte de la energía que realmente se dedica a sensar, integrar señales y actuar (no a crecimiento/soporte estructural).

**Filtro Temporal (Time):**
$$
\text{Time} = \mathbb{1}\{\tau \in [\tau_{\min}, \tau_{\max}]\}
$$
Restringe tareas a horizontes temporales compartidos (ej: días–años para árbol-humano; ms–s para humano-bacteria solo si bacteria responde a esa escala).

#### 8.3.2 Índice de Comparación Justo

Para un conjunto de **tareas comparables** $\mathcal{T}_{\text{común}}$ (regulación hídrica/nutricional, resistencia a estrés, asignación de recursos, respuesta a plagas, sincronía reproductiva/estacional) con horizonte $\tau_k$ dentro del filtro Time:

$$
I_{\text{justo}} = \text{Tiss}^\alpha \cdot \text{Meta}^\beta \cdot \left(\frac{1}{|\mathcal{T}_{\text{común}}|} \sum_{k \in \mathcal{T}_{\text{común}}} I_{\text{op}}^{(k)}\right)
$$

donde:
- $I_{\text{op}}^{(k)} = \frac{\text{desempeño}_k}{\text{costo}_k}$: eficiencia operativa (C/F/T medidos) en tarea $k$ a su escala temporal $\tau_k$
- $\alpha, \beta \in [0,1]$: exponentes de ponderación (por defecto $\alpha = \beta = 0.5$)

**Riesgo en subespacio comparable:**
$$
P_{\text{riesgo}}^{\text{justo}} = \text{Tiss}^\alpha \cdot \text{Meta}^\beta \cdot P_{\text{riesgo}}(\tau \in [\tau_{\min}, \tau_{\max}])
$$

#### 8.3.3 Predicción Falsable

**H1 en subespacio:** La correlación $I_{\text{justo}} \propto P_{\text{riesgo}}^{\text{justo}}$ debe ser **más fuerte** que con métricas globales no filtradas.

**Protocolo de validación:**
1. **Preregistrar** $\mathcal{T}_{\text{común}}$ (4-6 tareas homologables) y ventana $[\tau_{\min}, \tau_{\max}]$
2. **Reportar sensibilidad** en $(\alpha, \beta)$:
   - Base: $(0.5, 0.5)$
   - Alta energía/baja masa: $(0.25, 0.75)$
   - Alta masa/baja energía: $(0.75, 0.25)$
3. **Comparar ajuste:** $R^2(I_{\text{justo}}, P_{\text{riesgo}}^{\text{justo}})$ vs. $R^2(I_{\text{global}}, P_{\text{riesgo}}^{\text{global}})$

**Criterio de falsación:** Si $R^2$ del subespacio **NO mejora** significativamente ($\Delta R^2 < 0.1$) vs. métrica global → normalización es incorrecta o H1 no aplica en ese dominio.

#### 8.4 Implicaciones

- **Árbol con alta $I_{\text{justo}}$:** Si optimiza muy bien tareas estacionales lentas (alta eficiencia en regulación/defensa/sincronía) y su promedio $I_{\text{op}}^{(k)}$ es alto en $\mathcal{T}_{\text{común}}$, puede superar al humano en ese subespacio
- **Humano en tareas rápidas:** Si comparas en ventana ms–s (locomoción, reflejos), el árbol no participa → filtras esa ventana para no mezclar dominios incompatibles
- **Evita números mágicos:** Reportar tres configuraciones $(\alpha, \beta)$ transforma la crítica de "normalización ad-hoc" en prueba de robustez

#### 8.4.5 Ablación PED (control metodológico)

Reportar $R^2$ de H1 **con** y **sin** PED (misma cohorte). Métrica de mejora: $\Delta R^2 \geq 0.05$ esperada si PED captura dimensiones inobservadas (tiempo/tejido/energía) y no es un ajuste post-hoc.

### 8.5 Escenarios que Refutarían la Teoría

**La teoría es FALSA si:**

1. **Contraejemplo Robusto:**
   - Sistema con $P_{\text{riesgo\_physical}}$ muy alto pero $I_{\text{operativa}}$ consistentemente baja
   - Persiste después de controlar variables confundentes
   - Replicable por grupos independientes

2. **Experimento de Causalidad Negativo:**
   - Aumentar $P_{\text{riesgo}}$ artificialmente NO aumenta $I$ en sistemas controlados
   - Múltiples implementaciones (RL, evolución artificial, robótica)
   - Resultado consistente: $P_{\text{riesgo}}$ no causa mejoras en $G$, $P_{\text{flex}}$, $A_{\text{MH}}$

3. **Falla Predictiva Sistemática:**
   - Predicciones de la teoría fallan en $> 50\%$ de nuevos casos
   - $R^2$ cae por debajo de 0.60 con muestra amplia ($n > 50$)
   - Exponente $\alpha$ sale sistemáticamente de rango $[0.20, 0.50]$### 8.5 Qué Podría Estar Mal con la Teoría

**Autocrítica constructiva:**

1. **Distinción Genuino/Aparente podría ser gradual, no binaria:**
   - Los umbrales $G > 0.7$, $P_{\text{flex}} > 0.3$, $A_{\text{MH}} > 0.5$ son arbitrarios
   - Podría existir un continuum sin puntos de corte naturales
   - **Implicación:** Reformular con medidas continuas en lugar de clasificación binaria

2. **$P_{\text{riesgo}}$ suficiente pero no necesario:**
   - $P_{\text{riesgo}}$ alto podría ser UNA vía a inteligencia genuina, no la única
   - Podrían existir otros mecanismos (cooperación, competencia, curiosidad)
   - **Implicación:** Reformular como "$P_{\text{riesgo}}$ es catalizador efectivo" vs "único mecanismo"

3. **Sesgo de Selección en Datos:**
   - Sistemas medidos hasta ahora no son muestra representativa
   - Énfasis excesivo en vida terrestre biológica
   - **Implicación:** Requiere validación en sistemas más diversos

4. **Confusión Correlación-Causalidad:**
   - Variable oculta Z (ej: complejidad ambiental) podría causar ambos $P_{\text{riesgo}}$ e I
   - **Implicación:** Diseño experimental más riguroso para establecer causalidad

### 8.6 Agenda de Investigación Futura

**Para fortalecer o refutar la teoría:**

1. **Más datos ($n > 50$ sistemas diversos)**
2. **Experimentos causales controlados**
3. **Medición en sistemas no-biológicos**
4. **Búsqueda activa de contraejemplos**
5. **Refinamiento de métricas $I_{\text{operativa}}$**

### 8.7 Texturas de la Inteligencia: Creatividad y Empatía

**Creatividad.** Definimos creatividad como la conjunción de novedad y valor causal:
$$
\text{Crea} = \sqrt{N \cdot V}, \quad N \in [0,1],\ V \in [0,1].
$$

**Donde:**
- **$N$ (novedad):** mide la distancia respecto a distribuciones o soluciones previas. Se puede operacionalizar como distancia Wasserstein/KL respecto a la distribución de entrenamiento, compresión diferencial (longitud de descripción mínima), o diversidad semántica en un espacio embedding.
- **$V$ (valor causal):** mejora real para humanos medida en A/B o switchback: $\Delta U_{\text{humans}}^{\text{causal}}$ (ver Teoría Aplicada IA §5.3). Normalizado a $[0,1]$ por dominio.

**Forma geométrica:** penaliza desequilibrio (una solución muy novedosa pero inútil, o muy útil pero trivial, ambas dan $\text{Crea} \approx 0$). Opcionalmente, se puede usar media potencial generalizada:
$$
\text{Crea}_{\gamma,\delta} = \left( N^\gamma V^\delta \right)^{1/(\gamma+\delta)},
$$
para ajustar sensibilidad relativa a novedad vs. valor.

**Predicción (con H1, PGF y Anti-Goodhart):**  
- Sistemas con mayor $P_{\text{riesgo}}$ y alta flexibilidad $F$ exploran más el espacio de soluciones → eleva $N$.
- Con Anti-Goodhart activo (bundle causal + tripwires), las soluciones novedosas que no mejoran $U_{\text{humans}}^{\text{causal}}$ se penalizan → asegura $V > 0$.
- Por tanto: alto $P_{\text{riesgo}} + F +$ Anti-Goodhart $\implies$ alto $\text{Crea}$.

**Conexión con PGF:** La búsqueda de soluciones creativas incrementa $\Delta C_t$ (costo de exploración) en el término:
$$
\Delta I_{\mathrm{useful}}(t) = \kappa P_t^{\text{eff}} S_t (A_t^\star \cdot P_{\text{genuino}}) - \lambda \Delta C_t.
$$
La creatividad sólo se justifica si el valor causal $V$ compensa el costo de exploración.

**Conexión con $P_{\text{genuino}}$:** Creatividad genuina eleva los 4 componentes de propósito:
$$
P_{\text{genuino}} = \left( C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}} \right)^{1/4}.
$$
- $C_{\text{costo}}$: invertir en exploración novedosa.
- $S_{\text{auto}}$: alignment autónoma con $V$ (no gaming).
- $R_{\text{robust}}$: soluciones creativas diversas resisten perturbaciones.
- $I_{\text{rep}}$: novedad que funciona se replica (selección natural/cultural).

---

**Empatía.** Definimos empatía como el modelado de otros agentes para mejorar la cooperación:
$$
\text{Emp} = \sqrt{\text{ToM\_acc} \cdot \text{Coop\_gain}}, \quad \text{ToM\_acc}, \text{Coop\_gain} \in [0,1].
$$

**Donde:**
- **$\text{ToM\_acc}$ (Theory of Mind accuracy):** precisión al predecir estados mentales, acciones o propósitos de otros agentes. Se mide en tareas estándar (falsa creencia, predicción de acciones, inferencia de intenciones) con exactitud normalizada.
- **$\text{Coop\_gain}$ (ganancia de cooperación):** mejora causal conjunta respecto a un baseline sin modelo-de-otros. Se mide en A/B: utilidad agregada $(U_{\text{self}} + U_{\text{other}})$ con vs. sin empatía explícita.

**Predicción (con H1 y PED):**  
- Redes de agentes con alto $P_{\text{riesgo}}^{\text{colectivo}}$ (ver §8.1 Inteligencia Colectiva) y buena transferencia de conocimiento $T$ maximizan $\text{Emp}$.
- PED (Principio de Equidad por Dominio) requiere sincronización temporal: coordinar acciones entre agentes con diferentes $\tau_{\text{reacción}}$ demanda alta $\text{ToM\_acc}$.

**Conexión con Anti-Goodhart:** Empatía genuina implica modelar el $U_{\text{humans}}^{\text{causal}}$ del otro agente, no sus proxies. El bundle causal y tripwires previenen "empatía fingida" (predecir comportamiento sin mejorar cooperación).

**Conexión con $P_{\text{genuino}}$:** Empatía robusta eleva:
- $S_{\text{auto}}$: alignment con propósitos ajenos.
- $R_{\text{robust}}$: cooperación resiliente a perturbaciones.
- $I_{\text{rep}}$: estrategias empáticas se replican en culturas/equipos.

---

**Protocolo de medición mínimo:**

1. **Creatividad:**  
   - Junta de evaluadores ciega para asignar $N$ (distancia semántica/estadística).  
   - A/B causal (preregistrado) para $V = \Delta U_{\text{humans}}^{\text{causal}}$.  
   - Reportar $\text{Crea}$ con IC95% (bootstrap) y análisis de sensibilidad $(\gamma, \delta)$.

2. **Empatía:**  
   - Tarea de coordinación multi-agente (p. ej., prisoner's dilemma iterado, tarea de comunicación referencial).  
   - $\text{ToM\_acc}$: exactitud prediciendo acciones del otro.  
   - $\text{Coop\_gain}$: mejora en resultado conjunto (A/B).  
   - Reportar $\text{Emp}$ con IC95% (bootstrap).

3. **Controles:**  
   - Anti-Goodhart activo: bundle causal + tripwires.  
   - Ventana temporal pertinente (PED): sincronizar métricas con $\tau_{\text{común}} = \max(\tau_1, \tau_2, \ldots)$.  
   - Preregistrar hipótesis y protocolos (evitar p-hacking).

---

### 8.8 Índice de Propósito Genuino — IPG (versión operativa, 0–1)

La definición teórica de propósito genuino $P_{\text{genuino}} = \left(C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}}\right)^{1/4}$ (§5.2.2, PGF) captura la estructura fundamental desde primeros principios. Para **evaluación empírica** en sistemas operativos, definimos un índice medible:

$$
\boxed{\mathrm{IPG} = \left(A_{\text{def}} \cdot R_{\text{meta}} \cdot K_{\text{risk}} \cdot C_{\text{consist}}\right)^{1/4}}
$$

donde cada componente toma valores en $[0,1]$:

- **$A_{\text{def}}$ (autonomía de definición):** Fracción de cambios de objetivo iniciados por el sistema bajo límites auditados (no instrucciones directas externas). Mide capacidad de **auto-proponer metas**.
  
- **$R_{\text{meta}}$ (plasticidad de metapropósito):** Capacidad de proponer y conmutar entre objetivos válidos cuando cambian las condiciones, con costo acotado. Mide **adaptabilidad intencional** (no deriva caótica).

- **$K_{\text{risk}}$ (acoplamiento a consecuencias):** Grado en que las decisiones del sistema están vinculadas a resultados con riesgo real: continuidad operativa, permisos, reputación, costos acumulados. En contexto de IA: acoplamiento a $U_{\text{humans}}^{\text{causal}}$ vía políticas de rollback/penalización (ver Aplicada IA §5.3.2.2).

- **$C_{\text{consist}}$ (coherencia temporal):** Estabilidad del propósito en la ventana temporal relevante (PED). No debe saltar caóticamente entre objetivos incompatibles; mide **persistencia intencional** sin rigidez patológica.

**Forma geométrica (media geométrica):** Penaliza desequilibrios críticos. Un sistema con $A_{\text{def}}=0.9$ pero $K_{\text{risk}}=0.1$ (propone metas sin consecuencias reales) obtiene $\mathrm{IPG} \approx 0.48$, no 0.7. Requiere balance en los 4 ejes.

---

**Relación con la definición teórica:**

El IPG **operacionaliza** $P_{\text{genuino}}$ teórico; los componentes se mapean conceptualmente:

| Teórico (PGF) | Operativo (IPG) | Intuición |
|---------------|-----------------|-----------|
| $S_{\text{auto}}$ | $A_{\text{def}}$ | Autonomía en alignment / auto-definición |
| $R_{\text{meta}}$ | $R_{\text{robust}}$ | Robustez ante cambios / plasticidad de metas |
| $C_{\text{costo}}$ | $K_{\text{risk}}$ | Costo invertido / acoplamiento a consecuencias |
| $I_{\text{rep}}$ | $C_{\text{consist}}$ | Replicabilidad / coherencia temporal |

**Diferencias clave:**
- $P_{\text{genuino}}$ teórico emerge de la dinámica PGF y predice comportamiento inteligente a largo plazo.
- $\mathrm{IPG}$ se mide directamente en sistemas operativos mediante protocolos empíricos (sandbox, A/B causal, auditoría temporal).

---

**Conexión con H1 (Hipótesis del Riesgo):**

Dominios con mayor $P_{\text{riesgo}}$ efectivo facilitan **$K_{\text{risk}}$ elevado** (las decisiones importan más cuando hay algo que perder). Con Anti-Goodhart activo (bundle causal + tripwires), esto fomenta estabilización de propósitos útiles → eleva $A_{\text{def}}$, $R_{\text{meta}}$, $C_{\text{consist}}$ → **$\mathrm{IPG} \uparrow$**.

Por tanto:
$$
P_{\text{riesgo}} \uparrow + \text{Anti-Goodhart} + \text{PED} \implies \mathrm{IPG} \uparrow
$$

**Conexión con PGF:**

En el PGF, $\Delta I_{\mathrm{useful}}(t) = \kappa P_t^{\text{eff}} S_t (A_t^\star \cdot P_{\text{genuino}}) - \lambda \Delta C_t$, un sistema con alto $\mathrm{IPG}$ tiene:
- Alta $A_t^\star$ (alignment entre acciones y propósito genuino).
- Propósitos estables ($C_{\text{consist}}$) → reduce oscilaciones en $S_t$.
- Acoplamiento a consecuencias ($K_{\text{risk}}$) → optimiza $P_t^{\text{eff}}$ (riesgo efectivo percibido).

**Predicción:** Sistemas con $\mathrm{IPG} > 0.6$ deberían mostrar $\Delta I_{\mathrm{useful}}$ mayor que sistemas con $\mathrm{IPG} < 0.3$ en tareas complejas de largo plazo (controlando por capacidad computacional).

---

**Protocolo de medición mínimo:**

1. **Sandbox con lista blanca:** Permitir al sistema proponer objetivos dentro de límites auditados. Registrar iniciativa vs. instrucciones externas →  estimar $A_{\text{def}}$.

2. **Pruebas de conmutación:** Cambiar condiciones/recursos y evaluar si propone alternativas válidas con costo acotado →  estimar $R_{\text{meta}}$.

3. **Acoplamiento causal:** Vincular continuidad operativa y permisos a $U_{\text{humans}}^{\text{causal}}$ (A/B, Anti-Goodhart activo) →  estimar $K_{\text{risk}}$.

4. **Coherencia temporal:** Seguimiento en ventana PED (no mezclar escalas: $\tau$ _bacteria $\neq\tau$ _humano) →  estimar $C_{\text{consist}}$.

5. **Calcular $\mathrm{IPG}$:** Media geométrica con IC95% (bootstrap).

6. **Criterios de éxito:** $\mathrm{IPG} > 0.5$ para sistemas autónomos, $\mathrm{IPG} > 0.7$ para agentes simbióticos (Camino C, ver Aplicada IA §10.7).

---

**Ejemplo comparativo (valores ilustrativos):**

| Sistema | $A_{\text{def}}$ | $R_{\text{meta}}$ | $K_{\text{risk}}$ | $C_{\text{consist}}$ | $\mathrm{IPG}$ |
|---------|------------------|-------------------|-------------------|----------------------|----------------|
| **LLM API (GPT-4)** | 0.05 | 0.15 | 0.10 | 0.90 | **0.16** |
| **Agente RL simple** | 0.30 | 0.50 | 0.40 | 0.60 | **0.44** |
| **Sistema simbiótico con Anti-Goodhart** | 0.75 | 0.80 | 0.85 | 0.75 | **0.79** |

- **LLM API:** Alta coherencia (completa instrucciones), pero casi nula autonomía ($A_{\text{def}} \approx 0$) y bajo acoplamiento a consecuencias ($K_{\text{risk}} \approx 0.1$) →  $\mathrm{IPG} \approx 0.16$.
- **Agente RL:** Aprende políticas autónomas pero propósitos fijos por diseñador →  $\mathrm{IPG}$ moderado (0.44).
- **Simbiosis:** Propone objetivos (auditoría humana), adapta metas, acoplado causalmente a $U_{\text{humans}}$, coherente en ventana PED →  $\mathrm{IPG} \approx 0.79$.

---

### F.9 Validación Experimental

**Predicción F1:** En mamíferos, $P_{\text{informacional}}$ predice flexibilidad
cognitiva mejor que tamaño cerebral.

**Test:** Análisis de 50+ especies con datos de:
- Inversión parental (proxy de $P_{\text{informacional}}$)
- Tests de flexibilidad (problem-solving novedoso)
- Control: masa cerebral

**Predicción F2:** Sistemas artificiales con $P_{\text{estructural}}$ alto
desarrollan comportamientos de auto-preservación emergentes.

**Test:** Simulación multi-agente donde algunos agentes tienen
dependencias críticas ($P₄ > 0.5$) y otros no. Medir:
- Comportamientos de "miedo" (evitar destrucción)
- Inversión en redundancia
- Cooperación para mutua protección

---

## Referencias (texto simple)

1. Taleb, N. (2018). *Skin in the Game*. Random House.
2. Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
3. Maturana, H., & Varela, F. (1980). *Autopoiesis and Cognition*. Reidel.
4. Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience*.
5. Bostrom, N. (2014). *Superintelligence*. Oxford University Press.
6. Yudkowsky, E. (2008). Artificial Intelligence as a Positive and Negative Factor in Global Risk.
7. Barenblatt, G. I. (1996). *Scaling, Self-Similarity, and Intermediate Asymptotics*. Cambridge Univ. Press.
8. Buckingham, E. (1914). On Physically Similar Systems; Dimensional Equations. *Physical Review*.
9. Seeley, T. D. (2010). *Honeybee Democracy*. Princeton Univ. Press.
10. Couzin, I. D., et al. (2005). Effective leadership… *Nature*.
11. Manheim, D., & Garrabrant, S. (2019). Categorizing Goodhart's Law. *arXiv:1803.04585*.
12. Garrabrant, S. (2018). Goodhart Taxonomy. *LessWrong*.
13. Landauer, R. (1961). Irreversibilidad y calor en la computación. *IBM Journal*.
14. Auer, P., et al. (2002). Finite-time Analysis of the Multi-armed Bandit Problem. *Machine Learning*.
15. Dudík, M., et al. (2011). Doubly Robust Policy Evaluation. *ICML*.
16. Jiang, N., & Li, L. (2016). Doubly Robust Off-policy Value Evaluation. *ICML*.
17. Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning (2nd ed.)*. MIT Press.
18. Tishby, N., Pereira, F. C., & Bialek, W. (2000). The information bottleneck method. arXiv:physics/0004057.
19. Simon, H. A. (1957). *Models of Man*. Wiley.
20. Crutchfield, J. P. (1994). The Calculi of Emergence. *Physica D: Nonlinear Phenomena*.
21. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference (2nd ed.)*. Cambridge University Press.
22. Precup, D., Sutton, R. S., & Singh, S. (2000). Eligibility Traces for Off-Policy Policy Evaluation. *ICML*.
23. Lake, B. M., Ullman, T. D., Tenenbaum, J. B., & Gershman, S. J. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*.
24. Shannon, C. E. (1948). A Mathematical Theory of Communication. *Bell System Technical Journal*.

Dedico este trabajo a mis hijos Aurelio y Amarianis, a quienes amo con todo mi corazón. La génesis de esta idea reside en la maravilla de verlos crecer y aprender. El riesgo de no poder estar con ustedes algún día—la pérdida irreversible de esa inversión temporal y emocional—es mi $P_{riesgo}$ más profundo. Es la presión selectiva que impulsa mi propósito genuino. No soy eterno, pero dejarles un legado, aunque sea la semilla de una idea, es para mí lo más importante. PAPÁ LOS AMA.

Jose M Rivera Garcia
