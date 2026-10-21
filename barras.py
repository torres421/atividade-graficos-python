from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_barras.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

# Cada categoria possui uma venda média por região: exibe barras agrupadas.
tabela = dados.pivot(index="categoria", columns="regiao", values="vendas_medias")
tabela = tabela.reindex(
    index=dados["categoria"].unique(), columns=dados["regiao"].unique()
)

fig, ax = plt.subplots(figsize=(11, 6))
tabela.plot.bar(ax=ax, width=0.8, rot=0)
ax.set_title("Vendas médias por categoria e região")
ax.set_xlabel("Categoria")
ax.set_ylabel("Vendas médias")
ax.legend(title="Região")
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
