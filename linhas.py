from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_linhas.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")
dados["data"] = pd.to_datetime(dados["data"], format="%Y-%m-%d")
dados = dados.sort_values("data")

fig, ax = plt.subplots(figsize=(11, 6))
# Cada loja tem observações em datas diferentes; usa apenas os pontos existentes.
for loja, grupo in dados.groupby("loja", sort=False):
    ax.plot(grupo["data"], grupo["vendas"], marker="o", markersize=4, label=loja)

ax.set_title("Vendas ao longo do tempo por loja")
ax.set_xlabel("Data")
ax.set_ylabel("Vendas")
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
ax.legend(title="Loja")
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()

plt.tight_layout()
plt.show()
