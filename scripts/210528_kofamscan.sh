#!/bin/bash -eu

run_kofamscan () {
    local infile=$1
    local outfile=${infile/cds_prot/kofamscan}
    outfile=${outfile/.faa/.tsv}
    tmpdir=$(mktemp -d)
    trap "[[ -d $tmpdir ]] && rm -rf $tmpdir" ERR EXIT
    exec_annotation -p /db/profiles -k /db/ko_list --cpu 20 --tmp-dir $tmpdir -f detail-tsv $infile > $outfile
}

export -f run_kofamscan

ls /data/cds_prot/*.faa | xargs -t -P5 -L1 -I{} /bin/bash -c 'run_kofamscan {}'

