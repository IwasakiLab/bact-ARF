FROM continuumio/miniconda3:4.9.2
RUN conda install -c conda-forge -y mamba==0.8.2
RUN mamba install -c conda-forge -c bioconda -y \
        sra-tools==2.10.9 fastqc==0.11.9 skewer==0.2.2 bowtie2==2.4.3 samtools==1.12  

