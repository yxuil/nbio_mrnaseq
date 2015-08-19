
progPath=`dirname $0`
exe=`basename $0`
echo "######## mRNAseq pipeline #########"
USAGE="USAGE:     $exe  config_file [snakemake options]
 examples:  $exe  config_file
               => Run pipeline with defaults
            $exe  config_file -n -p
               => Dont run pipeline; just print out shell command
            $exe  configfile deliver
               => Deliver the result
            $exe  -h
               => Print snakemake options
            $exe
               => Print this help
            "

sm_com=`grep SNAKEMAKE ${progPath}/config/toolsinfo`; sm_com=(${sm_com/=/ / })
snakemake_com=${sm_com[2]}; snakemake_com=${snakemake_com//\"/}
snakemake_file=rnaseq.sm

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
            # make JSON file from the config file
            # and copy to workdir
            cfg_line=`grep workdir $1 | tr -s [\'\"\=] ' '`  # grep the 'workdir' line; and replace = " ' with spaces
            cfg=($cfg_line)             # separate out the path (by space)
            workdir=${cfg[1]}           # get the path
            [ ! -d ${cfg} ] && mkdir -p ${workdir}  # make the work dir if not exists

            # convert and copy run config json file to workdirectory
            if echo $1 | grep -iq .json; then # case insensitive match for *.json
                cp $1 ${workdir}              # already Json file
            else
                ${progPath}/config/ini2json.py $1 > ${workdir}/run_config.json # convert ini style file to json format
            fi

            cd ${workdir}

            # gather the rest of options
            shift

            echo "Working in:" `pwd`

            # assign appropriate number of core/threads
            if [[ " $* " == *" -j "* ]]; then
                # already set -j parameter
                set -x
                $snakemake_com -s ${progPath}/${snakemake_file} "$@"
            else
                # -j parameter is not assigned
                if hash nproc 2>/dev/null; then  let p=`nproc`/2  # use half of the available cores
                else let p=`grep processor /proc/cpuinfo | wc -l`/2
                fi
                set -x
                $snakemake_com -s ${progPath}/${snakemake_file} "$@" -j ${p}

            fi

            cd -
        else
            echo "Config file $1 doesn't exist!"
            echo "$USAGE"
        fi
    fi
else
    echo "Cannot find snakemake to run the pipeline"
fi
