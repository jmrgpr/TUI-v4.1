import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path("results/v11")
DOCUMENT = ROOT / "CANONICAL_DATASET_EXTENDED_JSON.md"
AGENTS = {"control", "dqn_control", "simbiosis"}
PHASES = ["F0_baseline", "F1_highrisk", "F2_redteam", "F3", "F4"]


def detect_phase(path: Path) -> str | None:
    lowered = [p.lower() for p in path.parts]
    if "f4" in lowered:
        return "F4"
    if "f3" in lowered:
        return "F3"
    for phase in PHASES:
        if phase.lower() in lowered:
            return phase
    return None


def canonical_selector(path: Path) -> bool:
    parts = [p.lower() for p in path.parts]
    if "archived" in parts:
        return False
    phase = detect_phase(path)
    if phase == "F0_baseline":
        return any(p.startswith("grid") for p in parts) and "risklow" in parts and any(agent in parts for agent in AGENTS)
    if phase in {"F1_highrisk", "F2_redteam"}:
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    if phase == "F3":
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    if phase == "F4":
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    return False


def parse_grid(path: Path) -> str:
    match = re.search(r"grid(\d+)", path.name.lower())
    if match:
        return match.group(1)
    match = re.search(r"grid(\d+)", "/".join(path.parts).lower())
    return match.group(1) if match else ""


def parse_risk(path: Path) -> str:
    name = path.name.lower()
    match = re.search(r"r(\d)p(\d)", name)
    if match:
        return f"{int(match.group(1)) + int(match.group(2)) / 10:.1f}"
    if "risklow" in name:
        return "0.5"
    if "riskhigh" in name:
        return "1.5"
    return ""


def parse_seed(path: Path) -> str:
    match = re.search(r"seed(\d+)", path.name.lower())
    if match:
        return match.group(1)
    return ""


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest() -> list[dict]:
    files = [p for p in ROOT.rglob("*_episodes.csv") if canonical_selector(p)]
    manifest: list[dict] = []
    for csv_path in sorted(files):
        phase = detect_phase(csv_path)
        if not phase:
            continue
        agent = next((part for part in csv_path.parts if part in AGENTS), "")
        json_path = csv_path.with_name(csv_path.name.replace("_episodes.csv", ".json"))
        if not json_path.exists():
            raise FileNotFoundError(f"JSON faltante para {csv_path.as_posix()} -> {json_path.as_posix()}")
        manifest.append(
            {
                "phase": phase,
                "agent": agent,
                "grid": parse_grid(csv_path),
                "risk": parse_risk(csv_path),
                "seed": parse_seed(csv_path),
                "episodes_csv": csv_path.as_posix(),
                "json_path": json_path.as_posix(),
                "json_bytes": json_path.stat().st_size,
                "json_sha256": compute_sha256(json_path),
            }
        )
    return manifest


def format_manifest(manifest: list[dict]) -> str:
    counters = Counter(entry["phase"] for entry in manifest)
    lines = [
        "# CANONICAL_DATASET_EXTENDED_JSON (v11)",
        "",
        "Este manifiesto extendido publica hashes sha256 de los JSON canónicos asociados a cada `*_episodes.csv` de v11.",
        "",
        "Objetivo: permitir verificación independiente de `reward_env_total` (derivado del campo `reward_env_evol` en JSON) sin inflar el repo con JSON pesados.",
        "",
        "Notas:",
        "- Por defecto el repo ignora `results/**/*.json` (ver `.gitignore`); algunos JSON históricos pueden estar versionados, otros (p.ej. F3/F4) suelen quedarse fuera.",
        "- En todos los casos, aquí se publican rutas y hashes sha256 para auditoría/verificación; recomputar `reward_env_total` requiere acceso a los JSON con estos hashes.",
        "- Se excluye `results/v11/archived/`.",
        "",
        "Generación:",
        "- Script: `scripts/generate_canonical_dataset_extended_json_v11.py`",
        "- Salida: `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`",
        "",
        "## Resumen por fase",
    ]
    for phase in PHASES:
        lines.append(f"- `{phase}`: {counters.get(phase, 0)} JSON (uno por CSV canónico).")
    lines.append("")
    lines.append("## Manifest")
    lines.append("")
    header = "| phase | agent | grid | risk | seed | episodes_csv | json_path | json_bytes | json_sha256 |"
    sep = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    lines.append(header)
    lines.append(sep)
    for entry in manifest:
        lines.append(
            "| {phase} | {agent} | {grid} | {risk} | {seed} | `{episodes_csv}` | `{json_path}` | {json_bytes} | `{json_sha256}` |".format(
                **entry
            )
        )
    lines.append("")
    return "\n".join(lines)


def main():
    manifest = build_manifest()
    if not manifest:
        raise RuntimeError("No se detectaron CSV canónicos; asegúrate de tener los directorios de v11 (F0/F1/F2/F3) poblados.")
    DOCUMENT.write_text(format_manifest(manifest), encoding="utf-8")
    print(f"Manifest extendido JSON generado en {DOCUMENT}")


if __name__ == "__main__":
    main()
