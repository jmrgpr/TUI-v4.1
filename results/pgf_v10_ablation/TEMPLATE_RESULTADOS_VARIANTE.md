# TEMPLATE_RESULTADOS_VARIANTE.md

## Resultados – Variante: <nombre_variante>

### Resumen de configuración
- Describir aquí los componentes activos/inactivos y los hiperparámetros relevantes para la variante.
- Ejemplo: "Sin shaping, sin transfer, learning rate=0.0005, gamma=0.99, ..."

### Seeds ejecutadas
- Listar las seeds utilizadas (ejemplo: 13, 42)

### Tabla de métricas por seed
| Seed | success_last_100 | success_rate_total | gate | gate_passed | first_success_episode | convergence_episode | CSV fuente |
|------|------------------|--------------------|------|-------------|----------------------|--------------------|------------|
|      |                  |                    |      |             |                      |                    |            |

### Ejemplo de extracción
- Para obtener `success_last_100` de la seed 13:
  - Archivo: `<ruta_al_csv>`
  - Columna: `success_last_100`

### Interpretación
- Comparar con baseline v10 y otras variantes.
- Documentar cualquier hallazgo relevante.

---

*Plantilla de resultados para variantes de Fase 2. Revisión: 2025-12-05.*
