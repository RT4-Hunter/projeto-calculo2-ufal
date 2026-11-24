# Modelagem Matemática e Simulação Numérica da Perda de Calor em Tanque de Armazenamento Industrial (ODS 7)

Repositório oficial dos códigos de simulação numérica desenvolvidos para o projeto da disciplina de **Cálculo 2** — Centro de Tecnologia (CTEC), **Universidade Federal de Alagoas (UFAL)**.

O trabalho modela o fluxo térmico transiente ao longo de um ciclo operacional de 24 horas em um tanque cilíndrico industrial aquecido, integrando a **Meta 7.3 do Objetivo de Desenvolvimento Sustentável 7 (ODS 7 — Energia Limpa e Acessível)** para avaliar o impacto energético e financeiro do isolamento térmico.

---

## Formulação Matemática e Parâmetros do Sistema

A energia térmica total perdida ($Q_{\text{total}}$, em Joules) ao longo de um dia ($t \in [0, 24]\text{ h}$) é dada pela integral definida da taxa instantânea de transferência de calor $q(t)$:

$$Q_{\text{total}} = 3600 \int_{0}^{24} U \cdot A \cdot \left[T_{\text{int}} - T_{\text{amb}}(t)\right] dt$$

Onde o perfil diário da temperatura ambiente (°C) segue a função periódica:

$$T_{\text{amb}}(t) = T_{\text{média}} + \Delta T \cdot \cos\left(\frac{\pi}{12}(t - 14)\right)$$

### Parâmetros Consolidados
* **Geometria do tanque (Normas API 650 / NBR 7821):** Raio $R = 8,0\text{ m}$, altura $H = 7,2\text{ m}$ e área superficial lateral/teto $A = 562,97\text{ m}^2$.
* **Condição interna:** Temperatura do fluido mantida em regime permanente a $T_{\text{int}} = 80,0\,^\circ\text{C}$.
* **Discretização numérica:** $N = 1000$ subintervalos ($\Delta t = 0,024\text{ h}$) integrados pela **Regra de 1/3 de Simpson composta**.
* **Premissas econômicas:** Tarifa industrial de $\text{R\$ } 0,75/\text{kWh}$ em operação contínua de $30\text{ dias/mês}$.

---

## Estrutura dos Arquivos

| Arquivo | Descrição | Saída Principal |
| :--- | :--- | :--- |
| `01_cenario_base.py` | Simulação do tanque sem isolamento ($U = 12,0\text{ W/m}^2\cdot^\circ\text{C}$) em clima padrão ($T_{\text{média}} = 27\,^\circ\text{C}$). | $30,94\text{ GJ/dia}$ ($8.593,17\text{ kWh/dia}$) |
| `02_validacao_analitica.py` | Verificação da precisão do integrador numérico frente à solução analítica exata de $\int_0^2 (3x^2 + 2x)\,dx = 12$. | Erro numérico $\approx 0$ |
| `03_comparacao_metodos.py` | Estudo de convergência entre a Regra de 1/3 de Simpson e a Regra dos Trapézios para $N \in \{12, 24, 48, 1000\}$. | Tabela comparativa de erros |
| `04_cenario1_poliuretano.py` | Simulação da Variação 1 com isolamento de poliuretano injetado ($U = 0,5\text{ W/m}^2\cdot^\circ\text{C}$). | $1,29\text{ GJ/dia}$ ($358,05\text{ kWh/dia}$) |
| `05_cenario2_frente_fria.py` | Simulação da Variação 2 sob frente fria climática ($T_{\text{média}} = 18\,^\circ\text{C}$) sem isolamento térmico. | $36,19\text{ GJ/dia}$ ($10.052,39\text{ kWh/dia}$) |
| `06_gerar_graficos.py` | Geração das curvas de perda térmica $q(t)$ em 24h e do comparativo energético e econômico mensal (300 dpi). | Figuras 1 e 2 (`PNG`) |

---

## Resumo dos Resultados (ODS 7 — Meta 7.3)

| Cenário Operacional | Coeficiente $U$ ($\text{W/m}^2\cdot^\circ\text{C}$) | Perda Diária ($\text{GJ}$) | Consumo Diário ($\text{kWh/dia}$) | Custo Mensal ($\text{R\$}$) | Variação vs. Base |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cenário Base** (Sem isolamento) | $12,0$ | $30,94$ | $8.593,17$ | $\text{R\$ } 193.346,40$ | Referência |
| **Cenário 1** (Poliuretano injetado) | $0,5$ | $1,29$ | $358,05$ | $\text{R\$ } 8.056,20$ | $-95,83\%$ |
| **Cenário 2** (Frente fria, $18\,^\circ\text{C}$) | $12,0$ | $36,19$ | $10.052,39$ | $\text{R\$ } 226.178,70$ | $+16,98\%$ |

---

## Instruções de Execução

1. **Pré-requisitos:** Certifique-se de ter o **Python 3.9+** instalado junto às bibliotecas científicas:
   ```bash
   pip install numpy scipy matplotlib
