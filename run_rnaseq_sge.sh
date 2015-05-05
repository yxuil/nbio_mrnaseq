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
#
#    progPath=`dirname $0`
#    sm_com=`grep SNAKEMAKE ${progPath}/toolsinfo`
#    sm_com=(${sm_com/=/ / })
#    snakemake_com=${sm_com[2]}
#    snakemake_com=${snakemake_com//\"/}
#    if hash $snakemake_com 2>/dev/null; then
#        if [ $# -eq 0 ]; then  # no config file specified
#            echo "$USAGE"
#        else
#            if [ "$1" == "-h" ]; then  # print help message
#                echo  "$USAGE"
#                echo
#                echo "Options for snakemake:\n"
#                $snakemake_com -h
#            elif [ -f $1 ]; then # config file exist, but no grid submission command
#                config=$1
#                shift
#                jn=gbs_`date +%Y_%m_%d`
#                set -x
#                qsub -V -cwd -j y -b y -o ${jn}.log -N ${jn} -q brchigh.q "$snakemake_com --cluster \"${qsub_default}\" \
#                --jn s.\{rulename\}.\{jobid\}.sh -s ${progPath}/tassel.sm --configfile ${config} $@ -j 10 -w 30"
#            else
#                echo "config file $1 does not exist!"
#                echo "$USAGE"
#            fi
#        fi
#    else
#        echo "Cannot find snakemake at " $snakemake_com "!"
#    fi
#else
#    echo "Cannot find command qsub. Use run_qiime.sh instead"
#fi
