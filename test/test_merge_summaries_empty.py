import runpy
from pathlib import Path
from scripts import merge_summaries


def test_merge_summaries_empty(tmp_path):
    out = tmp_path / "out.csv"
    # Sin archivos summary, debe crear CSV vacío sin fallar
    merge_summaries.merge_summaries(str(tmp_path), str(out))
    assert out.exists()


def test_merge_summaries_main_no_files(monkeypatch, tmp_path):
    monkeypatch.setattr(merge_summaries.glob, "glob", lambda pattern: [])
    monkeypatch.setattr(merge_summaries, "merge_summaries", lambda *a, **k: None)
    runpy.run_path(str(Path("scripts/merge_summaries.py")), run_name="__main__")

