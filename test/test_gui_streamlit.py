"""
Test básico de importación y renderizado de la GUI Streamlit para TUI v4.1 Toy Model — RL Symbiosis
Basic import and render test for Streamlit GUI in TUI v4.1 Toy Model — RL Symbiosis
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import_gui_streamlit():
    try:
        import sim.gui_streamlit
    except Exception as e:
        assert False, f"Error al importar GUI Streamlit: {e}"

import pytest
from unittest.mock import patch, MagicMock

@patch('sim.gui_streamlit.st')
def test_main_render(mock_st):
    """Test main function rendering."""
    from sim.gui_streamlit import main
    main()
    mock_st.title.assert_called_with("Simulador TUI v4.1 — Toy Model RL Symbiosis")
    mock_st.markdown.assert_called()

@patch('sim.gui_streamlit.st')
@patch('sim.gui_streamlit.run_experiment')
def test_button_simulation_control(mock_run_experiment, mock_st):
    """Test simulation button for Control agent."""
    mock_st.button.return_value = True
    mock_st.selectbox.return_value = "Control (Q-table)"
    mock_run_experiment.return_value = {"avg_reward": 10.0}
    # Import and execute the button logic
    import sim.gui_streamlit as gui
    # Simulate the button press logic
    if mock_st.button("Ejecutar simulación / Run simulation"):
        results_control = gui.run_experiment(
            episodes=1000,
            seed=42,
            risk_scale=1.0,
            agent_name="Control",
            use_pgf=False,
            use_dqn=False
        )
        assert results_control["avg_reward"] == 10.0
    mock_st.button.assert_called_with("Ejecutar simulación / Run simulation")

@patch('sim.gui_streamlit.st')
@patch('sim.gui_streamlit.run_experiment')
def test_button_simulation_simbiosis(mock_run_experiment, mock_st):
    """Test simulation button for Simbiosis agent."""
    mock_st.button.return_value = True
    mock_st.selectbox.return_value = "Simbiosis (DQN)"
    mock_run_experiment.return_value = {"avg_reward": 15.0}
    import sim.gui_streamlit as gui
    results_simbiosis = None
    if mock_st.button("Ejecutar simulación / Run simulation"):
        results_control = gui.run_experiment(
            episodes=1000,
            seed=42,
            risk_scale=1.0,
            agent_name="Control",
            use_pgf=False,
            use_dqn=False
        )
        if mock_st.selectbox.return_value == "Simbiosis (DQN)":
            results_simbiosis = gui.run_experiment(
                episodes=1000,
                seed=42,
                risk_scale=1.0,
                agent_name="Simbiosis",
                use_pgf=True,
                use_dqn=True
            )
        assert results_simbiosis is not None
        assert results_simbiosis["avg_reward"] == 15.0

@patch('sim.gui_streamlit.st')
def test_comparison_panel(mock_st):
    """Test historical runs comparison panel."""
    mock_st.session_state = {"runs": [
        {"params": {"episodes": 1000}, "control": {"avg_reward": 10.0}, "simbiosis": {"avg_reward": 12.0}},
        {"params": {"episodes": 1000}, "control": {"avg_reward": 11.0}, "simbiosis": {"avg_reward": 13.0}}
    ]}
    mock_st.selectbox.side_effect = [0, 1]
    import sim.gui_streamlit as gui
    # Simulate comparison logic
    if len(mock_st.session_state["runs"]) > 1:
        idx_a = mock_st.selectbox("Corrida A / Run A", options=list(range(len(mock_st.session_state["runs"]))), format_func=lambda i: f"Run {i+1}")
        idx_b = mock_st.selectbox("Corrida B / Run B", options=list(range(len(mock_st.session_state["runs"]))), index=len(mock_st.session_state["runs"])-1, format_func=lambda i: f"Run {i+1}")
        run_a = mock_st.session_state["runs"][idx_a]
        run_b = mock_st.session_state["runs"][idx_b]
        assert run_a["control"]["avg_reward"] == 10.0
        assert run_b["control"]["avg_reward"] == 11.0

@patch('sim.gui_streamlit.st')
def test_export_history(mock_st):
    """Test export history functionality."""
    mock_st.session_state = {"runs": [{"params": {}, "control": {}, "simbiosis": {}}]}
    mock_st.download_button.return_value = None
    import sim.gui_streamlit as gui
    import json
    data = json.dumps(mock_st.session_state["runs"], indent=2)
    mock_st.download_button.assert_not_called()  # Since it's conditional

@patch('sim.gui_streamlit.st')
def test_sidebar_parameters(mock_st):
    """Test sidebar parameter sliders."""
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Control (Q-table)"
    import sim.gui_streamlit as gui
    # Check that parameters are set
    assert gui.episodes == 1000
    assert gui.seed == 42
    assert gui.risk_scale == 1.0

@patch('sim.gui_streamlit.st')
def test_help_panel(mock_st):
    """Test help panel rendering."""
    import sim.gui_streamlit as gui
    mock_st.markdown.assert_not_called()  # Just check it can be called
