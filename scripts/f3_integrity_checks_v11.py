import re
from pathlib import Path

import pandas as pd

F3_DIR = Path("results/v11/F3")
MASTER_CSV = Path("results/master_results_clean.csv")
OUT_MD = Path("results/v11/data/f3_integrity_report_v11.md")

EXPECTED_EPISODES = 200
MIN_EPISODES_OK = 190


def find_f3_csvs() -> list[Path]:
    return sorted([p for p in F3_DIR.rglob("*_episodes.csv") if p.is_file() and "raw" not in [x.lower() for x in p.parts]])


def find_f3_raw_csvs() -> list[Path]:
    raw_dir = F3_DIR / "raw"
    if not raw_dir.exists():
        return []
    return sorted([p for p in raw_dir.rglob("*_episodes.csv") if p.is_file()])


def parse_tokens(path: Path) -> dict:
    s = path.as_posix().lower()
    cond = "F1_highrisk" if "/f1_highrisk/" in s else ("F2_redteam" if "/f2_redteam/" in s else "unknown")
    grid_m = re.search(r"grid(\d+)", s)
    seed_m = re.search(r"seed(\d+)", s)
    mix_m = re.search(r"_m(\d+)p(\d+)_v11_episodes\.csv$", s)
    return {
        "condition": cond,
        "grid": int(grid_m.group(1)) if grid_m else None,
        "seed": int(seed_m.group(1)) if seed_m else None,
        "pgf_mix": float(f"{int(mix_m.group(1))}.{int(mix_m.group(2))}") if mix_m else None,
        "agent": path.parent.name,
    }


def main() -> None:
    csvs = find_f3_csvs()
    if not csvs:
        raise RuntimeError(f"No se encontraron CSV F3 en {F3_DIR}")

    raw_csvs = find_f3_raw_csvs()

    rows = []
    for p in csvs:
        meta = parse_tokens(p)
        try:
            df = pd.read_csv(p)
            n_rows = int(len(df))
        except Exception:
            n_rows = -1
        rows.append({**meta, "path": p.as_posix(), "csv_rows": n_rows})

    df_rows = pd.DataFrame(rows)
    bad_read = df_rows[df_rows["csv_rows"] < 0]
    bad_trunc = df_rows[(df_rows["csv_rows"] >= 0) & (df_rows["csv_rows"] < MIN_EPISODES_OK)]
    warn_short = df_rows[(df_rows["csv_rows"] >= MIN_EPISODES_OK) & (df_rows["csv_rows"] < EXPECTED_EPISODES)]

    # Expected counts: m0.0 => 3 agents; m0.2 => only simbiosis (control/dqn would be duplicates)
    count_total = int(len(df_rows))
    count_m0 = int((df_rows["pgf_mix"] == 0.0).sum())
    count_m2 = int((df_rows["pgf_mix"] == 0.2).sum())

    expected_m0 = 3 * 2 * 2 * 5  # agent * condition * grid * seed
    expected_m2 = 1 * 2 * 2 * 5
    expected_total = expected_m0 + expected_m2

    # Master sanity
    master_rows = 0
    master_f3_rows = 0
    if MASTER_CSV.exists():
        master = pd.read_csv(MASTER_CSV)
        master_rows = int(len(master))
        f3_mask = master["filename"].astype(str).str.replace("\\\\", "/", regex=True).str.contains("results/v11/F3/", case=False, na=False)
        master_f3_rows = int(f3_mask.sum())

    lines = [
        "# F3 integrity checks (v11)",
        "",
        f"- CSVs organizados encontrados (excluye `raw/`): {count_total} (esperado={expected_total})",
        f"- Por pgf_mix: m0.0={count_m0} (esperado={expected_m0}), m0.2={count_m2} (esperado={expected_m2})",
        f"- CSVs agregados en raw/: {len(raw_csvs)} (informativo; no canónico)",
        f"- Episodios esperados por archivo: {EXPECTED_EPISODES} (umbral truncamiento < {MIN_EPISODES_OK})",
        "",
        "## Lectura de CSV",
        f"- Archivos no legibles: {len(bad_read)}",
        f"- Archivos truncados (<{MIN_EPISODES_OK} filas): {len(bad_trunc)}",
        f"- Archivos con warning (>= {MIN_EPISODES_OK} y < {EXPECTED_EPISODES} filas): {len(warn_short)}",
        "",
        "## Master reconsolidado",
        f"- `results/master_results_clean.csv` existe: {MASTER_CSV.exists()}",
        f"- Filas master (total): {master_rows}",
        f"- Filas master (F3): {master_f3_rows}",
        "",
    ]

    if bad_read.any().any():
        lines.append("### No legibles")
        lines.extend([f"- `{p}`" for p in bad_read["path"].tolist()[:20]])
        lines.append("")

    if bad_trunc.any().any():
        lines.append("### Truncados")
        lines.extend([f"- `{p}` ({n} filas)" for p, n in zip(bad_trunc["path"].tolist()[:20], bad_trunc["csv_rows"].tolist()[:20])])
        lines.append("")

    if warn_short.any().any():
        lines.append("### Warning (menos de 200 episodios)")
        lines.extend([f"- `{p}` ({n} filas)" for p, n in zip(warn_short["path"].tolist()[:20], warn_short["csv_rows"].tolist()[:20])])
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Escrito: {OUT_MD}")


if __name__ == "__main__":
    main()
