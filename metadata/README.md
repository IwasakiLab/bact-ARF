# Metadata

This directory contains information of genomes and sequence reads on publicly available databases used in this project.

Specifically, it contains the following files:

```
metadata/
├── bac120_r202.tree                 : Phylogenetic tree of GTDB representative genomes, downloaded from https://data.gtdb.ecogenomic.org/releases/release202/202.0/bac120_r202.tree. (Created by the GTDB team. Redistrubuted under CC BY-SA 4.0.)
├── bac120_r202.tree.pkl.bz2         : Binarized version of the bac120_r202.tree to make it easier to load in Python. (Created by Shun Yamanouchi based on bac120_r202.tree by the GTDB team.)
├── expression                       : Metadata for the expression data analyses.
│   ├── DGY14PNAS_refs.tsv               : (Davis, Gohara & Yap, Proc Natl Acad Sci USA., 2014; Reference genome)
│   ├── DGY14PNAS_runs.tsv               : (Davis, Gohara & Yap, Proc Natl Acad Sci USA., 2014; RNA/Ribo-Seq data)
│   ├── HB17NAR_refs.tsv                 : (Hwang & Buskirk, Nucleic Acids Res., 2017; Reference genome)
│   ├── HB17NAR_runs.tsv                 : (Hwang & Buskirk, Nucleic Acids Res., 2017; RNA/Ribo-Seq data)
│   ├── Kim+20SciData_refs.tsv           : (Kim et al., Sci Data., 2020; Reference genomes)
│   └── Kim+20SciData_runs.tsv           : (Kim et al., Sci Data., 2020; RNA/Ribo-Seq data)
├── GTDB_sp_clusters_r202.tsv        : Metadata file of GTDB r202 downloaded from https://data.gtdb.ecogenomic.org/releases/release202/auxillary_files/sp_clusters_r202.tsv. (Created by the GTDB team. Redistrubuted under CC BY-SA 4.0.)
├── GTDB_taxonomy_inuse.pkl.bz2      : GTDB taxonomic information of the genomes analyzed in this study. (Created by Shun Yamanouchi based on sp_clusters_r202.tsv by the GTDB team. Licenced under CC BY-SA 4.0.)
├── ko_list                          : KOfam relsease 2021-02-04, downloaded from https://www.genome.jp/ftp/db/kofam/ (not released here). 
├── NCBI_asm_inuse.pkl.bz2           : NCBI assembly summary information for the genomes analyzed in this study.
├── NCBI_refseq_bacteria_assembly_summary_210520.txt : NCBI assembly summary downloaded from NCBI FTP server (https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt). We appreciate the National Library of Medicine for this public domain data.
├── ProkAtlas_env_clusters.tsv       : Clusters of ProkAtlas environmental categories, retrieved from Figure S7 of Mise & Iwasaki (2020).
├── README.md                        : This file.
└── refseq_gtdbrep_mappings.pkl.bz2  : Mapping table between NCBI RefSeq genomes analyzed in this study and representative genomes of GTDB. (This file was created by Shun Yamanouchi based on sp_clusters_r202.tsv by the GTDB team. Licenced under CC BY-SA 4.0.) 
```

