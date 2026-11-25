import numpy as np
try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson


def fmt_br(valor, casas=2):
    # Formato brasileiro: 30.935.426.688,00
    texto = f"{valor:_.{casas}f}"
    return texto.replace('.', ',').replace('_', '.')


# Parâmetros fixos (Seção 2.1 do relatório)
A = 562.97      # Área de troca (costado + teto) [m²]
Tint = 80.0     # Temperatura interna do fluido, constante [°C]
TARIFA = 0.75   # Tarifa industrial [R$/kWh]
DIAS = 30       # Dias de operação por mês
N = 1000        # Subintervalos de Simpson (h = 0,024 h)

# Cenários: (nome, U [W/(m²·°C)], Tmédia [°C], amplitude [°C])
cenarios = [
    ("Base", 12.0, 27.0, 4.0),
    ("Cenario 1 (poliuretano)", 0.5, 27.0, 4.0),
    ("Cenario 2 (frente fria)", 12.0, 18.0, 2.0),
    ("Referencia (la de rocha)", 1.2, 27.0, 4.0),
]

t = np.linspace(0.0, 24.0, N + 1)
res = {}
for nome, U, Tm, dT in cenarios:
    Tamb = Tm + dT * np.cos((np.pi / 12.0) * (t - 14.0))
    q = U * A * (Tint - Tamb)                    # Eq. 1, em W
    Q_Wh = simpson(q, x=t)                       # Eq. 3, em W·h
    Q_J = Q_Wh * 3600.0                          # Eq. 4, em J
    kwh = Q_Wh / 1000.0                          # Eq. 6, em kWh/dia
    custo_dia = round(kwh * TARIFA, 2)           # Eq. 7
    custo_mes = DIAS * custo_dia
    Q_eq9_Wh = 24.0 * U * A * (Tint - Tm)        # Eq. 9
    res[nome] = {
        "U": U, "Tm": Tm, "GJ": Q_J / 1e9, "kwh": kwh,
        "mes": custo_mes,
        "pico": U * A * (Tint - (Tm - dT)) / 1000.0,   # 02h00
        "vale": U * A * (Tint - (Tm + dT)) / 1000.0,   # 14h00
        "erro_eq9": abs(Q_Wh - Q_eq9_Wh) * 3600.0,
    }

base = res["Base"]
c1 = res["Cenario 1 (poliuretano)"]
c2 = res["Cenario 2 (frente fria)"]
la = res["Referencia (la de rocha)"]

print("-" * 78)
print("RESUMO ENERGETICO E FINANCEIRO (R$ 0,75/kWh, 30 DIAS/MES)")
print("-" * 78)
print(f"{'Cenario':<25} | {'GJ/dia':>6} | {'kWh/dia':>9} | "
      f"{'Custo mensal (R$)':>17}")
print("-" * 78)
for nome, r in res.items():
    print(f"{nome:<25} | {fmt_br(r['GJ']):>6} | "
          f"{fmt_br(r['kwh']):>9} | {fmt_br(r['mes']):>17}")
print("-" * 78)

print("TAXA INSTANTANEA q(t): PICO (02h00) E VALE (14h00), EM kW")
print("-" * 78)
for nome, r in res.items():
    print(f"{nome:<25} | pico = {fmt_br(r['pico']):>7} | "
          f"vale = {fmt_br(r['vale']):>7}")
print("-" * 78)

print("COMPARACOES COM O CENARIO BASE")
print("-" * 78)
var1 = (c1["kwh"] - base["kwh"]) / base["kwh"] * 100.0
var2 = (c2["kwh"] - base["kwh"]) / base["kwh"] * 100.0
eco1 = base["mes"] - c1["mes"]
acr2 = c2["mes"] - base["mes"]
print(f"Cenario 1: variacao de consumo = {fmt_br(var1)}%")
print(f"Cenario 1: economia mensal     = R$ {fmt_br(eco1)}")
print(f"Cenario 1: economia anual      = R$ {fmt_br(eco1 * 12)}")
print(f"Cenario 2: variacao de consumo = +{fmt_br(var2)}%")
print(f"Cenario 2: acrescimo mensal    = R$ {fmt_br(acr2)}")
print("-" * 78)

print("POLIURETANO VS. LA DE ROCHA")
print("-" * 78)
print(f"Economia: {fmt_br(la['kwh'] - c1['kwh'])} kWh/dia "
      f"e R$ {fmt_br(la['mes'] - c1['mes'])}/mes")
print("-" * 78)

erro_max = max(r["erro_eq9"] for r in res.values())
print(f"Erro maximo de Simpson em relacao a Eq. (9): {erro_max:.2e} J")
print("-" * 78)