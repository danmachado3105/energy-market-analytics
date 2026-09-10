import pandas as pd

arquivo = "data/raw/samp-2026.csv"

dados = pd.read_csv(
    arquivo,
    encoding="latin1",
    sep=";",
    decimal=","
)

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