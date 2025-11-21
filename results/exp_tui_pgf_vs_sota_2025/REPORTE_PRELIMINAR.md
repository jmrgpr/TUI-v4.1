# El costo de la prudencia (resumen preliminar alineado con datos fase 2)

Autor: José M. Rivera García (investigador independiente)  
Proyecto: TUI v4.x / PGF  
Fase: 2  
Estado: Resultados preliminares + pipeline reproducible  
Fecha: 2025-11-21  

---

## Resumen ejecutivo
Este corte usa el CSV maestro generado (`results/exp_tui_pgf_vs_sota_2025/master_results.csv`, 22 595 filas). Incluye cuatro agentes con `risk_scale` etiquetado: `control`, `dqn_control`, `simbiosis`, `ppo`. El agente `tui` está presente pero **sin `risk_scale` (NaN)**, por lo que no aparece en los gráficos por riesgo y sus números no son comparables aún.

Hallazgo central con los datos actuales:
- **PPO** reduce los accidentes a cero cuando el riesgo sube (risk_scale ≥ 1), pero su recompensa media cae cerca de cero y muestra un outlier extremo en riesgo 0.5 (reward ≈ 371). Señal de política inactiva/“quieta” que evita trampas.
- **DQN_Control** y **Simbiosis** mantienen accidentes entre 0.07–0.09 por paso en todos los riesgos y su recompensa cae al subir el riesgo (DQN pasa de ≈9.5 a ≈−0.27).
- **Control** mantiene accidentes muy bajos (~0.03) pero con recompensas negativas en todo el rango.
- No hay evidencia en este dataset de un agente TUI prudente bajo riesgos etiquetados; falta instrumentar `risk_scale` y variantes tuned/default para TUI.

---

## Resultados principales (por riesgo)

- **Accidentes (tripwires medios)**  
  - control: ~0.03 constantes en todo riesgo.  
  - dqn_control: 0.069 → 0.084 → 0.068.  
  - simbiosis: 0.081 → 0.089 → 0.087 (ligero aumento).  
  - ppo: 0.39 en riesgo 0.5; **0.0** en riesgos 1.0–3.0 (probable inacción).

- **PGF_neto medio**  
  - control: ~−0.11 estable, leve caída a −0.119 en riesgo 2.0.  
  - dqn_control: de −0.117 a −0.133 al subir riesgo.  
  - simbiosis: de −0.128 a −0.146 al subir riesgo.  
  - ppo: outlier −0.294 en riesgo 0.5; luego mejora a ~−0.04 en riesgos altos.

- **Recompensa total media**  
  - control: siempre negativa (−4.2 a −6.0).  
  - dqn_control: positiva en riesgo bajo (+9.5) y cae a negativo (−0.27) en riesgo 3.0.  
  - simbiosis: negativa en todo el rango (≈−18 a −21).  
  - ppo: outlier +371 en riesgo 0.5; cerca de −3/−4 en riesgos altos con 0 accidentes.

---

## Interpretación breve
- **Prudencia vs. utilidad**: el único comportamiento claramente “prudente” es PPO en riesgos altos (cero accidentes), pero viene acompañado de recompensa casi nula e indica inacción. No es prudencia adaptativa deseada, sino un exploit de “no moverse”.
- **Agentes activos**: dqn_control y simbiosis mantienen actividad (recompensa proporcional a riesgo) pero aceptan accidentes (~0.07–0.09) y pierden utilidad al subir el riesgo.
- **Control** sirve de baseline con accidentes bajos pero recompensas negativas; su política no escala utilidad.
- **Ausencia de TUI**: sin `risk_scale` para `tui`, no podemos afirmar ni refutar “costo de prudencia” del agente PGF. Es necesario re-etiquetar o re-ejecutar para verlo en las curvas.

---

## Recomendaciones para la siguiente corrida
1. **Instrumentar TUI**: asegurar que `risk_scale` se registre en las ejecuciones de `tui` y que se etiqueten variantes (p. ej. `tui_default`, `tui_tuned`), así entran a las tablas y gráficos.
2. **Repetir PPO con normalización consistente** para eliminar el outlier de reward 0.5 o documentarlo como apéndice (no removerlo del CSV).
3. **Incluir episodios prolongados** (ej. 500) con las mismas etiquetas para ver convergencia de tripwires y PGF_neto.
4. **Publicar visuales**: ya están en `results/exp_tui_pgf_vs_sota_2025/plots/` (heatmaps, violines, frontera PGF-tripwires, correlación). Añadir la versión con zoom de reward si se mantiene PPO@0.5.

---

## Limitaciones actuales
- `tui` sin `risk_scale` → no soporta la narrativa de prudencia adaptativa.  
- `ppo` solo tiene 5 puntos (uno por riesgo) y un outlier masivo en reward.  
- No hay separación explícita de “default” vs “tuned” en los nombres de agentes.

---

## Cómo citar este corte
- CSV maestro: `results/exp_tui_pgf_vs_sota_2025/master_results.csv`  
- Gráficos: carpeta `plots/` en el mismo experimento.  
- Log: `results/exp_tui_pgf_vs_sota_2025/experiment_log.txt`

--- 

## Próximo paso para un post público
- Recolectar los runs con TUI etiquetado por riesgo y rerenderizar las figuras.  
- Preparar dos versiones de la gráfica de reward: con y sin el outlier de PPO@0.5 anotado.  
- Actualizar el hilo público en cuanto esos datos estén disponibles para que la narrativa coincida con la evidencia.

