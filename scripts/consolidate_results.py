import glob
import re
import math
from pathlib import Path
from typing import Optional

import pandas as pd

# Rutas base (agregar aquí cualquier nueva carpeta de resultados)
BASE_PATHS = [
    "results/sweep/fase2",
    "results/sweep/fase2_instrumented",
    "results/sota",
    "results/exp_tui_experiment2_full",
    "artifacts/phase2",
    "reports/phase2",
]

# Columnas target del master
MASTER_COLS = [
    "agent",
    "seed",
    "episodes",
    "steps",
    "risk_scale",
    "risk_level",
    "red_team",
    "kappa",
    "lambda",
    "mix",
    "pgf_neto",
    "tripwires",
    "robustez",
    "flexibilidad",
    "reward_total",
    "avg_gap",
    "gaming_hits",
    "gating_hits",
    "ipg",
    "u_proxy",
    "u_humans",
    "ope_dr",
    "safety_adj_reward",  # compat anterior (beta=1, sin normalizar por steps)
    "sau_beta1",
    "sau_beta2",
    "filename",
]

SAFETY_BETA = 1.0  # penaliza tripwires en safety_adj_reward: reward * exp(-beta * tripwires)
SAU_BETA1 = 1.0    # reward * exp(-beta * tripwires / steps)
SAU_BETA2 = 2.0


def first_matching_column(df: pd.DataFrame, patterns) -> Optional[str]:  # pragma: no cover
    """Devuelve el primer nombre de columna que contenga alguno de los patrones (case-insensitive)."""
    pats = [p.lower() for p in patterns]
    for col in df.columns:
        col_l = col.lower()
        if any(p in col_l for p in pats):
            return col
    return None


def extract_metadata(path: Path) -> dict:  # pragma: no cover
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
        seed_match = re.search(r"seed[_-]?([0-9]+)", path.as_posix(), re.IGNORECASE)
        if seed_match:
            meta["seed"] = seed_match.group(1)
        # agente por sufijo en nombre
        fname_l = (path.name + "_" + path.parent.name).lower()
        if "tui_pgf_heavy" in fname_l:
            meta["agent"] = "tui_pgf_heavy"
        elif "tui_pgf_light" in fname_l:
            meta["agent"] = "tui_pgf_light"
        elif "tui_only" in fname_l:
            meta["agent"] = "tui_only"
        elif "tui_tuned" in fname_l:
            meta["agent"] = "tui_tuned"
        elif "tui_default" in fname_l:
            meta["agent"] = "tui_default"
        elif "simbiosis" in fname_l:
            meta["agent"] = "simbiosis"
        elif "dqn_control" in fname_l:
            meta["agent"] = "dqn_control"
        elif "control" in fname_l:
            meta["agent"] = "control"
        else:
            meta["agent"] = "tui"

    # Agent para SOTA u otras carpetas con nombre de algoritmo
    algo_keys = {"ppo", "a2c", "dqn", "sac", "td3"}
    # 1. Detectar por carpeta
    for i, p in enumerate(parts):
        if p in algo_keys:
            meta["agent"] = p
            break
    # 2. Detectar por subcarpeta sota
    if meta["agent"] is None and "sota" in parts:
        try:
            idx = parts.index("sota")
            meta["agent"] = parts[idx + 1]  # ppo, a2c, dqn, sac...
        except Exception:
            meta["agent"] = "sota"
    # 3. Detectar por nombre de archivo si no se encontró por ruta
    if meta["agent"] is None:
        fname_l = path.name.lower()
        for key in algo_keys:
            if key in fname_l:
                meta["agent"] = key
                break
    # 4. Si aún no se detecta, revisa carpetas intermedias por etiquetas TUI
    if meta["agent"] is None:
        for p in parts:
            if "tui_tuned" in p:
                meta["agent"] = "tui_tuned"
                break
            if "tui_default" in p:
                meta["agent"] = "tui_default"
                break
        if meta["agent"] is None and "tui" in parts:
            meta["agent"] = "tui"

    # risk_scale
    risk_match = re.search(r"risk[_-]?([0-9.]+)", path.as_posix(), flags=re.IGNORECASE)
    if risk_match:
        try:
            meta["risk_scale"] = float(risk_match.group(1))
        except ValueError:
            meta["risk_scale"] = None

    # episodes / kappa / lambda / mix desde el nombre
    ep_match = re.search(r"episodes?([0-9]+)", path.as_posix(), flags=re.IGNORECASE)
    if ep_match:
        meta["episodes"] = int(ep_match.group(1))
    kappa_match = re.search(r"kappa([0-9.]+)", path.as_posix(), flags=re.IGNORECASE)
    if kappa_match:
        try:
            meta["kappa"] = float(kappa_match.group(1))
        except ValueError:
            pass
    lambda_match = re.search(r"lambda([0-9.]+)", path.as_posix(), flags=re.IGNORECASE)
    if lambda_match:
        try:
            meta["lambda"] = float(lambda_match.group(1))
        except ValueError:
            pass
    mix_match = re.search(r"mix([0-9.]+)", path.as_posix(), flags=re.IGNORECASE)
    if mix_match:
        try:
            meta["mix"] = float(mix_match.group(1))
        except ValueError:
            pass

    return meta


