from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_pizza.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

fig, ax = plt.subplots(figsize=(8, 7))
ax.pie(
    dados["faturamento"],
    labels=dados["canal_venda"],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white"},
)
ax.set_title("Participação de cada canal de venda no faturamento")
ax.axis("equal")

plt.tight_layout()
plt.show()
