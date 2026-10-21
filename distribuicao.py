from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_distribuicao.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

fig, ax = plt.subplots(figsize=(9, 6))
# Analisa as idades; cliente_id é apenas um identificador.
# A regra de Sturges escolhe o número de intervalos a partir do tamanho da amostra.
ax.hist(dados["idade"], bins="sturges", color="steelblue", edgecolor="white")
ax.set_title("Distribuição das idades dos clientes")
ax.set_xlabel("Idade (anos)")
ax.set_ylabel("Frequência (número de clientes)")
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
