# Modelagem Matemática e Simulação Numérica da Perda de Calor em Tanque de Armazenamento Industrial (ODS 7)

Repositório oficial dos códigos de simulação numérica desenvolvidos para o projeto da disciplina de **Cálculo 2** — Centro de Tecnologia (CTEC), **Universidade Federal de Alagoas (UFAL)**.

O trabalho modela o fluxo térmico transiente ao longo de um ciclo operacional de 24 horas em um tanque cilíndrico industrial aquecido, integrando a **Meta 7.3 do Objetivo de Desenvolvimento Sustentável 7 (ODS 7 — Energia Limpa e Acessível)** para avaliar o impacto energético e financeiro do isolamento térmico.

---

## Formulação Matemática e Parâmetros do Sistema

A energia térmica total perdida (*Q_total*, em Joules) ao longo de um dia (*t* ∈ [0, 24] h) é dada pela integral definida da taxa instantânea de transferência de calor *q(t)*:

$$Q_{\text{total}} = 3600 \int_{0}^{24} U \cdot A \cdot \left[T_{\text{int}} - T_{\text{amb}}(t)\right] dt$$

Onde o perfil diário da temperatura ambiente (°C) segue a função periódica:

$$T_{\text{amb}}(t) = T_{\text{média}} + \Delta T \cdot \cos\left(\frac{\pi}{12}(t - 14)\right)$$

### Parâmetros Consolidados
* **Geometria do tanque (Normas API 650 / NBR 7821):** Raio *R* = 8,0 m, altura *H* = 7,2 m e área superficial lateral/teto *A* = 562,97 m².
* **Condição interna:** Temperatura do fluido mantida em regime permanente a *T_int* = 80,0 °C.
* **Discretização numérica:** *N* = 1000 subintervalos (Δ*t* = 0,024 h) integrados pela **Regra de 1/3 de Simpson composta**.
* **Premissas econômicas:** Tarifa industrial de R$ 0,75/kWh em operação contínua de 30 dias/mês.

---

## Estrutura dos Arquivos

| Arquivo | Descrição | Saída Principal |
| :--- | :--- | :--- |
| `01_cenario_base.py` | Simulação do tanque sem isolamento (*U* = 12,0 W/m²·°C) em clima padrão (*T_média* = 27 °C). | 30,94 GJ/dia (8.593,17 kWh/dia) |
| `02_validacao_analitica.py` | Verificação da precisão do integrador numérico frente à solução analítica exata de ∫₀² (3x² + 2x) dx = 12. | Erro numérico ≈ 0 |
| `03_comparacao_metodos.py` | Estudo de convergência entre a Regra de 1/3 de Simpson e a Regra dos Trapézios para *N* ∈ {12, 24, 48, 1000}. | Tabela comparativa de erros |
| `04_cenario1_poliuretano.py` | Simulação da Variação 1 com isolamento de poliuretano injetado (*U* = 0,5 W/m²·°C). | 1,29 GJ/dia (358,05 kWh/dia) |
| `05_cenario2_frente_fria.py` | Simulação da Variação 2 sob frente fria climática (*T_média* = 18 °C) sem isolamento térmico. | 36,19 GJ/dia (10.052,39 kWh/dia) |
| `06_gerar_graficos.py` | Geração das curvas de perda térmica *q(t)* em 24h e do comparativo energético e econômico mensal (300 dpi). | Figuras 1 e 2 (`PNG`) |

---

## Resumo dos Resultados (ODS 7 — Meta 7.3)

| Cenário Operacional | Coeficiente *U* (W/m²·°C) | Perda Diária (GJ) | Consumo Diário (kWh/dia) | Custo Mensal (R$) | Variação vs. Base |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cenário Base** (Sem isolamento) | 12,0 | 30,94 | 8.593,17 | R$ 193.346,40 | Referência |
| **Cenário 1** (Poliuretano injetado) | 0,5 | 1,29 | 358,05 | R$ 8.056,20 | -95,83% |
| **Cenário 2** (Frente fria, 18 °C) | 12,0 | 36,19 | 10.052,39 | R$ 226.178,70 | +16,98% |

---

## Instruções de Execução

1. **Pré-requisitos:** Certifique-se de ter o **Python 3.9+** instalado junto às bibliotecas científicas:
   ```bash
   pip install numpy scipy matplotlib
