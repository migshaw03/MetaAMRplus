import pandas as pd
import random

# -----------------------------
# USER PARAMETERS
# -----------------------------
metadata_file = "~/Desktop/plsdb_metadata/IMGPR_plasmid_data.tsv"  # path to your TSV metadata
output_file = "sampled_plasmids.txt"                              # output accession list
n_total = 200                                                      # total plasmids to sample
size_min = 50000                                                   # 50 kb
size_max = 500000                                                  # 500 kb
hosts_include = ["Escherichia coli", "Klebsiella pneumoniae", "Salmonella enterica",
                 "Enterobacter cloacae", "Proteus mirabilis"]
bla_genes = ["bla"]                                                # filter plasmids containing 'bla'
neg_control_fraction = 0.1                                         # fraction of negative controls (~10%)

# -----------------------------
# LOAD METADATA
# -----------------------------
df = pd.read_csv(metadata_file, sep='\t')

# Ensure 'size' column is numeric
df['size'] = pd.to_numeric(df['size'], errors='coerce')
df = df.dropna(subset=['size'])

# Fill missing ARGs column
df['ARGs'] = df['ARGs'].fillna('')

# -----------------------------
# FILTER POSITIVE PLASMIDS (at least one bla gene)
# -----------------------------
df_positive = df[
    (df['size'] >= size_min) &
    (df['size'] <= size_max) &
    (df['host'].isin(hosts_include)) &
    (df['ARGs'].str.contains('|'.join(bla_genes), case=False))
]

# -----------------------------
# FILTER NEGATIVE CONTROL PLASMIDS (no ARGs)
# -----------------------------
n_neg = int(n_total * neg_control_fraction)
df_negative_candidates = df[
    (df['size'] >= size_min) &
    (df['size'] <= size_max) &
    (df['host'].isin(hosts_include)) &
    (df['ARGs'].str.strip() == '')
]

# Randomly sample negative controls
df_negative = df_negative_candidates.sample(min(n_neg, len(df_negative_candidates)), random_state=42)

# -----------------------------
# SAMPLE POSITIVE PLASMIDS
# -----------------------------
n_positive = n_total - len(df_negative)
df_positive_sampled = df_positive.sample(min(n_positive, len(df_positive)), random_state=42)

# -----------------------------
# COMBINE POSITIVE + NEGATIVE
# -----------------------------
df_final = pd.concat([df_positive_sampled, df_negative]).reset_index(drop=True)

# -----------------------------
# OUTPUT LIST
# -----------------------------
df_final['accession'].to_csv(output_file, index=False, header=False)

print(f"Sampled {len(df_final)} plasmids ({len(df_positive_sampled)} positive, {len(df_negative)} negative).")
print(f"Accessions saved to {output_file}")
