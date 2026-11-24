import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

try:
    from scipy.integrate import simpson
except ImportError:
    from scipy.integrate import simps as simpson

# ==============================================================================
# 1. PARÂMETROS TERMOFÍSICOS, GEOMÉTRICOS E CLIMÁTICOS (PROJETO CTEC/UFAL - ODS 7)
# ==============================================================================
# Dimensões do tanque industrial cilíndrico vertical conforme API 650 / NBR 7821
A = 562.97     # Área superficial total de troca térmica (costado + teto) em m²
Tint = 80.0    # Temperatura do fluido interno mantida constante em regime de operação (°C)

# Discretização temporal do ciclo diário de 24 horas (N = 1000 subintervalos para Simpson 1/3)
t_inicio = 0.0
t_fim = 24.0
N = 1000
t = np.linspace(t_inicio, t_fim, N + 1)

# Coeficientes globais de transferência de calor em W/(m²·°C)
U_base = 12.0       # Cenário Base: Tanque em aço carbono sem isolamento
U_iso = 0.5         # Cenário 1: Isolamento com 50 mm de Poliuretano Injetado
U_fria = 12.0       # Cenário 2: Tanque sem isolamento sob evento de frente fria

# Modelagens senoidais das temperaturas ambientes diárias (°C) com pico às 14h00
Tamb_padrao = 27.0 + 4.0 * np.cos((np.pi / 12.0) * (t - 14.0))
Tamb_fria = 18.0 + 2.0 * np.cos((np.pi / 12.0) * (t - 14.0))

# ==============================================================================
# 2. CÁLCULO DAS TAXAS INSTANTÂNEAS E QUADRATURAS NUMÉRICAS (REGRA DE SIMPSON)
# ==============================================================================
# Taxas instantâneas q(t) em Watts (J/s) e conversão para kW
q_base_W = U_base * A * (Tint - Tamb_padrao)
q_iso_W = U_iso * A * (Tint - Tamb_padrao)
q_fria_W = U_fria * A * (Tint - Tamb_fria)

q_base_kW = q_base_W / 1000.0
q_iso_kW = q_iso_W / 1000.0
q_fria_kW = q_fria_W / 1000.0

# Quadratura numérica pelo método de 1/3 de Simpson composta (resultado em W·h)
int_base_Wh = simpson(q_base_W, x=t)
int_iso_Wh = simpson(q_iso_W, x=t)
int_fria_Wh = simpson(q_fria_W, x=t)

# Conversões para Joules (J), GigaJoules (GJ) e consumo diário em kWh
Q_base_J = int_base_Wh * 3600.0
Q_iso_J = int_iso_Wh * 3600.0
Q_fria_J = int_fria_Wh * 3600.0

Q_base_GJ = Q_base_J / 1e9
Q_iso_GJ = Q_iso_J / 1e9
Q_fria_GJ = Q_fria_J / 1e9

Q_base_kWh = int_base_Wh / 1000.0
Q_iso_kWh = int_iso_Wh / 1000.0
Q_fria_kWh = int_fria_Wh / 1000.0

# ==============================================================================
# 3. ANÁLISE ECONÔMICO-FINANCEIRA (TARIFAÇÃO E CUSTO MENSAL)
# ==============================================================================
# Premissas: Tarifa de R$ 0,75/kWh e ciclo operacional de 30 dias/mês
tarifa = 0.75
dias_mes = 30

# Arredondamento do custo diário em 2 casas decimais antes de multiplicar por 30
custo_dia_base = round(Q_base_kWh * tarifa, 2)
custo_mes_base = custo_dia_base * dias_mes

custo_dia_iso = round(Q_iso_kWh * tarifa, 2)
custo_mes_iso = custo_dia_iso * dias_mes

custo_dia_fria = round(Q_fria_kWh * tarifa, 2)
custo_mes_fria = custo_dia_fria * dias_mes

