import matplotlib.pyplot as plt
gamma_agua = 10.0
gamma_sat = 18.0
prof_max = 10

profundidades = []
tensoes_totais = []
tensoes_efetivas = []
poropressoes = []

print("Calculando o perfil de tensoes no solo marinho")

for r in range(prof_max + 1):
    sigma = r * gamma_sat
    u = r * gamma_agua
    sigma_efetiva = sigma - u
    profundidades.append(r)
    tensoes_totais.append(sigma)
    tensoes_efetivas.append(sigma_efetiva)
    poropressoes.append(u)

    print(f"Profundidade: {r} m, Tensao total: {sigma} kPa, Tensao efetiva: {sigma_efetiva: .1f} Poropressao: {u} kPa")

plt.figure(figsize=(7, 5))
plt.plot(tensoes_totais, profundidades, label='Tensão Total', color='black', linestyle='--')
plt.plot(tensoes_efetivas, profundidades, label='Tensão Efetiva', color='red', linewidth=2)
plt.plot(poropressoes, profundidades, label='Poropressão', color='blue', linestyle=':')
plt.title('Perfil de Tensões no Solo Marinho(E-Sub)')
plt.xlabel('Tensão (kPa)')
plt.ylabel('Profundidade (m)')
plt.gca().invert_yaxis()
plt.grid(True)
plt.legend()
plt.show()