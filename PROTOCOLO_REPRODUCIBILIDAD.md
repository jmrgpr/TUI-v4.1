# Protocolo de reproducibilidad científica / Scientific Reproducibility Protocol

Este documento describe los pasos y requisitos para reproducir los resultados principales del proyecto TUI-v4.1, siguiendo estándares internacionales de auditoría científica.

## Requisitos / Requirements
- Python 3.8+
- Sistema operativo: Windows, Linux o MacOS
- Dependencias listadas y pinneadas en `requirements.txt`
- GPU opcional para acelerar entrenamiento (CUDA compatible)

## Pasos para reproducir / Steps to reproduce

### 1. Clonar el repositorio / Clone the repository
```bash
git clone https://github.com/jmrgpr/TUI-v4.1.git
cd TUI-v4.1
```

### 2. Crear y activar entorno virtual / Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/MacOS
source .venv/bin/activate
```

### 3. Instalar dependencias / Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Ejecutar experimentos principales / Run main experiments
```bash
python run_fase2.py
```
Resultados en `results/fase2/`.

### 5. Unir resúmenes / Merge summaries
```bash
python merge_summaries.py
```
Archivo final: `results/fase2_global_summary.csv`

### 6. Generar gráficos automáticos / Generate automatic plots
```bash
jupyter notebook notebooks/quickstart_graficos.ipynb
```

### 7. Validar resultados / Validate results
- Comparar métricas y gráficos generados con los publicados en Zenodo y el README.
- Revisar logs y archivos exportados en `results/`.

## Auditoría y checklist / Audit & checklist
- [x] Código y datos versionados y con DOI Zenodo
- [x] Dependencias pinneadas
- [x] Scripts y notebooks reproducibles
- [x] Resultados exportados en formatos estándar (CSV, JSON, PNG)
- [x] Cobertura de tests >99%
- [x] Documentación bilingüe
- [x] Licencias claras y actualizadas

## Contacto / Contact
Para dudas o problemas de reproducibilidad: jmrgpr@gmail.com

---

This document describes the steps and requirements to reproduce the main results of the TUI-v4.1 project, following international scientific audit standards.

## Requirements
- Python 3.8+
- OS: Windows, Linux or MacOS
- Dependencies listed and pinned in `requirements.txt`
- Optional GPU for faster training (CUDA compatible)

## Steps to reproduce

### 1. Clone the repository
```bash
git clone https://github.com/jmrgpr/TUI-v4.1.git
cd TUI-v4.1
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/MacOS
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run main experiments
```bash
python run_fase2.py
```
Results in `results/fase2/`.

### 5. Merge summaries
```bash
python merge_summaries.py
```
Final file: `results/fase2_global_summary.csv`

### 6. Generate automatic plots
```bash
jupyter notebook notebooks/quickstart_graficos.ipynb
```

### 7. Validate results
- Compare metrics and generated plots with those published in Zenodo and the README.
- Review logs and exported files in `results/`.

## Audit & checklist
- [x] Code and data versioned and Zenodo DOI
- [x] Pinned dependencies
- [x] Reproducible scripts and notebooks
- [x] Results exported in standard formats (CSV, JSON, PNG)
- [x] Test coverage >99%
- [x] Bilingual documentation
- [x] Clear and updated licenses

## Contact
For reproducibility questions or issues: jmrgpr@gmail.com
