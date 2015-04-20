#!/usr/bin/env python

import pandas as pd
import sys, json

def align_report(samples, output):
    '''
    Parse the reads trimming information
    :param samples, output:
    :return html table :
    '''
    sample_summary = pd.DataFrame()
    for sample in samples:
        # alignment stat
        log = 'logs/star_align_{}.final.log'.format(sample)
        aln_stat = pd.Series.from_csv(log, sep="|", index_col=[0]).map(str.strip, na_action='ignore')
        aln_stat = aln_stat.iloc[[4, 7, 8, 16, 22, 23, 27, 28, 29]]
        sample_summary[sample] = aln_stat

    sample_summary.index = map(lambda x: str(x).strip(), sample_summary.index)
    sample_summary = sample_summary.T

    sample_summary.to_csv(output + ".txt", sep="\t")
    with open ( output + ".html", 'w') as f_out:
        f_out.write( sample_summary.to_html(classes="brc") )

if __name__ == "__main__" :
    if len(sys.argv) != 3 :
        print("USAGE: {} <run_config> <output_prefix>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    samples = [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ]
    align_report(samples, sys.argv[2])