import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Parâmetros do Cenário 1 (Seção 2.1 do relatório)
U = 0.5      # Coef. global [W/(m²·°C)], poliuretano injetado de 50 mm
A = 562.97   # Área de troca (costado + teto) [m²]
Tint = 80.0  # Temperatura interna do fluido, constante [°C]

# Intervalo de análise: ciclo operacional de 24 horas
t_inicio = 0.0
t_fim = 24.0

# N = 1000 subintervalos (par, como exige a Regra de 1/3 de Simpson);
# o erro de truncamento global da quadratura é O(h^4)
N = 1000
t = np.linspace(t_inicio, t_fim, N + 1)

# Temperatura ambiente senoidal, com máximo às 14h00 (Eq. 2)
Tamb = 27.0 + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))

# Taxa de perda de calor q(t) em watts, ou J/s (Eq. 1)
q = U * A * (Tint - Tamb)

# Regra de Simpson sobre [0, 24] h: com t em horas, o resultado
# da integral está em W·h (Eq. 3)
integral_Wh = simpson(q, x=t)

# Conversão de W·h para J: 1 W·h = 3600 J (Eq. 4)
Q_total_J = integral_Wh * 3600.0

# Conversão de W·h para kWh, para o cálculo do custo (Eq. 6)
Q_total_kWh = integral_Wh / 1000.0

q_joules_str = f"{Q_total_J:_.2f}".replace('.', ',').replace('_', '.')
q_kwh_str = f"{Q_total_kWh:_.2f}".replace('.', ',').replace('_', '.')
q_gj = Q_total_J / 1e9

print("-" * 55)
print("RESULTADOS - VARIACAO 1 (POLIURETANO INJETADO U=0.5)")
print("-" * 55)
print(f"Subintervalos adotados (N) : {N} passos")
print(f"Perda Total de Calor (J)   : {q_joules_str} J")
print(f"Notacao Cientifica         : {Q_total_J:.4e} J")
print(f"Ordem de Grandeza (GJ)     : {q_gj:.2f} GJ")
print(f"Consumo Equivalente (kWh)  : {q_kwh_str} kWh")
print("-" * 55)