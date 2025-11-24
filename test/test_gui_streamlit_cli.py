# Tests de cobertura para sim/gui_streamlit_cli.py
from unittest.mock import patch, MagicMock
import sim.gui_streamlit_cli as gui


@patch("sim.gui_streamlit_cli.pd.read_csv")
@patch("sim.gui_streamlit_cli.Path")
def test_render_results_preview_error(mock_path, mock_read_csv):
    mock_path.return_value.exists.return_value = True
    mock_read_csv.side_effect = Exception("CSV error")
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.markdown = MagicMock()
        mock_st.write = MagicMock()
        mock_st.warning = MagicMock()
        gui.render_results_preview()
        assert mock_st.warning.called


@patch("sim.gui_streamlit_cli.run_command_live")
def test_cli_mode_all_param_types(mock_run_command_live):
    mock_run_command_live.return_value = True
    params = {
        "int_param": {"type": "int", "default": 1, "label": "Int", "flag": "--int"},
        "float_param": {"type": "float", "default": 1.5, "label": "Float", "flag": "--float"},
        "bool_param": {"type": "bool", "default": True, "label": "Bool", "flag": "--bool"},
        "list_param": {"type": "list", "default": "a,b", "label": "List", "flag": "--list"},
        "str_param": {"type": "str", "default": "text", "label": "Str", "flag": "--str"},
    }
    with patch("sim.gui_streamlit_cli.get_script_params", return_value=params):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.selectbox.return_value = "run_full_experiment.py"
            mock_st.form = MagicMock()
            mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
            mock_st.form_submit_button.return_value = True
            mock_st.number_input = MagicMock(return_value=1)
            mock_st.checkbox = MagicMock(return_value=True)
            mock_st.text_input = MagicMock(return_value="a,b")
            mock_st.code = MagicMock()
            mock_st.balloons = MagicMock()
            gui.render_cli_mode()
            mock_run_command_live.assert_called()


@patch("sim.gui_streamlit_cli.run_command_live")
def test_cli_mode_edge_values(mock_run_command_live):
    mock_run_command_live.return_value = True
    params = {
        "int_param": {"type": "int", "default": 0, "label": "Int", "flag": "--int"},
        "list_param": {"type": "list", "default": "", "label": "List", "flag": "--list"},
    }
    with patch("sim.gui_streamlit_cli.get_script_params", return_value=params):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.selectbox.return_value = "run_full_experiment.py"
            mock_st.caption = MagicMock()
            mock_st.form = MagicMock()
            mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
            mock_st.form_submit_button.return_value = True
            mock_st.number_input = MagicMock(return_value=0)
            mock_st.text_input = MagicMock(return_value="")
            mock_st.code = MagicMock()
            mock_st.balloons = MagicMock()
            gui.render_cli_mode()
            mock_run_command_live.assert_called()


@patch("sim.gui_streamlit_cli.run_experiment")
def test_toy_model_error(mock_run_experiment):
    mock_run_experiment.side_effect = Exception("Toy error")
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.header = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.slider = MagicMock(return_value=100)
        mock_st.number_input = MagicMock(return_value=42)
        mock_st.checkbox = MagicMock(return_value=True)
        mock_st.button = MagicMock(return_value=True)
        mock_st.spinner = MagicMock()
        mock_st.error = MagicMock()
        gui.render_toy_mode()
        assert mock_st.error.called


def test_import_gui_streamlit_cli():
    try:
        import sim.gui_streamlit_cli  # noqa: F401
    except Exception as e:
        assert False, f"Error al importar GUI CLI: {e}"


@patch("sim.gui_streamlit_cli.run_command_live")
def test_cli_execution_success(mock_run_command_live):
    mock_run_command_live.return_value = True
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.sidebar.radio.return_value = "dYs? Ejecutor de Experimentos (CLI)"
        mock_st.selectbox.return_value = "run_full_experiment.py"
        mock_st.form_submit_button.return_value = True
        mock_st.code = MagicMock()
        gui.render_cli_mode()
        mock_run_command_live.assert_called()


@patch("sim.gui_streamlit_cli.run_command_live")
def test_cli_execution_failure(mock_run_command_live):
    mock_run_command_live.return_value = False
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.sidebar.radio.return_value = "dYs? Ejecutor de Experimentos (CLI)"
        mock_st.selectbox.return_value = "run_full_experiment.py"
        mock_st.form_submit_button.return_value = True
        mock_st.code = MagicMock()
        gui.render_cli_mode()
        mock_run_command_live.assert_called()


@patch("sim.gui_streamlit_cli.load_experiment_spec")
@patch("sim.gui_streamlit_cli.extract_argparse_params")
def test_loader_hibrido_spec(mock_extract, mock_load):
    mock_load.return_value = {"params": {"test_mode": {"type": "bool", "default": False, "flag": "--test"}}}
    mock_extract.return_value = {}
    params = gui.get_script_params("run_ablation_quick.py")
    assert "test_mode" in params

    mock_load.return_value = None
    mock_extract.return_value = {"episodes": {"type": "int", "default": 200, "flag": "--episodes"}}
    params = gui.get_script_params("run_search_pgf.py")
    assert "episodes" in params


