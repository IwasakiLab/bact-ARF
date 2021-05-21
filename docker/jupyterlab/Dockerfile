FROM jupyter/datascience-notebook:notebook-6.2.0
RUN conda install -c conda-forge -y mamba==0.8.2
RUN mamba install -c conda-forge -c bioconda -y \
        regex==2021.3.17 intervaltree==3.0.2 biopython==1.78 ete3==3.1.2 pysam==0.16.0.1 

