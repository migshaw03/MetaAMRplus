import pandas as pd
import subprocess
import os

# -----------------------------
# Parameters
# -----------------------------
assembly_summary_file = "assembly_summary.txt"
min_size = 4_500_000       # 4.5 Mbp
max_size = 5_500_000       # 5.5 Mbp
species_include = ["Escherichia coli", "Salmonella enterica"]  # Optional species filter
n_genomes = 100
output_dir = "ncbigenomes"  # Folder to store downloaded genomes

# -----------------------------
# Load assembly summary
# -----------------------------
df = pd.read_csv(assembly_summary_file, sep='\t', skiprows=1, low_memory=False)

# Ensure genome size is numeric
df['total_length'] = pd.to_numeric(df['total_length'], errors='coerce')
df = df.dropna(subset=['total_length'])

# Filter by size
df_filtered = df[(df['total_length'] >= min_size) & (df['total_length'] <= max_size)]

# Optional: filter by species
df_filtered = df_filtered[df_filtered['organism_name'].isin(species_include)]

# Randomly sample N genomes
df_sampled = df_filtered.sample(n=min(n_genomes, len(df_filtered)), random_state=42)

print(f"Selected {len(df_sampled)} genomes for download.")

# Save assembly accessions
accession_file = "sampled_100_genomes.txt"
df_sampled['assembly_accession'].to_csv(accession_file, index=False, header=False)

# -----------------------------
# Create output directory
# -----------------------------
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Download genomes using ncbi-genome-download
# -----------------------------
subprocess.run([
    "ncbi-genome-download",
    "bacteria",
    "--assembly-accessions", accession_file,
    "--format", "fna",
    "-o", output_dir
])
