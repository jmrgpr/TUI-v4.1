# CHANGELOG

## [2025-11-13] Proveniencia y estructura de datos
- Se agrega el archivo `Cacería de sistemas inteligencia riesgo.txt` con documentación detallada de fuentes, estructura y referencias del dataset principal.
- Se actualiza el `README.md` para citar el nuevo archivo y resaltar la transparencia y trazabilidad de los datos.

## [2025-11-13] Mejoras en simuladores
- Correcciones y mejoras en los módulos de simulación (Aprendizaje Simbiótico, PED en sistemas reales, Sensibilidad de Pesos).
- Scripts y datos listos para publicación y revisión científica.


Para detalles de versiones anteriores, consulte el historial de commits en GitHub.

## [2025-11-17] Limpieza y profesionalización de resultados experimentales
- Se movieron los archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raíz a la carpeta `results/` para mejorar la trazabilidad y limpieza del workspace.
- Se eliminó el archivo temporal vacío `test_export_empty.json`.
Motivo: Estos archivos estaban en la raíz por prácticas de desarrollo y pruebas rápidas. Ahora, siguiendo la estructura profesional, se centralizan en `results/`.