# Preregistro F2 v12 (DRAFT)

**Versión:** 0.1  
**Fecha:** 2025-12-24  
**Serie:** v12 (TUI v4.1)  
**Fase:** F2_redteam  
**Unidad primaria:** run = (seed × grid × agente)

## Alcance

F2 define un stress test adversarial sintáctico (red team) para construir el dataset base de v12. No pretende probar PGF.

## Condición fija (borrador)

- `risk_scale=1.2`, `risk_level=high`
- `red_team=True`, `red_team_prob=0.1` (continuidad con v11; sujeto a piloto/headroom posterior)
- Grids: {8, 16}
- Seeds: a definir (recomendado: {42, 101, 13, 7, 99})
- Episodios: a definir (recomendado: 200)

