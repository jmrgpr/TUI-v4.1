import csv
import json
import re
from pathlib import Path

F3_DIR = Path("results/v11/F3")
RAW_BASE = F3_DIR / "raw"

AGENTS = ("control", "simbiosis", "dqn_control")


def iter_raw_runs():
    if not RAW_BASE.exists():
        raise FileNotFoundError(f"No existe el directorio RAW: {RAW_BASE}")
    for condition_dir in (RAW_BASE / "F1_highrisk", RAW_BASE / "F2_redteam"):
        if not condition_dir.exists():
            continue
        for path in condition_dir.glob("grid*_riskhigh*_v11.json"):
            yield path


def parse_stem(stem: str) -> dict:
    # grid16_riskhigh_r1p2_f2rt0p1_seed42_m0p2_v11
    m = re.match(
        r"^grid(?P<grid>\d+)_riskhigh_(?P<risk>r\d+p\d+)_(?P<cond>f1|f2rt0p1)_seed(?P<seed>\d+)_m(?P<mix_a>\d+)p(?P<mix_b>\d+)_v11$",
        stem,
    )
    if not m:
        raise ValueError(f"Nombre raw inesperado: {stem}")
    grid = int(m.group("grid"))
    seed = int(m.group("seed"))
    mix = float(f"{m.group('mix_a')}.{m.group('mix_b')}")
    condition = "F1_highrisk" if m.group("cond") == "f1" else "F2_redteam"
    risk_token = m.group("risk")
    return {"grid": grid, "seed": seed, "pgf_mix": mix, "condition": condition, "risk_token": risk_token}


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


def agent_out_dir(condition: str, grid: int, agent: str) -> Path:
    return F3_DIR / condition / f"grid{grid}" / "riskhigh" / agent


def organize_f3_results() -> None:
    """
    Organiza F3 en estructura final por condición:
    - results/v11/F3/F1_highrisk/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/
    - results/v11/F3/F2_redteam/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/

    Regla anti-duplicados:
    - Para pgf_mix=0.0: se exportan los 3 agentes.
    - Para pgf_mix>0.0: se exporta solo `simbiosis` (control/dqn_control serían duplicados).
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
            out_dir = agent_out_dir(meta["condition"], meta["grid"], agent)
            agent_json_path = write_agent_json(json_data, out_dir, agent, base_stem)
            agent_csv_path = write_agent_csv(rows, fieldnames, out_dir, agent, base_stem)
            print(f"[OK] {meta['condition']} grid{meta['grid']} seed={meta['seed']} pgf_mix={meta['pgf_mix']} agent={agent}")
            print(f"     JSON: {agent_json_path}")
            print(f"     CSV : {agent_csv_path}")


def main() -> None:
    organize_f3_results()


if __name__ == "__main__":
    main()

