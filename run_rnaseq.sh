progPath=`dirname $0`
exe=`basename $0`
echo "######## mRNAseq pipeline #########"
echo "USAGE:    " $exe " config_file [snakemake options]"
echo "examples: " $exe " config_file"
echo "            Run pipeline with defaults"
echo "          " $exe " config_file -n -p"
echo "            Dont run pipeline; just print out shell command"
echo "          " $exe " configfile deliver"
echo "            deliver the result"
echo "          " $exe " -h"
echo "            Print pipeline options"
echo "          " $exe " "
echo "            "

sm_com=`grep SNAKEMAKE ${progPath}/toolsinfo`
sm_com=(${sm_com/=/ / })
snakemake_com=${sm_com[2]}
snakemake_com=${snakemake_com//\"/}
snakemake_file=mrnaseq.sm
if hash $snakemake_com 2>/dev/null; then
    if [ $# -eq 0 ]; then  # no config file specified
        echo "$USAGE"
    else
        if [ "$1" == "-h" ]; then  # print help message
            echo  "$USAGE"
            echo
            echo "Options for snakemake:"
            $snakemake_com -h
        elif [ -f $1 ]; then

            # remove comments from the config file
            # and copy to workdir
            cfg_line=`grep workdir $1`     # grep the 'workdir' line
            cfg_line=${cfg_line//"\""/" "} # replace " with spaces
            cfg_line=${cfg_line//"\'"/" "} # replace ' with spaces
            cfg=($cfg_line)             # separate out the path (by space)
            workdir=${cfg[2]}           # get the path
            [ ! -d ${cfg} ] && mkdir -p ${workdir}  # make the work dir if not exists

            # remove comments from the config file
            # use a tmp file to avoid the run_config.json gets cleared when the source are destinate files are the same
            dt=`date '+%y%m%d_%H%M%S'` # use date_time in filename
            tmp_cfg=/tmp/_rnaseq_${dt}.tmp
            grep -v "^\x*\#" $1 > ${tmp_cfg}
            mv ${tmp_cfg} ${workdir}/run_config.json

            cd ${workdir}

            # gather the rest of options
            shift
            if [[ " $* " == *" -j "* ]]; then
                set -x
                $snakemake_com -s ${progPath}/${snakemake_file}  "$@"
            else
                if hash nproc 2>/dev/null; then  let p=`nproc`/2  # use half of the available cores
                else let p=`grep processor /proc/cpuinfo | wc -l`/2
                fi
                set -x
                $snakemake_com -s ${progPath}/${snakemake_file} "$@" -j ${p}
            fi

            cd -
        else
            echo "Config file $1 doesn't exist!"
        fi
    fi
else
    echo "Cannot find snakemake to run the pipeline"
fi
