#!/bin/bash
# this should be run in the mRNAseq analysis output directory, which contains the mRNAseq_analysis.tar.gz and alignments folder
exe=`basename $0`
USAGE="USAGE: $exe <delivery_folder>\nThe delivery folder is typically /mnt/grl/agar/users/Pi_name/projects/rtNNN_abc\n"

if [ $# -ne 1 ]; then  # no config file specified
    echo -e $USAGE
else
    [ ! -d $1/alignments ] && mkdir -p $1/alignments

    # move the compressed results
    mv *.tar.gz $1

    # move genome aligned BAM files
    for fn in alignments/*_aligned_genome.*; do
        echo "moving file: $fn ..."
        mv $fn $1/alignments  # move the file to the delivery folder
        echo "file - $fn - has been moved. Save a symbolic link"
        ln -s $1/$fn $fn      # make a symbolic link in the original place
    done

    echo "Files are delivered to $1"
    echo "Change file permission"

    chgrp -R "BIOTECH\\brcdownloaders" $1  # update the group to allow user download previllege

    echo "Done"

fi