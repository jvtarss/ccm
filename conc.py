#!/usr/bin/env python3

import pandas as pd
import glob

combined_file = 'combined_reports.tabular'
df = pd.read_csv(combined_file, sep='\t', header=None)
df.columns = ['percentage', 'reads_clade', 'reads_taxon', 'rank', 'NCBI_taxon_ID', 'name']

total_reads = df['reads_clade'].sum()
df['normalized_reads'] = (df['reads_clade'] / total_reads) * 1e6

final_df = df.groupby(['NCBI_taxon_ID', 'name', 'rank']).agg({
    'normalized_reads': 'sum'
}).reset_index()

final_df = final_df.sort_values(by='normalized_reads', ascending=False)

final_df.to_csv('combined_normalized_report.csv', index=False)
