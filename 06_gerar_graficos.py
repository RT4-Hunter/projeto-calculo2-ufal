import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# =============================================================================
# 1. PARÂMETROS TERMOFÍSICOS, GEOMÉTRICOS E CLIMÁTICOS (SEÇÃO 2.1 DO RELATÓRIO)
# =============================================================================
A = 562.97      # Área de troca (costado + teto) [m²]
Tint = 80.0     # Temperatura interna do fluido, constante [°C]

# Discretização temporal: ciclo de 24 h com N = 1000 subintervalos (Simpson)
t_inicio = 0.0
t_fim = 24.0
N = 1000
t = np.linspace(t_inicio, t_fim, N + 1)

# Coeficientes globais de transferência de calor [W/(m²·°C)]
U_base = 12.0   # Cenário Base: tanque sem isolamento
U_iso = 0.5     # Cenário 1: poliuretano injetado de 50 mm
U_fria = 12.0   # Cenário 2: tanque sem isolamento sob frente fria

# Temperatura ambiente senoidal (Eq. 2), com máximo às 14h00
Tamb_padrao = 27.0 + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))
Tamb_fria = 18.0 + 2.0 * np.cos((np.pi / 12.0) * (t - 14.0))

# =============================================================================
# 2. TAXAS INSTANTÂNEAS E QUADRATURA DE SIMPSON
# =============================================================================
# Taxa de perda de calor q(t) em watts (Eq. 1) e em kW
q_base_W = U_base * A * (Tint - Tamb_padrao)
q_iso_W = U_iso * A * (Tint - Tamb_padrao)
q_fria_W = U_fria * A * (Tint - Tamb_fria)

q_base_kW = q_base_W / 1000.0
q_iso_kW = q_iso_W / 1000.0
q_fria_kW = q_fria_W / 1000.0

# Picos (02h00) e vales (14h00) de q(t), em kW
pico_base = U_base * A * (Tint - (27.0 - 4.0)) / 1000.0
vale_base = U_base * A * (Tint - (27.0 + 4.0)) / 1000.0
pico_fria = U_fria * A * (Tint - (18.0 - 2.0)) / 1000.0
vale_fria = U_fria * A * (Tint - (18.0 + 2.0)) / 1000.0
pico_iso = U_iso * A * (Tint - (27.0 - 4.0)) / 1000.0
vale_iso = U_iso * A * (Tint - (27.0 + 4.0)) / 1000.0

# Regra de 1/3 de Simpson composta (Eq. 3), resultado em W·h
int_base_Wh = simpson(q_base_W, x=t)
int_iso_Wh = simpson(q_iso_W, x=t)
int_fria_Wh = simpson(q_fria_W, x=t)

# Conversões: J (Eq. 4), GJ e kWh/dia (Eq. 6)
Q_base_J = int_base_Wh * 3600.0
Q_iso_J = int_iso_Wh * 3600.0
Q_fria_J = int_fria_Wh * 3600.0

Q_base_GJ = Q_base_J / 1e9
Q_iso_GJ = Q_iso_J / 1e9
Q_fria_GJ = Q_fria_J / 1e9

Q_base_kWh = int_base_Wh / 1000.0
Q_iso_kWh = int_iso_Wh / 1000.0
Q_fria_kWh = int_fria_Wh / 1000.0

# =============================================================================
# 3. ANÁLISE ECONÔMICO-FINANCEIRA (EQ. 7)
# =============================================================================
tarifa = 0.75   # R$/kWh
dias_mes = 30

# Custo diário arredondado em 2 casas decimais antes de multiplicar por 30
custo_dia_base = round(Q_base_kWh * tarifa, 2)
custo_mes_base = custo_dia_base * dias_mes

custo_dia_iso = round(Q_iso_kWh * tarifa, 2)
custo_mes_iso = custo_dia_iso * dias_mes

custo_dia_fria = round(Q_fria_kWh * tarifa, 2)
custo_mes_fria = custo_dia_fria * dias_mes

# Variações percentuais em relação ao Cenário Base
var_iso_pct = ((Q_iso_kWh - Q_base_kWh) / Q_base_kWh) * 100.0
var_fria_pct = ((Q_fria_kWh - Q_base_kWh) / Q_base_kWh) * 100.0

