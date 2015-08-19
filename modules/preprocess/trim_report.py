#!/usr/bin/env python
import pandas as pd
import sys, json

def get_num_from_line(l):
    '''
    given a string return a list of numbers that in the string
    '''
    return [ int(i) for i in l.split() if i.isdigit() ]

def trim_report(samples, output):
    '''
    Parse the reads trimming information
    :param samples, output:
    :return html table :
    '''
    sample_summary = pd.DataFrame()
    for sample in samples:
        # trim stat
        log = 'tmp/pipeline_log/{}_trim.log'.format(sample)

        # detect if it is single end or paired end trimming in the log
        with open(log) as f_in:
            while (1):
                line = f_in.readline()
                if line.startswith("Input file"):
                    next_line = f_in.readline()
                    if next_line.startswith("Paired file"):
                        pairTrimmed = True
                    else:
                        pairTrimmed = False
                    break
        # process the log
        with open(log) as f_in:
            if pairTrimmed: # paired end reads trim report

                total, too_short, read_pair, trimed_pair = 0,0,0,0
                for line in f_in:
                    if "read pairs processed; of these:" in line:
                        total += get_num_from_line(line)[0]
                    elif "read pairs filtered out after trimming by size control" in line:
                        too_short += get_num_from_line(line)[0]
                    elif "read pairs available; of these:" in line:
                        read_pair += get_num_from_line(line)[0]
                    elif " trimmed read pairs available after processing" in line:
                        trimed_pair += get_num_from_line(line)[0]

                trim_stat = pd.Series([total, trimed_pair, too_short, read_pair],
                                         index=["Total number of reads",
                                               "Number of read pairs being trimmed",
                                               "Size filtered after trimming",
                                               "Total paired reads after trimming"])
            else: # single end reads trim report
                total, too_short, reads, trimed_reads = 0,0,0,0
                for line in f_in:
                    if "reads processed; of these:" in line:
                        total += get_num_from_line(line)[0]
                    elif "reads filtered out after trimming by size control" in line:
                        too_short += get_num_from_line(line)[0]
                    elif "reads available; of these:" in line:
                        reads += get_num_from_line(line)[0]
                    elif " trimmed reads available after processing" in line:
                        trimed_reads += get_num_from_line(line)[0]
                trim_stat = pd.Series([total, trimed_reads, too_short, reads],
                                         index=["Total number of reads",
                                               "Number of reads being trimmed",
                                               "Size filtered after trimming",
                                               "Total reads after trimming"])



        sample_summary[sample] = trim_stat

    sample_summary.index = map(lambda x: str(x).strip(), sample_summary.index)
    sample_summary = sample_summary.T

    sample_summary.to_csv( output + ".txt", sep="\t")
    with open ( output + ".html", 'w') as f_out:
        f_out.write(sample_summary.to_html(classes="brc"))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("USAGE: {} <run_config> <output_prefix>".format(sys.argv[0]))
        exit()
    config = json.load(open(sys.argv[1]))
    samples = [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ]
    trim_report(samples, sys.argv[2])