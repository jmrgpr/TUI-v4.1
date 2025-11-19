import pandas as pd
import matplotlib.pyplot as plt
import os

# Datos manuales extraídos de los CSVs de resumen
# Formato: [config, seed, success_total, success_last_100, first_success]
data = [
    ["A_curriculum", 42, 0.613, 0.87, 1],
    ["B_direct_8x8", 13, 0.659, 0.98, 199],
    ["B_direct_8x8", 42, 0.643, 0.95, 2],
    ["B_direct_8x8", 101, 0.713, 0.60, 3],
    ["B_direct_8x8", 2025, 0.744, 0.85, 10],
    ["B_direct_8x8", 9999, 0.763, 0.90, 26],
    ["C_inverse", 42, 0.552, 0.54, 64],
    ["C_inverse", 101, 0.536, 0.46, 13],
    ["C_inverse", 2025, 0.583, 0.95, 46],
    ["C_inverse", 9999, 0.23, 0.83, 714],
    ["D_only_6x6", 13, 0.629, 0.54, 21],
    ["D_only_6x6", 42, 0.589, 0.83, 10],
    ["D_only_6x6", 101, 0.549, 0.79, 2],
    ["D_only_6x6", 2025, 0.68, 0.88, 29],
    ["D_only_6x6", 9999, 0.621, 0.87, 23],
]
df = pd.DataFrame(data, columns=["config", "seed", "success_total", "success_last_100", "first_success"])

os.makedirs("plots/FASE1", exist_ok=True)

# Gráfico 1: Éxito total por configuración y semilla
plt.figure(figsize=(10,6))
for config in df["config"].unique():
    subset = df[df["config"] == config]
    plt.plot(subset["seed"], subset["success_total"], marker='o', label=config)
plt.title("Éxito total por configuración y semilla")
plt.xlabel("Seed")
plt.ylabel("Éxito total")
plt.legend()
plt.grid(True)
plt.savefig("plots/FASE1/exito_total_por_configuracion.png")
plt.close()

# Gráfico 2: Éxito últimos 100 episodios
plt.figure(figsize=(10,6))
for config in df["config"].unique():
    subset = df[df["config"] == config]
    plt.plot(subset["seed"], subset["success_last_100"], marker='o', label=config)
plt.title("Éxito últimos 100 episodios por configuración y semilla")
plt.xlabel("Seed")
plt.ylabel("Éxito últimos 100")
plt.legend()
plt.grid(True)
plt.savefig("plots/FASE1/exito_ultimos100_por_configuracion.png")
plt.close()

# Gráfico 3: Primer éxito por configuración y semilla
plt.figure(figsize=(10,6))
for config in df["config"].unique():
    subset = df[df["config"] == config]
    plt.plot(subset["seed"], subset["first_success"], marker='o', label=config)
plt.title("Primer éxito por configuración y semilla")
plt.xlabel("Seed")
plt.ylabel("Primer éxito (episodio)")
plt.legend()
plt.grid(True)
plt.savefig("plots/FASE1/primer_exito_por_configuracion.png")
plt.close()

print("Gráficos generados en plots/FASE1/")