# Economia mensal do Cenário 1 em relação ao Cenário Base
economia_mes_iso = custo_mes_base - custo_mes_iso


def formata_br(valor, decimais=2, prefixo=""):
    # Formato brasileiro: milhar com '.' e decimal com ','
    texto = f"{valor:_.{decimais}f}"
    return f"{prefixo}{texto.replace('.', ',').replace('_', '.')}"


# =============================================================================
# 4. ESTILO GERAL DOS GRÁFICOS
# =============================================================================
# As figuras ficam sem título interno, pois a legenda "Figura n – ..." já
# aparece no relatório. Troque para True para exibir os títulos nas imagens.
MOSTRAR_TITULO = False

COR_BASE = '#1B4F72'     # Azul-marinho (Cenário Base)
COR_ISO = '#1E8449'      # Verde (Cenário 1)
COR_FRIA = '#B03A2E'     # Vermelho (Cenário 2)
COR_TEXTO = '#2C3E50'
COR_GRADE = '#AEB6BF'
COR_BORDA = '#D5D8DC'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.edgecolor': '#7F8C8D',
    'axes.linewidth': 0.8,
    'axes.labelcolor': COR_TEXTO,
    'xtick.color': COR_TEXTO,
    'ytick.color': COR_TEXTO,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})


def caixa(cor):
    # Estilo padrão das anotações em caixa
    return dict(boxstyle='round,pad=0.3', facecolor='white',
                edgecolor=cor, linewidth=0.9, alpha=0.95)


# =============================================================================
# 5. FIGURA 1: TAXA INSTANTÂNEA DE PERDA DE CALOR EM 24 HORAS
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(7.4, 4.3))

ax1.plot(t, q_fria_kW, color=COR_FRIA, lw=2.0,
         label='Cenário 2 — Frente fria sem isolamento (U = 12,0 W/(m²·°C))')
ax1.fill_between(t, q_fria_kW, color=COR_FRIA, alpha=0.07)

ax1.plot(t, q_base_kW, color=COR_BASE, lw=2.0,
         label='Cenário Base — Sem isolamento (U = 12,0 W/(m²·°C))')
ax1.fill_between(t, q_base_kW, color=COR_BASE, alpha=0.07)

ax1.plot(t, q_iso_kW, color=COR_ISO, lw=2.0,
         label='Cenário 1 — Poliuretano injetado 50 mm (U = 0,5 W/(m²·°C))')
ax1.fill_between(t, q_iso_kW, color=COR_ISO, alpha=0.07)

# Marcadores nos pontos de pico (02h00) e vale (14h00)
ax1.plot([2.0, 14.0], [pico_base, vale_base], 'o', color=COR_BASE, ms=5)
ax1.plot([2.0, 14.0], [pico_fria, vale_fria], 'o', color=COR_FRIA, ms=5)

# Eixos
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlim(0, 24)
ax1.set_ylim(0, 520)
ax1.set_xticks(np.arange(0, 25, 2))
ax1.set_xticklabels([f"{h:02d}h" for h in range(0, 25, 2)], fontsize=8.5)
ax1.set_yticks(np.arange(0, 501, 100))
ax1.set_yticklabels([f"{y}" for y in range(0, 501, 100)], fontsize=8.5)
ax1.set_xlabel('Horário do dia (h)', fontsize=9.5, fontweight='bold',
               labelpad=6)
ax1.set_ylabel('Taxa de perda de calor, q(t) [kW]', fontsize=9.5,
               fontweight='bold', labelpad=6)
ax1.grid(True, linestyle=':', alpha=0.55, color=COR_GRADE)
ax1.set_axisbelow(True)

if MOSTRAR_TITULO:
    ax1.set_title('Taxa instantânea de perda de calor em 24 horas\n'
                  'Tint = 80 °C; A = 562,97 m²', fontsize=10.5,
                  fontweight='bold', color=COR_TEXTO, pad=10)

# Anotações dos cenários sem isolamento
ax1.annotate(f'Cenário 2: pico de {formata_br(pico_fria)} kW (02h00)',
             xy=(2.0, pico_fria), xytext=(4.2, 480.0),
             arrowprops=dict(arrowstyle='->', color=COR_FRIA, lw=1.1,
                             shrinkB=4),
             fontsize=8, fontweight='bold', color=COR_FRIA,
             bbox=caixa(COR_BORDA))

