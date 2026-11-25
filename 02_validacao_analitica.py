import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Teste de validação: f(x) = 3x² + 2x no intervalo [0, 2].
# Primitiva F(x) = x³ + x², logo a integral vale F(2) − F(0) = 12,0
a = 0.0
b = 2.0
valor_analitico = 12.0

# N = 1000 subintervalos, o mesmo N do problema físico
# (aqui h = 0,002, pois o intervalo é [0, 2])
N = 1000
x = np.linspace(a, b, N + 1)
f_x = 3.0 * (x ** 2) + 2.0 * x

# Regra de 1/3 de Simpson composta (exata para polinômios de grau ≤ 3)
valor_numerico = simpson(f_x, x=x)

# Erro absoluto entre o valor analítico e o numérico
erro_absoluto = abs(valor_analitico - valor_numerico)