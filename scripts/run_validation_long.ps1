# Script de validación larga: 1000 episodios × 3 seeds
# Valida robustez estadística de pgf_mix=0.2 post smoke-test fix
# Fecha: 2025-12-01

Write-Host "=== TUI v4.2 - Validación Estadística Robusta ===" -ForegroundColor Cyan
Write-Host "Configuración: 1000 episodios × 3 seeds (42, 123, 456)" -ForegroundColor Yellow
Write-Host "Objetivo: Confirmar convergencia y estabilidad con pgf_mix=0.2" -ForegroundColor Yellow
Write-Host ""

$seeds = @(42, 123, 456)
$episodes = 1000
$grid_size = 3
$risk_scale = 0.5

foreach ($seed in $seeds) {
    Write-Host "--- Ejecutando seed $seed ---" -ForegroundColor Green
    
    # Run con configuración validada (pgf_mix=0.2 por default ahora)
    python sim/prototipo_rl_simbiosis.py `
        --episodes $episodes `
        --seed $seed `
        --grid_size $grid_size `
        --risk_scale $risk_scale `
        --tui_only `
        --output_prefix "results/validation_long/pgf02_seed${seed}"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR en seed $seed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Seed $seed completado" -ForegroundColor Green
    Write-Host ""
}

Write-Host "=== Validación completada ===" -ForegroundColor Cyan
Write-Host "Analizar resultados en: results/validation_long/" -ForegroundColor Yellow
Write-Host ""
Write-Host "Próximo paso: Ejecutar análisis comparativo" -ForegroundColor Magenta
Write-Host "  python scripts/analyze_validation_long.py" -ForegroundColor Gray
