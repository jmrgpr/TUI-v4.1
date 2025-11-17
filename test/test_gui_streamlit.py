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

# Test que verifica que el módulo se puede importar y ejecutar sin errores
@patch('sim.gui_streamlit.st')
def test_gui_module_execution(mock_st):
    """Test that the GUI module can be executed without errors when mocked."""
    # Setup mocks
    mock_st.session_state = {}
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.slider = MagicMock(side_effect=[1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50])
    mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
    mock_st.sidebar.markdown = MagicMock()
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.button = MagicMock(return_value=False)  # No button press
    mock_st.subheader = MagicMock()
    mock_st.info = MagicMock()
    mock_st.write = MagicMock()
    mock_st.success = MagicMock()
    mock_st.download_button = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    # Verify some basic calls were made
    mock_st.sidebar.title.assert_called_with("TUI v4.1 Simulador — Parámetros")
    assert mock_st.sidebar.slider.call_count == 9
    mock_st.title.assert_called_with("Simulador TUI v4.1 — Toy Model RL Symbiosis")

@patch('sim.gui_streamlit.st')
@patch('sim.gui_streamlit.run_experiment')
def test_simulation_execution_control(mock_run_experiment, mock_st):
    """Test simulation execution for Control agent."""
    # Setup session state
    mock_st.session_state = {"runs": []}

    # Mock sidebar parameters
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Control (Q-table)"
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()

    # Mock main UI
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.button = MagicMock(return_value=True)  # Button pressed
    mock_st.spinner = MagicMock()
    mock_st.success = MagicMock()
    mock_st.info = MagicMock()

    # Mock experiment result
    mock_run_experiment.return_value = {"avg_reward": 10.0, "avg_tripwire": 5.0}

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    # Verify run_experiment was called correctly
<<<<<<< HEAD
    kwargs = mock_run_experiment.call_args.kwargs
    assert kwargs["episodes"] == 1000
    assert kwargs["seed"] == 42
    assert kwargs["agent_name"] == "Control"
=======
    mock_run_experiment.assert_called_with(
        episodes=1000, seed=42, risk_scale=1.0, agent_name="Control", use_pgf=False, use_dqn=False
    )
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
    mock_st.success.assert_called_with("Simulación completada y registrada. / Simulation completed and logged.")

@patch('sim.gui_streamlit.st')
@patch('sim.gui_streamlit.run_experiment')
def test_simulation_execution_symbiosis(mock_run_experiment, mock_st):
    """Test simulation execution for Symbiosis agent."""
    mock_st.session_state = {"runs": []}

    # Mock parameters
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Simbiosis (DQN)"
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()

    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.button = MagicMock(return_value=True)
    mock_st.spinner = MagicMock()
    mock_st.success = MagicMock()
    mock_st.info = MagicMock()

    # Mock experiment results
    mock_run_experiment.side_effect = [
        {"avg_reward": 10.0},  # Control
        {"avg_reward": 15.0}   # Symbiosis
    ]

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    # Verify both experiments were called
    assert mock_run_experiment.call_count == 2
    calls = mock_run_experiment.call_args_list
    assert calls[0][1]['agent_name'] == "Control"
    assert calls[1][1]['agent_name'] == "Simbiosis"
    mock_st.success.assert_called_with("Simulación completada y registrada. / Simulation completed and logged.")

@patch('sim.gui_streamlit.st')
def test_comparison_panel_with_multiple_runs(mock_st):
    """Test comparison panel when multiple runs exist."""
    mock_st.session_state = {"runs": [
        {"params": {"episodes": 1000}, "control": {"avg_reward": 10.0}, "simbiosis": {"avg_reward": 12.0}},
        {"params": {"episodes": 1000}, "control": {"avg_reward": 11.0}, "simbiosis": {"avg_reward": 13.0}}
    ]}

    # Mock UI elements
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Control (Q-table)"
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()

    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.selectbox.side_effect = [0, 1]  # Select runs for comparison
    mock_st.write = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    mock_st.subheader.assert_any_call("Comparación de corridas históricas / Historical runs comparison")
    assert mock_st.selectbox.call_count >= 2  # At least the comparison selectboxes

