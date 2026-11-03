import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Parâmetros termofísicos e geométricos consolidados na Microentrega 2
U = 12.0       # Coeficiente global de transferência de calor
A = 562.97     # Área superficial de troca térmica do costado e teto do tanque em m²
Tint = 80.0    # Temperatura do fluido interno mantida constante em regime de operação

# Intervalo temporal de análise referente ao ciclo operacional de 24 horas
t_inicio = 0.0
t_fim = 24.0

# Adotamos N = 1000 subintervalos para satisfazer os pressupostos da Regra de 1/3 de Simpson composta,
# minimizando o erro de truncamento da quadratura a uma magnitude O
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

print("=" * 70)
print("MEMORIAL DE CÁLCULO - PERDA TÉRMICA GLOBAL NO TANQUE (24 HORAS)")
print("=" * 70)
print(f"Partições adotadas (N): {N} (Passo h = {(t_fim - t_inicio)/N:.4f} h)")
print(f"Perda total de calor calculada (Joules): {Q_total_J:.6e} J")
print(f"Perda total de calor calculada (Joules - valor integral): {Q_total_J:,.2f} J")
print(f"Energia térmica equivalente dissipada: {Q_total_kWh:,.2f} kWh")
print("=" * 70)

