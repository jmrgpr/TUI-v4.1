# Resumen Ejecutivo / Executive Summary — Teoría Unificada v4.2

## ES
- **Tesis central:** La inteligencia operativa crece con el riesgo físico acumulado en sistemas con aprendizaje efectivo: \(I_{op} \propto (P_{\text{riesgo}})^\alpha \cdot \Phi(\text{plasticidad})\).
- **Fórmula núcleo:** \(I_{op} = k \cdot (P_{\text{riesgo\_physical}})^\alpha \cdot \Phi + \varepsilon\). \(\Phi \in [0,1]\) mide aprendizaje/plasticidad; \(\Phi \approx 0\) en controles sin aprendizaje (ej. secuoya).
- **Datos actuales (piloto):** n≈6 mediciones primarias (E.coli, hormiga, rata, delfín, humano, secuoya). GPT‑4 y mini A/B están segregados como ilustrativos (no cuentan para r/R²/α).
- **Resultados piloto:** r(I_op, P_riesgo) ≈ 0.87 (p<0.05) solo con datos empíricos; evidencia correlacional preliminar.
- **α ≈ 1/3:** Conjetura plausible (no probada). Plan: estimar α libre, comparar α fijo vs libre (AIC/BIC), cohorte n≥20 con IC95%.
- **Alcance y límites:** Explica inteligencia operativa bajo riesgo irreversible; no cubre IQ psicométrico ni creatividad estética. Evidencia actual es correlacional; causalidad pendiente (manipular P_riesgo).
- **Próximos pasos:** (1) Cohorte n≥20 con mediciones primarias. (2) Intervención causal variando P_riesgo. (3) Preregistro y validación out‑of‑sample de PED. (4) Mantener separación empírico vs ilustrativo en tablas.

> **Pilot stats:** r≈0.87 (p<0.05), n≈6 (solo empírico); α≈1/3 = conjetura pendiente de validación causal.

**Impacto potencial (ES):**
- Guía de diseño y evaluación para sistemas bio/IA bajo riesgo medible.
- Marco falsable para separar datos empíricos vs ilustrativos y evitar “pseudodatos”.

**Comparativa TUI vs Aplicada IA (resumen rápido)**

| Aspecto                 | TUI v4.2                                                | Aplicada IA v4.2                                 | Sinergia                                                |
|-------------------------|---------------------------------------------------------|--------------------------------------------------|---------------------------------------------------------|
| Objeto                  | Marco teórico de inteligencia operativa bajo riesgo     | Ingeniería de IA segura (Camino C, anti-Goodhart)| Aplicada usa definiciones/axiomas de TUI                |
| Núcleo                  | H1 refinada: \(I_{op} \propto (P_{\text{riesgo}})^\alpha \cdot \Phi\) | Anti-oráculo: LCB + OPE DR + gating + tripwires  | H1 informa el diseño de riesgo e IPG                    |
| Datos actuales          | n≈6 empíricos, correlacional piloto                     | Demo A/B ilustrativa (10h), sin causal robusta   | Próximos experimentos pueden compartir métrica I_op/IPG |
| Próximos pasos          | Cohorte n≥20, manipular P_riesgo, validar α/PED         | A/B largo con red team, calibrar γ/σ_thr/λ_G, validar IPG | Datos futuros de IA pueden alimentar tablas ilustrativas |

**Referencias rápidas:** ver `TUI/Teoria_Unificada_Inteligencia_v4.2.md` (H1 formal, Tablas F.1/F.2, estado v4.2).

## EN
- **Core thesis:** Operative intelligence scales with physical accumulated risk in systems with effective learning: \(I_{op} \propto (P_{\text{risk}})^\alpha \cdot \Phi(\text{plasticity})\).
- **Core formula:** \(I_{op} = k \cdot (P_{\text{risk\_physical}})^\alpha \cdot \Phi + \varepsilon\). \(\Phi \in [0,1]\) captures effective learning; \(\Phi \approx 0\) for non-learning controls (e.g., sequoia).
- **Current data (pilot):** n≈6 primary measurements (E.coli, ant, rat, dolphin, human, sequoia). GPT‑4 and mini A/B are illustrative only (excluded from r/R²/α).
- **Pilot results:** r(I_op, P_risk) ≈ 0.87 (p<0.05) on empirical data only; correlational, preliminary.
- **α ≈ 1/3:** Plausible conjecture, unproven. Plan: free α estimation, α fixed vs free via AIC/BIC, cohort n≥20 with 95% CIs.
- **Scope & limits:** Explains operative intelligence under irreversible risk; not psychometric IQ or aesthetic creativity. Evidence is correlational; causality pending (manipulate P_risk).
- **Next steps:** (1) Cohort n≥20 with primary measurements. (2) Causal intervention on P_risk. (3) PED preregistration and out‑of‑sample validation. (4) Keep empirical vs illustrative tables separate.

> **Pilot stats:** r≈0.87 (p<0.05), n≈6 (empirical only); α≈1/3 = conjecture pending causal validation.

**Potential impact (EN):**
- Design/evaluation guide for bio/AI systems under measurable risk.
- Falsifiable framework to separate empirical vs illustrative data and avoid “pseudo-data”.

**TUI vs Applied AI (quick view)**

| Aspect                  | TUI v4.2                                               | Applied AI v4.2                                  | Synergy                                                |
|-------------------------|--------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------|
| Scope                   | Theoretical framework: operative intelligence under risk | Engineering: safe AI (Path C, anti-Goodhart)     | Applied reuses TUI definitions/axioms                  |
| Core                    | H1 refined: \(I_{op} \propto (P_{\text{risk}})^\alpha \cdot \Phi\) | Anti-oracle: LCB + OPE DR + gating + tripwires   | H1 guides risk design and IPG                          |
| Current data            | n≈6 empirical, pilot correlation                       | 10h A/B demo, illustrative, not causal           | Future AI data can feed illustrative tables            |
| Next steps              | n≥20 cohort, manipulate P_risk, validate α/PED         | Long A/B with red team, tune γ/σ_thr/λ_G, validate IPG | Shared metrics (I_op/IPG) enable cross-checks          |

**Quick refs:** see `TUI/Teoria_Unificada_Inteligencia_v4.2.md` for full definitions and tables F.1/F.2.
