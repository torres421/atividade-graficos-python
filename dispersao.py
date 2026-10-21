from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_dispersao.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

fig, ax = plt.subplots(figsize=(9, 6))
for sexo, grupo in dados.groupby("sexo", sort=False):
    ax.scatter(grupo["altura_cm"], grupo["peso_kg"], s=40, alpha=0.7, label=sexo)

ax.set_title("Relação entre altura e peso")
ax.set_xlabel("Altura (cm)")
ax.set_ylabel("Peso (kg)")
ax.legend(title="Sexo")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
