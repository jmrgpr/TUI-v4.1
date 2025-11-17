# ROADMAP_v10_COMPLETO.md

## Roadmap y checklist de cierre – Protocolo TUI v10

Este documento resume el avance, estado y enlaces de cada fase del protocolo v10, marcando el cierre científico y reproducible antes de abrir v11.

### Fases principales

- [x] **F0 – v10_viable**
  - Curriculum completo 4×4→6×6→8×8
  - Gates superados: 93% (4×4), 68% (6×6), 87% (8×8)
  - Reporte: REPORTE_FINAL_v10_viable.md

- [x] **F1 – Ablation núcleo v10 (A/B/C/D)**
  - Comparación de curriculum, directo, inverso y solo 6×6
  - Reporte: REPORTE_ABLATION_v10.md

- [x] **F2 – Ablation de componentes v10**
  - Variantes: baseline, shaping, reward_extra, regularización, curriculum local
  - Reporte: REPORTE_ABLATION_COMPONENTES_v10.md

- [x] **F3 – PGF Offline**
  - Enriquecimiento y análisis de episodios con PGF/I_op
  - Reporte: REPORTE_PGF_OFFLINE_v10.md

- [x] **F4 – Escalabilidad v10 (16×16)**
  - 2 configs (sin/con regularización), 2 seeds, 3000 episodios
  - Reporte: REPORTE_FASE4_SCALABILITY_v10.md

- [ ] **F5 – Documentación y reproducibilidad global**
  - README_MASTER_v10.md enlazando todos los artefactos
  - Logs y preregistros completos

- [ ] **F6 – Síntesis y puente hacia v11**
  - REPORTE_SINTESIS_v10_a_v11.md
  - PREREGISTRO_v11_alpha.md

### Estado actual

- Todas las fases F0–F4 están cerradas, reproducibles y auditadas.
- F5 y F6 en proceso de consolidación y síntesis.

---
*Documento generado automáticamente el 8/12/2025 por GitHub Copilot.*
