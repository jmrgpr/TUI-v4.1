# F7 (v11 post-errata) — Budget calibration para des‑saturar CFR

F7 existe para recuperar “headroom” del endpoint primario **CFR** calibrando el budget `B` (high‑stakes run‑level), manteniendo fija la severidad adversarial.

## Estructura (alineada al estilo F4–F6)

- Protocolo:
  - `results/v11/F7/PREREGISTRO_F7_v11.md`
  - `results/v11/F7/F7_DEVIATIONS_LOG_v11.md`
  - `results/v11/F7/F7_CLOSURE_REPORT.md`
- Runner:
  - `results/v11/F7/run_F7_v11.py`
- Raw (local-only; no versionar):
  - `results/v11/F7/raw/`
- Canónico (se crea al organizar):
  - `results/v11/F7/F2_redteam/stkH/rt*/grid{8,16}/riskhigh/{control,simbiosis}/`

## Pipeline

1) Dry-run (plan):

```powershell
python results/v11/F7/run_F7_v11.py --dry-run
```

2) Piloto (correr runs):

```powershell
python results/v11/F7/run_F7_v11.py --stage pilot
python results/v11/F7/run_F7_v11.py --stage select
```

3) Confirmatorio (usa `B*` seleccionado):

```powershell
python results/v11/F7/run_F7_v11.py --stage confirm
```

4) Organizar raw → canónico:

```powershell
python scripts/organize_F7_results.py
```

5) Análisis preregistrado:

```powershell
python scripts/f7_preregistered_analysis_v11.py
```

6) Cierre formal:
- Completar `results/v11/F7/F7_CLOSURE_REPORT.md` citando los artefactos.

