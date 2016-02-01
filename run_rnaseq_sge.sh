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

# default qsub parameter and email notification
# parameters in {} are placeholders, which are replaced by snakemake in the pipeline
qsub_default="qsub -V -cwd -S /bin/bash -sync y -j y -b y -o {log} -l vf={params.mem} -q all.q "

# use qsub_email if you want email notification when the run is finished
# email="-m abe -M liu@biotech.wisc.edu "

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

if hash qsub 2>/dev/null; then  # check if qsub available
    config=$1
    shift              # get everything after the config file
    qsub -V -cwd -S /bin/bash -j y -b y -o pipeline.log -N runRNAseq ${email} ${progPath}/run_rnaseq.sh $config \
    --cluster-sync \"$qsub_default\" --jn s.\{rulename\}.\{jobid\} -w 120 -j 10 $@
else
    # qsub not available
    echo "WARNING: qsub cannot be found. Use local machine instead!"
    ${progPath}/run_rnaseq.sh $@
fi