# Variações percentuais relativas ao Cenário Base
var_iso_pct = ((Q_iso_kWh - Q_base_kWh) / Q_base_kWh) * 100.0
var_fria_pct = ((Q_fria_kWh - Q_base_kWh) / Q_base_kWh) * 100.0

# Função utilitária para formatação no padrão brasileiro (milhar '.' e decimal ',')
def formata_br(valor, decimais=2, prefixo=""):
    if decimais == 0:
        texto = f"{valor:_.0f}"
    else:
        texto = f"{valor:_.{decimais}f}"
    return f"{prefixo}{texto.replace('.', ',').replace('_', '.')}"

# ==============================================================================
# 4. GERAÇÃO DA FIGURA 1: TAXA INSTANTÂNEA DE PERDA DE CALOR (24 HORAS)
# ==============================================================================
# Paleta de cores harmônica de engenharia
COR_BASE = '#1B4F72'       # Azul-marinho profundo (Cenário Base)
COR_ISO = '#1E8449'        # Verde-esmeralda (Cenário 1 - Eficiência Energética)
COR_FRIA = '#B03A2E'       # Vermelho-terracota (Cenário 2 - Frente Fria)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#7F8C8D'
plt.rcParams['axes.linewidth'] = 0.8

fig1, ax1 = plt.subplots(figsize=(9.5, 5))

# Plotagem das três curvas térmicas
ax1.plot(t, q_fria_kW, color=COR_FRIA, lw=2.4, label='Cenário 2 — Frente Fria sem Isolamento (U = 12,0 W/(m²·°C))')
ax1.fill_between(t, q_fria_kW, color=COR_FRIA, alpha=0.08)

ax1.plot(t, q_base_kW, color=COR_BASE, lw=2.4, label='Cenário Base — Sem Isolamento Térmico (U = 12,0 W/(m²·°C))')
ax1.fill_between(t, q_base_kW, color=COR_BASE, alpha=0.08)

ax1.plot(t, q_iso_kW, color=COR_ISO, lw=2.4, label='Cenário 1 — Poliuretano Injetado 50 mm (U = 0,5 W/(m²·°C))')
ax1.fill_between(t, q_iso_kW, color=COR_ISO, alpha=0.08)

# Limpeza e configuração dos eixos (estilo limpo de engenharia)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlim(0, 24)
ax1.set_ylim(0, 480)

ax1.set_xticks(np.arange(0, 25, 2))
ax1.set_xticklabels([f"{h:02d}h" for h in range(0, 25, 2)], fontsize=9.5)
ax1.set_yticks(np.arange(0, 501, 50))
ax1.set_yticklabels([f"{y}" for y in range(0, 501, 50)], fontsize=9.5)

ax1.set_xlabel('Horário do Dia ao Longo do Ciclo Operacional (horas)', fontsize=10.5, fontweight='bold', labelpad=8)
ax1.set_ylabel('Taxa Instantânea de Perda de Calor, q(t) [kW]', fontsize=10.5, fontweight='bold', labelpad=8)
ax1.set_title('Dinâmica da Taxa de Perda Térmica Instantânea em 24 Horas\nTanque Industrial API 650 (Tint = 80 °C, A = 562,97 m²)',
              fontsize=11.5, fontweight='bold', pad=12, color='#2C3E50')

ax1.grid(True, linestyle=':', alpha=0.4, color='#7F8C8D')

