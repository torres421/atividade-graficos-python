from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


st.set_page_config(
    page_title="Dashboard - Atividade 06",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Informações do aluno")
st.sidebar.write("**Nome:** Luca Torres Castanheira")
st.sidebar.write("**Número da chamada:** 33")
st.sidebar.write("**Turma:** 3D1")

st.title("Dashboard de Análise de Dados")
st.caption("Atividade 06 - Visualização de Dados")
st.divider()

pasta = Path(__file__).resolve().parent


def numero(valor, casas=2):
    """Formata os números das análises com vírgula decimal."""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Primeira linha: heatmap, linhas e pizza.
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Heatmap")
    dados = pd.read_csv(pasta / "dados_heatmap.csv", sep=",", encoding="utf-8")
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
            quantidade = matriz.iloc[linha, coluna]
            cor = "white" if mapa.norm(quantidade) > 0.5 else "black"
            ax.text(
                coluna, linha, str(quantidade), ha="center", va="center", color=cor
            )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    maior = dados.loc[dados["movimento_clientes"].idxmax()]
    menor = dados.loc[dados["movimento_clientes"].idxmin()]
    st.markdown(
        f"**Análise:** O maior movimento é de {maior['movimento_clientes']} clientes, "
        f"em {maior['dia_semana']} às {maior['horario']}. "
        f"O menor é de {menor['movimento_clientes']} clientes, "
        f"em {menor['dia_semana']} às {menor['horario']}."
    )

with col2:
    st.subheader("Gráfico de linhas")
    dados = pd.read_csv(pasta / "dados_linhas.csv", sep=",", encoding="utf-8")
    dados["data"] = pd.to_datetime(dados["data"], format="%Y-%m-%d")
    dados = dados.sort_values("data")

    fig, ax = plt.subplots(figsize=(11, 6))
    # Cada loja usa somente as datas em que possui observações.
    for loja, grupo in dados.groupby("loja", sort=False):
        ax.plot(
            grupo["data"], grupo["vendas"], marker="o", markersize=4, label=loja
        )

    ax.set_title("Vendas ao longo do tempo por loja")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendas")
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    ax.legend(title="Loja")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    medias_mensais = dados.groupby(dados["data"].dt.to_period("M"))["vendas"].mean()
    maior = dados.loc[dados["vendas"].idxmax()]
    st.markdown(
        f"**Análise:** A média das vendas registradas passa de "
        f"{numero(medias_mensais.iloc[0])} em {medias_mensais.index[0].strftime('%m/%Y')} "
        f"para {numero(medias_mensais.iloc[-1])} em "
        f"{medias_mensais.index[-1].strftime('%m/%Y')}. "
        f"O maior valor é {numero(maior['vendas'])}, na {maior['loja']} "
        f"em {maior['data'].strftime('%d/%m/%Y')}."
    )

with col3:
    st.subheader("Gráfico de pizza")
    dados = pd.read_csv(pasta / "dados_pizza.csv", sep=",", encoding="utf-8")

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
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    maior = dados.loc[dados["faturamento"].idxmax()]
    menor = dados.loc[dados["faturamento"].idxmin()]
    participacao = maior["faturamento"] / dados["faturamento"].sum() * 100
    st.markdown(
        f"**Análise:** O canal {maior['canal_venda']} possui o maior faturamento, "
        f"com {numero(maior['faturamento'])}, equivalente a {numero(participacao, 1)}% "
        f"do total. O canal {menor['canal_venda']} tem o menor faturamento, "
        f"com {numero(menor['faturamento'])}."
    )

st.divider()

# Segunda linha: regressão, barras e boxplot.
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Regressão linear")
    dados = pd.read_csv(pasta / "dados_regressao.csv", sep=",", encoding="utf-8")
    coeficientes = np.polyfit(dados["renda_mensal"], dados["gasto_mensal"], deg=1)
    rendas = np.linspace(
        dados["renda_mensal"].min(), dados["renda_mensal"].max(), 100
    )
    gastos_estimados = np.polyval(coeficientes, rendas)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(
        dados["renda_mensal"], dados["gasto_mensal"], alpha=0.7, label="Dados originais"
    )
    ax.plot(
        rendas, gastos_estimados, color="crimson", linewidth=2, label="Regressão linear"
    )
    ax.set_title("Relação entre renda mensal e gasto mensal")
    ax.set_xlabel("Renda mensal")
    ax.set_ylabel("Gasto mensal")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    correlacao = dados["renda_mensal"].corr(dados["gasto_mensal"])
    st.markdown(
        f"**Análise:** A correlação entre renda e gasto mensal é "
        f"{numero(correlacao)}, indicando que rendas maiores tendem a acompanhar "
        f"gastos maiores nesta amostra. A reta ajustada estima um aumento de "
        f"{numero(coeficientes[0] * 100)} no gasto para cada 100 de aumento na renda."
    )

with col5:
    st.subheader("Gráfico de barras")
    dados = pd.read_csv(pasta / "dados_barras.csv", sep=",", encoding="utf-8")
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
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    maior = dados.loc[dados["vendas_medias"].idxmax()]
    menor = dados.loc[dados["vendas_medias"].idxmin()]
    st.markdown(
        f"**Análise:** A maior venda média é de {numero(maior['vendas_medias'])}, "
        f"na categoria {maior['categoria']} da região {maior['regiao']}. "
        f"A menor é de {numero(menor['vendas_medias'])}, "
        f"em {menor['categoria']} na região {menor['regiao']}."
    )

with col6:
    st.subheader("Boxplot")
    dados = pd.read_csv(pasta / "dados_boxplot.csv", sep=",", encoding="utf-8")
    departamentos = dados["departamento"].unique()
    salarios = [
        dados.loc[dados["departamento"] == departamento, "salario"]
        for departamento in departamentos
    ]

    fig, ax = plt.subplots(figsize=(9, 6))
    # Mantém os salários extremos, assim como no script original.
    ax.boxplot(salarios, patch_artist=True)
    ax.set_xticks(range(1, len(departamentos) + 1), labels=departamentos)
    ax.set_title("Distribuição dos salários por departamento")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Salário")
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    medianas = dados.groupby("departamento")["salario"].median()
    st.markdown(
        f"**Análise:** {medianas.idxmax()} apresenta a maior mediana salarial "
        f"({numero(medianas.max())}), enquanto {medianas.idxmin()} apresenta a menor "
        f"({numero(medianas.min())}). Os pontos fora das caixas e dos limites "
        f"indicam salários mais afastados dos demais em cada departamento."
    )

st.divider()

# Terceira linha: dispersão, distribuição e frequência.
col7, col8, col9 = st.columns(3)

with col7:
    st.subheader("Gráfico de dispersão")
    dados = pd.read_csv(pasta / "dados_dispersao.csv", sep=",", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 6))
    for sexo, grupo in dados.groupby("sexo", sort=False):
        ax.scatter(
            grupo["altura_cm"], grupo["peso_kg"], s=40, alpha=0.7, label=sexo
        )

    ax.set_title("Relação entre altura e peso")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(title="Sexo")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    correlacao = dados["altura_cm"].corr(dados["peso_kg"])
    st.markdown(
        f"**Análise:** Altura e peso apresentam correlação de {numero(correlacao)}: "
        f"pessoas mais altas tendem a apresentar maior peso nesta amostra. "
        f"Os pesos variam de {numero(dados['peso_kg'].min(), 1)} a "
        f"{numero(dados['peso_kg'].max(), 1)} kg."
    )

