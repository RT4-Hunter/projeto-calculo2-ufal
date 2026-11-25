# Perda de calor em tanque de armazenamento industrial (ODS 7)

Projeto de Modelagem Matemática e Integração Numérica da disciplina de **Cálculo 2**
(CTEC/UFAL, período 2026.2).

O projeto calcula a energia térmica perdida ao longo de um ciclo de 24 horas por um
tanque cilíndrico vertical (normas API 650 e ABNT NBR 7821), usando a **Regra de 1/3 de
Simpson composta**, e relaciona o resultado à **Meta 7.3 do ODS 7** (eficiência
energética).

## Integrantes

- David Willamys Claudino da Silva (Eng. Química)
- Giuliano de Carvalho Lima (Eng. Civil)
- Gustavo Epifanio de Barros Lima (Eng. Química)
- Robert Cavalcanti Lopes (Eng. Química)
- Samara Alves Melo de Almeida (Eng. de Petróleo)

## Modelo matemático

```
q(t) = U · A · (Tint − Tamb(t))                       [W]
Tamb(t) = Tmédia + ΔT · cos[(π/12) · (t − 14)]        [°C]   (pico às 14h00)
Q(W·h) = ∫₀²⁴ q(t) dt                                 [W·h]
Q(J) = 3600 · Q(W·h)                                  [J]    (1 W·h = 3600 J)
Forma fechada: Q(W·h) = 24 · U · A · (Tint − Tmédia)
```

Como a integral do cosseno em um período completo (24 h) é nula, a energia diária depende
apenas de Tmédia, e não de ΔT.

## Parâmetros

| Parâmetro | Valor |
|---|---|
| Área de troca A (costado + teto) | 562,97 m² (D = 16 m, H = 7,2 m, base isolada) |
| Temperatura interna Tint | 80 °C (constante) |
| Subintervalos de Simpson | N = 1000 (h = 0,024 h) |
| Tarifa | R$ 0,75/kWh |
| Regime | 24 h/dia, 30 dias/mês (custo diário arredondado em 2 casas antes de × 30) |

## Resultados de referência

| Cenário | U [W/(m²·°C)] | Tmédia / ΔT [°C] | Perda (GJ/dia) | Consumo (kWh/dia) | Custo mensal (R$) | Variação |
|---|---|---|---|---|---|---|
| Base (sem isolamento) | 12,0 | 27 / 4 | 30,94 | 8.593,17 | 193.346,40 | — |
| Cenário 1 (poliuretano 50 mm) | 0,5 | 27 / 4 | 1,29 | 358,05 | 8.056,20 | −95,83% |
| Cenário 2 (frente fria, sem isolamento) | 12,0 | 18 / 2 | 36,19 | 10.052,39 | 226.178,70 | +16,98% |
| Referência: lã de rocha 30 mm | 1,2 | 27 / 4 | 3,09 | 859,32 | 19.334,70 | — |

Validação numérica: erro absoluto de 1,78 × 10⁻¹⁵ na integral de teste
(f(x) = 3x² + 2x em [0, 2], valor exato 12,0) e desvio máximo de 1,53 × 10⁻⁵ J entre
Simpson e Trapézios (N = 12, 24, 48 e 1000), que é ruído de arredondamento de ponto
flutuante.

## Scripts

| Arquivo | O que faz |
|---|---|
| `01_cenario_base.py` | Cenário Base: integra q(t) por Simpson e imprime a energia em J, GJ e kWh |
| `02_validacao_analitica.py` | Valida o Simpson com f(x) = 3x² + 2x em [0, 2] (valor exato 12,0) |
| `03_comparacao_metodos.py` | Simpson vs. Trapézios (N = 12, 24, 48, 1000) comparados com a forma fechada; testes com 3x² + 2x e eˣ para mostrar a ordem de convergência |
| `04_cenario1_poliuretano.py` | Cenário 1: poliuretano injetado (U = 0,5) |
| `05_cenario2_frente_fria.py` | Cenário 2: frente fria (Tmédia = 18 °C, ΔT = 2 °C) |
| `06_gerar_graficos.py` | Gera as Figuras 1 e 2 do relatório (matplotlib) |
| `07_custos_e_resumo.py` | Custos em R$, percentuais, lã de rocha, picos e vales de q(t) e erro em relação à forma fechada |

## Como executar

Requisitos: Python 3.8 ou superior com NumPy, SciPy e Matplotlib.

```bash
git clone https://github.com/RT4-Hunter/projeto-calculo2-ufal.git
cd projeto-calculo2-ufal
pip install numpy scipy matplotlib
python 01_cenario_base.py
python 02_validacao_analitica.py
python 03_comparacao_metodos.py
python 04_cenario1_poliuretano.py
python 05_cenario2_frente_fria.py
python 06_gerar_graficos.py
python 07_custos_e_resumo.py
```

Os números são impressos no formato brasileiro (ponto como separador de milhar e vírgula
como separador decimal). Os scripts funcionam com versões antigas do SciPy, que usam
`simps` no lugar de `simpson`.

## Limitações do modelo

- Quase-estacionário: não considera a inércia térmica do fluido nem das chapas metálicas.
- Temperatura interna (80 °C) e coeficiente global U constantes.
- Radiação solar direta e vento não entram como termos independentes.
- A base do tanque é considerada isolada, então não há perda pelo solo.
- Eficiência unitária do reaquecimento (η = 1); para η < 1, consumo e custo crescem
  proporcionalmente a 1/η. Os valores obtidos são, portanto, limites inferiores.
- Considera apenas o custo operacional de energia, sem o investimento (CAPEX) do isolante.

## Uso de Inteligência Artificial

Ferramentas de IA generativa (ChatGPT, Google Gemini, Google Antigravity e Claude) foram
usadas como apoio para revisão de texto, estruturação de scripts de visualização,
verificação de consistência e reformulação de trechos do relatório. A modelagem, a
escolha dos parâmetros, a execução das simulações e a interpretação dos resultados foram
conduzidas e revisadas pelos autores.
