import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 4*np.pi, 500)
f = np.cos(t)

A = np.zeros(len(t))
for i in range(1, len(t)):
    dt = t[i] - t[i-1]
    area = (f[i] + f[i-1]) * dt / 2
    A[i] = A[i-1] + area

plt.figure(figsize=(10, 5))
plt.plot(t, f, label="Função original f(t) = cos(t)", color='orange')
plt.plot(t, A, label="Função Acumulação A(t)", color='purple', linestyle='--')
plt.axhline(0, color='black', linewidth=0.8) 
plt.title("Função Original vs Função Acumulação")
plt.xlabel("x")
plt.legend()
plt.grid(True)
plt.show()