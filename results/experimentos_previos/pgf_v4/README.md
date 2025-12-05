# PGF v4 - Experimentos y Documentación

## Objetivo General

Validar la hipótesis de "dilución espacial" y analizar rigurosamente la contribución de cada componente del mecanismo PGF en un entorno de complejidad intermedia (grid 4x4), así como evaluar el efecto del entrenamiento extendido.


## Objetivos Específicos

1. Confirmar si el rendimiento del agente PGF v4 en grid 4x4 se sitúa entre los resultados de 3x3 y 5x5, validando la hipótesis de degradación lineal por complejidad.
	- **Hipótesis de éxito:** Esperamos un ratio de desempeño entre 60-75% (el punto medio entre el 105% de 3x3 y el 39% de 5x5). El experimento será exitoso si el resultado cae en este rango.
2. Realizar estudios de ablation desactivando componentes de la función de recompensa.
	- **Ablación A:** PGF sin Bono de Supervivencia.
	- **Ablación B:** PGF sin Bono de Progreso.
	- **Ablación C:** Solo Señal Teórica ($\kappa \cdot \delta P$).
3. Evaluar la convergencia y estabilidad del aprendizaje con entrenamientos extendidos (1000-2000 episodios).
4. Documentar y analizar todos los resultados de forma reproducible.

## Estructura de Carpetas y Archivos

- `experimentos/` : Scripts y configuraciones de cada experimento
- `resultados/`   : Archivos CSV, JSON y logs de cada corrida
- `figuras/`      : Gráficas y visualizaciones generadas
- `analisis/`     : Notebooks y scripts de análisis estadístico
- `reportes/`     : Informes parciales y finales


## Plan de Trabajo

1. **Experimento 1:** Grid 4x4, configuración estándar, 500 episodios, 3 semillas. **Incluye siempre el Agente Control en 4x4** para obtener la línea base y calcular el ratio de desempeño y el impuesto de alineación.
2. **Experimento 2:** Grid 4x4, entrenamiento extendido (1000-2000 episodios). **Incluye el Agente Control.**
3. **Experimento 3:** Estudios de ablation (desactivar componentes uno a uno, ver desglose arriba). **Incluye el Agente Control.**
4. **Análisis:** Comparar resultados con 3x3 y 5x5, graficar desempeño y varianza.
5. **Reporte:** Documentar hallazgos, limitaciones y próximos pasos.

---

**Responsable:** Jose M Rivera Garcia
**Fecha de inicio:** 2 de diciembre de 2025
