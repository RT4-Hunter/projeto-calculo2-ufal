import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# Função polinomial de teste com primitiva analítica conhecida:
# Integral de (3x² + 2x) dx no intervalo [0, 2] -> [x³ + x²] de 0 a 2 = 12,0
a = 0.0
b = 2.0
valor_analitico = 12.0

# Discretização do domínio com N = 1000 subintervalos (mesma malha adotada no problema físico)
N = 1000
x = np.linspace(a, b, N + 1)
f_x = 3.0 * (x ** 2) + 2.0 * x

# Aplicação da Regra de 1/3 de Simpson composta
valor_numerico = simpson(f_x, x=x)

# Cálculo do erro absoluto entre o resultado analítico e a aproximação numérica
erro_absoluto = abs(valor_analitico - valor_numerico)

print("-" * 55)
print("RESULTADOS - VALIDACAO ANALITICA (INTEGRAL DE TESTE)")
print("-" * 55)
print(f"Funcao avaliada            : f(x) = 3x^2 + 2x em [0, 2]")
print(f"Subintervalos adotados (N) : {N} passos")
print(f"Valor Analitico Exato      : {valor_analitico:.15f}")
print(f"Valor Numerico (Simpson)   : {valor_numerico:.15f}")
print(f"Erro Absoluto              : {erro_absoluto:.2e}")
print("-" * 55)