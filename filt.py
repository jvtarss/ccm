#!/usr/bin/env python3

import pandas as pd

# Caminho para o arquivo CSV original
input_file_path = 'runinfo.csv'

# Carregar o arquivo CSV
df = pd.read_csv(input_file_path)

# Filtrar as linhas que contêm os termos 'AMPLICON' e 'microbial fuel cell metagenome'
filtered_df = df[(df['LibraryStrategy'] == 'AMPLICON') & (df['ScientificName'] == 'microbial fuel cell metagenome')]

# Caminho para o novo arquivo CSV
output_file_path = 'filtered_runinfo.csv'

# Salvar o resultado em um novo arquivo CSV
filtered_df.to_csv(output_file_path, index=False)

print(f"Filtered data saved to {output_file_path}")
