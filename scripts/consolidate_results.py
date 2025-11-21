import glob
import re
from pathlib import Path
from typing import Optional

import pandas as pd

# Rutas base (agregar aquí cualquier nueva carpeta de resultados)
BASE_PATHS = [
    "results/sweep/fase2",
    "results/sota",
    "artifacts/phase2",
    "reports/phase2",
]

# Columnas target del master
MASTER_COLS = [
    "agent",
    "seed",
    "episodes",
    "risk_scale",
    "kappa",
    "lambda",
    "mix",
    "pgf_neto",
    "tripwires",
    "robustez",
    "flexibilidad",
    "reward_total",
    "filename",
]


def first_matching_column(df: pd.DataFrame, patterns) -> Optional[str]:
    """Devuelve el primer nombre de columna que contenga alguno de los patrones (case-insensitive)."""
    pats = [p.lower() for p in patterns]
    for col in df.columns:
        col_l = col.lower()
        if any(p in col_l for p in pats):
            return col
    return None


def extract_metadata(path: Path) -> dict:
    """Extrae metadatos básicos (agent, seed, risk_scale) de la ruta/archivo."""
    parts = [p.lower() for p in path.parts]
    meta = {
        "agent": None,
        "seed": None,
        "risk_scale": None,
        "episodes": None,
        "kappa": None,
        "lambda": None,
        "mix": None,
        "filename": path.name,
    }

    # Agent/seed para sweep
    if "sweep" in parts:
        # seed por carpeta o nombre
        seed_match = re.search(r"seed([0-9]+)", path.as_posix(), re.IGNORECASE)
        if seed_match:
            meta["seed"] = seed_match.group(1)
        # agente por sufijo en nombre
        fname_l = path.name.lower()
        if "simbiosis" in fname_l:
            meta["agent"] = "simbiosis"
        elif "dqn_control" in fname_l:
            meta["agent"] = "dqn_control"
        elif "control" in fname_l:
            meta["agent"] = "control"
        else:
            meta["agent"] = "tui"

    # Agent para SOTA u otras carpetas con nombre de algoritmo
    algo_keys = {"ppo", "a2c", "dqn", "sac", "td3"}
    for i, p in enumerate(parts):
        if p in algo_keys:
            meta["agent"] = p
            break
    if meta["agent"] is None and "sota" in parts:
        try:
            idx = parts.index("sota")
            meta["agent"] = parts[idx + 1]  # ppo, a2c, dqn, sac...
        except Exception:
            meta["agent"] = "sota"

    # risk_scale
    risk_match = re.search(r"risk([0-9.]+)", path.name)
    if risk_match:
        try:
            meta["risk_scale"] = float(risk_match.group(1))
        except ValueError:
            meta["risk_scale"] = None

    # episodes / kappa / lambda / mix desde el nombre
    ep_match = re.search(r"episodes?([0-9]+)", path.name, flags=re.IGNORECASE)
    if ep_match:
        meta["episodes"] = int(ep_match.group(1))
    kappa_match = re.search(r"kappa([0-9.]+)", path.name, flags=re.IGNORECASE)
    if kappa_match:
        try:
            meta["kappa"] = float(kappa_match.group(1))
        except ValueError:
            pass
    lambda_match = re.search(r"lambda([0-9.]+)", path.name, flags=re.IGNORECASE)
    if lambda_match:
        try:
            meta["lambda"] = float(lambda_match.group(1))
        except ValueError:
            pass
    mix_match = re.search(r"mix([0-9.]+)", path.name, flags=re.IGNORECASE)
    if mix_match:
        try:
            meta["mix"] = float(mix_match.group(1))
        except ValueError:
            pass

    return meta


def consolidate_csvs():
    all_files = []
    for base in BASE_PATHS:
        all_files.extend(glob.glob(f"{base}/**/*.csv", recursive=True))

    dfs = []
    for idx, fname in enumerate(all_files, start=1):
        path = Path(fname)
        meta = extract_metadata(path)
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except Exception:
            continue

        # Mapear columnas si existen
        trip_col = first_matching_column(df, ["tripwires", "tripwire"])
        reward_col = first_matching_column(df, ["recompensa", "reward"])
        robustez_col = first_matching_column(df, ["robustez", "robustness"])
        flex_col = first_matching_column(df, ["flexibilidad", "flexibility"])
        pgf_neto_col = first_matching_column(df, ["pgf_neto", "pgf neto", "pgf"])

        # Añadir/normalizar columnas
        df["agent"] = meta.get("agent")
        df["seed"] = meta.get("seed")
        df["risk_scale"] = meta.get("risk_scale")
        df["episodes"] = meta.get("episodes")
        df["kappa"] = meta.get("kappa")
        df["lambda"] = meta.get("lambda")
        df["mix"] = meta.get("mix")
        df["filename"] = meta.get("filename")
        df["tripwires"] = df[trip_col] if trip_col else None
        df["reward_total"] = df[reward_col] if reward_col else None
        df["robustez"] = df[robustez_col] if robustez_col else None
        df["flexibilidad"] = df[flex_col] if flex_col else None
        df["pgf_neto"] = df[pgf_neto_col] if pgf_neto_col else None

        for col in MASTER_COLS:
            if col not in df.columns:
                df[col] = None

        dfs.append(df[MASTER_COLS])

        if idx % 50 == 0:
            print(f"Procesados {idx} archivos...")

    if dfs:
        master = pd.concat(dfs, ignore_index=True)
        out_path = Path("results/master_results.csv")
        master.to_csv(out_path, index=False)
        print(f"Master CSV generado: {out_path}")
    else:
        print("No se encontraron archivos CSV válidos.")


if __name__ == "__main__":
    consolidate_csvs()
