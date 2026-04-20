# AGENTS Operating Guide (TUI-v4.1)

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
