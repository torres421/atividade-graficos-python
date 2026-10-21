from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_frequencia.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

# Conta os tipos de atendimento; id_chamado identifica cada registro.
frequencias = dados["tipo_atendimento"].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
barras = ax.bar(frequencias.index, frequencias.values, color="steelblue")
ax.bar_label(barras, padding=3)
ax.set_title("Frequência dos tipos de atendimento")
ax.set_xlabel("Tipo de atendimento")
ax.set_ylabel("Frequência (número de chamados)")
ax.set_ylim(0, frequencias.max() * 1.15)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
