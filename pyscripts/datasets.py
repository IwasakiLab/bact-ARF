import gzip
import hashlib
import shutil
import tempfile
import urllib.request
from Bio import SeqIO
from .config import path2

class MetadataManager:
    def __init__(self): pass
    
    def load(self, name, dirname=None):
        metadata = None
        if name == 'genomes':
            metadata = pd.read_csv(
                path2.metadata/f'NCBI_refseq_bacteria_assembly_summary_{today.strftime("%y%m%d")}.txt',
                sep='\t', skiprows=1, converters={'excluded_from_refseq': str}, index_col=0
            )
        return metadata

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
        dirname = dirname or path2.data/'pubdata'/'genomic_gbff'
        
        with gzip.open(dirname/f'{gcf}.gbff.gz', 'rt') as file:
            for rec in SeqIO.parse(file, 'gb'):
                yield rec