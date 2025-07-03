import pandas as pd
import re

## LIMPA data_raw2.csv

data = {
    "party": [
        "PSL", "PATRIOTA", "DEM", "PSC", "NOVO", "PSDB", "MDB", "PP",
        "REPUBLICANOS", "PL", "PSD", "PTB", "SOLIDARIEDADE", "CIDADANIA",
        "PODEMOS", "PROS", "AVANTE", "PV", "PDT", "PSB", "REDE",
        "PCDOB", "PT", "PSOL"
    ],
    "alignment_with_bolsonaro_government_perc": [
        97, 94, 93, 93, 92, 92, 91, 91, 91, 90, 90, 90, 89, 87,
        77, 75, 74, 68, 48, 46, 36, 29, 20, 15
    ],
    "government_or_opposition_position": [
        "Governo", "Governo", "Governo", "Governo",
        "Governo", "Governo", "Governo", "Governo",
        "Governo", "Governo", "Governo", "Governo",
        "Governo", "Governo", "Neutro", "Neutro",
        "Neutro", "Neutro", "Oposição", "Oposição", "Oposição",
        "Oposição", "Oposição", "Oposição"
    ],
}

df_party_alignment = pd.DataFrame(data)
df_termos = pd.read_csv('covid_terms.csv')
df_tweets = pd.read_csv('../data/data_raw2.csv')

df_tweets = df_tweets.merge(df_party_alignment, left_on='sigla_partido', right_on='party', how='left')
df_tweets['government_or_opposition_position'] = df_tweets['government_or_opposition_position'].fillna('Desconhecido')


filter_terms = df_termos['Keywords'].str.cat(sep='; ').split(';')
filter_terms = [s.strip() for s in filter_terms]
filter_terms = list(filter(None, filter_terms))


df_tweets = df_tweets[df_tweets.text.str.contains('|'.join(filter_terms), regex=True, na=False, flags=re.IGNORECASE)]


df_tweets.to_csv('dados_filtrados.csv', index=False)