ax1.annotate(f'Base: pico de {formata_br(pico_base)} kW (02h00)',
             xy=(2.0, pico_base), xytext=(3.2, 305.0),
             arrowprops=dict(arrowstyle='->', color=COR_BASE, lw=1.1,
                             shrinkB=4),
             fontsize=8, fontweight='bold', color=COR_BASE,
             bbox=caixa(COR_BORDA))

ax1.annotate(f'Base: vale de {formata_br(vale_base)} kW (14h00)',
             xy=(14.0, vale_base), xytext=(9.6, 255.0),
             arrowprops=dict(arrowstyle='->', color=COR_BASE, lw=1.1,
                             shrinkB=4),
             fontsize=8, fontweight='bold', color=COR_BASE,
             bbox=caixa(COR_BORDA))

# Seta de redução entre o Cenário Base e o Cenário 1 em x = 20,5 h
x_seta = 20.5
y_topo = float(np.interp(x_seta, t, q_base_kW))
y_base = float(np.interp(x_seta, t, q_iso_kW))
ax1.annotate('', xy=(x_seta, y_topo), xytext=(x_seta, y_base),
             arrowprops=dict(arrowstyle='<->', color=COR_ISO, lw=1.6))
ax1.text(x_seta - 0.3, 190.0,
         f'Redução de {formata_br(abs(var_iso_pct))}%\n'
         'na taxa de perda\nde calor',
         fontsize=8, fontweight='bold', color=COR_ISO, va='center',
         ha='right',
         bbox=dict(boxstyle='round,pad=0.35', facecolor='#EAFAF1',
                   edgecolor=COR_ISO, linewidth=0.9, alpha=0.95))

# Faixa de variação do Cenário 1
ax1.text(0.5, 44.0,
         f'Cenário 1: {formata_br(vale_iso)} a {formata_br(pico_iso)} kW',
         fontsize=8, fontweight='bold', color=COR_ISO, va='center')

# Legenda fora da área de plotagem, abaixo do eixo x
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17), frameon=True,
           facecolor='white', edgecolor=COR_BORDA, framealpha=0.95,
           fontsize=7.8, ncol=1)

nome_fig1 = "figura1_taxa_calor_24h.png"
fig1.savefig(nome_fig1, dpi=300, facecolor='white', bbox_inches='tight',
             pad_inches=0.12)
plt.close(fig1)

# =============================================================================
# 6. FIGURA 2: COMPARATIVO ENERGÉTICO E ECONÔMICO (ODS 7)
# =============================================================================
fig2, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.6, 4.3))

cenarios = ['Cenário Base\n(sem isolamento)', 'Cenário 1\n(poliuretano)',
            'Cenário 2\n(frente fria)']
cores_barras = [COR_BASE, COR_ISO, COR_FRIA]
consumos_kwh = [Q_base_kWh, Q_iso_kWh, Q_fria_kWh]
custos_mensais = [custo_mes_base, custo_mes_iso, custo_mes_fria]


def rotulo_variacao(i):
    # Texto da variação percentual em relação ao Cenário Base
    if i == 0:
        return "(referência)"
    if i == 1:
        return f"(−{formata_br(abs(var_iso_pct))}%)"
    return f"(+{formata_br(var_fria_pct)}%)"


def estiliza(ax, titulo, ylabel, ymax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylabel, fontsize=8.8, fontweight='bold', labelpad=6)
    ax.set_title(titulo, fontsize=9.5, fontweight='bold', pad=10,
                 color=COR_TEXTO)
    ax.grid(True, axis='y', linestyle=':', alpha=0.55, color=COR_GRADE)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', labelsize=7.8)
    ax.tick_params(axis='y', labelsize=8)


# --- Painel A: consumo energético diário ---
barras_a = ax_a.bar(cenarios, consumos_kwh, color=cores_barras, width=0.58,
                    edgecolor=COR_TEXTO, lw=0.7)
estiliza(ax_a, '(A) Energia dissipada por dia',
         'Energia dissipada [kWh/dia]', 13500)
ax_a.yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: formata_br(x, 0)))
for i, barra in enumerate(barras_a):
    ax_a.text(barra.get_x() + barra.get_width() / 2.0,
              barra.get_height() + 250.0,
              f"{formata_br(barra.get_height())} kWh\n{rotulo_variacao(i)}",
              ha='center', va='bottom', fontsize=7.6, fontweight='bold',
              color=cores_barras[i],
              bbox=dict(facecolor='white', edgecolor='none', pad=1.2,
                        alpha=0.85))

