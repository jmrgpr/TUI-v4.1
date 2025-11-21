import warnings
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para tests
<<<<<<< HEAD
import streamlit as st
import os
from pathlib import Path

# Streamlit session_state shim para entorno de pruebas sin runtime
class _DummyState(dict):
    def __getattr__(self, item):
        return self.get(item)
    def clear(self):
        super().clear()

if not isinstance(st.session_state, dict):
    st.session_state = _DummyState()

# Asegurar que el cwd usado en algunos tests de subprocess exista en Windows
try:
    if os.name == "nt":
        os.makedirs(r"c:\Proyectos\TUI-v4.1", exist_ok=True)
        # Prepend venv Scripts to PATH para que los subprocesos usen el intérprete correcto
        venv_scripts = Path(__file__).resolve().parent / ".venv" / "Scripts"
        if venv_scripts.exists():
            os.environ["PATH"] = str(venv_scripts) + os.pathsep + os.environ.get("PATH", "")
except Exception:
    pass
=======
>>>>>>> 1c1f237 (Actualización científica y operativa: protocolo bilingüe, criterios cuantitativos, checklist y scripts alineados. Listo para experimento Fase 2.)

# Suprimir warnings específicos
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=UserWarning, message="FigureCanvasAgg is non-interactive")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="scipy.stats")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="runpy")
warnings.filterwarnings("ignore", category=DeprecationWarning)
<<<<<<< HEAD
warnings.filterwarnings("ignore", category=FutureWarning)
=======
warnings.filterwarnings("ignore", category=FutureWarning)
>>>>>>> 1c1f237 (Actualización científica y operativa: protocolo bilingüe, criterios cuantitativos, checklist y scripts alineados. Listo para experimento Fase 2.)
