import numpy as np
try:
    from scipy.integrate import simpson, trapezoid
except ImportError:
    from scipy.integrate import simps as simpson
    from numpy import trapz as trapezoid

# Parâmetros termofísicos e geométricos do Cenário Base
U = 12.0       # Coeficiente global de transferência de calor em W/(m²·°C)
A = 562.97     # Área superficial de troca térmica do tanque em m²
Tint = 80.0    # Temperatura interna do fluido em regime permanente (°C)

# Intervalo temporal de 24 horas e níveis de refinamento avaliados
t_inicio = 0.0
t_fim = 24.0
niveis_N = [12, 24, 48, 1000]

print("-" * 78)
print("COMPARACAO DE METODOS NUMERICOS: SIMPSON 1/3 VS. TRAPEZIOS (CENARIO BASE)")
print("-" * 78)
print(f"{'N':>6} | {'Simpson (J)':>20} | {'Trapezios (J)':>20} | {'Diferenca Abs (J)':>20}")
print("-" * 78)

desvio_maximo = 0.0

for N in niveis_N:
    t = np.linspace(t_inicio, t_fim, N + 1)
    Tamb = 27.0 + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))
    q = U * A * (Tint - Tamb)

    # Integração numérica em W·h convertida para Joules (* 3600)
    Q_simpson_J = simpson(q, x=t) * 3600.0
    Q_trapezio_J = trapezoid(q, x=t) * 3600.0

    diferenca = abs(Q_simpson_J - Q_trapezio_J)
    if diferenca > desvio_maximo:
        desvio_maximo = diferenca

    simp_str = f"{Q_simpson_J:_.2f}".replace('.', ',').replace('_', '.')
    trap_str = f"{Q_trapezio_J:_.2f}".replace('.', ',').replace('_', '.')

    print(f"{N:>6} | {simp_str:>20} | {trap_str:>20} | {diferenca:>20.2e}")

print("-" * 78)
print(f"Desvio maximo observado entre os metodos: {desvio_maximo:.2e} J")
print("-" * 78)