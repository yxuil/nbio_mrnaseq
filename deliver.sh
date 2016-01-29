#!/bin/bash
# this should be run in the mRNAseq analysis output directory, which contains the mRNAseq_analysis.tar.gz and alignments folder
exe=`basename $0`
USAGE="USAGE: $exe <config_file> \nMove the deliverable, and alignment files to the delivery folder.\nThe delivery folder is typically /mnt/grl/agar/users/Pi_name/projects/rtNNN_abc\n"

if [ $# -ne 1 ]; then  # no config file specified
    echo -e $USAGE
else
    cfg_line=`grep delivery $1 | tr -s [\'\"\=] ' '`  # grep the 'delivery' line; and replace = " ' with spaces
    cfg=($cfg_line)             # separate out the path (by space)
    deliver_path=${cfg[1]}           # get the path

    cfg_line=`grep workdir $1 | tr -s [\'\"\=] ' '`  # grep the 'workdir' line; and replace = " ' with spaces
    cfg=($cfg_line)             # separate out the path (by space)
    workdir=${cfg[1]}           # get the path

    pipeline_path=`dirname $0`

    # make folder
    [ ! -d ${deliver_path}/alignments ] && mkdir -p ${deliver_path}/alignments

    # create and move zipped report files
    ${pipelin_path}/run_runaseq.sh $1 deliverable 
    mv ${workdir}/mRNAseq_Analysis.zip ${deliver_path}

    # move genome aligned BAM files

    for fn in ${workdir}/alignments/*_aligned_genome.*; do
        echo "moving file: $fn ..."
        mv $fn ${deliver_path}/alignments  # move the file to the delivery folder
        echo "file - $fn - has been moved. Save a symbolic link"
        ln -s ${deliver_path}/alignments/`basename $fn` $fn      # make a symbolic link in the original place
    done

    echo "Files are delivered to $2"
    echo "Change file permission"

    chgrp -R "BIOTECH\\brcdownloaders" ${deliver_path}  # update the group to allow user download previllege

    echo "Done"

fi
