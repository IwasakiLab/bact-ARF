#!/bin/bash -eu

# reference genome indexing
run_bowtie2build () {
    local infile=$1
    local outfile=${infile/reference/bowtie2_idx}
    local logfile=${outfile/.fna/.log}
    outfile=${outfile/.fna/}
    
    bowtie2-build $infile $outfile &> $logfile
}

export -f run_bowtie2build

ls /data/expression/Kim+20SciData/reference/*.fna | xargs -t -P5 -L1 -I{} /bin/bash -c 'run_bowtie2build {}'

# read mapping
run_bowtie2align () {
    local basename=/data/expression/Kim+20SciData
    local readsfile=${basename/data/data\/pubdata}/trimmed_fastq/$1.fastq.gz
    local reffile=$basename/bowtie2_idx/$2
    local outfile=$basename/bam/$1.bam
    local logfile=$basename/bam/$1.log
    bowtie2 --very-sensitive --no-unal -x $reffile -U $readsfile -p 8 2> $logfile | samtools view -b | samtools sort -o $outfile -@ 8
}

export -f run_bowtie2align

tail -n +2 /metadata/expression/Kim+20SciData_runs.tsv | awk '{print $1,$12}' | xargs -t -P12 -L2 -I{} /bin/bash -c 'run_bowtie2align {}'

