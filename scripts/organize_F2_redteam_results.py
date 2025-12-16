import csv
import json
import re
from pathlib import Path

RAW_DIR = Path("results/v11/F2_redteam/raw")
BASE_DIR = RAW_DIR.parent
AGENTS = ("control", "simbiosis", "dqn_control")

def iter_raw_runs():
    """
    Itera sobre los archivos JSON crudos de F2_redteam que deben organizarse.
    Se excluyen los archivos archivados con prefijos obsoletos.
    """
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"No existe el directorio RAW: {RAW_DIR}")
    for path in RAW_DIR.glob("grid*_riskhigh*_seed*_v11.json"):
        if "archivados" in path.parts:
            continue
        yield path

def parse_grid_from_stem(stem: str) -> str:
    m = re.match(r"grid(\d+)_riskhigh", stem)
    if not m:
        raise ValueError(f"No se pudo extraer grid_size de '{stem}'")
    return m.group(1)

def load_csv_rows(csv_path: Path) -> tuple[list[dict], list[str]]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not rows:
        raise ValueError(f"CSV vacío o sin filas: {csv_path}")
    return rows, fieldnames

def write_agent_json(json_data: dict, agent: str, grid: str, base_stem: str) -> Path:
    agent_dir = BASE_DIR / f"grid{grid}" / "riskhigh" / agent
    agent_dir.mkdir(parents=True, exist_ok=True)
    if agent == "dqn_control" and "dqn_params" in json_data:
        agent_payload = dict(json_data[agent])
        agent_payload["dqn_params"] = json_data["dqn_params"]
    else:
        agent_payload = json_data[agent]
    out_path = agent_dir / f"{base_stem}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(agent_payload, f, indent=2)
    return out_path

def write_agent_csv(rows: list[dict], fieldnames: list[str], agent: str, grid: str, base_stem: str) -> Path:
    agent_dir = BASE_DIR / f"grid{grid}" / "riskhigh" / agent
    agent_dir.mkdir(parents=True, exist_ok=True)
    out_path = agent_dir / f"{base_stem}_episodes.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row.get("Agente") == agent:
                writer.writerow(row)
    return out_path

def organize_f2_results() -> None:
    """
    Organiza F2_redteam v11 en la estructura científica final:
    un archivo por (grid, agente, seed) en:
        results/v11/F2_redteam/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/
    a partir de los archivos agregados en raw/.
    """
    for json_path in iter_raw_runs():
        base_stem = json_path.stem
        grid = parse_grid_from_stem(base_stem)
        csv_path = json_path.with_name(f"{base_stem}_episodes.csv")
        if not csv_path.exists():
            raise FileNotFoundError(f"Falta el CSV de episodios para {json_path.name}: {csv_path}")
        with json_path.open("r", encoding="utf-8") as f:
            json_data = json.load(f)
        rows, fieldnames = load_csv_rows(csv_path)
        for agent in AGENTS:
            if agent not in json_data:
                print(f"[WARN] Agente '{agent}' no está presente en {json_path.name}, se omite.")
                continue
            agent_json_path = write_agent_json(json_data, agent, grid, base_stem)
            agent_csv_path = write_agent_csv(rows, fieldnames, agent, grid, base_stem)
            print(f"[OK] Generados archivos para {agent} - grid{grid}:")
            print(f"     JSON: {agent_json_path}")
            print(f"     CSV : {agent_csv_path}")

def main() -> None:
    organize_f2_results()

if __name__ == "__main__":
    main()
