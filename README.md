
**MetaAMRplus**
MetaAMRplus is a command-line platform for the simultaneous detection of antimicrobial resistance (AMR) genes, 
metal and biocide resistance genes, and their genomic colocalisation in bacterial genomes and plasmids. 
The tool integrates curated AMR and metal resistance databases with genome annotation and distance-based colocalisation analysis, 
enabling reproducible large-scale resistome profiling.

**Features**
i.	Simultaneous detection of AMR and metal resistance genes
ii.	Distance-based AMR–metal colocalisation analysis
iii.	Filtering of intrinsic resistance determinants
iv.	Crash-safe ORF prediction using Prodigal
v.	Supports single genomes and batch processing
vi.	Designed for reproducible analyses via Conda/Bioconda

**Installation**
MetaAMRplus is distributed via Bioconda.
To install this package, run the following:

conda install bioconda::metaamrplus

This installs the following commands:
i.	metaamrplus
ii.	metaamrplus_batch
iii.	metaamrplus-download-db

**Database installation (required)**
MetaAMRplus requires a reference database that is not bundled with the Bioconda package.
After installation, the database must be downloaded once using:
metaamrplus-download-db
By default, the database is installed into the active conda environment at:
$CONDA_PREFIX/db/
MetaAMRplus automatically detects this location at runtime.
Custom database location (optional)
Advanced users may store the database in a custom location by setting:
export METAAMRPLUS_DB=/path/to/metaamrplus_db

**Usage**
Single genome analysis
metaamrplus genome.fasta
Results are written to:
metaamrplus_results/<genome_name>/
Batch mode
metaamrplus_batch genomes/
Where genomes/ contains one or more FASTA files.

**Output files**
Key output files include:
i.	*.metaamrplus.filtered.tsv – filtered resistance gene hits
ii.	*.AMR.acquired.tsv – acquired AMR genes
iii.	*.metal.acquired.tsv – metal resistance genes
iv.	*.AMR_metal_colocalised_10kb.tsv – colocalised AMR–metal gene pairs
v.	*.gff – gene coordinates
Colocalisation is calculated using a default distance threshold of 10 kb.

**Dependencies**
All dependencies are installed automatically via Bioconda, including:
i.	Prodigal
ii.	BLAST+
iii.	AMRFinderPlus
iv.	Python ≥ 3.8
v.	Pandas
vi.	awk
No manual dependency installation is required.

**Environment variables**
Variable	Description
METAAMRPLUS_DB	Override default database location
METAAMRPLUS_RESULTS	Custom output directory

**Versioning**
MetaAMRplus follows semantic versioning.
The current release is v1.4.1.

**License**
MetaAMRplus is released under the MIT License.

**Software availability**
MetaAMRplus is open-source and freely available.
Source code, documentation, and database scripts are hosted at:
https://github.com/migshaw03/MetaAMRplus
The software is distributed via the Bioconda package repository.
<img width="468" height="640" alt="image" src="https://github.com/user-attachments/assets/d136dc85-5971-4054-81e6-2d4241ea5471" />
