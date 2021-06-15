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

ls /data/expression/HB17NAR/reference/*.fna | xargs -t -P5 -L1 -I{} /bin/bash -c 'run_bowtie2build {}'

# adapter sequence trimming
run_fastp () {
    local infile=$1
    local outfile=${infile/pubdata\//}
    outfile=${outfile/fastq/trimmed_fastq}
    local htmlfile=${outfile/.fastq.gz/.html}
    local jsonfile=${outfile/.fastq.gz/.json}
    local logfile=${outfile/.fastq.gz/.log}
    outfile=${outfile/.fastq.gz/.trimmed.fastq.gz}
    
    fastp -i $infile -a CTGTAGGCACCATCAAT -o $outfile -h $htmlfile -j $jsonfile 2> $logfile
}

export -f run_fastp

ls /data/pubdata/expression/HB17NAR/fastq/*.fastq.gz | xargs -t -P40 -L1 -I{} /bin/bash -c 'run_fastp {}'

# read mapping
run_bowtie2align () {
    local basename=/data/expression/HB17NAR
    local readsfile=$basename/trimmed_fastq/$1.trimmed.fastq.gz
    local reffile=$basename/bowtie2_idx/$2
    local outfile=$basename/bam/$1.bam
    local logfile=$basename/bam/$1.log
    bowtie2 --very-sensitive --no-unal -x $reffile -U $readsfile -p 8 2> $logfile | samtools view -b | samtools sort -o $outfile -@ 8
}

export -f run_bowtie2align

tail -n +2 /metadata/expression/HB17NAR_runs.tsv | awk '{print $1,$12}' | xargs -t -P12 -L2 -I{} /bin/bash -c 'run_bowtie2align {}'

