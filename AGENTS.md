# AGENTS Operating Guide (TUI-v4.1)

## Context hygiene for agents

- Read this file first, then `docs/AI_CONTEXT.md`, then the required governance references below as needed.
- Use `rg`, `rg --files`, or targeted globbing before opening full files.
- Do not read `data/`, generated `results/`, generated report payloads, `plots/`, `htmlcov/`, `.venv/`, caches, run logs, binary documents, generated PDFs/images, or generated experiment artifacts unless the user explicitly asks for that evidence.
- Keep `TUI/`, `test/`, `docs/`, `scripts/`, `notebooks/`, `planificacion/`, `publicaciones/`, `results/INDEX.md`, `README.md`, `environment.yml`, `requirements.txt`, and governance docs visible.
- Ignored paths are not permission to delete, rewrite, or modify files; they only reduce broad search/context.
- Work plan-first for non-trivial changes and prefer small, auditable patches.
- Do not change scientific strategy, publication direction, canon, phase closure, or architecture without explicit approval.
- Run focused validation first; do not regenerate broad outputs unless requested.
This repository uses a centralized workflow in `main`.

## Authority and decision flow

- Project architect and final decision maker: Jose Manuel.
- Agents execute implementation and propose options.
- Strategic direction and publication decisions are approved by Jose Manuel.

## Non-negotiable operating rules

1. Work directly on `main` unless explicitly instructed otherwise.
2. Do not delete historical scientific evidence.
3. Preserve reproducibility: code -> data -> report traceability.
4. Keep repository sustainable: avoid committing non-canonical heavy artifacts.
5. Follow commit protocol and phase closure checklist in `docs/`.

## Required references before major changes

- `docs/GOVERNANCE_MAIN.md`
- `docs/PROTOCOL_COMMIT.md`
- `docs/PHASE_CLOSE_CHECKLIST.md`
- `docs/ARTIFACT_POLICY.md`
- `results/INDEX.md`

## Expected execution behavior

- Prefer small, auditable changes with explicit rationale.
- Keep canonical outputs clearly separated from temporary/debug outputs.
- When uncertain, propose options but default to conservative, traceable actions.
