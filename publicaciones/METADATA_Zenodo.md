# Metadata for Zenodo Publication

## Title

**English (Main)**:  
Prudential Gating Function v3: Multi-Seed Validation of a Risk-Aware Reward Shaping Mechanism for Reinforcement Learning

**Short Title**:  
PGF v3: Risk-Aware Reward Shaping Multi-Seed Validation

---

## Author

**Full name**: Jose M Rivera Garcia  
**Affiliation**: Independent Researcher  
**ORCID**: 0009-0000-3013-725X  
**Email**: jmrgpr@gmail.com  
**Country**: Puerto Rico / United States

---

## Abstract (max 250 words)

We present a multi-seed validation of the Prudential Gating Function (PGF) v3, a reward shaping mechanism designed to induce risk-aware behavior in reinforcement learning agents operating in stochastic environments. Across three independent random seeds in a 5×5 gridworld with moderate risk conditions (risk_scale=1.5), PGF v3 achieves a mean performance ratio of 38.93% ± 0.59% relative to a risk-blind control agent, with exceptional statistical reproducibility (coefficient of variation = 1.52%). This represents a cumulative +131.7% improvement over our initial baseline implementation.

While the ~39% ratio may appear suboptimal in absolute terms, we argue this quantifies the **alignment tax**—the inherent performance cost of imposing safety constraints and risk-awareness in environments where optimal reward-maximization strategies involve high variance. The control agent achieves higher mean rewards but with 192% coefficient of variation, while the PGF agent maintains 71% CV, demonstrating the stability-performance tradeoff. In simplified settings (3×3 grid), PGF enables agents to exceed control performance (105%), validating the mechanism's functional correctness.

Statistical analysis confirms significant improvement over the previous iteration. However, we document that ~70% of the PGF signal derives from engineered heuristic bonuses rather than purely theoretical risk-reduction signals, indicating complexity-imposed limitations. This work contributes empirical data to the AI safety discourse on quantifying safety-performance tradeoffs and provides a reproducible framework for risk-aware RL research. All code, data, and analysis scripts are publicly available.

**Keywords**: reinforcement learning, reward shaping, risk-aware agents, alignment tax, statistical validation, multi-seed reproducibility, safe reinforcement learning, prudential behavior

---

## BibTeX Reference

@misc{rivera2025tui,
  title={Unified Intelligence Theory v4.1: A Risk-Driven Framework},
  author={Rivera Garcia, Jose M},
  year={2025},
  doi={10.5281/zenodo.17702378},
  url={https://github.com/jmrgpr/TUI-v4.1},
  note={Version 4.1}
}

---

## Note on AI Assistance

During the preparation of this work, AI-based tools (such as code completion, translation, and formatting assistants) were used strictly as technical support. All scientific decisions, analysis, and conclusions are the sole responsibility of the author. The use of AI tools did not influence the scientific integrity or originality of the research, in accordance with best practices for responsible research conduct.
