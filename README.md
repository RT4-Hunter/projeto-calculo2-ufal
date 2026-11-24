# Modelagem Matemática e Simulação Numérica da Perda de Calor em Tanque de Armazenamento Industrial (ODS 7)

Projeto desenvolvido na disciplina de **Cálculo 2 (Período 2026.2)** do **Centro de Tecnologia (CTEC)** da **Universidade Federal de Alagoas (UFAL)**.

## Integrantes do Grupo
* **David Willamys Claudino da Silva** — Engenharia Química
* **Giuliano de Carvalho Lima** — Engenharia Civil
* **Gustavo Epifanio de Barros Lima** — Engenharia Química
* **Robert Cavalcanti Lopes** — Engenharia Química
* **Samara Alves Melo de Almeida** — Engenharia de Petróleo

---

## Descrição do Projeto
Este repositório reúne os algoritmos em Python desenvolvidos para quantificar a perda térmica acumulada ao longo de um ciclo operacional de 24 horas em um tanque cilíndrico vertical de óleo combustível (Norma API 650 / NBR 7821, área superficial $A = 562,97\text{ m}^2$ e temperatura interna constante $T_{\text{int}} = 80\,^\circ\text{C}$), alinhado à **Meta 7.3 do ODS 7 (Eficiência Energética)**:

$$Q_{\text{total}} = 3600 \int_{0}^{24} U \cdot A \cdot [T_{\text{int}} - T_{\text{amb}}(t)]\,dt$$

A integração numérica é realizada via **Regra de 1/3 de Simpson composta** ($N = 1000$ subintervalos), acompanhada de validação analítica e análise de convergência frente à **Regra dos Trapézios**.

---

## Estrutura do Repositório

| Arquivo | Descrição | Principais Resultados |
| :--- | :--- | :--- |
| `01_cenario_base.py` | Simulação de referência do tanque em aço carbono sem isolamento ($U = 12,0\text{ W/m}^2\cdot^\circ\text{C}$). | **30,94 GJ** (`8.593,17 kWh/dia`) |
| `02_validacao_analitica.py` | Verificação numérica contra a integral exata $\int_0^2 (3x^2 + 2x)\,dx = 12$ para $N = 1000$. | Erro absoluto de **$1,78 \times 10^{-15}$** |
| `03_comparacao_metodos.py` | Estudo de convergência entre Simpson 1/3 e Trapézios para $N \in \{12, 24, 48, 1000\}$. | Desvio máximo de **$1,53 \times 10^{-5}\text{ J}$** |
| `04_cenario1_poliuretano.py` | Variação 1: aplicação de isolamento com poliuretano injetado ($U = 0,5\text{ W/m}^2\cdot^\circ\text{C}$). | **1,29 GJ** (`358,05 kWh/dia` — redução de **95,83%**) |
| `05_cenario2_frente_fria.py` | Variação 2: operação sem isolamento sob frente fria climática ($T_{\text{média}} = 18\,^\circ\text{C}$, amplitude $2\,^\circ\text{C}$). | **36,19 GJ** (`10.052,39 kWh/dia` — aumento de **16,98%**) |

---

## Como Executar os Códigos

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.10+** instalado e instale as bibliotecas científicas `numpy` e `scipy`:

```bash
pip install numpy scipy
```

### 2. Execução dos Scripts
Clone o repositório ou baixe os arquivos `.py` para uma mesma pasta, abra o terminal no diretório e execute cada script individualmente:

```bash
python 01_cenario_base.py
python 02_validacao_analitica.py
python 03_comparacao_metodos.py
python 04_cenario1_poliuretano.py
python 05_cenario2_frente_fria.py
```

Todos os parâmetros físicos e discretizações temporais já estão configurados no cabeçalho de cada arquivo, não sendo necessária nenhuma entrada manual via teclado.
