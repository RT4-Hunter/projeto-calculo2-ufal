import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Parâmetros termofísicos e geométricos (Cenário 2: Frente Fria sem isolamento)
U = 12.0       # Coeficiente global de transferência de calor em W/(m²·°C) (Tanque sem isolamento)
A = 562.97     # Área superficial de troca térmica do costado e teto do tanque em m²
Tint = 80.0    # Temperatura do fluido interno mantida constante em regime de operação (°C)

# Intervalo temporal de análise referente ao ciclo operacional de 24 horas
t_inicio = 0.0
t_fim = 24.0

# Discretização com N = 1000 subintervalos para a Regra de 1/3 de Simpson composta
N = 1000
t = np.linspace(t_inicio, t_fim, N + 1)

# Perfil senoidal térmico sob frente fria climática (T_média = 18 °C e amplitude térmica reduzida de 2 °C)
Tamb = 18.0 + 2.0 * np.cos((np.pi / 12.0) * (t - 14.0))

# Equação constitutiva da taxa de transferência de calor instantânea q(t) em Watts (J/s)
q = U * A * (Tint - Tamb)

# Quadratura numérica de Simpson sobre o ciclo de 24 h (resultado em W·h)
integral_Wh = simpson(q, x=t)

# Conversão de W·h para Joules (* 3600) e para kWh (/ 1000)
Q_total_J = integral_Wh * 3600.0
Q_total_kWh = integral_Wh / 1000.0

q_joules_str = f"{Q_total_J:_.2f}".replace('.', ',').replace('_', '.')
q_kwh_str = f"{Q_total_kWh:_.2f}".replace('.', ',').replace('_', '.')
q_gj = Q_total_J / 1e9

print("-" * 55)
print("RESULTADOS - VARIACAO 2 (FRENTE FRIA T_MEDIA=18C, U=12.0)")
print("-" * 55)
print(f"Subintervalos adotados (N) : {N} passos")
print(f"Perda Total de Calor (J)   : {q_joules_str} J")
print(f"Notacao Cientifica         : {Q_total_J:.4e} J")
print(f"Ordem de Grandeza (GJ)     : {q_gj:.2f} GJ")
print(f"Consumo Equivalente (kWh)  : {q_kwh_str} kWh")
print("-" * 55)