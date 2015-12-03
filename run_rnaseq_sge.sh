#!/bin/bash
progPath=`dirname $0`
exe=`basename $0`
USAGE="Usage: run_rnaseq_sge.sh run_config_file [-c \"qsub_command\"] [snakemake options]
  run_config_file: Run configuration in JSON format. Refer to the example.
                   Required paramter
  qsub_command:    cluster submission command, like: \"qsub -V -cwd -j y -b y -o {log} -q all.q\"
                   if it is specified, it has to be right after config file
  options:         Other valid snakemake options

  examples:  $exe  -h
               => print this help
             $exe  config_file
               => Run pipeline with defaults
             $exe  config_file -n -p
               => Dont run pipeline; just print out shell command "

qsub_default="qsub -V -cwd -S /bin/bash -sync y -j y -b y -o {log} -l vf={params.mem} -q all.q " # -m abe -M liu@biotech.wisc.edu"
#DRMAA = " -q all.q -V -cwd -l vf={params.mem} -j y -b y -o {log}"
{
CMD=`echo $0 | sed -e 's/^.*\///'`
# should scan all args first for --X options
if [ $# -lt 1 ]; then
  echo "$CMD: Invalid number of arguments." >&2
  echo -e "$USAGE" >&2
  exit 1;
fi
if [ "$1" = "-h" ]; then
    echo -e "$USAGE" >&2
    exit 0
fi
}

#while getopts "hDLw:o:p:s:t:j:b:B:" opt
#do
#  case $opt in
#    c) CLUSTER_SUB=$OPTARG;;
#    q) CLUSTER_QUEUE=$OPTARG;;
#

if hash qsub 2>/dev/null; then  # check if qsub available
    config=$1
    shift              # get everything after the config file
    qsub -V -cwd -S /bin/bash -j y -b y -o pipeline.log -N runRNAseq -m abe -M liu@biotech.wisc.edu \
       ${progPath}/run_rnaseq.sh $config --cluster-sync \"$qsub_default\" --jn s.\{rulename\}.\{jobid\} -w 120 -j 20 $@
#    ${progPath}/run_rnaseq.sh $config --drmaa " $DRMAA"  -w 30 -j 20 $@
else
    # qsub not available
    echo "WARNING: qsub cannot be found. Use local machine instead!"
    ${progPath}/run_rnaseq.sh $@
fi
