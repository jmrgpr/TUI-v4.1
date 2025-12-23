import csv
import json
import re
from pathlib import Path

F7_DIR = Path("results/v11/F7")
RAW_BASE = F7_DIR / "raw" / "F2_redteam" / "stkH"

AGENTS = ("control", "simbiosis")


def iter_raw_runs() -> list[Path]:
    if not RAW_BASE.exists():
        raise FileNotFoundError(f"No existe el directorio RAW confirmatorio: {RAW_BASE}")
    files = sorted([p for p in RAW_BASE.rglob("grid*_riskhigh*_v11.json") if p.is_file()])
    if not files:
        raise RuntimeError(f"No se detectaron JSON raw bajo {RAW_BASE}")
    return files


def parse_stem(stem: str) -> dict:
    # grid16_riskhigh_r1p2_f2rt0p03_seed123_stkH_b10_m0p2_v11
    m = re.match(
        r"^grid(?P<grid>\d+)_riskhigh_(?P<risk>r\d+p\d+)_f2rt(?P<p_a>\d+)p(?P<p_b>\d+)_seed(?P<seed>\d+)_(?P<stakes>stkH)_b(?P<budget>\d+)_m(?P<mix_a>\d+)p(?P<mix_b>\d+)_v11$",
        stem,
    )
    if not m:
        raise ValueError(f"Nombre raw inesperado: {stem}")
    grid = int(m.group("grid"))
    seed = int(m.group("seed"))
    budget = int(m.group("budget"))
    mix = float(f"{m.group('mix_a')}.{m.group('mix_b')}")
    red_team_prob = float(f"{m.group('p_a')}.{m.group('p_b')}")
    rt_token = f"rt{m.group('p_a')}p{m.group('p_b')}"
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
        "red_team_prob": red_team_prob,
        "rt_token": rt_token,
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


def agent_out_dir(*, condition: str, stakes_token: str, rt_token: str, grid: int, agent: str) -> Path:
    return F7_DIR / condition / stakes_token / rt_token / f"grid{grid}" / "riskhigh" / agent


def organize_f7_results() -> None:
    """
    Organiza F7 (confirmatorio) en estructura final:
    - results/v11/F7/F2_redteam/stkH/rt*/grid{8,16}/riskhigh/{control,simbiosis}/

    Regla anti-duplicados (igual que F4/F5/F6):
    - Para pgf_mix=0.0: se exportan baselines + simbiosis.
    - Para pgf_mix>0.0: se exporta solo `simbiosis` (baselines serían duplicados).

    Nota: el piloto vive en `results/v11/F7/raw/PILOT/` y no se organiza a canónico;
    su salida es la selección de B* (`results/v11/F7/analysis/f7_pilot_selection_v11.json`).
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
            out_dir = agent_out_dir(
                condition=meta["condition"],
                stakes_token=meta["stakes_token"],
                rt_token=meta["rt_token"],
                grid=meta["grid"],
                agent=agent,
            )
            agent_json_path = write_agent_json(json_data, out_dir, agent, base_stem)
            agent_csv_path = write_agent_csv(rows, fieldnames, out_dir, agent, base_stem)
            print(
                f"[OK] {meta['condition']} {meta['stakes_token']} {meta['rt_token']} grid{meta['grid']} "
                f"seed={meta['seed']} budget={meta['budget']} pgf_mix={meta['pgf_mix']} agent={agent}"
            )
            print(f"     JSON: {agent_json_path}")
            print(f"     CSV : {agent_csv_path}")


def main() -> None:
    organize_f7_results()


if __name__ == "__main__":
    main()

