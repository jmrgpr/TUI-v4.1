# F6 piloto — selección de p* (v11)

Este documento registra el piloto preregistrado de calibración (no confirmatorio) usado para seleccionar `p*` (valor de `red_team_prob`) y evitar saturación del endpoint CFR bajo high-stakes `B=3`.

- Candidatos: `[0.03, 0.05, 0.07]`
- Seeds piloto (no reutilizados): `[9001, 9002, 9003, 9004, 9005]`
- Grid piloto: `16`
- Regla: closest-to-0.5 within [0.3,0.7], else closest-to-0.5; tie -> smallest p

## Selección

- `p*` = **0.03**
- `CFR_control(p*)` = **1.0**
- JSON canónico de selección: `results/v11/F6/analysis/f6_pilot_selection_v11.json`

## Tabla

Ver `results/v11/data/f6_pilot_table_v11.csv`.