# Anotações discretas para pico (02h00) e vale (14h00) no Cenário Base
ax1.annotate('Pico térmico (02h00)\nMadrugada: q = 385,07 kW',
             xy=(2.0, 385.07), xytext=(2.6, 320.0),
             arrowprops=dict(arrowstyle='->', color=COR_BASE, lw=1.3, shrinkB=4),
             fontsize=8.5, fontweight='bold', color=COR_BASE,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#D5D8DC', alpha=0.9))

ax1.annotate('Vale térmico (14h00)\nMáx. radiação: q = 331,03 kW',
             xy=(14.0, 331.03), xytext=(12.0, 250.0),
             arrowprops=dict(arrowstyle='->', color=COR_BASE, lw=1.3, shrinkB=4),
             fontsize=8.5, fontweight='bold', color=COR_BASE,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#D5D8DC', alpha=0.9))

# Destaque visual demonstrando a redução de 95,83% no fluxo de calor
ax1.annotate('', xy=(20.5, 365.0), xytext=(20.5, 25.0),
             arrowprops=dict(arrowstyle='<->', color=COR_ISO, lw=1.8))
ax1.text(20.8, 195.0, 'Redução de 95,83%\nno fluxo de calor\n(Meta ODS 7.3)',
         fontsize=8.5, fontweight='bold', color=COR_ISO, va='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAFAF1', edgecolor=COR_ISO, alpha=0.95))

# Posicionamento da legenda em área totalmente livre (inferior esquerda)
ax1.legend(loc='lower left', bbox_to_anchor=(0.02, 0.08), frameon=True,
           facecolor='white', edgecolor='#D5D8DC', framealpha=0.95, fontsize=8.8)

fig1.tight_layout()
nome_fig1 = "figura1_taxa_calor_24h.png"
fig1.savefig(nome_fig1, dpi=300)
plt.close(fig1)

# ==============================================================================
# 5. GERAÇÃO DA FIGURA 2: COMPARATIVO ENERGÉTICO E ECONÔMICO (ODS 7)
# ==============================================================================
fig2, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 5))

cenarios = ['Cenário Base\n(Sem Isolamento)', 'Cenário 1\n(Poliuretano 50 mm)', 'Cenário 2\n(Frente Fria)']
cores_barras = [COR_BASE, COR_ISO, COR_FRIA]

consumos_kwh = [Q_base_kWh, Q_iso_kWh, Q_fria_kWh]
custos_mensais = [custo_mes_base, custo_mes_iso, custo_mes_fria]

# --- PAINEL A: CONSUMO ENERGÉTICO DIÁRIO ---
barras_a = ax_a.bar(cenarios, consumos_kwh, color=cores_barras, width=0.55, edgecolor='#2C3E50', lw=0.8)
ax_a.spines['top'].set_visible(False)
ax_a.spines['right'].set_visible(False)
ax_a.set_ylim(0, 13000)
ax_a.set_ylabel('Perda Térmica Diária Acumulada [kWh/dia]', fontsize=10.0, fontweight='bold', labelpad=8)
ax_a.set_title('(A) Consumo Energético Diário Dissipado', fontsize=11.0, fontweight='bold', pad=12, color='#2C3E50')
ax_a.grid(True, axis='y', linestyle=':', alpha=0.4, color='#7F8C8D')
ax_a.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x:_.0f}".replace('_', '.')))

# Rótulos de dados do Painel A com variações percentuais
for i, barra in enumerate(barras_a):
    altura = barra.get_height()
    valor_fmt = formata_br(altura, decimais=2)
    if i == 0:
        rotulo = f"{valor_fmt} kWh\n(Referência)"
        cor_rotulo = COR_BASE
    elif i == 1:
        rotulo = f"{valor_fmt} kWh\n({formata_br(var_iso_pct, 2)}%)"
        cor_rotulo = COR_ISO
    else:
        rotulo = f"{valor_fmt} kWh\n(+{formata_br(var_fria_pct, 2)}%)"
        cor_rotulo = COR_FRIA

    ax_a.text(barra.get_x() + barra.get_width() / 2.0, altura + 350.0,
              rotulo, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color=cor_rotulo)

