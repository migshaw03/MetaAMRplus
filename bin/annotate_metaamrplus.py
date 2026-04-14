#!/usr/bin/env python3
import sys
import os

# -----------------------------
# Detect BLAST database path
# -----------------------------
db_dir = os.environ.get("METAAMRPLUS_DB")

if db_dir is None:
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        db_dir = os.path.join(
            conda_prefix,
            "share",
            "metaamrplus",
            "db",
            "MetaAMRplus_DB_v1.0"
        )
    else:
        db_dir = None

if db_dir is None or not os.path.exists(db_dir + ".psq"):
    sys.stderr.write("ERROR: MetaAMRplus BLAST DB not found.\n")
    sys.stderr.write("Set METAAMRPLUS_DB or install via Conda.\n")
    sys.exit(1)

VERSION = "1.4"

if len(sys.argv) != 3:
    sys.stderr.write(
        f"MetaAMRplus annotate script v{VERSION}\n"
        "Usage: annotate_metaamrplus.py blast.filtered.tsv idmap.tsv\n"
    )
    sys.exit(1)

blast_file = sys.argv[1]
idmap_file = sys.argv[2]

# -----------------------------
# Metal keywords & gene systems
# -----------------------------
METAL_KEYWORDS = [
    "copper", "silver", "arsenic", "mercury", "cadmium",
    "zinc", "nickel", "cobalt", "chromium", "lead",
    "iron", "manganese", "multimetal", "biocide"
]

METAL_GENE_PREFIXES = (
    "pco", "sil", "cus", "ars", "mer", "cop",
    "czc", "znt", "nik", "rcn", "chr"
)

# -----------------------------
# Load ID map
# -----------------------------
idmap = {}
with open(idmap_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            acc, meta = line.split("\t", 1)
            idmap[acc.strip()] = meta.strip()
        except ValueError:
            continue

# -----------------------------
# Output header
# -----------------------------
print("\t".join([
    "query_protein",
    "metaamrplus_id",
    "gene",
    "type",
    "phenotype",
    "mechanism",
    "source",
    "pident",
    "coverage",
    "bitscore"
]))

# -----------------------------
# Process BLAST hits
# -----------------------------
with open(blast_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        cols = line.split("\t")
        if len(cols) < 7:
            continue

        qseqid, sseqid, pident, length, qlen, evalue, bitscore = cols

        # -----------------------------
        # Coverage calculation
        # -----------------------------
        try:
            coverage = round((float(length) / float(qlen)) * 100, 2)
            if coverage > 100:
                coverage = 100.0
        except Exception:
            coverage = "NA"

        # -----------------------------
        # Lookup annotation
        # -----------------------------
        meta = idmap.get(sseqid.strip(), "NA")

        # Default safe values (IMPORTANT FIX)
        gene = "NA"
        gene_type = "NA"
        phenotype = "NA"
        mechanism = "NA"
        source = "NA"

        # -----------------------------
        # Parse annotation metadata
        # -----------------------------
        if meta != "NA":

            meta_dict = {}

            # Case 1: structured format (key=value)
            if "|" in meta and "=" in meta:
                for item in meta.split("|"):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        meta_dict[k.strip()] = v.strip()

            # Case 2: legacy whitespace format
            else:
                parts = meta.split()

                if len(parts) >= 1:
                    meta_dict["gene"] = parts[0]
                if len(parts) >= 2:
                    meta_dict["type"] = parts[1]
                if len(parts) >= 3:
                    meta_dict["source"] = parts[2]

            gene = meta_dict.get("gene", "NA")
            gene_type = meta_dict.get("type", "NA")
            phenotype = meta_dict.get("phenotype", "NA")
            mechanism = meta_dict.get("mechanism", "NA")
            source = meta_dict.get("source", "NA")

            # -----------------------------
            # Metal override logic
            # -----------------------------
            is_metal = False

            if phenotype != "NA":
                for kw in METAL_KEYWORDS:
                    if kw in phenotype.lower():
                        is_metal = True
                        break

            if gene != "NA":
                for prefix in METAL_GENE_PREFIXES:
                    if gene.lower().startswith(prefix):
                        is_metal = True
                        break

            if is_metal:
                gene_type = "metal"

        # -----------------------------
        # Output result
        # -----------------------------
        print("\t".join([
            qseqid,
            sseqid,
            gene,
            gene_type,
            phenotype,
            mechanism,
            source,
            pident,
            str(coverage),
            bitscore
        ]))
