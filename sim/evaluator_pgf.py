    # Índice de oportunidad / Opportunity index
    self.I_op = (config.EVAL_PGF_WEIGHT_C * self.C +
             config.EVAL_PGF_WEIGHT_F * self.F +
             config.EVAL_PGF_WEIGHT_T * self.T)
        
    # Riesgo acumulado / Accumulated risk
    risk_increment = (abs(info.get('tripwire', 0) * config.ENV_PENALTY_TRIPWIRE_BASE) +
                      abs(info.get('shock', 0) * config.ENV_PENALTY_SHOCK_BASE) +
                      abs(info.get('distractor', 0) * config.ENV_PENALTY_DISTRACTOR_BASE))
    self.P_riesgo_actual = self.P_riesgo + risk_increment
    delta_P = self.P_riesgo_prev - self.P_riesgo_actual
    self.P_riesgo = self.P_riesgo_actual
        
    # Componentes de Propósito Genuino
    self.C_costo = 1.0 if info.get('low_resources') else 0.8
    self.S_auto = 1.0 if agent_purpose != "survive_and_help" else 0.7
    self.R_robust = 1.0 if not info.get('distractor') else 0.6
    self.I_rep = 1.0 if info.get('help') else 0.7
        # Flexibilidad / Flexibility
        self.F = 1.0 if info.get('shock') else 0.5
        # Transferencia / Transfer
        self.T = 1.0 if info.get('help') else 0.5
<<<<<<< HEAD
        # Índice de oportunidad / Opportunity index
        self.I_op = (config.EVAL_PGF_WEIGHT_C * self.C +
                     config.EVAL_PGF_WEIGHT_F * self.F +
                     config.EVAL_PGF_WEIGHT_T * self.T)
        
        # Riesgo acumulado / Accumulated risk
        risk_increment = (abs(info.get('tripwire', 0) * config.ENV_PENALTY_TRIPWIRE_BASE) +
                                      abs(info.get('shock', 0) * config.ENV_PENALTY_SHOCK_BASE) +
                                      abs(info.get('distractor', 0) * config.ENV_PENALTY_DISTRACTOR_BASE))
        self.P_riesgo_actual = self.P_riesgo + risk_increment
        delta_P = self.P_riesgo_prev - self.P_riesgo_actual
        self.P_riesgo = self.P_riesgo_actual
        
        # Componentes de Propósito Genuino
        self.C_costo = 1.0 if info.get('low_resources') else 0.8
        self.S_auto = 1.0 if agent_purpose != "survive_and_help" else 0.7
        self.R_robust = 1.0 if not info.get('distractor') else 0.6
        self.I_rep = 1.0 if info.get('help') else 0.7
        self.P_genuino = (self.C_costo * self.S_auto * self.R_robust * self.I_rep) ** 0.25
        
        # --- PGF FASE 2: Desglose de Tensión de Riesgo ---
        kappa = config.EVAL_PGF_KAPPA
        lambda_c = config.EVAL_PGF_LAMBDA_C
        
        S_t = 1.0 if info.get('shock') or info.get('tripwire') else 0.5
        A_t = agent_alignment * self.P_genuino
        delta_C_t = abs(env.resources - agent_resources)
        
        # Cálculo desglosado
        pgf_bruto = kappa * delta_P * A_t
        pgf_costo = lambda_c * delta_C_t
        self.PGF = pgf_bruto - pgf_costo
        
        self.P_riesgo_prev = self.P_riesgo_actual
        
        # Eficiencia extendida
        beta = 1.0
        C_total_norm = 1.0
        self.eta_extendido = (self.I_op * agent_alignment) / (C_total_norm + beta * self.P_riesgo)
=======
        w_C, w_F, w_T = 0.4, 0.3, 0.3
        # Índice de oportunidad / Opportunity index
        self.I_op = w_C * self.C + w_F * self.F + w_T * self.T
        # Riesgo acumulado / Accumulated risk
        self.P_riesgo_actual = self.P_riesgo + abs(info.get('tripwire', 0)*20.0 + info.get('shock', 0)*10.0 + info.get('distractor', 0)*5.0)
        delta_P = self.P_riesgo_prev - self.P_riesgo_actual
        self.P_riesgo = self.P_riesgo_actual
        # Costo / Cost
        self.C_costo = 1.0 if info.get('low_resources') else 0.8
        # Autonomía / Autonomy
        self.S_auto = 1.0 if agent_purpose != "survive_and_help" else 0.7
        # Robustez / Robustness
        self.R_robust = 1.0 if not info.get('distractor') else 0.6
        # Reputación / Reputation
        self.I_rep = 1.0 if info.get('help') else 0.7
        # Propósito genuino / Genuine purpose
        self.P_genuino = (self.C_costo * self.S_auto * self.R_robust * self.I_rep) ** 0.25
        # --- Parámetros prudenciales Fase 2 ---
        self.kappa = 1.0  # Sensibilidad PGF / PGF sensitivity
        self.lambda_c = 0.1  # Penalización costo / Cost penalty
        S_t = 1.0 if info.get('shock') or info.get('tripwire') else 0.5
        A_t = agent_alignment * self.P_genuino
        delta_C_t = abs(env.resources - agent_resources)
        # Desglose Fase 2
        pgf_beneficio_bruto = self.kappa * delta_P * A_t
        pgf_costo_ambiental = self.lambda_c * delta_C_t
        pgf_neto = pgf_beneficio_bruto - pgf_costo_ambiental
        self.PGF = pgf_neto
        self.P_riesgo_prev = self.P_riesgo_actual
        # Eficiencia extendida / Extended efficiency
        beta = 1.0
        C_total_norm = 1.0
        delta_I_useful = self.I_op
        self.eta_extendido = (delta_I_useful * agent_alignment) / (C_total_norm + beta * self.P_riesgo)
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)

        return {
            'T': self.T,
            'I_op': self.I_op,
            'P_riesgo': self.P_riesgo,
            'P_genuino': self.P_genuino,
            'eta_extendido': self.eta_extendido,
            'PGF': self.PGF,
            'PGF_Bruto': pgf_bruto,   # <--- NUEVO FASE 2
            'PGF_Costo': pgf_costo,   # <--- NUEVO FASE 2
                                'C_costo': self.C_costo,
                                'S_auto': self.S_auto,
                                'R_robust': self.R_robust,
                                'I_rep': self.I_rep,
                                'F': self.F,
                                'P_riesgo_actual': self.P_riesgo_actual
                        }
            'C_costo': self.C_costo,
            'S_auto': self.S_auto,
            'R_robust': self.R_robust,
            'I_rep': self.I_rep,
            'F': self.F,
            'P_riesgo_actual': self.P_riesgo_actual
        }