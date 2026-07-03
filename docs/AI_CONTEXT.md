# AI Context - TUI-v4.1

## Purpose

TUI-v4.1 is a scientific/reproducibility repository for the Tension of Risk theory, experiments, simulations, reports, publication materials, and validation workflow. Treat results and claims as governed scientific artifacts.

## Read Order

1. `AGENTS.md`
2. This file
3. `docs/GOVERNANCE_MAIN.md`
4. `docs/PROTOCOL_COMMIT.md`
5. `docs/PHASE_CLOSE_CHECKLIST.md`
6. `docs/ARTIFACT_POLICY.md`
7. `results/INDEX.md` when result status matters

## Main Code Paths

- `TUI/` - primary implementation package.
- `sim/` - simulation code and experiment runners.
- `scripts/` - operational scripts.
- `test/` - tests.
- `notebooks/` - exploratory notebooks; avoid executing or reading outputs unless needed.
- `planificacion/`, `publicaciones/`, `docs/` - planning, publication, and governance docs.

## Tests

- Use focused `pytest` commands around touched files.
- `conftest.py`, `environment.yml`, and `requirements.txt` are important setup/configuration files and remain visible.

## Canonical Docs

- `README.md`
- `README_MASTER_v10.md`
- `docs/GOVERNANCE_MAIN.md`
- `docs/PROTOCOL_COMMIT.md`
- `docs/PHASE_CLOSE_CHECKLIST.md`
- `docs/ARTIFACT_POLICY.md`
- `results/INDEX.md`

## Sensitive / Heavy Paths

Excluded by `.ignore` for agent search:

- `data/`, generated `results/`, generated `reports/`, `plots/`, `htmlcov/`, `.venv/`, caches.
- Local inventory/output files such as `local_files.txt`, `diff_files.txt`, `*_integridad.txt`, `experiment_log.txt`, `None.json`, `None_episodes.csv`.
- Binary documents/images and model/store formats.

`results/INDEX.md` remains visible intentionally as the cheap canonical result map.

## Invariants

- Do not delete historical scientific evidence.
- Preserve reproducibility: code -> data -> command -> result -> report.
- Do not claim validation, phase closure, or publication readiness without the required evidence and governance docs.
- Jose Manuel is final authority for strategic direction and publication decisions.

## Recommended Agent Flow

1. Read `AGENTS.md` and this map.
2. Locate relevant code/docs with `rg --files`.
3. Inspect canonical indices before opening generated outputs.
4. Patch narrowly and keep generated artifacts out of broad context.
5. Run focused tests/validation and summarize residual risk.