@patch("sim.gui_streamlit_cli.pd.read_csv")
@patch("sim.gui_streamlit_cli.Path")
def test_render_results_preview(mock_path, mock_read_csv):
    mock_path.return_value.exists.return_value = True
    mock_read_csv.return_value = MagicMock()
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.markdown = MagicMock()
        mock_st.write = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.download_button = MagicMock()
        gui.render_results_preview()
        assert mock_st.dataframe.called

    mock_path.return_value.exists.return_value = False
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.info = MagicMock()
        gui.render_results_preview()
        assert mock_st.info.called


def test_render_results_preview_download_error(tmp_path):
    csv_file = tmp_path / "master_results.csv"
    csv_file.write_text("a,b\n1,2\n", encoding="utf-8")
    with patch("sim.gui_streamlit_cli.pd.read_csv", return_value=MagicMock()):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.markdown = MagicMock()
            mock_st.write = MagicMock()
            mock_st.dataframe = MagicMock()
            mock_st.download_button = MagicMock(side_effect=Exception("boom"))
            mock_st.warning = MagicMock()
            gui.render_results_preview(csv_path=str(csv_file))
            assert mock_st.warning.called


def test_load_experiment_spec_reads_spec(tmp_path):
    script = tmp_path / "dummy.py"
    script.write_text("EXPERIMENT_SPEC = {'params': {'x': 1}}", encoding="utf-8")
    result = gui.load_experiment_spec(str(script))
    assert result == {"params": {"x": 1}}


def test_load_experiment_spec_exception(monkeypatch):
    monkeypatch.setattr("builtins.open", MagicMock(side_effect=IOError("boom")))
    assert gui.load_experiment_spec("any") is None


def test_extract_argparse_params_exception():
    # Archivo inexistente provoca la ruta de excepcion y devuelve {}.
    assert gui.extract_argparse_params("nonexistent_file.py") == {}


def test_run_command_live_success_and_failure(monkeypatch):
    class FakeStdout:
        def __init__(self, lines):
            self._iter = iter(lines)

        def readline(self):
            return next(self._iter, "")

        def close(self):
            pass

    class FakePopen:
        def __init__(self, lines, rc):
            self.stdout = FakeStdout(lines)
            self._rc = rc

        def wait(self):
            return self._rc

    calls = []

    def fake_popen(cmd, **kwargs):
        calls.append(cmd)
        return FakePopen(["line1\n", "line2\n"], rc=0)

    with patch("sim.gui_streamlit_cli.subprocess.Popen", side_effect=fake_popen):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.info = MagicMock()
            mock_st.expander = MagicMock()
            mock_st.expander.return_value.__enter__.return_value = None
            mock_st.empty = MagicMock()
            mock_st.empty.return_value.code = MagicMock()
            mock_st.success = MagicMock()
            assert gui.run_command_live(["echo", "ok"]) is True
            mock_st.success.assert_called()

    def failing_popen(cmd, **kwargs):
        return FakePopen([], rc=1)

    with patch("sim.gui_streamlit_cli.subprocess.Popen", side_effect=failing_popen):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.info = MagicMock()
            mock_st.expander = MagicMock()
            mock_st.expander.return_value.__enter__.return_value = None
            mock_st.empty = MagicMock()
            mock_st.empty.return_value.code = MagicMock()
            mock_st.error = MagicMock()
            assert gui.run_command_live(["echo", "fail"]) is False
            mock_st.error.assert_called()

    with patch("sim.gui_streamlit_cli.subprocess.Popen", side_effect=Exception("explode")):
        with patch("sim.gui_streamlit_cli.st") as mock_st:
            mock_st.info = MagicMock()
            mock_st.expander = MagicMock()
            mock_st.expander.return_value.__enter__.return_value = None
            mock_st.empty = MagicMock()
            mock_st.empty.return_value.code = MagicMock()
            mock_st.error = MagicMock()
            assert gui.run_command_live(["echo", "explode"]) is False
            mock_st.error.assert_called()


@patch("sim.gui_streamlit_cli.run_experiment")
def test_toy_model_execution(mock_run_experiment):
    mock_run_experiment.return_value = {"avg_reward": 10.0, "total_rewards": [1, 2, 3]}
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.header = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.slider = MagicMock(return_value=100)
        mock_st.number_input = MagicMock(return_value=42)
        mock_st.checkbox = MagicMock(return_value=True)
        mock_st.button = MagicMock(return_value=True)
        mock_st.spinner = MagicMock()
        mock_st.metric = MagicMock()
        mock_st.line_chart = MagicMock()
        gui.render_toy_mode()
        assert mock_st.metric.called
        assert mock_st.line_chart.called

    mock_run_experiment.side_effect = Exception("Sim error")
    with patch("sim.gui_streamlit_cli.st") as mock_st:
        mock_st.header = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.slider = MagicMock(return_value=100)
        mock_st.number_input = MagicMock(return_value=42)
        mock_st.checkbox = MagicMock(return_value=True)
        mock_st.button = MagicMock(return_value=True)
        mock_st.spinner = MagicMock()
        mock_st.error = MagicMock()
        gui.render_toy_mode()
        assert mock_st.error.called
