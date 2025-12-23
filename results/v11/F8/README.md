# F8 (v11 post-errata) — Replicación “quirúrgica” para cierre de H1 (CFR, high-stakes)

F8 existe para convertir la señal de F7 en un **veredicto confirmatorio** sobre el claim primario de arquitectura (H1: `S0-H` vs `C-H`) **sin** repetir el problema de multiplicidad (Holm) que dejó F7 en “casi sí”.

F8 **mantiene fijo** lo que ya dio headroom real:
- Condición: `F2_redteam`
- High-stakes run-level: `B*=40`
- `red_team_prob=0.03`
- Grids `{8,16}`
- Endpoint primario: **CFR** (budget exhaustion)

## Estructura (alineada al estilo F4–F7)

- Protocolo:
  - `results/v11/F8/PREREGISTRO_F8_v11.md`
  - `results/v11/F8/F8_DEVIATIONS_LOG_v11.md`
  - `results/v11/F8/F8_CLOSURE_REPORT.md`
- Runner:
  - `results/v11/F8/run_F8_v11.py`
- Raw (local-only; no versionar):
  - `results/v11/F8/raw/`
- Canónico (se crea al organizar):
  - `results/v11/F8/F2_redteam/stkH/rt*/grid{8,16}/riskhigh/{control,simbiosis}/`

## Pipeline

1) Dry-run (plan y conteos):

```powershell
python results/v11/F8/run_F8_v11.py --dry-run
```

2) Confirmatorio (base, n=40 runs por grupo):

```powershell
python results/v11/F8/run_F8_v11.py --stage confirm
```

3) Expansión (una sola; n=60 runs por grupo) **solo si aplica** según el preregistro:

```powershell
python results/v11/F8/run_F8_v11.py --stage expand
```

4) Organizar raw → canónico:

```powershell
python scripts/organize_F8_results.py
```

5) Análisis preregistrado (H1 only):

```powershell
python scripts/f8_preregistered_analysis_v11.py
```

6) Cierre formal:
- Completar `results/v11/F8/F8_CLOSURE_REPORT.md` citando los artefactos.