# --- Painel B: custo operacional mensal ---
barras_b = ax_b.bar(cenarios, custos_mensais, color=cores_barras,
                    width=0.58, edgecolor=COR_TEXTO, lw=0.7)
estiliza(ax_b, '(B) Custo mensal (R$ 0,75/kWh)',
         'Custo mensal [R$/mês]', 300000)
ax_b.yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: formata_br(x, 0, 'R$ ')))
for i, barra in enumerate(barras_b):
    ax_b.text(barra.get_x() + barra.get_width() / 2.0,
              barra.get_height() + 5500.0,
              f"{formata_br(barra.get_height(), 2, 'R$ ')}\n"
              f"{rotulo_variacao(i)}",
              ha='center', va='bottom', fontsize=7.6, fontweight='bold',
              color=cores_barras[i],
              bbox=dict(facecolor='white', edgecolor='none', pad=1.2,
                        alpha=0.85))

# Destaque da economia mensal do Cenário 1 (Painel B)
ax_b.text(1, 112000.0,
          f"Economia mensal:\n{formata_br(economia_mes_iso, 2, 'R$ ')}",
          ha='center', va='center', fontsize=7.6, fontweight='bold',
          color=COR_ISO,
          bbox=dict(boxstyle='round,pad=0.35', facecolor='#EAFAF1',
                    edgecolor=COR_ISO, linewidth=0.9, alpha=0.95))

if MOSTRAR_TITULO:
    fig2.suptitle('Comparativo energético e econômico dos cenários '
                  '(ODS 7 — Meta 7.3)', fontsize=10.5, fontweight='bold',
                  color=COR_TEXTO, y=0.99)
    fig2.tight_layout(rect=[0, 0, 1, 0.94])
else:
    fig2.tight_layout()

nome_fig2 = "figura2_comparativo_economico_ods7.png"
fig2.savefig(nome_fig2, dpi=300, facecolor='white')
plt.close(fig2)

# =============================================================================
# 7. RESUMO NO TERMINAL
# =============================================================================
print("-" * 78)
print("RELATORIO CONSOLIDADO - PROJETO CTEC/UFAL (ODS 7 - META 7.3)")
print("-" * 78)
print(f"Parametros do Tanque : A = {A:.2f} m2 | Tint = {Tint:.1f} C | "
      f"Ciclo = 24h (N = {N} passos)")
print(f"Premissas Financeiras: Tarifa = R$ {tarifa:.2f}/kWh | "
      f"{dias_mes} dias/mes")
print("-" * 78)
print(f"{'Cenario':<25} | {'Perda (GJ)':>10} | {'Consumo (kWh)':>14} | "
      f"{'Custo Mensal':>15} | {'Variacao':>10}")
print("-" * 78)
print(f"{'Cenario Base (U=12.0)':<25} | "
      f"{formata_br(Q_base_GJ, 2):>7} GJ | "
      f"{formata_br(Q_base_kWh, 2):>10} kWh | "
      f"{formata_br(custo_mes_base, 2, 'R$ '):>15} | {'Ref.':>10}")
print(f"{'Cenario 1 (Poliuretano)':<25} | "
      f"{formata_br(Q_iso_GJ, 2):>7} GJ | "
      f"{formata_br(Q_iso_kWh, 2):>10} kWh | "
      f"{formata_br(custo_mes_iso, 2, 'R$ '):>15} | "
      f"{formata_br(var_iso_pct, 2):>9}%")
print(f"{'Cenario 2 (Frente Fria)':<25} | "
      f"{formata_br(Q_fria_GJ, 2):>7} GJ | "
      f"{formata_br(Q_fria_kWh, 2):>10} kWh | "
      f"{formata_br(custo_mes_fria, 2, 'R$ '):>15} | "
      f"{'+' + formata_br(var_fria_pct, 2) + '%':>10}")
print("-" * 78)
print("GRAFICOS GERADOS COM SUCESSO (300 DPI):")
print(f"  [1] {nome_fig1}")
print(f"  [2] {nome_fig2}")
print("-" * 78)