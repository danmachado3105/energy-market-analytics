import pandas as pd

arquivo = "data/raw/samp-2026.csv"

dados = pd.read_csv(
    arquivo,
    encoding="latin1",
    sep=";",
    decimal=","
)

dados["DatCompetencia"] = pd.to_datetime(dados["DatCompetencia"])

print("Quantidade de linhas:", len(dados))
print("Quantidade de colunas:", len(dados.columns))

print("\nInformações do dataset:")
print(dados.info())

print("\nValores ausentes:")
print(dados.isnull().sum())

print("\nDistribuidoras:")
print(dados["NomAgenteDistribuidora"].unique())

print("\nTipos de mercado:")
print(dados["NomTipoMercado"].unique())

print("\nClasses de consumo:")
print(dados["DscClasseConsumoMercado"].unique())

print("\nTop 10 distribuidoras por valor de mercado:")

ranking = (
    dados.groupby("NomAgenteDistribuidora")["VlrMercado"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(ranking)

print("\nValor de mercado por classe de consumo:")

mercado_por_classe = (
    dados.groupby("DscClasseConsumoMercado")["VlrMercado"]
    .sum()
    .sort_values(ascending=False)
)

print(mercado_por_classe)

print("\nValor de mercado por mês:")

mercado_por_mes = (
    dados.groupby("DatCompetencia")["VlrMercado"]
    .sum()
    .sort_index()
)

print(mercado_por_mes)

print("\nQuantidade de registros por mês:")

registros_por_mes = (
    dados.groupby("DatCompetencia")
    .size()
    .sort_index()
)

print(registros_por_mes)

dados_completos = dados[dados["DatCompetencia"] < "2026-07-01"]

print("\nEvolução do valor de mercado - dados completos:")

mercado_por_mes_completo = (
    dados_completos.groupby("DatCompetencia")["VlrMercado"]
    .sum()
    .sort_index()
)

print(mercado_por_mes_completo)

variacao_mensal = mercado_por_mes_completo.pct_change() * 100

print("\nVariação mensal do valor de mercado (%):")
print(variacao_mensal)

print("\nValor de mercado por mês e classe de consumo:")

mercado_mes_classe = (
    dados_completos
    .groupby(["DatCompetencia", "DscClasseConsumoMercado"])["VlrMercado"]
    .sum()
)

print(mercado_mes_classe)

tabela_mes_classe = mercado_mes_classe.unstack()

print(tabela_mes_classe)

participacao_mes_classe = (
    tabela_mes_classe
    .div(tabela_mes_classe.sum(axis=1), axis=0)
    * 100
)

print(participacao_mes_classe)

dados_industrial = dados_completos[
    dados_completos["DscClasseConsumoMercado"] == "Industrial"
]

industrial_por_distribuidora = (
    dados_industrial
    .groupby("NomAgenteDistribuidora")["VlrMercado"]
    .sum()
    .sort_values(ascending=False)
)

print(industrial_por_distribuidora.head(15))

industrial_mes_distribuidora = (
    dados_industrial
    .groupby(["DatCompetencia", "NomAgenteDistribuidora"])["VlrMercado"]
    .sum()
)

tabela_industrial = industrial_mes_distribuidora.unstack()

print(tabela_industrial)

queda_industrial = (
    tabela_industrial.loc[pd.Timestamp("2026-05-01")]
    - tabela_industrial.loc[pd.Timestamp("2026-04-01")]
).sort_values()

print("\nMaiores quedas no valor de mercado industrial:")
print(queda_industrial.head(15))

cemig_industrial = dados_completos[
    (dados_completos["NomAgenteDistribuidora"] == "CEMIG DISTRIBUIÇÃO S.A") &
    (dados_completos["DscClasseConsumoMercado"] == "Industrial")
]

cemig_por_tipo = (
    cemig_industrial
    .groupby(["DatCompetencia", "NomTipoMercado"])["VlrMercado"]
    .sum()
    .unstack()
)

print("\nCEMIG - Industrial por tipo de mercado:")
print(cemig_por_tipo)

cemig_regular = cemig_industrial[
    cemig_industrial["NomTipoMercado"] == "Regular"
]

cemig_regular_tarifa = (
    cemig_regular
    .groupby(["DatCompetencia", "DscModalidadeTarifaria"])["VlrMercado"]
    .sum()
    .unstack()
)

print("\nCEMIG - Industrial - Regular por modalidade tarifária:")
print(cemig_regular_tarifa)

cemig_regular_azul_verde = cemig_regular[
    cemig_regular["DscModalidadeTarifaria"].isin(["Azul", "Verde"])
]

cemig_subgrupo = (
    cemig_regular_azul_verde
    .groupby(
        ["DatCompetencia", "DscModalidadeTarifaria", "DscSubGrupoTarifario"]
    )["VlrMercado"]
    .sum()
    .unstack()
)

print("\nCEMIG - Industrial - Regular - Azul/Verde por subgrupo:")
print(cemig_subgrupo)