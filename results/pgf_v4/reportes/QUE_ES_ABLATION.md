# ¿Qué es Ablation Study? (Estudio de Ablación)

## Concepto Simple

Un **estudio de ablación** es como desarmar un motor pieza por pieza para ver qué parte hace qué.

En tu caso: Tu mecanismo PGF tiene 3 componentes principales:
1. **Bono de supervivencia** (no morir)
2. **Bono de progreso** (acercarte al objetivo)
3. **Señal teórica pura** (el δP matemático de tu teoría)

**Pregunta:** ¿Cuál de estos 3 componentes es el que realmente sostiene el 39% de rendimiento?

---

## Por Qué Es Importante

En tu informe v3 admitiste honestamente:
> "~70% de la señal PGF viene de bonos heurísticos (ingeniería), solo 30% de teoría pura"

**Problema:** Si quitas los bonos, ¿el agente sigue funcionando? ¿O colapsa?

**Si colapsa:** Significa que tu teoría (δP) todavía no es suficiente por sí sola.  
**Si no colapsa:** Significa que los bonos son redundantes y podrías simplificar.

---

## Cómo Funciona en Práctica

### Experimento 2: Ablation Studies

**Baseline (ya lo tienes):**  
PGF completo = Bono Supervivencia + Bono Progreso + Señal Teórica  
Resultado: 38.93%

**Ablación A: Sin Bono de Supervivencia**  
PGF = ~~Bono Supervivencia~~ + Bono Progreso + Señal Teórica  
Predicción: Si el agente muere constantemente, ratio caerá a <20%

**Ablación B: Sin Bono de Progreso**  
PGF = Bono Supervivencia + ~~Bono Progreso~~ + Señal Teórica  
Predicción: Si el agente no sabe avanzar, ratio caerá pero no tanto

**Ablación C: Solo Señal Teórica Pura**  
PGF = ~~Bono Supervivencia~~ + ~~Bono Progreso~~ + Señal Teórica  
Predicción: Ratio caerá drásticamente (posiblemente <10%) si la teoría es insuficiente

---

## Ejemplo del Mundo Real

**Medicina:** Si un medicamento tiene 3 ingredientes, ¿cuál de los 3 es el que realmente cura?
- Prueba A: Quitar ingrediente 1 → Paciente sigue curándose
- Prueba B: Quitar ingrediente 2 → Paciente empeora un poco
- Prueba C: Quitar ingrediente 3 → Paciente no se cura

**Conclusión:** El ingrediente 3 es el componente activo crítico.

---

## En Tu Caso

Si después de los ablation studies descubres que:
- Sin supervivencia → agente colapsa
- Sin progreso → agente sobrevive pero no avanza
- Solo teoría → agente es inútil

**Entonces sabrás:**
1. Los bonos son **necesarios** (no redundantes)
2. La teoría pura (δP) todavía necesita trabajo
3. La "ingeniería" está compensando limitaciones teóricas

---

## Objetivo Científico

**No es malo** que los bonos sean necesarios. Lo importante es saberlo con certeza y documentarlo honestamente.

Si publicas diciendo "mi teoría funciona" pero resulta que el 90% es ingeniería ad-hoc, los revisores te destruirán.

Pero si dices "mi teoría necesita bonos heurísticos para funcionar en entornos complejos, aquí está el desglose", eso es ciencia rigurosa y respetable.

---

## ¿Listo para empezar?

Voy a preparar 3 experimentos (A, B, C) desactivando cada componente. Cada uno con 3 semillas para mantener rigor estadístico.

Total: 9 corridas (3 ablaciones × 3 semillas).

Tiempo estimado: ~2-3 horas de cómputo.

¿Procedemos? 🔬
