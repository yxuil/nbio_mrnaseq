#! /usr/bin/env python
__author__ = 'liu'

import pandas as pd
import sys

def read_sj(sj_fn):
    """
    Read junction list from the file; and filter out the junction that are:
    already annotated (== 1) or
    non-canonical splice sites (== 0)  with few reads support
    :param sj_fn:
    :return:
    """
    uniq_read_threshold = 1
    colnames = "chr start end strand motif annotated uniq_reads multi_reads overhang".split()
    df = pd.read_table(sj_fn, index_col=[0,1,2], names=colnames)
    df = df[ (df.annotated==0) & ( (df.motif != 0) | (df.uniq_reads > uniq_read_threshold) )]
    return df

def merge_sj(sj_list):
    """
    :param sj_list:
    :return: merged_sj
    return a list of junction merged from multiple SJ.out files from STAR
    """
    merged_sj = read_sj(sj_list[0])
    for fn in sj_list[1:]:
        added_sj = read_sj(fn)
        matching_merged, matching_added = merged_sj.align(added_sj, fill_value=0)
        merged_sj = matching_merged.ix[:, ["uniq_reads", "multi_reads"]]\
                    .add(matching_added.ix[:, ["uniq_reads", "multi_reads"]])
    return merged_sj

if __name__ == "__main__":
    sj = merge_sj(sys.argv[1:])
    # filter for uniq_reads >=2 or multi_reads >=5
    sj = sj[ (sj.uniq_reads >=2 ) | (sj.multi_reads >= 5) ]
    print(sj.to_csv(sep="\t", header=False ))
