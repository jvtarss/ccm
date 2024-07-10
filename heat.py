#!/usr/bin/env python3

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np

# Função para carregar e processar os dados de um arquivo de report do Kraken2
def load_kraken2_report(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None)
    df.columns = ['percentage', 'reads_clade', 'reads_taxon', 'rank', 'NCBI_taxon_ID', 'name']
    return df

# Caminho para a pasta contendo os arquivos de report do Kraken2
report_dir = '/home/jvtars/Kraken2 on collection 2040: Report'

# Listar todos os arquivos .tabular na pasta
report_files = [os.path.join(report_dir, file) for file in os.listdir(report_dir) if file.endswith('.tabular')]

# Carregar todos os reports
dfs = [load_kraken2_report(file) for file in report_files]

# Filtrar apenas os filos
phylum_dfs = [df[df['rank'] == 'P'] for df in dfs]

# Criar uma matriz de co-ocorrência
phylum_names = set()
for df in phylum_dfs:
    phylum_names.update(df['name'])

phylum_names = list(phylum_names)
co_occurrence_matrix = pd.DataFrame(0, index=phylum_names, columns=phylum_names)

# Preencher a matriz de co-ocorrência
for df in phylum_dfs:
    present_phyla = df['name'].tolist()
    for phylum1, phylum2 in combinations(present_phyla, 2):
        co_occurrence_matrix.loc[phylum1, phylum2] += 1
        co_occurrence_matrix.loc[phylum2, phylum1] += 1

# Normalizar os dados para uma escala de 0 a 1
co_occurrence_matrix = co_occurrence_matrix.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

# Ordenar os filos por co-ocorrência total
phylum_order = co_occurrence_matrix.sum(axis=1).sort_values(ascending=False).index
co_occurrence_matrix = co_occurrence_matrix.loc[phylum_order, phylum_order]

# Gerar o heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(co_occurrence_matrix, cmap='Spectral', annot=False)
plt.title('Heatmap de Co-ocorrência de Filos (Normalizado)')
plt.show()
