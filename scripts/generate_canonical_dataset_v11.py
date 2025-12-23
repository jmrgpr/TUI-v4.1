import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path("results/v11")
DOCUMENT = ROOT / "CANONICAL_DATASET_v11.md"
AGENTS = {"control", "dqn_control", "simbiosis"}
PHASES = ["F0_baseline", "F1_highrisk", "F2_redteam", "F3", "F4", "F5", "F6", "F7", "F8"]


def detect_phase(path: Path) -> str | None:
    lowered = [p.lower() for p in path.parts]
    if "f8" in lowered:
        return "F8"
    if "f7" in lowered:
        return "F7"
    if "f6" in lowered:
        return "F6"
    if "f5" in lowered:
        return "F5"
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
    if phase == "F5":
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    if phase == "F6":
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    if phase == "F7":
        return any(p.startswith("grid") for p in parts) and "riskhigh" in parts and any(agent in parts for agent in AGENTS)
    if phase == "F8":
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
    manifest = []
    for path in sorted(files):
        phase = detect_phase(path)
        if not phase:
            continue
        agent = next((part for part in path.parts if part in AGENTS), "")
        manifest.append(
            {
                "phase": phase,
                "agent": agent,
                "grid": parse_grid(path),
                "risk": parse_risk(path),
                "seed": parse_seed(path),
                "path": path.as_posix(),
                "sha256": compute_sha256(path),
            }
        )
    return manifest


def format_manifest(manifest: list[dict]) -> str:
    counters = Counter(entry["phase"] for entry in manifest)
    lines = [
        "# CANONICAL_DATASET_v11",
        "",
        "Este manifiesto lista los CSV canónicos de la serie v11 (F0_baseline, F1_highrisk, F2_redteam, F3, F4, F5, F6, F7 y F8) y excluye las copias archivadas en `results/v11/archived` para garantizar trazabilidad única.",
        "",
        "El script `scripts/generate_canonical_dataset_v11.py` controla la selección de archivos y el cálculo de su hash sha256.",
        "",
        "## Resumen por fase",
    ]
    for phase in PHASES:
        lines.append(f"- `{phase}`: {counters.get(phase, 0)} archivos canónicos.")
    lines.append("")
    lines.append("## Manifest general")
    lines.append("")
    header = "| phase | agent | grid | risk | seed | path | sha256 |"
    sep = "| --- | --- | --- | --- | --- | --- | --- |"
    lines.append(header)
    lines.append(sep)
    for entry in manifest:
        lines.append(
            f"| {entry['phase']} | {entry['agent']} | {entry['grid']} | {entry['risk']} | {entry['seed']} | `{entry['path']}` | `{entry['sha256']}` |"
        )
    lines.append("")
    lines.append("Se documenta adicionalmente en `results/v11/data/f2_vs_f1_diff.md` la comparativa F1 vs F2 y los campos meta `phase/attack_*` que enriquecen cada JSON.")
    lines.append("Los archivos `raw/` y las copias en `archived/` solo se conservan para auditoría histórica; no se usan en análisis estadístico.")
    return "\n".join(lines)


def main():
    manifest = build_manifest()
    if not manifest:
        raise RuntimeError("No se detectaron CSV canónicos; asegúrate de tener los directorios de v11 (F0/F1/F2/F3) poblados.")
    DOCUMENT.write_text(format_manifest(manifest), encoding="utf-8")
    print(f"Manifest canónico generado en {DOCUMENT}")


if __name__ == "__main__":
    main()
