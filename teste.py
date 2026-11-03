import numpy as np  # importa a biblioteca numpy para trabalhar com matrizes e vetores
def jacobi(A, b, x0=None, tol=1e-5, max_iter=100):  # define a funcao do metodo de jacobi
    A = np.array(A, dtype=float)  # garante que a matriz A seja do tipo float do numpy
    b = np.array(b, dtype=float)  # garante que o vetor b seja do tipo float do numpy
    n = len(b)  # pega o tamanho do sistema a partir do tamanho do vetor b
    if x0 is None:  # verifica se o usuario nao passou um chute inicial
        x = np.zeros(n)  # cria um vetor de zeros do tamanho n como chute inicial padrao
    else:  # caso o usuario tenha passado um chute inicial proprio
        x = np.array(x0, dtype=float)  # converte o chute informado para array float
    for k in range(max_iter):  # laco de repeticao que controla as iteracoes
        x_novo = np.zeros(n)  # cria um vetor temporario para guardar os valores calculados nesta iteracao
        for i in range(n):  # percorre cada linha da matriz (cada equacao)
            soma = 0.0  # zera a soma dos termos que nao estao na diagonal principal
            for j in range(n):  # percorre cada coluna da equacao atual
                if i != j:  # ignora o elemento da diagonal principal
                    soma += A[i][j] * x[j]  # acumula a multiplicacao do coeficiente pelo valor antigo da variavel
            x_novo[i] = (b[i] - soma) / A[i][i]  # calcula o novo valor isolando a variavel da diagonal
        if np.linalg.norm(x_novo - x) < tol:  # calcula a diferenca entre a iteracao atual e a anterior
            return x_novo, k + 1  # se a diferenca for menor que a tolerancia, retorna a solucao e as iteracoes
        x = x_novo.copy()  # atualiza o vetor x com os valores novos para a proxima rodada
    return x, max_iter  # retorna o resultado encontrado caso atinja o limite maximo de iteracoes
def gauss_seidel(A, b, x0=None, tol=1e-5, max_iter=100):  # define a funcao do metodo de gauss-seidel
    A = np.array(A, dtype=float)  # converte a matriz A para float do numpy
    b = np.array(b, dtype=float)  # converte o vetor b para float do numpy
    n = len(b)  # pega o numero de equacoes pelo tamanho do vetor b
    if x0 is None:  # checa se o chute inicial nao foi fornecido
        x = np.zeros(n)  # inicia com vetor zerado se nao houver chute inicial
    else:  # se o usuario passou um chute inicial
        x = np.array(x0, dtype=float)  # converte o chute passado para float
    for k in range(max_iter):  # laco principal para contar as iteracoes
        x_antigo = x.copy()  # salva uma copia dos valores antes de atualizar para calcular o erro depois
        for i in range(n):  # percorre cada linha do sistema linear
            soma = 0.0  # zera a variavel que vai somar os outros termos
            for j in range(n):  # percorre as colunas da equacao i
                if i != j:  # pula o elemento que esta na diagonal principal
                    soma += A[i][j] * x[j]  # soma usando os valores ja atualizados no proprio vetor x
            x[i] = (b[i] - soma) / A[i][i]  # atualiza diretamente a posicao i do vetor x com o novo valor
        if np.linalg.norm(x - x_antigo) < tol:  # calcula a norma da diferenca entre os passos
            return x, k + 1  # retorna o vetor solucao e o total de passos dados se atingir a tolerancia
    return x, max_iter  # retorna a resposta final se estourar o limite de iteracoes
# =======================================================  # divisoria visual para separar as funcoes do exemplo
# EXEMPLO PRATICO DE USO:  # secao onde colocamos os dados de teste
# =======================================================  # divisoria visual de fechamento
A = [  # matriz A: coeficientes das equacoes (funciona para qualquer tamanho n x n)
    [10, 2, 1],  # primeira linha: 10*x1 + 2*x2 + 1*x3
    [1, 5, 1],  # segunda linha: 1*x1 + 5*x2 + 1*x3
    [2, 3, 10]  # terceira linha: 2*x1 + 3*x2 + 10*x3
]  # fecha a lista da matriz A
b = [7, -8, 6]  # vetor b: termos independentes das equacoes (depois da igualdade)
sol_jacobi, iter_jacobi = jacobi(A, b)  # chama a funcao de jacobi passando a matriz A e o vetor b
sol_gs, iter_gs = gauss_seidel(A, b)  # chama a funcao de gauss-seidel passando a matriz A e o vetor b
print("--- METODO DE JACOBI ---")  # exibe o texto de cabecalho para jacobi
print(f"Solucao: {sol_jacobi}")  # imprime o array com os valores encontrados para as variaveis
print(f"Iteracoes: {iter_jacobi}")  # imprime quantas voltas o laco precisou dar para convergir
print("\n--- METODO DE GAUSS-SEIDEL ---")  # exibe o texto de cabecalho para gauss-seidel
print(f"Solucao: {sol_gs}")  # imprime o array com a solucao calculada por gauss-seidel
print(f"Iteracoes: {iter_gs}")  # imprime quantas voltas o gauss-seidel precisou para convergir