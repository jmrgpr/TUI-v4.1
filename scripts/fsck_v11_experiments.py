import csv
import json
from pathlib import Path
from typing import Iterable


AGENTS = ("control", "simbiosis", "dqn_control")
ROOT = Path("results/v11")


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _count_agent_rows(csv_path: Path, agent: str) -> int:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return sum(1 for row in reader if row.get("Agente") == agent)


def _check_raw_run(
    exp_dir: Path,
    base_stem: str,
    risk_label: str,
    gridsize: int,
    episodes_expected: int,
    seeds_label: str,
) -> list[str]:
    issues: list[str] = []
    raw_dir = exp_dir / "raw"
    json_path = raw_dir / f"{base_stem}.json"
    csv_path = raw_dir / f"{base_stem}_episodes.csv"

    if not json_path.exists():
        issues.append(f"[RAW-MISSING] Falta JSON: {json_path}")
        return issues
    if not csv_path.exists():
        issues.append(f"[RAW-MISSING] Falta CSV: {csv_path}")
        return issues

    data = _load_json(json_path)

    for agent in AGENTS:
        if agent not in data:
            issues.append(f"[AGENT-MISSING] '{agent}' no está en {json_path.name}")
            continue

        res = data[agent]
        rewards = res.get("total_rewards", [])
        if len(rewards) != episodes_expected:
            issues.append(
                f"[EPISODES-MISMATCH] {json_path.name} agente={agent}: "
                f"{len(rewards)} episodios, esperado={episodes_expected}"
            )

        n_rows = _count_agent_rows(csv_path, agent)
        if n_rows != episodes_expected:
            issues.append(
                f"[CSV-MISMATCH] {csv_path.name} agente={agent}: "
                f"{n_rows} filas, esperado={episodes_expected}"
            )

        cfg = res.get("config", {})
        if cfg.get("grid_size") != gridsize:
            issues.append(
                f"[GRID-MISMATCH] {json_path.name} agente={agent}: "
                f"grid_size={cfg.get('grid_size')} pero esperado={gridsize}"
            )
        if cfg.get("risk_level") != risk_label.replace("risk", "").replace("high", "high").replace("low", "low"):
            # risk_level debe ser "high" o "low" según el label
            expected_level = "high" if "high" in risk_label else "low"
            issues.append(
                f"[RISK-MISMATCH] {json_path.name} agente={agent}: "
                f"risk_level={cfg.get('risk_level')} pero esperado={expected_level}"
            )

    return issues


def _check_split_outputs(
    exp_dir: Path,
    base_stem: str,
    risk_label: str,
    gridsize: int,
    episodes_expected: int,
) -> list[str]:
    """
    Verifica que existan los archivos por agente en:
      exp_dir/grid{gridsize}/risk{high,low}/{agent}/...
    Esta comprobación solo se aplica a F1_highrisk, que ya está organizado.
    """
    issues: list[str] = []
    for agent in AGENTS:
        agent_dir = exp_dir / f"grid{gridsize}" / risk_label / agent
        json_path = agent_dir / f"{base_stem}.json"
        csv_path = agent_dir / f"{base_stem}_episodes.csv"
        if not json_path.exists():
            issues.append(f"[SPLIT-MISSING] Falta JSON por agente: {json_path}")
        if not csv_path.exists():
            issues.append(f"[SPLIT-MISSING] Falta CSV por agente: {csv_path}")
        else:
            n_rows = _count_agent_rows(csv_path, agent)
            if n_rows != episodes_expected:
                issues.append(
                    f"[SPLIT-CSV-MISMATCH] {csv_path} agente={agent}: "
                    f"{n_rows} filas, esperado={episodes_expected}"
                )
    return issues


def check_experiment(
    name: str,
    risk_label: str,
    expect_split_outputs: bool,
) -> list[str]:
    exp_dir = ROOT / name
    meta_path = exp_dir / "metadata.json"
    if not meta_path.exists():
        return [f"[META-MISSING] Falta metadata.json en {exp_dir}"]

    meta = _load_json(meta_path)
    cfg = meta.get("config_global", {})

    issues: list[str] = []

    episodes_expected = cfg.get("episodes")
    if not isinstance(episodes_expected, int):
        issues.append(f"[META-EPISODES] 'episodes' inválido en metadata de {name}: {episodes_expected}")
        episodes_expected = 0

    grids = cfg.get("grid_sizes") or meta.get("grids")
    if not isinstance(grids, Iterable):
        issues.append(f"[META-GRIDS] 'grid_sizes' inválido en metadata de {name}: {grids}")
        grids = []

    seeds = meta.get("seeds") or [cfg.get("seed")]
    if not isinstance(seeds, Iterable):
        issues.append(f"[META-SEEDS] 'seeds' inválido en metadata de {name}: {seeds}")
        seeds = []

    agents_declared = cfg.get("agents", [])
    for agent in AGENTS:
        if agent not in agents_declared:
            issues.append(f"[META-AGENT] '{agent}' no está listado en config_global.agents de {name}")

    for grid in grids:
        try:
            g = int(grid)
        except Exception:
            issues.append(f"[GRID-INVALID] Grid no entero en {name}: {grid}")
            continue

        for seed in seeds:
            try:
                s_val = int(seed)
            except Exception:
                issues.append(f"[SEED-INVALID] Seed no entero en {name}: {seed}")
                continue

            if name == "F1_highrisk":
                base_stem = f"grid{g}_riskhigh_r1p2_seed{s_val}_v11"
            elif name == "F0_baseline":
                base_stem = f"grid{g}_risklow_seed{s_val}_v11"
            else:
                base_stem = f"grid{g}_{risk_label}_seed{s_val}_v11"

            issues.extend(
                _check_raw_run(
                    exp_dir,
                    base_stem=base_stem,
                    risk_label=risk_label,
                    gridsize=g,
                    episodes_expected=episodes_expected,
                    seeds_label=str(seed),
                )
            )

            if expect_split_outputs:
                issues.extend(
                    _check_split_outputs(
                        exp_dir,
                        base_stem=base_stem,
                        risk_label=risk_label,
                        gridsize=g,
                        episodes_expected=episodes_expected,
                    )
                )
    return issues


def main() -> None:
    all_issues: list[str] = []

    # F0_baseline: riesgo bajo, solo comprobamos RAW (no hay splits por agente aún).
    all_issues.extend(check_experiment("F0_baseline", risk_label="risklow", expect_split_outputs=False))

    # F1_highrisk: riesgo alto, comprobamos RAW + splits por agente.
    all_issues.extend(check_experiment("F1_highrisk", risk_label="riskhigh", expect_split_outputs=True))

    if all_issues:
        print("=== FSCK v11 EXPERIMENTS: PROBLEMAS DETECTADOS ===")
        for issue in all_issues:
            print(issue)
    else:
        print("=== FSCK v11 EXPERIMENTS: TODO OK ===")


if __name__ == "__main__":
    main()

