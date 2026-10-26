import numpy as np

def jacobi(A, b, x0=None, tol=1e-5, max_iter=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)
    for k in range(max_iter):
        x_novo = np.zeros(n)
        for i in range(n):
            soma = 0.0
            for j in range(n):
                if i != j:
                    soma += A[i][j] * x[j]
            x_novo[i] = (b[i] - soma) / A[i][i]
        if np.linalg.norm(x_novo - x) < tol:
            return x_novo, k + 1
        x = x_novo.copy()
    return x, max_iter

def gauss_seidel(A, b, x0=None, tol=1e-5, max_iter=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)
    for k in range(max_iter):
        x_antigo = x.copy()
        for i in range(n):
            soma = 0.0
            for j in range(n):
                if i != j:
                    soma += A[i][j] * x[j]
            x[i] = (b[i] - soma) / A[i][i]
        if np.linalg.norm(x - x_antigo) < tol:
            return x, k + 1
    return x, max_iter

A = [
    [10, 2, 1],
    [1, 5, 1],
    [2, 3, 10]
]
b = [7, -8, 6]

sol_jacobi, iter_jacobi = jacobi(A, b)
sol_gs, iter_gs = gauss_seidel(A, b)

print("--- METODO DE JACOBI ---")
print(f"Solucao: {sol_jacobi}")
print(f"Iteracoes: {iter_jacobi}")

print("\n--- METODO DE GAUSS-SEIDEL ---")
print(f"Solucao: {sol_gs}")
print(f"Iteracoes: {iter_gs}")