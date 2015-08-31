#!/bin/bash
# this should be run in the mRNAseq analysis output directory, which contains the mRNAseq_analysis.tar.gz and alignments folder
exe=`basename $0`
USAGE="USAGE: $exe <config_file> <delivery_folder>\nMove the deliverable, and alignment files to the delivery folder.\nThe delivery folder is typically /mnt/grl/agar/users/Pi_name/projects/rtNNN_abc\n"

if [ $# -ne 2 ]; then  # no config file specified
    echo -e $USAGE
else
    [ ! -d $2/alignments ] && mkdir -p $2/alignments

    # move the compressed results
    cfg_line=`grep deliverable $1 | tr -s [\'\"\=] ' '`  # grep the 'workdir' line; and replace = " ' with spaces
    cfg=($cfg_line)             # separate out the path (by space)
    deliverable=${cfg[1]}           # get the path
    mv ${deliverable}* $1

    # move genome aligned BAM files
    cfg_line=`grep deliverable $1 | tr -s [\'\"\=] ' '`  # grep the 'workdir' line; and replace = " ' with spaces
    cfg=($cfg_line)             # separate out the path (by space)
    workdir=${cfg[1]}           # get the path

    for fn in ${workdir}/alignments/*_aligned_genome.*; do
        echo "moving file: $fn ..."
        mv $fn $2/alignments  # move the file to the delivery folder
        echo "file - $fn - has been moved. Save a symbolic link"
        ln -s $2/alignments/`basename $fn` $fn      # make a symbolic link in the original place
    done

    echo "Files are delivered to $2"
    echo "Change file permission"

    chgrp -R "BIOTECH\\brcdownloaders" $2  # update the group to allow user download previllege

    echo "Done"

fi