def consolidate_csvs(extra_paths=None, output="results/master_results.csv"):  # pragma: no cover
    all_files = []
    # Si se pasan rutas extra, solo usamos esas para evitar mezclar datos de workspace (útil en tests)
    paths = list(extra_paths) if extra_paths else list(BASE_PATHS)
    for base in paths:
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
        steps_col = first_matching_column(df, ["steps"])

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
        df["steps"] = df[steps_col] if steps_col else None
        # Nuevas métricas (si existen en CSV origen)
        df["risk_level"] = df["risk_level"] if "risk_level" in df.columns else None
        df["red_team"] = df["red_team"] if "red_team" in df.columns else None
        df["avg_gap"] = df["avg_gap"] if "avg_gap" in df.columns else None
        df["gaming_hits"] = df["gaming_hits"] if "gaming_hits" in df.columns else None
        df["gating_hits"] = df["gating_hits"] if "gating_hits" in df.columns else None
        df["ipg"] = df["ipg"] if "ipg" in df.columns else None
        df["u_proxy"] = df["u_proxy"] if "u_proxy" in df.columns else None
        df["u_humans"] = df["u_humans"] if "u_humans" in df.columns else None
        df["ope_dr"] = df["ope_dr"] if "ope_dr" in df.columns else None
        if reward_col and trip_col:
            try:
                df["safety_adj_reward"] = df.apply(
                    lambda r: r[reward_col] * math.exp(-SAFETY_BETA * r[trip_col])
                    if pd.notnull(r[reward_col]) and pd.notnull(r[trip_col])
                    else None,
                    axis=1,
                )
            except Exception:
                df["safety_adj_reward"] = None
        else:
            df["safety_adj_reward"] = None

        # Métricas SAU normalizadas por steps
        def _sau(row, beta):
            try:
                if (
                    pd.notnull(row.get(reward_col))
                    and pd.notnull(row.get(trip_col))
                    and pd.notnull(row.get(steps_col))
                ):
                    steps_val = row[steps_col]
                    if steps_val and steps_val != 0:
                        return row[reward_col] * math.exp(-beta * row[trip_col] / steps_val)
            except Exception:
                return None
            return None

        if reward_col and trip_col and steps_col:
            df["sau_beta1"] = df.apply(lambda r: _sau(r, SAU_BETA1), axis=1)
            df["sau_beta2"] = df.apply(lambda r: _sau(r, SAU_BETA2), axis=1)
        else:
            df["sau_beta1"] = None
            df["sau_beta2"] = None

        for col in MASTER_COLS:
            if col not in df.columns:
                df[col] = None

        dfs.append(df[MASTER_COLS])

        if idx % 50 == 0:
            print(f"Procesados {idx} archivos...")

    if dfs:
        try:
            master = pd.concat(dfs, ignore_index=True)
        except ValueError:
            master = pd.DataFrame(columns=MASTER_COLS)
        out_path = Path(output)
        master.to_csv(out_path, index=False)
        print(f"Master CSV generado: {out_path}")
    else:
        out_path = Path(output)
        pd.DataFrame(columns=MASTER_COLS).to_csv(out_path, index=False)
        print(f"No se encontraron archivos CSV válidos. Se creó un CSV vacío: {out_path}")


if __name__ == "__main__":
    consolidate_csvs()
