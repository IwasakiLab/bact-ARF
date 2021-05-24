import gzip
import hashlib
import shutil
import tempfile
import urllib.request
import pandas as pd
from Bio import SeqIO
from pathlib import Path
from .config import path2

class Metadata:
    def __init__(self):
        self.__asm_all   = None
        self.__asm_inuse = None
        self.__tax_all   = None
        self.__tax_inuse = None
        self.__acc       = None
        
    @property
    def asm_all(self):
        if self.__asm_all is None:
            self.__asm_all = pd.read_csv(
                path2.metadata/'NCBI_refseq_bacteria_assembly_summary_210520.txt',
                sep='\t', skiprows=1, converters={'excluded_from_refseq': str}, index_col=0
            )
        return self.__asm_all
    
    @property
    def asm_inuse(self):
        if self.__asm_inuse is None:
            self.__asm_inuse = pd.read_pickle(path2.metadata/'NCBI_asm_inuse.pkl.bz2')
        return self.__asm_inuse
    
    @property
    def tax_all(self):
        if self.__tax_all is None:
            self.__tax_all = pd.read_csv(path2.metadata/'GTDB_sp_clusters_r202.tsv', sep='\t')
        return self.__tax_all
    
    @property
    def tax_inuse(self):
        if self.__tax_inuse is None:
            self.__tax_inuse = pd.read_pickle(path2.metadata/'NCBI_asm_inuse.pkl.bz2')
        return self.__tax_inuse
    
    @property
    def acc(self):
        if self.__acc is None:
            self.__acc = pd.read_pickle(path2.metadata/'refseq_gtdbrep_mappings.pkl.bz2')
        return self.__acc

class DatasetDownloader:
    def __init__(self): pass
        
    def fetch_NCBI_genome(self, ftp_path, file_to_save):
        genome_ftp_path = f'{ftp_path}/{ftp_path.rsplit("/",1)[-1]}_genomic.gbff.gz'
        md5_ftp_path = f'{ftp_path}/md5checksums.txt'
        for trial in range(3):
            try:
                with urllib.request.urlopen(genome_ftp_path) as genome_resp, tempfile.TemporaryFile() as genome_tmp:
                    shutil.copyfileobj(genome_resp, genome_tmp)
                    genome_tmp.seek(0)
                    calculated_md5 = hashlib.md5(genome_tmp.read()).hexdigest()
                    with urllib.request.urlopen(md5_ftp_path) as md5_resp:
                        correct_md5 = [
                            line.decode().split('  ')[0] for line in md5_resp.readlines() if b'_genomic.gbff.gz' in line
                        ][0]    
                    if calculated_md5 == correct_md5:
                        genome_tmp.seek(0)    
                        with open(file_to_save, 'wb') as genome_out:
                            shutil.copyfileobj(genome_tmp, genome_out)
                    else:
                        raise Exception('Checksum did not match.')
            except Exception as e:
                print(e)
            else:
                break
        else:
            raise Exception(f'Failed to download the genome in {ftp_path}')
        
class DatasetLoader:
    def __init__(self): pass
    
    def load_genome(self, gcf, dirname=None):
        dirname = Path(dirname or path2.data/'pubdata'/'genomic_gbff')
        
        with gzip.open(dirname/f'{gcf}.gbff.gz', 'rt') as file:
            for rec in SeqIO.parse(file, 'gb'):
                yield rec