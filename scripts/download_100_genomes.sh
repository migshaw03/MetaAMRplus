#!/bin/bash
set -e

# -----------------------------
# Parameters
# -----------------------------
ASSEMBLY_SUMMARY="assembly_summary.txt"
OUTPUT_DIR="ncbigenomes"
SAMPLE_SIZE=100
SPECIES_REGEX="Escherichia coli|Salmonella enterica|^Shigella|^Enterobacter|^Klebsiella"

# -----------------------------
# 1️⃣ Fresh download of assembly summary
# -----------------------------
echo "[1/5] Downloading RefSeq bacterial assembly summary..."
wget -nc ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt

# -----------------------------
# 2️⃣ Filter assemblies by size, species, and valid FTP
# -----------------------------
echo "[2/5] Filtering assemblies by size (4.5–5.5 Mbp) and species..."
awk -F'\t' -v regex="$SPECIES_REGEX" 'NR>1 && $27>=4500000 && $27<=5500000 && $20!="" && $8 ~ regex {print $1}' $ASSEMBLY_SUMMARY > filtered_accessions.txt

filtered_count=$(wc -l < filtered_accessions.txt)
echo "Filtered genomes available: $filtered_count"

if [ "$filtered_count" -lt "$SAMPLE_SIZE" ]; then
    echo "Warning: Only $filtered_count genomes available, less than requested $SAMPLE_SIZE. Will download all available."
    SAMPLE_SIZE=$filtered_count
fi

# -----------------------------
# 3️⃣ Randomly sample 100 genomes (or all if fewer available)
# -----------------------------
echo "[3/5] Randomly sampling $SAMPLE_SIZE genomes..."
shuf -n $SAMPLE_SIZE filtered_accessions.txt > sampled_100_genomes.txt
echo "Sampled genomes: $(wc -l < sampled_100_genomes.txt)"

# -----------------------------
# 4️⃣ Prepare output folder
# -----------------------------
echo "[4/5] Preparing download folder..."
rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

# -----------------------------
# 5️⃣ Download genome FASTAs
# -----------------------------
echo "[5/5] Downloading genome FASTAs into $OUTPUT_DIR..."
while read accession; do
    # Get FTP path
    ftp=$(awk -F'\t' -v acc="$accession" '$1==acc {print $20}' $ASSEMBLY_SUMMARY)
    if [ -n "$ftp" ]; then
        filename=$(basename $ftp)
        wget -q -O "$OUTPUT_DIR/${filename}.fna.gz" "${ftp}/${filename}_genomic.fna.gz"
    else
        echo "Skipping $accession: no FTP path found"
    fi
done < sampled_100_genomes.txt

echo "Download complete. Check $OUTPUT_DIR for genome FASTA files."
