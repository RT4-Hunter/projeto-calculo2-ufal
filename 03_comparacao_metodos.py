import numpy as np
try:
    from scipy.integrate import simpson, trapezoid
except ImportError:
    from scipy.integrate import simps as simpson
    from numpy import trapz as trapezoid


def fmt_br(valor):
    # Formato brasileiro: 30.935.426.688,00
    return f"{valor:_.2f}".replace('.', ',').replace('_', '.')


# Parâmetros do Cenário Base (Seção 2.1 do relatório)
U = 12.0     # Coef. global de transferência de calor [W/(m²·°C)]
A = 562.97   # Área de troca (costado + teto) [m²]
Tint = 80.0  # Temperatura interna do fluido, constante [°C]
Tmedia = 27.0
niveis_N = [12, 24, 48, 1000]

# Forma fechada (Eq. 9) e conversão de W·h para J (Eq. 4)
Q_analitico_Wh = 24.0 * U * A * (Tint - Tmedia)
Q_analitico_J = Q_analitico_Wh * 3600.0

# PARTE 1: Cenário Base, Simpson 1/3 vs. Trapézios vs. Eq. (9)
print("-" * 78)
print("PARTE 1 - CENARIO BASE: SIMPSON 1/3 VS. TRAPEZIOS VS. EQ. (9)")
print("-" * 78)
print(f"Q analitico (Eq. 9): {fmt_br(Q_analitico_J)} J")
print("-" * 78)
print(f"{'N':>5} | {'Simpson (J)':>19} | {'Trapezios (J)':>19}")
print("-" * 78)

linhas_erro = []
desvio_maximo = 0.0
for N in niveis_N:
    t = np.linspace(0.0, 24.0, N + 1)
    Tamb = Tmedia + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))
    q = U * A * (Tint - Tamb)
    Q_simpson_J = simpson(q, x=t) * 3600.0
    Q_trapezio_J = trapezoid(q, x=t) * 3600.0
    erro_s = abs(Q_simpson_J - Q_analitico_J)
    erro_t = abs(Q_trapezio_J - Q_analitico_J)
    desvio = abs(Q_simpson_J - Q_trapezio_J)
    desvio_maximo = max(desvio_maximo, desvio)
    linhas_erro.append((N, erro_s, erro_t, desvio))
    q_s = fmt_br(Q_simpson_J)
    q_t = fmt_br(Q_trapezio_J)
    print(f"{N:>5} | {q_s:>19} | {q_t:>19}")

print("-" * 78)
print("    N | Erro Simpson (J) | Erro Trapezios (J) | Desvio (J)")
print("-" * 78)
for N, erro_s, erro_t, desvio in linhas_erro:
    print(f"{N:>5} | {erro_s:>16.2e} | {erro_t:>18.2e} | "
          f"{desvio:>10.2e}")
print("-" * 78)
print(f"Desvio maximo entre os metodos: {desvio_maximo:.2e} J")
print("-" * 78)

# PARTE 2: funções não periódicas em [0, 2] (ordem de convergência)
funcoes = [
    ("f(x) = 3x^2 + 2x", lambda x: 3.0 * x**2 + 2.0 * x, 12.0),
    ("f(x) = exp(x)", np.exp, np.exp(2.0) - 1.0),
]
for nome, f, exato in funcoes:
    print()
    print("-" * 78)
    print(f"PARTE 2 - {nome} EM [0, 2] (valor exato = {exato:.12f})")
    print("-" * 78)
    print("    N |        h |   Erro Simpson | Erro Trapezios")
    print("-" * 78)
    for N in niveis_N:
        x = np.linspace(0.0, 2.0, N + 1)
        y = f(x)
        erro_s = abs(exato - simpson(y, x=x))
        erro_t = abs(exato - trapezoid(y, x=x))
        h = 2.0 / N
        print(f"{N:>5} | {h:>8.4f} | {erro_s:>14.2e} | "
              f"{erro_t:>14.2e}")
    print("-" * 78)