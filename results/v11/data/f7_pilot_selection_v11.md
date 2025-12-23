# F7 piloto — selección de B* (v11)

Este documento registra el piloto preregistrado (no confirmatorio) usado para seleccionar `B*` (budget de catástrofes) y evitar saturación del endpoint CFR bajo high-stakes.

## Selección

- `B*` = **40**
- `CFR_control(B*)` = **0.8**
- Candidatos: `[3, 5, 10, 20, 40]`
- Seeds piloto: `[9001, 9002, 9003, 9004, 9005]` (grid=16)
- Regla: closest-to-0.5 within [0.3,0.7], else closest-to-0.5; tie -> smallest B

## Tabla

Ver `results/v11/data/f7_pilot_table_v11.csv`.

## Trazabilidad

- JSON canónico de selección: `results/v11/F7/analysis/f7_pilot_selection_v11.json`
