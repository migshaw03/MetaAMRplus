#!/usr/bin/env python3
import sys

VERSION = "1.4.3-final"

if len(sys.argv) != 3:
    sys.stderr.write(
        f"MetaAMRplus annotate v{VERSION}\n"
        "Usage: annotate_metaamrplus.py blast.tsv idmap.tsv\n"
    )
    sys.exit(1)

blast_file = sys.argv[1]
idmap_file = sys.argv[2]

# -----------------------------
# LOAD IDMAP
# -----------------------------
idmap = {}
with open(idmap_file) as f:
    for line in f:
        if not line.strip():
            continue
        try:
            acc, meta = line.strip().split("\t", 1)
            idmap[acc] = meta
        except:
            continue

# -----------------------------
# HEADER
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
# PROCESS BLAST
# -----------------------------
with open(blast_file) as f:
    for line in f:
        if not line.strip():
            continue

        cols = line.strip().split("\t")
        if len(cols) < 7:
            continue

        qseqid, sseqid, pident, length, qlen, evalue, bitscore = cols

        try:
            coverage = round((float(length) / float(qlen)) * 100, 2)
        except:
            coverage = "NA"

        meta = idmap.get(sseqid, "")

        gene = "NA"
        gene_type = "AMR"
        phenotype = "NA"
        mechanism = "NA"
        source = "NA"

        is_metal = False

        # -----------------------------
        # PARSE METADATA
        # -----------------------------
        if meta:
            parts = meta.split("|")

            for p in parts:
                if "=" not in p:
                    continue

                k, v = p.split("=", 1)
                k = k.strip().lower()
                v = v.strip()

                if k == "gene":
                    gene = v

                elif k == "type":
                    if v.lower() == "metal":
                        is_metal = True
                        gene_type = "metal"
                    elif v.lower() == "amr":
                        if not is_metal:
                            gene_type = "AMR"

                elif k == "phenotype":
                    phenotype = v

                elif k == "mechanism":
                    mechanism = v

                elif k == "source":
                    source = v.lower()
                    if "bacmet" in source:
                        is_metal = True
                        gene_type = "metal"

        # -----------------------------
        # FINAL OVERRIDE RULE (DEDUP FIX)
        # -----------------------------
        if is_metal:
            gene_type = "metal"

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