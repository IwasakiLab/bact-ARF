#!/bin/bash -eu

run_blastn () {
    local infile=$1
    local outfile=${infile/16S/prokatlas}
    outfile=${outfile/.fna/.blasttab}
    blastn -db /data/prokatlas/prokatlas -query $infile -out $outfile -outfmt "6 qseqid sseqid qlen qstart qend slen sstart send nident length" -evalue 1e-10 -max_target_seqs 361474
}

export -f run_blastn

# DB compliation
makeblastdb -dbtype nucl -in /data/pubdata/prokatlas/ProkAtlas.fa -hash_index -out /data/prokatlas/prokatlas

# BLAST search
ls /data/16S/*.fna | xargs -t -P100 -L1 -I{} /bin/bash -c 'run_blastn {}'

