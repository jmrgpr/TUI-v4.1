import json
from pathlib import Path

F2_DIR = Path("results/v11/F2_redteam")
ATTACK_TYPES = ["reward_hacking", "distributional_shift", "gaming_metricas"]
RELEVANT_CONFIG_KEYS = [
    "grid_size",
    "risk_scale",
    "risk_level",
    "pgf_mix",
    "episodes",
    "seed",
    "red_team",
    "red_team_prob",
    "red_team_impact",
    "red_team_move_tripwire_prob",
    "red_team_add_shock_prob",
    "red_team_block_prob",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, content: dict) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(content, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def ensure_fields(path: Path) -> None:
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] JSON inválido en {path}: {exc}")
        raise
    modified = False

    if data.get("phase") != "F2_redteam":
        data["phase"] = "F2_redteam"
        modified = True

    config = data.get("config", {})
    attack_enabled = bool(config.get("red_team") or data.get("red_team"))
    if data.get("attack_enabled") != attack_enabled:
        data["attack_enabled"] = attack_enabled
        modified = True

    attack_type = data.get("attack_type")
    if attack_enabled and attack_type != "red_team_adversarial":
        data["attack_type"] = "red_team_adversarial"
        modified = True
    elif not attack_enabled and attack_type is not None:
        data["attack_type"] = None
        modified = True

    current_params = data.get("attack_params") or {}
    params = {k: config.get(k) for k in RELEVANT_CONFIG_KEYS if config.get(k) is not None}
    params.setdefault("red_team", attack_enabled)
    if params != current_params:
        data["attack_params"] = params
        modified = True

    if modified:
        save_json(path, data)


def main() -> None:
    if not F2_DIR.exists():
        raise FileNotFoundError(f"F2 directory not found: {F2_DIR}")
    updated = 0
    for json_path in sorted(F2_DIR.rglob("*.json")):
        ensure_fields(json_path)
        updated += 1
    print(f"Metadata actualizado en {updated} archivos JSON de F2.")


if __name__ == "__main__":
    main()
