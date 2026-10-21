from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados_regressao.csv"
dados = pd.read_csv(arquivo, sep=",", encoding="utf-8")

# Ajusta uma reta: gasto mensal = coeficiente * renda mensal + intercepto.
coeficientes = np.polyfit(dados["renda_mensal"], dados["gasto_mensal"], deg=1)
rendas = np.linspace(dados["renda_mensal"].min(), dados["renda_mensal"].max(), 100)
gastos_estimados = np.polyval(coeficientes, rendas)

fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(dados["renda_mensal"], dados["gasto_mensal"], alpha=0.7, label="Dados originais")
ax.plot(rendas, gastos_estimados, color="crimson", linewidth=2, label="Regressão linear")
ax.set_title("Relação entre renda mensal e gasto mensal")
ax.set_xlabel("Renda mensal")
ax.set_ylabel("Gasto mensal")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
