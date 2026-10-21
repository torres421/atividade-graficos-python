from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_boxplot.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

departamentos = dados["departamento"].unique()
salarios = [
    dados.loc[dados["departamento"] == departamento, "salario"]
    for departamento in departamentos
]

fig, ax = plt.subplots(figsize=(9, 6))
# Os valores extremos permanecem nos dados e aparecem como pontos no boxplot.
ax.boxplot(salarios, patch_artist=True)
ax.set_xticks(range(1, len(departamentos) + 1), labels=departamentos)
ax.set_title("Distribuição dos salários por departamento")
ax.set_xlabel("Departamento")
ax.set_ylabel("Salário")
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
