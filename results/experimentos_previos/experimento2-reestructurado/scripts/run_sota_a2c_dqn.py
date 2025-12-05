# Script para ejecutar SOTA A2C/DQN con overrides por entorno
# Documenta cómo ejecutar y modificar parámetros

import argparse

def main():
    parser = argparse.ArgumentParser(description='Run SOTA A2C/DQN experiment')
    parser.add_argument('--env', type=str, required=True, help='Nombre del entorno')
    parser.add_argument('--risk', type=float, default=1.0, help='Nivel de riesgo')
    parser.add_argument('--episodes', type=int, default=1000, help='Número de episodios')
    parser.add_argument('--output_dir', type=str, default='experimento2-reestructurado/data/sota/', help='Directorio de salida para resultados SOTA')
    args = parser.parse_args()
    OUTPUT_DIR = args.output_dir
    print(f'Ejecutando SOTA en entorno {args.env} con riesgo {args.risk} y {args.episodes} episodios')
    print(f'Resultados se guardarán en: {OUTPUT_DIR}')
    # Aquí iría la lógica de entrenamiento y evaluación, asegurando que los resultados se escriban en OUTPUT_DIR

if __name__ == '__main__':
    main()
