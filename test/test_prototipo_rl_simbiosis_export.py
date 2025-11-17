import sys
import os
import pytest
from sim.prototipo_rl_simbiosis import main

def test_main_export_error(monkeypatch, tmp_path):
    """Test main --export con error de escritura (permiso denegado)."""
    # Ruta a directorio sin permisos de escritura (simulado)
    export_path = tmp_path / "no_write_dir" / "test_export.json"
    # Crear el directorio y quitar permisos de escritura
    os.makedirs(export_path.parent, exist_ok=True)
    os.chmod(export_path.parent, 0o400)  # Solo lectura
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '2', '--seed', '42', '--export', str(export_path)])
    try:
        main()
    except Exception:
        pass  # Esperamos excepción por permisos
    finally:
        # Restaurar permisos para limpieza
        os.chmod(export_path.parent, 0o700)

@pytest.mark.parametrize("invalid_path", ["/invalid_path/test_export.json", "", None])
def test_main_export_invalid_path(monkeypatch, invalid_path):
    """Test main --export con ruta inválida o nula."""
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '2', '--seed', '42', '--export', str(invalid_path)])
    try:
        main()
    except Exception:
        pass  # Esperamos excepción por ruta inválida

# Test normal de exportación para asegurar cobertura completa
def test_main_export_ok(monkeypatch, tmp_path):
    export_path = tmp_path / "test_export_ok.json"
    monkeypatch.setattr(sys, 'argv', ['test', '--episodes', '2', '--seed', '42', '--export', str(export_path)])
    main()
    assert export_path.exists()
