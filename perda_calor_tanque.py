import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Parâmetros termofísicos e geométricos consolidados na Microentrega 2
U = 12.0       # Coeficiente global de transferência de calor em W/(m²·°C)
A = 562.97     # Área superficial de troca térmica do costado e teto do tanque em m²
Tint = 80.0    # Temperatura do fluido interno mantida constante em regime de operação (°C)

# Intervalo temporal de análise referente ao ciclo operacional de 24 horas
t_inicio = 0.0
t_fim = 24.0

# Adotamos N = 1000 subintervalos para satisfazer os pressupostos da Regra de 1/3 de Simpson composta,
# minimizando o erro de truncamento da quadratura a uma magnitude O(h^4)
N = 1000
t = np.linspace(t_inicio, t_fim, N + 1)

# Perfil senoidal térmico diurno com defasagem de 14h, representando o pico de radiação e temperatura ambiente
Tamb = 27.0 + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))

# Equação constitutiva da taxa de transferência de calor instantânea q(t) em Watts (J/s)
q = U * A * (Tint - Tamb)

# Aplicação da quadratura numérica de Simpson sobre a função contínua amostrada no intervalo [0, 24] h;
# o resultado dimensional obtido desta integração direta no tempo corresponde a W·h
integral_Wh = simpson(q, x=t)

# Fator de conversão aplicado aqui para compatibilizar a análise dimensional de W·h para Joules, conforme definido na Microentrega 2
Q_total_J = integral_Wh * 3600.0

# Conversão da energia térmica acumulada para kWh para mensuração de custos operacionais na planta
Q_total_kWh = integral_Wh / 1000.0

q_joules_str = f"{Q_total_J:_.2f}".replace('.', ',').replace('_', '.')
q_kwh_str = f"{Q_total_kWh:_.2f}".replace('.', ',').replace('_', '.')
q_gj = Q_total_J / 1e9

print("-" * 55)
print("     RESULTADOS DA INTEGRACAO - REGRA DE SIMPSON")
print("-" * 55)
print(f"Subintervalos adotados (N) : {N} passos")
print(f"Perda Total de Calor (J)   : {q_joules_str} J")
print(f"Notacao Cientifica         : {Q_total_J:.4e} J")
print(f"Ordem de Grandeza (GJ)     : {q_gj:.2f} GJ")
print(f"Consumo Equivalente (kWh)  : {q_kwh_str} kWh")
print("-" * 55)
