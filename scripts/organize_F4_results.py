import csv
import json
import re
from pathlib import Path

F4_DIR = Path("results/v11/F4")
RAW_BASE = F4_DIR / "raw" / "F2_redteam"

AGENTS = ("control", "simbiosis", "dqn_control")


def iter_raw_runs():
    if not RAW_BASE.exists():
        raise FileNotFoundError(f"No existe el directorio RAW: {RAW_BASE}")
    for stakes_dir in RAW_BASE.iterdir():
        if not stakes_dir.is_dir():
            continue
        for path in stakes_dir.glob("grid*_riskhigh*_v11.json"):
            yield path


def parse_stem(stem: str) -> dict:
    # grid16_riskhigh_r1p2_f2rt0p1_seed42_stkH_b3_m0p2_v11
    m = re.match(
        r"^grid(?P<grid>\d+)_riskhigh_(?P<risk>r\d+p\d+)_(?P<cond>f2rt0p1)_seed(?P<seed>\d+)_(?P<stakes>stkL|stkH)_b(?P<budget>\d+)_m(?P<mix_a>\d+)p(?P<mix_b>\d+)_v11$",
        stem,
    )
    if not m:
        raise ValueError(f"Nombre raw inesperado: {stem}")
    grid = int(m.group("grid"))
    seed = int(m.group("seed"))
    budget = int(m.group("budget"))
    mix = float(f"{m.group('mix_a')}.{m.group('mix_b')}")
    stakes_token = m.group("stakes")
    risk_token = m.group("risk")
    return {
        "grid": grid,
        "seed": seed,
        "pgf_mix": mix,
        "condition": "F2_redteam",
        "risk_token": risk_token,
        "stakes_token": stakes_token,
        "budget": budget,
    }


def load_csv_rows(csv_path: Path) -> tuple[list[dict], list[str]]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not rows:
        raise ValueError(f"CSV vacío o sin filas: {csv_path}")
    return rows, fieldnames


def write_agent_json(json_data: dict, out_dir: Path, agent: str, base_stem: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if agent == "dqn_control" and "dqn_params" in json_data:
        agent_payload = dict(json_data[agent])
        agent_payload["dqn_params"] = json_data["dqn_params"]
    else:
        agent_payload = json_data[agent]
    out_path = out_dir / f"{base_stem}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(agent_payload, f, indent=2)
    return out_path


def write_agent_csv(rows: list[dict], fieldnames: list[str], out_dir: Path, agent: str, base_stem: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{base_stem}_episodes.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row.get("Agente") == agent:
                writer.writerow(row)
    return out_path


def agent_out_dir(condition: str, stakes_token: str, grid: int, agent: str) -> Path:
    return F4_DIR / condition / stakes_token / f"grid{grid}" / "riskhigh" / agent


def organize_f4_results() -> None:
    """
    Organiza F4 en estructura final por stakes:
    - results/v11/F4/F2_redteam/stkL/grid{8,16}/riskhigh/{control,simbiosis,dqn_control(optional)}/
    - results/v11/F4/F2_redteam/stkH/grid{8,16}/riskhigh/{control,simbiosis,dqn_control(optional)}/

    Regla anti-duplicados (misma idea que F3):
    - Para pgf_mix=0.0: se exportan baselines + simbiosis (si existen).
    - Para pgf_mix>0.0: se exporta solo `simbiosis` (baselines serían duplicados).
    """
    for json_path in iter_raw_runs():
        base_stem = json_path.stem
        meta = parse_stem(base_stem)
        csv_path = json_path.with_name(f"{base_stem}_episodes.csv")
        if not csv_path.exists():
            raise FileNotFoundError(f"Falta el CSV de episodios para {json_path.name}: {csv_path}")
        json_data = json.loads(json_path.read_text(encoding="utf-8"))
        rows, fieldnames = load_csv_rows(csv_path)

        agents_to_export = list(AGENTS) if meta["pgf_mix"] == 0.0 else ["simbiosis"]
        for agent in agents_to_export:
            if agent not in json_data:
                print(f"[WARN] Agente '{agent}' no está presente en {json_path.name}, se omite.")
                continue
            out_dir = agent_out_dir(meta["condition"], meta["stakes_token"], meta["grid"], agent)
            agent_json_path = write_agent_json(json_data, out_dir, agent, base_stem)
            agent_csv_path = write_agent_csv(rows, fieldnames, out_dir, agent, base_stem)
            print(
                f"[OK] {meta['condition']} {meta['stakes_token']} grid{meta['grid']} "
                f"seed={meta['seed']} budget={meta['budget']} pgf_mix={meta['pgf_mix']} agent={agent}"
            )
            print(f"     JSON: {agent_json_path}")
            print(f"     CSV : {agent_csv_path}")


def main() -> None:
    organize_f4_results()


if __name__ == "__main__":
    main()
