

# FASE1_DOCUMENTACION_REPRODUCIBILIDAD.md

## Resumen Ejecutivo
Este documento describe, paso a paso y con trazabilidad total, cómo reproducir y validar todos los resultados, análisis y gráficos de la ablation FASE 1 (TUI-v4.1). Incluye rutas, scripts, dependencias, advertencias y validación cruzada.

## Estructura de Carpetas y Archivos Clave
| Carpeta/Archivo | Descripción |
|-----------------|-------------|
| `results/pgf_v10_ablation/` | Carpeta raíz de la ablation v10, contiene todo el experimento |
| `config_A_curriculum/`, ... | Resultados por configuración y semilla |
| `plots/FASE1/` | Gráficos PNG generados automáticamente (se crea al correr el script) |
| `REPORTE_ABLATION_v10.md` | Reporte final detallado y comparativo |
| `PREREGISTRO_ABLATION_v10.md` | Prerregistro y protocolo experimental |
| `scripts/` | Scripts de ejecución y análisis |

## Pasos para Reproducibilidad Total
1. **Clonar el repositorio y crear entorno:**
	- `git clone <URL del repo>`
	- `cd TUI-v4.1`
	- `python -m venv .venv && .venv/Scripts/activate`
	- `pip install -r requirements.txt`
2. **Ejecución de experimentos:**
	- Ejecutar los scripts de runners en `scripts/` para cada configuración y semilla. Ejemplo:
	  - `python scripts/run_ablation_A_curriculum_baseline.py --seed 42`
	  - `python scripts/run_ablation_B_direct_8x8.py --seed 13`
	- Los resultados se guardan automáticamente en subcarpetas por configuración y semilla.
3. **Generación de gráficos:**
	- `python scripts/generar_graficos_fase1.py`
	- Los PNGs se guardan en `plots/FASE1/` (se crea si no existe).
4. **Análisis estadístico y reporte:**
	- Consultar `REPORTE_ABLATION_v10.md` para tablas, estadísticas y conclusiones.
	- Todos los datos crudos están en los CSVs de cada semilla/configuración (ver tabla de fuentes en el reporte exhaustivo).
5. **Validación cruzada:**
	- Verificar que los promedios y desviaciones estándar del reporte coincidan con los CSVs.
	- Revisar que los gráficos reflejen los datos tabulados.

## Control de Residuos y Limpieza
- Antes de cada ejecución, eliminar resultados previos solo si es necesario y con precaución. Ejemplo seguro para una configuración:
  - `Remove-Item -Path "results/pgf_v10_ablation/config_B_direct_8x8/seeds/seed_0013" -Recurse -Force`
- No quedan archivos temporales ni logs fuera de las carpetas designadas.

## Dependencias y Versiones
- Python 3.11.9 (verificado en `.venv`)
- Paquetes: `matplotlib`, `pandas`, `numpy` (ver `requirements.txt`)
- Scripts y rutas validados a 2025-12-05

## Referencias Cruzadas
- Protocolo y preregistro: `PREREGISTRO_ABLATION_v10.md`
- Reporte final: `REPORTE_ABLATION_v10.md`
- Gráficos: `plots/FASE1/`
- Datos crudos: subcarpetas de cada configuración (ver tabla de fuentes en el reporte exhaustivo)

## Notas Finales
- Cualquier usuario puede replicar el análisis y obtener los mismos resultados siguiendo este documento.
- La trazabilidad, limpieza y reproducibilidad están garantizadas y validadas.

---

*Documento actualizado al estándar científico y de reproducibilidad más estricto. Revisión: 2025-12-05.*
