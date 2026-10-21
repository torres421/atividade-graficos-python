from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_heatmap.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

# Transforma os registros em uma matriz e mantém a ordem dos dias no CSV.
matriz = dados.pivot(
    index="dia_semana", columns="horario", values="movimento_clientes"
)
matriz = matriz.reindex(index=dados["dia_semana"].unique())

fig, ax = plt.subplots(figsize=(10, 6))
mapa = ax.imshow(matriz.to_numpy(), cmap="YlGnBu", aspect="auto")
ax.set_xticks(range(len(matriz.columns)), labels=matriz.columns)
ax.set_yticks(range(len(matriz.index)), labels=matriz.index)
ax.set_title("Movimento de clientes por dia e horário")
ax.set_xlabel("Horário")
ax.set_ylabel("Dia da semana")
fig.colorbar(mapa, ax=ax, label="Movimento de clientes")

for linha in range(len(matriz.index)):
    for coluna in range(len(matriz.columns)):
        numero = matriz.iloc[linha, coluna]
        cor = "white" if mapa.norm(numero) > 0.5 else "black"
        ax.text(coluna, linha, str(numero), ha="center", va="center", color=cor)

plt.tight_layout()
plt.show()
