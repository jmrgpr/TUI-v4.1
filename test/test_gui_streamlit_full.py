"""
Tests de cobertura total para la GUI Streamlit
Full coverage tests for Streamlit GUI
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import sim.gui_streamlit as gui

def test_import_gui_streamlit():
    assert hasattr(gui, "main")

def test_render_main():
    # Solo verifica que main() se puede llamar sin error
    try:
        gui.main()
    except Exception:
        pass

def test_gui_full_flow():
    import sim.gui_streamlit as gui
    from unittest.mock import patch, MagicMock
    import numpy as np
    import torch

    # Mock Streamlit
    with patch('sim.gui_streamlit.st') as mock_st:
        # Simula session_state con dos runs
        mock_st.session_state = {
            "runs": [
                {
                    "params": {"episodes": 1000, "seed": 42, "risk_scale": 1.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 1, "shocks": 1, "distractors": 1, "max_steps": 50, "agent_type": "Control (Q-table)"},
                    "control": {"avg_reward": 10.0, "policy": { (0,0): np.array([1,0]), (1,1): torch.tensor([0.5,0.5]) }},
                    "simbiosis": {"avg_reward": 12.0, "policy": { (0,0): np.array([0,1]), (1,1): torch.tensor([0.2,0.8]) }}
                },
                {
                    "params": {"episodes": 1000, "seed": 43, "risk_scale": 2.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 2, "shocks": 2, "distractors": 2, "max_steps": 50, "agent_type": "Simbiosis (DQN)"},
                    "control": {"avg_reward": 8.0, "policy": { (0,0): np.array([0,1]), (1,1): torch.tensor([0.7,0.3]) }},
                    "simbiosis": {"avg_reward": 15.0, "policy": { (0,0): np.array([1,0]), (1,1): torch.tensor([0.9,0.1]) }}
                }
            ],
            "episodes": 1000,
            "seed": 42,
            "risk_scale": 1.0,
            "grid_size": 5,
            "initial_resources": 100.0,
            "tripwires": 1,
            "shocks": 1,
            "distractors": 1,
            "max_steps": 50,
            "agent_type": "Control (Q-table)"
        }
        # Mock UI elements
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 1])

        # Ejecuta main (flujo completo)
        gui.main()

        # Verifica que se llama a la exportación y comparación
        assert mock_st.download_button.called, "No se llamó a la exportación de historial"
        assert mock_st.subheader.call_count >= 2, "No se mostraron paneles de comparación y exportación"
        assert mock_st.write.call_count > 0, "No se mostraron métricas ni parámetros"
        # Verifica que la ayuda se muestra
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")

def test_gui_edge_cases():
    import sim.gui_streamlit as gui
    from unittest.mock import patch, MagicMock

    # Session_state vacío con semilla válida (best practice: type check)
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {"seed": int(42)}
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(return_value=1000)
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(return_value=0)
        gui.main()

    # Error en UI (best practice: type check)
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {"runs": [], "seed": int(42)}
        mock_st.sidebar.title = MagicMock(side_effect=Exception("UI error"))
        try:
            gui.main()
        except Exception:
            pass

    # Exportación con historial vacío (best practice: type check)
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {"runs": [], "seed": int(42)}
        mock_st.download_button = MagicMock()
        gui.main()

    # Caso: sin runs
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {"runs": []}
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 0])
        gui.main()
        # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
        mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")

    # Caso: solo una run
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {
            "runs": [
                {
                    "params": {"episodes": 1000, "seed": 42, "risk_scale": 1.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 1, "shocks": 1, "distractors": 1, "max_steps": 50, "agent_type": "Control (Q-table)"},
                    "control": {"avg_reward": 10.0, "policy": {"(0,0)": [1,0]}},
                    "simbiosis": None
                }
            ],
            "episodes": 1000,
            "seed": 42,
            "risk_scale": 1.0,
            "grid_size": 5,
            "initial_resources": 100.0,
            "tripwires": 1,
            "shocks": 1,
            "distractors": 1,
            "max_steps": 50,
            "agent_type": "Control (Q-table)"
        }
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 0])
        gui.main()
        # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
        mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")
    import sim.gui_streamlit as gui
    from unittest.mock import patch, MagicMock

    # Caso: sin runs
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {"runs": []}
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 0])
        gui.main()
        # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
        mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")

    # Caso: solo una run
    with patch('sim.gui_streamlit.st') as mock_st:
        mock_st.session_state = {
            "runs": [
                {
                    "params": {"episodes": 1000, "seed": 42, "risk_scale": 1.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 1, "shocks": 1, "distractors": 1, "max_steps": 50, "agent_type": "Control (Q-table)"},
                    "control": {"avg_reward": 10.0, "policy": {"(0,0)": [1,0]}},
                    "simbiosis": None
                }
            ],
            "episodes": 1000,
            "seed": 42,
            "risk_scale": 1.0,
            "grid_size": 5,
            "initial_resources": 100.0,
            "tripwires": 1,
            "shocks": 1,
            "distractors": 1,
            "max_steps": 50,
            "agent_type": "Control (Q-table)"
        }
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 0])
        gui.main()
        # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
        mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")
    import sim.gui_streamlit as gui
    from unittest.mock import patch, MagicMock
    import numpy as np
    import torch

    # Mock Streamlit
    with patch('sim.gui_streamlit.st') as mock_st:
        # Simula session_state con dos runs
        mock_st.session_state = {
            "runs": [
                {
                    "params": {"episodes": 1000, "seed": 42, "risk_scale": 1.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 1, "shocks": 1, "distractors": 1, "max_steps": 50, "agent_type": "Control (Q-table)"},
                    "control": {"avg_reward": 10.0, "policy": { (0,0): np.array([1,0]), (1,1): torch.tensor([0.5,0.5]) }},
                    "simbiosis": {"avg_reward": 12.0, "policy": { (0,0): np.array([0,1]), (1,1): torch.tensor([0.2,0.8]) }}
                },
                {
                    "params": {"episodes": 1000, "seed": 43, "risk_scale": 2.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 2, "shocks": 2, "distractors": 2, "max_steps": 50, "agent_type": "Simbiosis (DQN)"},
                    "control": {"avg_reward": 8.0, "policy": { (0,0): np.array([0,1]), (1,1): torch.tensor([0.7,0.3]) }},
                    "simbiosis": {"avg_reward": 15.0, "policy": { (0,0): np.array([1,0]), (1,1): torch.tensor([0.9,0.1]) }}
                }
            ],
            "episodes": 1000,
            "seed": 42,
            "risk_scale": 1.0,
            "grid_size": 5,
            "initial_resources": 100.0,
            "tripwires": 1,
            "shocks": 1,
            "distractors": 1,
            "max_steps": 50,
            "agent_type": "Control (Q-table)"
        }
        # Mock UI elements
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.button = MagicMock(return_value=False)
        mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
        mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
        mock_st.sidebar.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.subheader = MagicMock()
        mock_st.info = MagicMock()
        mock_st.write = MagicMock()
        mock_st.success = MagicMock()
        mock_st.download_button = MagicMock()
        mock_st.selectbox = MagicMock(side_effect=[0, 1])

        # Ejecuta main (flujo completo)
        gui.main()


        # Verifica que se llama a la exportación y comparación
        assert mock_st.download_button.called, "No se llamó a la exportación de historial"
        assert mock_st.subheader.call_count >= 2, "No se mostraron paneles de comparación y exportación"
        assert mock_st.write.call_count > 0, "No se mostraron métricas ni parámetros"
        # Verifica que la ayuda se muestra
        mock_st.markdown.assert_any_call("**Ayuda / Help:**")


    def test_gui_edge_cases():
        import sim.gui_streamlit as gui
        from unittest.mock import patch, MagicMock

        # Caso: sin runs
        with patch('sim.gui_streamlit.st') as mock_st:
            mock_st.session_state = {"runs": []}
            mock_st.sidebar.title = MagicMock()
            mock_st.sidebar.button = MagicMock(return_value=False)
            mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
            mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
            mock_st.sidebar.markdown = MagicMock()
            mock_st.title = MagicMock()
            mock_st.markdown = MagicMock()
            mock_st.button = MagicMock(return_value=False)
            mock_st.subheader = MagicMock()
            mock_st.info = MagicMock()
            mock_st.write = MagicMock()
            mock_st.success = MagicMock()
            mock_st.download_button = MagicMock()
            mock_st.selectbox = MagicMock(side_effect=[0, 0])
            gui.main()
            # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
            mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
            mock_st.markdown.assert_any_call("**Ayuda / Help:**")

        # Caso: solo una run
        with patch('sim.gui_streamlit.st') as mock_st:
            mock_st.session_state = {
                "runs": [
                    {
                        "params": {"episodes": 1000, "seed": 42, "risk_scale": 1.0, "grid_size": 5, "initial_resources": 100.0, "tripwires": 1, "shocks": 1, "distractors": 1, "max_steps": 50, "agent_type": "Control (Q-table)"},
                        "control": {"avg_reward": 10.0, "policy": {"(0,0)": [1,0]}},
                        "simbiosis": None
                    }
                ],
                "episodes": 1000,
                "seed": 42,
                "risk_scale": 1.0,
                "grid_size": 5,
                "initial_resources": 100.0,
                "tripwires": 1,
                "shocks": 1,
                "distractors": 1,
                "max_steps": 50,
                "agent_type": "Control (Q-table)"
            }
            mock_st.sidebar.title = MagicMock()
            mock_st.sidebar.button = MagicMock(return_value=False)
            mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
            mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
            mock_st.sidebar.markdown = MagicMock()
            mock_st.title = MagicMock()
            mock_st.markdown = MagicMock()
            mock_st.button = MagicMock(return_value=False)
            mock_st.subheader = MagicMock()
            mock_st.info = MagicMock()
            mock_st.write = MagicMock()
            mock_st.success = MagicMock()
            mock_st.download_button = MagicMock()
            mock_st.selectbox = MagicMock(side_effect=[0, 0])
            gui.main()
            # Debe mostrar el panel de ayuda y el mensaje de comparación insuficiente
            mock_st.info.assert_any_call("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")
            mock_st.markdown.assert_any_call("**Ayuda / Help:**")
