## Registro de corrección y aprendizaje

**Fecha:** 26/11/2025

**Cambio realizado:**
Se corrigió el script de consolidación para incluir los resultados del agente personalizado `tui`, que no estaban siendo integrados en los archivos maestros. Antes, solo se consolidaban los agentes SOTA (`ppo_sota`, `a2c_sota`, `dqn_sota`). Ahora, el archivo `master_results_tui.csv` contiene los resultados completos de `tui` junto a los agentes de control y referencia.

**Motivo:**
El propósito del experimento es comparar el desempeño del agente `tui` frente a los SOTA y agentes de control bajo diferentes riesgos. Al no aparecer en los resultados consolidados, el análisis y la trazabilidad eran incompletos y el objetivo principal no se cumplía.

**Lección aprendida:**
Siempre validar que los scripts de consolidación incluyan todos los agentes relevantes. Revisar los patrones de búsqueda y los nombres de los archivos para evitar exclusiones involuntarias. Documentar cada corrección y su causa para mejorar la reproducibilidad y el aprendizaje del equipo.
# Experimento2 Reestructurado

Esta carpeta contiene la nueva version del experimento 2, aplicando las mejores practicas y lecciones aprendidas del proceso anterior.

## Objetivos
- Mantener referencias claras a los datos y scripts originales.
- Documentar todos los pasos, decisiones y problemas resueltos.
- Garantizar que los notebooks y scripts sean robustos y reproducibles.
- Evitar errores previos en graficos y tablas (validacion de columnas, chequeo de datos antes de visualizar).

## Estructura
- `data/` : Resultados nuevos y enlaces a los originales.
- `notebooks/` : Notebooks con celdas documentadas y robustas.
- `scripts/` : Scripts ajustados y documentados.
- `referencias/` : Resumenes y enlaces a los archivos clave de Experimento2.

## Referencias
- Experimento original: `results/Experimento2/`
- Notebook original: `results/Experimento2/analisis_experimento2.ipynb`
- Informe previo: `results/Experimento2/informe_resumen_exp2.md`

## Lecciones aprendidas
- Validar siempre las columnas y tipos de datos antes de graficar.
- Documentar cada paso y decision en el notebook.
- Mantener trazabilidad entre versiones y resultados.

---

## Log de validacion y ajustes de rutas
- Scripts y notebooks revisados para que las salidas se escriban exclusivamente en `experimento2-reestructurado/`.
- `run_sota_a2c_dqn.py` apunta a `experimento2-reestructurado/data/sota/`.
- El pipeline principal debe lanzarse con `--output_base experimento2-reestructurado/data/sweep/fase2_full`.
- `consolidar_master.py` usa glob recursivo y filtra `episodes == 1000` para generar masters en `experimento2-reestructurado/data/`.
- No se usan variables de entorno para rutas; todo esta explicito en los scripts.
- Validado: ningun resultado nuevo caera en `results/` si se usan los comandos indicados.

---

## Problemas historicos del Experimento 2 original y soluciones
- Mezcla de runs smoke (100 ep) y full (1000): eliminado; solo runs de 1000 en sweep y SOTA.
- Artefactos dispersos en `results/`: ahora todo esta en la carpeta reestructurada.
- Consolidacion incompleta: glob recursivo y filtro de episodios=1000 para incluir todos los CSV relevantes.
- SOTA fuera de la estructura: SOTA escribe en la carpeta reestructurada por defecto.
- Notebook fragil: notebooks nuevos validan columnas reales (`agent`, `risk_scale`, `reward`, `tripwires`) y rutas locales.
- Documentacion dispersa: README, indice de referencias e informe actualizados y centralizados.

---

## Diferencias clave (original vs reestructurado)
1. Ubicacion: original disperso en `results/`; reestructurado todo en `experimento2-reestructurado/`.
2. Limpieza: original con smoke+full mezclados; reestructurado solo full, masters limpios.
3. Consolidacion: original parcial; reestructurado con glob recursivo y filtro episodios=1000.
4. Notebook: original roto; reestructurado robusto y alineado a las columnas reales.
5. Documentacion: original dispersa; reestructurado centralizada y clara.

---

**Esta carpeta servira como base limpia para la comparativa final y futuras auditorias.**
