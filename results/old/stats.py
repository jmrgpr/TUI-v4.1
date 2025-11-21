import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings

# Suprimir warnings de convergencia si los datos son muy limpios
warnings.filterwarnings("ignore")

def analyze_results(csv_path='results/fase2_global_summary.csv'):
    print("=== TUI v4.1 Statistical Analysis (ANOVA & Tukey) ===\n")
    
    # 1. Carga de Datos
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {csv_path}")
        return

    # Métricas clave a evaluar
    metrics = ['avg_pgf_bruto', 'avg_pgf_neto', 'avg_pgf_costo', 'avg_reward', 'avg_tripwire']

    for metric in metrics:
        print(f"\n{'='*60}")
        print(f"METRIC: {metric}")
        print(f"{'='*60}")

        # 2. ANOVA Two-Way (Agente + Risk_Scale + Interacción)
        # Pregunta: ¿Influye el Agente? ¿Influye el Riesgo? ¿Influye la combinación?
        model = ols(f'{metric} ~ C(agent) + C(risk_scale) + C(agent):C(risk_scale)', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        print("\n>>> Two-Way ANOVA Results:")
        print(anova_table)
        
        p_agent = anova_table.loc['C(agent)', 'PR(>F)']
        p_inter = anova_table.loc['C(agent):C(risk_scale)', 'PR(>F)']

        # Interpretación Automática
        if p_agent < 0.05:
            print(f"\n✅ EFFECT FOUND: The agent type significantly affects {metric} (p={p_agent:.4f}).")
        else:
            print(f"\n❌ NO EFFECT: Agent type does not change {metric} significantly.")

        if p_inter < 0.05:
            print(f"✅ INTERACTION FOUND: Agents respond differently to changing risk levels (p={p_inter:.4f}).")
            print("   (This supports the 'Risk Tension' hypothesis if specific to PGF metrics)")

        # 3. Análisis Post-Hoc (Tukey) por nivel de riesgo
        # Si hay diferencias, ¿quién gana en cada nivel?
        print(f"\n>>> Detailed Post-Hoc Analysis (Tukey HSD) per Risk Level:")
        
        for risk in sorted(df['risk_scale'].unique()):
            subset = df[df['risk_scale'] == risk]
            tukey = pairwise_tukeyhsd(endog=subset[metric], groups=subset['agent'], alpha=0.05)
            
            # Solo mostramos si hay rechazo de H0 (diferencia significativa) para no llenar la pantalla
            if tukey.reject.any():
                print(f"\n  [Risk Scale {risk}] Significant differences found:")
                print(tukey.summary())
            else:
                print(f"  [Risk Scale {risk}] No significant differences between agents.")

if __name__ == "__main__":
    analyze_results()