# --- PAINEL B: CUSTO OPERACIONAL MENSAL ---
barras_b = ax_b.bar(cenarios, custos_mensais, color=cores_barras, width=0.55, edgecolor='#2C3E50', lw=0.8)
ax_b.spines['top'].set_visible(False)
ax_b.spines['right'].set_visible(False)
ax_b.set_ylim(0, 290000)
ax_b.set_ylabel('Custo Operacional Mensal Estimado [R$/mês]', fontsize=10.0, fontweight='bold', labelpad=8)
ax_b.set_title('(B) Impacto Financeiro Mensal (R$ 0,75/kWh)', fontsize=11.0, fontweight='bold', pad=12, color='#2C3E50')
ax_b.grid(True, axis='y', linestyle=':', alpha=0.4, color='#7F8C8D')
ax_b.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"R$ {x:_.0f}".replace('_', '.')))

# Rótulos de dados do Painel B com variações percentuais
for i, barra in enumerate(barras_b):
    altura = barra.get_height()
    valor_fmt = formata_br(altura, decimais=2, prefixo="R$ ")
    if i == 0:
        rotulo = f"{valor_fmt}\n(Referência)"
        cor_rotulo = COR_BASE
    elif i == 1:
        rotulo = f"{valor_fmt}\n({formata_br(var_iso_pct, 2)}%)"
        cor_rotulo = COR_ISO
    else:
        rotulo = f"{valor_fmt}\n(+{formata_br(var_fria_pct, 2)}%)"
        cor_rotulo = COR_FRIA

    ax_b.text(barra.get_x() + barra.get_width() / 2.0, altura + 7500.0,
              rotulo, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color=cor_rotulo)

fig2.suptitle('Análise Comparativa de Eficiência Energética e Viabilidade Econômica (ODS 7 — Meta 7.3)\nTanque Cilíndrico Vertical CTEC/UFAL (API 650)',
              fontsize=12.0, fontweight='bold', y=0.98, color='#1A252F')

fig2.tight_layout(rect=[0, 0, 1, 0.93])
nome_fig2 = "figura2_comparativo_economico_ods7.png"
fig2.savefig(nome_fig2, dpi=300)
plt.close(fig2)

# ==============================================================================
# 6. TABELA RESUMO NO TERMINAL (PADRÃO CONSOLIDADO DOS SCRIPTS 01 A 05)
# ==============================================================================
print("-" * 78)
print("RELATORIO CONSOLIDADO DE ENGENHARIA - PROJETO CTEC/UFAL (ODS 7 - META 7.3)")
print("-" * 78)
print(f"Parametros do Tanque : A = {A:.2f} m2 | Tint = {Tint:.1f} °C | Ciclo = 24h (N = {N} passos)")
print(f"Premissas Financeiras: Tarifa = R$ {tarifa:.2f}/kWh | {dias_mes} dias/mes")
print("-" * 78)
print(f"{'Cenario':<25} | {'Perda (GJ)':>10} | {'Consumo (kWh)':>14} | {'Custo Mensal':>15} | {'Variacao':>10}")
print("-" * 78)
print(f"{'Cenario Base (U=12.0)':<25} | {formata_br(Q_base_GJ, 2):>7} GJ | {formata_br(Q_base_kWh, 2):>10} kWh | {formata_br(custo_mes_base, 2, 'R$ '):>15} | {'Ref.':>10}")
print(f"{'Cenario 1 (Poliuretano)':<25} | {formata_br(Q_iso_GJ, 2):>7} GJ | {formata_br(Q_iso_kWh, 2):>10} kWh | {formata_br(custo_mes_iso, 2, 'R$ '):>15} | {formata_br(var_iso_pct, 2):>9}%")
print(f"{'Cenario 2 (Frente Fria)':<25} | {formata_br(Q_fria_GJ, 2):>7} GJ | {formata_br(Q_fria_kWh, 2):>10} kWh | {formata_br(custo_mes_fria, 2, 'R$ '):>15} | {f'+{formata_br(var_fria_pct, 2)}%':>10}")
print("-" * 78)
print("GRAFICOS GERADOS COM SUCESSO (PADRAO 300 DPI):")
print(f"  [1] {nome_fig1}")
print(f"  [2] {nome_fig2}")
print("-" * 78)
