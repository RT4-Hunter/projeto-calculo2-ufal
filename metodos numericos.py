import numpy as np
import matplotlib.pyplot as plt

m = 1.0
k = 1.0
w = np.sqrt(k / m)

print(f"Frequência do sistema (w): {w:.2f} rad/s")

dt_critico = 2.0 / w
print(f"dt crítico calculado: {dt_critico:.2f} s")

valores_dt = [0.05, 1.9, 2.1]  
tempo_total = 30.0

plt.figure(figsize=(10, 6))

for dt in valores_dt:
    n_passos = int(tempo_total / dt)
    
    x = np.zeros(n_passos)
    v = np.zeros(n_passos)
    tempo = np.linspace(0, tempo_total, n_passos)
    
    x[0] = 1.0  
    v[0] = 0.0  
    
    energia_inicial = 0.5 * m * v[0]**2 + 0.5 * k * x[0]**2
    
    erro_energia = np.zeros(n_passos)
    erro_energia[0] = 0.0
    
    for i in range(n_passos - 1):
        v[i+1] = v[i] - (k/m) * x[i] * dt
        x[i+1] = x[i] + v[i+1] * dt 
        
        energia_atual = 0.5 * m * v[i+1]**2 + 0.5 * k * x[i+1]**2
        erro_energia[i+1] = energia_atual - energia_inicial

    plt.plot(tempo, erro_energia, label=f'dt = {dt}')

plt.title('Impacto do dt no Erro da Energia Total (Oscilador Massa-Mola)')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro na Energia (Joules)')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.ylim(-1, 5)
plt.legend()
plt.grid(True)
plt.show()