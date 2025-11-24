#!/usr/bin/env python3
"""
Centro de Control Experimental (CLI) para TUI v4.1
--------------------------------------------------

Interfaz minima en Streamlit con dos modos:
1. Ejecutor de scripts CLI (usa los scripts de la carpeta scripts/).
2. Toy Model interactivo (llama directamente a run_experiment).
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.runner import run_experiment  # noqa: E402

# Config de scripts y descripcion
SCRIPT_CONFIGS = {
    "run_full_experiment.py": {
        "description": "Pipeline completo: barrido, comparacion SOTA y consolidado.",
        "path": "scripts/run_full_experiment.py",
    },
    "run_ablation_quick.py": {
        "description": "Ablacion rapida (Only vs PGF Light vs PGF Heavy).",
        "path": "scripts/run_ablation_quick.py",
    },
    "run_search_pgf.py": {
        "description": "Busqueda de hiperparametros PGF.",
        "path": "scripts/run_search_pgf.py",
    },
}


def load_experiment_spec(script_path):
    """Intenta cargar EXPERIMENT_SPEC del script, si existe."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "EXPERIMENT_SPEC":
                        return ast.literal_eval(node.value)
    except Exception:
        pass
    return None


def extract_argparse_params(script_path):
    """Extrae parametros y defaults de argparse en el script."""
    params = {}
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and hasattr(node.func, "attr")
                and node.func.attr == "add_argument"
            ):
                flag = None
                default = None
                label = None
                typ = "str"
                for arg in node.args:
                    if isinstance(arg, ast.Constant):
                        flag = arg.value
                for kw in node.keywords:
                    if kw.arg == "default":
                        default = kw.value.value if hasattr(kw.value, "value") else None
                    if kw.arg == "type":
                        typ = kw.value.id if hasattr(kw.value, "id") else "str"
                    if kw.arg == "help":
                        label = kw.value.value if hasattr(kw.value, "value") else None
                if flag:
                    params[flag.lstrip("-")] = {
                        "type": typ,
                        "default": default,
                        "label": label or flag,
                        "flag": flag,
                    }
    except Exception:
        pass
    return params


def get_script_params(script_name):
    """Obtiene los parametros y defaults del script."""
    script_path = SCRIPT_CONFIGS[script_name]["path"]
    spec = load_experiment_spec(script_path)
    if spec and "params" in spec:
        return spec["params"]
    return extract_argparse_params(script_path)


def run_command_live(cmd_list):
    """Ejecuta comando y muestra stdout/stderr en streaming."""
    st.info(f"Ejecutando comando:\n`{' '.join(str(x) for x in cmd_list)}`")
    log_expander = st.expander("Ver logs de ejecucion", expanded=True)
    with log_expander:
        log_placeholder = st.empty()
    logs = []
    try:
        proc = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        for line in iter(proc.stdout.readline, ""):
            logs.append(line)
            log_placeholder.code("".join(logs[-15:]), language="bash")
        proc.stdout.close()
        rc = proc.wait()
        if rc == 0:
            st.success("Proceso finalizado exitosamente.")
            return True
        st.error(f"El proceso fallo con codigo de salida {rc}.")
        st.error("Revisa los logs completos arriba para depurar.")
        return False
    except Exception as e:
        st.error(f"Error al intentar ejecutar: {str(e)}")
        return False


def render_results_preview(csv_path="results/master_results.csv"):
    """Muestra una vista previa de los resultados si existen."""
    path = Path(csv_path)
    if not path.exists():
        st.info("Aun no hay resultados consolidados (`master_results.csv`).")
        return

    st.markdown("### Vista previa de resultados")
    try:
        df = pd.read_csv(path)
        st.write(f"Archivo cargado: `{path}` ({len(df)} filas)")
        st.dataframe(df.tail(10), use_container_width=True)
        try:
            with open(path, "rb") as f:
                st.download_button(
                    label="Descargar CSV consolidado",
                    data=f,
                    file_name="master_results.csv",
                    mime="text/csv",
                )
        except Exception:
            # Evitar que falle la descarga si el archivo no esta accesible
            st.warning("No se pudo preparar la descarga del CSV.")
    except Exception as e:
        st.warning(f"No se pudo leer el archivo de resultados: {e}")


def render_cli_mode():  # pragma: no cover
    st.header("Ejecutor de Experimentos (CLI)")
    script_name = st.selectbox("Script de experimento", list(SCRIPT_CONFIGS.keys()))
    cfg = SCRIPT_CONFIGS[script_name]
    st.caption(cfg["description"])

    params = get_script_params(script_name)
    cli_args = []
    with st.form(key=f"form_{script_name}"):
        cols = st.columns(2)
        for i, (pkey, pcfg) in enumerate(params.items()):
            col = cols[i % 2]
            wkey = f"{script_name}_{pkey}"
            typ = pcfg.get("type", "str")
            default = pcfg.get("default", "")
            label = pcfg.get("label", pkey)
            flag = pcfg.get("flag", f"--{pkey}")
            if typ == "int":
                val = col.number_input(label, value=default, step=10, key=wkey)
                cli_args.extend([flag, str(val)])
            elif typ == "float":
                val = col.number_input(label, value=default, step=0.1, format="%.4f", key=wkey)
                cli_args.extend([flag, str(val)])
            elif typ == "bool":
                val = col.checkbox(label, value=default, key=wkey)
                if val:
                    cli_args.append(flag)
            elif typ == "list":
                val_str = col.text_input(label, value=default, key=wkey)
                if val_str:
                    items = [x.strip() for x in val_str.split(",") if x.strip()]
                    if items:
                        cli_args.append(flag)
                        cli_args.extend(items)
            else:
                val_str = col.text_input(label, value=default, key=wkey)
                if val_str:
                    cli_args.extend([flag, val_str])
        submitted = st.form_submit_button("Ejecutar experimento")

    if submitted:
        full_cmd = [sys.executable, cfg["path"]] + cli_args
        st.code(" ".join(str(x) for x in full_cmd), language="bash")
        success = run_command_live(full_cmd)
        if success:
            st.balloons()
        render_results_preview()


def render_toy_mode():  # pragma: no cover
    st.header("Toy Model Interactivo (Live)")
    cols = st.columns(3)
    if len(cols) >= 3:
        c1, c2, c3 = cols[:3]
    else:  # fallback defensivo para tests/mocks
        c1 = c2 = c3 = st
    episodes = c1.slider("Episodios", 10, 1000, 100)
    seed = c2.number_input("Semilla", value=42)
    risk_scale = c3.slider("Escala de Riesgo", 0.1, 5.0, 1.0)
    if st.button("Correr simulacion rapida"):
        try:
            with st.spinner("Simulando..."):
                res = run_experiment(
                    episodes=episodes,
                    seed=int(seed),
                    risk_scale=risk_scale,
                    agent_name="InteractiveAgent",
                    use_pgf=True,
                )
            st.metric("Recompensa Promedio", f"{res.get('avg_reward', 0):.2f}")
            if "total_rewards" in res:
                st.line_chart(res["total_rewards"])
        except Exception as exc:
            st.error(f"Error en la simulacion: {exc}")


def main():  # pragma: no cover
    st.set_page_config(page_title="TUI v4.1 - Experimental Dashboard", layout="wide")
    mode = st.sidebar.radio(
        "Seleccionar modo",
        ["Ejecutor de Experimentos (CLI)", "Toy Model Interactivo (Live)"],
        index=0,
    )
    if mode.startswith("Ejecutor"):
        render_cli_mode()
    else:
        render_toy_mode()


if __name__ == "__main__":  # pragma: no cover
    main()