with col8:
    st.subheader("Distribuição / Histograma")
    dados = pd.read_csv(pasta / "dados_distribuicao.csv", sep=",", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 6))
    # Usa idade, sem incluir o identificador cliente_id na distribuição.
    ax.hist(dados["idade"], bins="sturges", color="steelblue", edgecolor="white")
    ax.set_title("Distribuição das idades dos clientes")
    ax.set_xlabel("Idade (anos)")
    ax.set_ylabel("Frequência (número de clientes)")
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    ate_30 = dados["idade"].le(30).sum()
    percentual = ate_30 / len(dados) * 100
    st.markdown(
        f"**Análise:** As idades variam de {dados['idade'].min()} a "
        f"{dados['idade'].max()} anos, com mediana de "
        f"{numero(dados['idade'].median(), 1)} anos. "
        f"Há {ate_30} clientes com até 30 anos ({numero(percentual, 1)}% do total)."
    )

with col9:
    st.subheader("Gráfico de frequência")
    dados = pd.read_csv(pasta / "dados_frequencia.csv", sep=",", encoding="utf-8")
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
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    participacao = frequencias.max() / frequencias.sum() * 100
    st.markdown(
        f"**Análise:** {frequencias.idxmax()} é o tipo mais frequente, "
        f"com {frequencias.max()} chamados ({numero(participacao, 1)}% do total). "
        f"{frequencias.idxmin()} é o menos frequente, com {frequencias.min()} chamados."
    )
