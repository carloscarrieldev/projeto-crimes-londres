# BIBLIOTECAS
from google.cloud import bigquery
import pandas as pd
import sys

# CONFIGURAÇÃO

# Escolhendo o projeto
PROJECT_ID = 'projeto-ebac-512120'
# Selecionando tabela
TABLE  = "bigquery-public-data.london_crime.crime_by_lsoa"
# Região da tabela
DATASET_LOCATION = "EU"

# Criando um chamado ao BigQuery com Projeto
client = bigquery.Client(project=PROJECT_ID)

#  Criando uma função para execução dos códigos
def run_query(query: str) -> bigquery.job.QueryJob:
    if DATASET_LOCATION:
    #  Executa a consulta em SQL com a localização definida
        return client.query(query,location=DATASET_LOCATION)
    else:
    # Caso der erro retorna sem a localização
        return client.query(query)

# CONSULTAS

# Consutando tabela para visualização'
crimes = f'''SELECT 
* FROM {TABLE}
LIMIT 30
'''

df_londres = run_query(crimes).to_dataframe()
print('Tabela dos crimes:', df_londres.to_string(index=False))

# Visualizando quantidade de registro na tabela londres
registros = f'''
SELECT COUNT(*) 
FROM {TABLE}
'''

df_reg = run_query(registros).to_dataframe()
print('Total de registro em crimes:', df_reg.to_string(index=False))

# Criando dados brutos 
crimes_bruto = f'''
SELECT * 
FROM {TABLE}'''

df_completo = run_query(crimes_bruto).to_dataframe()

# LIMPEZA

# Criando uma copia para limpeza dos dados
df_limpo = df_completo.copy()

# Exbindo dados e colunas da tabela
print('Colunas na tabela:', df_completo.columns)
print('Tipos de dados:\n', df_completo.dtypes)

# Verificando valores nulos e duplicados + Estrutura
print('Nulos:', df_completo.isnull().sum())
print('Duplicados:', df_completo.duplicated().sum())
print('Estrutura da tabela:', df_completo.shape)

# Verificando colunas com '-' ou '_'
colunas = f''' SELECT DISTINCT *
FROM `{TABLE}`
WHERE REGEXP_CONTAINS (lsoa_code, r'[-_]')
OR REGEXP_CONTAINS (borough, r'[-_]')
OR REGEXP_CONTAINS(major_category, r'[-_]')
OR REGEXP_CONTAINS(minor_category, r'[-_]')
'''

df_col = run_query(colunas).to_dataframe()
print('Colunas com hifen:', df_col)

# SALVANDO

# Criando dados brutos da tabela
df_completo.to_csv('Output/crimes/DadosCrimes_Brutos.csv', index=False)
# Criando arquivo limpo após analise
df_limpo.to_csv('Output/crimes/DadosCrimes_Limpo.csv', index=False)