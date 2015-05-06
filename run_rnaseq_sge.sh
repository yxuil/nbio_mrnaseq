#!/bin/bash
USAGE="Usage: run_rnaseq_sge.sh run_config_file [-c \"qsub_command\"] [snakemake options]
  run_config_file: Run configuration in JSON format. Refer to the example.
                   Required paramter
  qsub_command:    qsub command, like: \"qsub -V -cwd -j y -b y -o {log} -q brchigh.q\"
                   if it is specified, it has to be right after config file
  options:         Other valid snakemake options"

qsub_default="qsub -V -cwd -S /bin/bash -j y -b y -o {log} -l vf={params.mem} -q all.q"

progPath=`dirname $0`
if hash qsub 2>/dev/null; then  # check if qsub available
    jn=`date +%Y_%m_%d`
    cfg=$1
    shift
    #qsub -V -cwd -S /bin/bash -j y -o mRNAseq_run_$jn.log -q all.q \
    ${progPath}/run_rnaseq.sh $cfg -c "$qsub_default" --jn s.\{rulename\}.\{jobid\} -w 30 -j 20 $@
else
    # qsub not available
    echo "WARNING: qsub cannot be found. Use local machine instead!"
    ${progPath}/run_rnaseq.sh $@
fi
