import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. VARIÁVEIS INICIAIS (FLEXÍVEIS)
# ==============================================================================
m = 2.0          # Massa do bloco (kg)
k = 50.0         # Constante elástica da mola (N/m)
g = 9.81         # Aceleração da gravidade (m/s²)
y_inicial = 0.0  # Posição de onde o bloco é solto em repouso (m)
                 # Referencial adotado: y = 0 é a ponta da mola relaxada (sentido para baixo positivo)

# ==============================================================================
# 2. CÁLCULOS FÍSICOS
# ==============================================================================
# Ponto de equilíbrio estático: onde a força elástica anula o peso (k * y0 = m * g)
y0 = (m * g) / k

# Frequência angular (omega) e Período (T)
# NOTA FÍSICA IMPORTANTE:
# A gravidade (g) NÃO altera a frequência angular (omega) nem o período (T).
# A gravidade apenas desloca o ponto de equilíbrio de y = 0 para y = y0.
# A rigidez (k) e a inércia (m) continuam sendo as únicas responsáveis pela oscilação.
omega = np.sqrt(k / m)
T = (2 * np.pi) / omega
f = 1 / T

# Amplitude de oscilação em relação ao ponto de equilíbrio
A = abs(y_inicial - y0)

# ==============================================================================
# 3. SAÍDAS NO TERMINAL
# ==============================================================================
print("=" * 45)
print("SISTEMA MASSA-MOLA VERTICAL (MHS)")
print("=" * 45)
print(f"Massa (m): {m:.2f} kg")
print(f"Constante elástica (k): {k:.2f} N/m")
print(f"Gravidade (g): {g:.2f} m/s²")
print(f"Ponto de equilíbrio estático (y0): {y0:.3f} m")
print(f"Frequência angular (omega): {omega:.2f} rad/s")
print(f"Período de oscilação (T): {T:.2f} s")
print(f"Amplitude (A): {A:.3f} m")
print("=" * 45)

# ==============================================================================
# 4. GERAÇÃO DO TEMPO E EQUAÇÃO DO MHS
# ==============================================================================
num_oscilacoes = 4
t_max = num_oscilacoes * T
t = np.linspace(0, t_max, 1000)  # 1000 pontos no tempo para curva suave

# Equação horária da posição no MHS em torno de y0:
# Como v(0) = 0, temos y(t) = y0 + (y_inicial - y0) * cos(omega * t)
y = y0 + (y_inicial - y0) * np.cos(omega * t)

# ==============================================================================
# 5. VISUALIZAÇÃO GRÁFICA (MATPLOTLIB)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# Curva da posição em função do tempo
ax.plot(t, y, color='#1f77b4', lw=2.5, label='Posição y(t) do bloco')

# Linha horizontal em y = 0 (mola relaxada / sem peso)
ax.axhline(0, color='gray', linestyle='--', lw=1.5, label='y = 0 (Mola relaxada sem peso)')

# Linha horizontal destacada em y = y0 (novo ponto de equilíbrio)
ax.axhline(y0, color='#d62728', linestyle='--', lw=2, label=f'y0 = {y0:.3f} m (Equilíbrio estático)')

# Inverte o eixo Y para que o gráfico reflita visualmente o mundo real (para baixo = descendo)
ax.invert_yaxis()

# Configurações de layout e rótulos
ax.set_title("Cinemática do Sistema Massa-Mola Vertical (MHS)", fontsize=14, pad=15)
ax.set_xlabel("Tempo (s)", fontsize=12)
ax.set_ylabel("Posição y (m) [para baixo]", fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.show()