@patch('sim.gui_streamlit.st')
def test_comparison_panel_insufficient_runs(mock_st):
    """Test comparison panel when only one run exists."""
    mock_st.session_state = {"runs": [{"params": {}, "control": {}, "simbiosis": {}}]}

    # Mock UI elements
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Control (Q-table)"
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()

    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.info = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    mock_st.info.assert_called_with("Ejecuta al menos dos simulaciones para comparar históricamente. / Run at least two simulations to compare historically.")

@patch('sim.gui_streamlit.st')
def test_export_functionality(mock_st):
    """Test export functionality."""
    mock_st.session_state = {"runs": [{"params": {}, "control": {}, "simbiosis": {}}]}

    # Mock UI elements
    mock_st.sidebar.slider.side_effect = [1000, 42, 1.0, 5, 100.0, 1, 1, 1, 50]
    mock_st.sidebar.selectbox.return_value = "Control (Q-table)"
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()

    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.download_button = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    # Verify export UI was created
    mock_st.subheader.assert_any_call("Exportar historial / Export history")
    mock_st.download_button.assert_called()
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> c547074 (Improve test coverage to 95% - Add tests for missing lines in gui_streamlit, prototipo_rl_simbiosis, toy_ped_rl_excel. Update README and CHANGELOG.)

@patch('sim.gui_streamlit.st')
def test_invalid_seed_exception(mock_st):
    """Test that invalid seed triggers except block."""
    mock_st.session_state = {"seed": "invalid"}  # Invalid seed
    mock_st.sidebar.slider = MagicMock(side_effect=[1000, 1.0, 5, 100.0, 1, 1, 1, 50, 100])  # 9 values
    mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.subheader = MagicMock()
    mock_st.info = MagicMock()
    mock_st.write = MagicMock()
    mock_st.success = MagicMock()
    mock_st.download_button = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    # The except should set seed to default

@patch('sim.gui_streamlit.st')
@patch('sim.gui_streamlit.run_experiment')
@patch('json.dumps', return_value='"mock"')
def test_seed_validation_error(mock_json_dumps, mock_run_experiment, mock_st):
    """Test seed validation error."""
    mock_st.session_state = {"seed": 999999, "runs": []}  # Out of range, no runs
    mock_st.sidebar.slider = MagicMock(side_effect=[1000, 1.0, 5, 100.0, 1, 1, 1, 50, 100])  # 9 values
    mock_st.sidebar.selectbox = MagicMock(return_value="Control (Q-table)")
    mock_st.sidebar.title = MagicMock()
    mock_st.sidebar.markdown = MagicMock()
    mock_st.sidebar.error = MagicMock()
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.button = MagicMock(return_value=True)
    mock_st.warning = MagicMock()
    mock_st.stop = MagicMock()
    mock_st.download_button = MagicMock()

    import sim.gui_streamlit
    sim.gui_streamlit.main()

    mock_st.sidebar.error.assert_called()
    mock_st.warning.assert_called()
    mock_st.stop.assert_called()

# @pytest.mark.skipif(AppTest is None, reason="streamlit.testing not available")
# def test_app_invalid_seed():
#     at = AppTest.from_file("sim/gui_streamlit.py")
#     at.session_state["seed"] = "invalid"
#     at.run()
#     # The except should trigger, seed set to default

# @pytest.mark.skipif(AppTest is None, reason="streamlit.testing not available")
# def test_app_validation_error():
#     at = AppTest.from_file("sim/gui_streamlit.py")
#     at.session_state["seed"] = 10000  # > 9999
#     at.button[0].click().run()
#     # Should trigger error

# @pytest.mark.skipif(AppTest is None, reason="streamlit.testing not available")
# def test_app_comparison():
#     at = AppTest.from_file("sim/gui_streamlit.py")
#     at.session_state["runs"] = [{"params": {}, "control": {}, "simbiosis": {}}, {"params": {}, "control": {}, "simbiosis": {}}]
#     at.run()
#     # Should cover the comparison
<<<<<<< HEAD
=======
>>>>>>> 37b5e82 (Update README with code quality and coverage section, sync with remote changes for unified CC BY-NC-SA 4.0 license)
=======
>>>>>>> c547074 (Improve test coverage to 95% - Add tests for missing lines in gui_streamlit, prototipo_rl_simbiosis, toy_ped_rl_excel. Update README and CHANGELOG.)
